from __future__ import annotations

import argparse
import importlib.util
import json
import subprocess
import sys
import tempfile
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
ADAPTER_PATH = ROOT / "scripts" / "tpsi5_thebitlab_assign.py"
FIRST_ACTIVITY = ROOT / "activities" / "tpsi5" / "html_anatomy_a" / "activity.json"
FIRST_ACTIVITY_ID = "tpsi5-activity-a-html-anatomy-001"
THEBITLAB_REF = "5472eef86568a4e7ce59ad34ba937220df27efd7"


@dataclass(frozen=True)
class Check:
    id: str
    status: str
    detail: str


def run_command(command: list[str], *, cwd: Path | None = None) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        command,
        cwd=cwd,
        check=False,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )


def git_sha(path: Path) -> str | None:
    completed = run_command(["git", "-C", str(path), "rev-parse", "HEAD"])
    if completed.returncode != 0:
        return None
    value = completed.stdout.strip().lower()
    return value if len(value) == 40 else None


def git_is_clean(path: Path) -> bool | None:
    completed = run_command(["git", "-C", str(path), "status", "--porcelain=v1"])
    if completed.returncode != 0:
        return None
    return not bool(completed.stdout.strip())


def load_adapter():
    spec = importlib.util.spec_from_file_location("tpsi5_thebitlab_assign_preflight", ADAPTER_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError("adapter-load-failed")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def load_platform_validator(platform_root: Path):
    platform_root = platform_root.resolve()
    platform_string = str(platform_root)
    if platform_string not in sys.path:
        sys.path.insert(0, platform_string)

    validator_path = platform_root / "scripts" / "validate_activity.py"
    if not validator_path.is_file():
        raise FileNotFoundError("validator-missing")

    spec = importlib.util.spec_from_file_location("thebitlab_validate_activity_preflight", validator_path)
    if spec is None or spec.loader is None:
        raise RuntimeError("validator-load-failed")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def add_check(checks: list[Check], identifier: str, status: str, detail: str) -> None:
    checks.append(Check(identifier, status, detail))


def verify_repository(checks: list[Check], path: Path, *, identifier: str, expected_sha: str | None = None) -> str | None:
    sha = git_sha(path)
    if sha is None:
        add_check(checks, f"{identifier}.git", "FAIL", "Git checkout not verifiable")
        return None

    if expected_sha is not None and sha != expected_sha.lower():
        add_check(checks, f"{identifier}.sha", "FAIL", "Unexpected commit SHA")
    else:
        add_check(checks, f"{identifier}.sha", "PASS", sha)

    clean = git_is_clean(path)
    if clean is None:
        add_check(checks, f"{identifier}.clean", "FAIL", "Worktree status not verifiable")
    elif clean:
        add_check(checks, f"{identifier}.clean", "PASS", "clean")
    else:
        add_check(checks, f"{identifier}.clean", "FAIL", "dirty worktree")
    return sha


def verify_python(checks: list[Check]) -> None:
    version = f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
    supported = sys.version_info.major == 3 and 11 <= sys.version_info.minor <= 13
    add_check(checks, "python.version", "PASS" if supported else "FAIL", version)


def verify_docker(checks: list[Check], *, skip: bool) -> None:
    if skip:
        add_check(checks, "docker.engine", "BLOCKED", "skipped explicitly; real-host gate still required")
        return
    try:
        completed = run_command(["docker", "version", "--format", "{{.Server.Version}}"])
    except OSError:
        add_check(checks, "docker.engine", "FAIL", "Docker CLI/engine unavailable")
        return
    if completed.returncode != 0 or not completed.stdout.strip():
        add_check(checks, "docker.engine", "FAIL", "Docker engine unavailable")
        return
    add_check(checks, "docker.engine", "PASS", completed.stdout.strip().splitlines()[0])


def validate_activity(checks: list[Check], platform_root: Path) -> None:
    try:
        validator = load_platform_validator(platform_root)
        data, load_errors = validator.load_json(FIRST_ACTIVITY)
        errors = list(load_errors)
        if data is not None:
            errors.extend(validator.validate_activity(data, "html_anatomy_a/activity.json"))
    except Exception as error:
        add_check(checks, "activity.schema", "FAIL", type(error).__name__)
        return

    if errors:
        add_check(checks, "activity.schema", "FAIL", f"{len(errors)} validation error(s)")
    else:
        add_check(checks, "activity.schema", "PASS", FIRST_ACTIVITY_ID)


def check_adapter_and_scaffold(checks: list[Check], platform_root: Path) -> None:
    try:
        adapter = load_adapter()
    except Exception as error:
        add_check(checks, "adapter.load", "FAIL", type(error).__name__)
        return

    try:
        capability = adapter.capability_for(FIRST_ACTIVITY)
    except Exception as error:
        add_check(checks, "adapter.capability", "FAIL", type(error).__name__)
        return

    if not capability.supported:
        add_check(checks, "adapter.capability", "FAIL", capability.reason or "unsupported")
        return
    add_check(checks, "adapter.capability", "PASS", "first HTML Activity scaffoldable")

    try:
        with tempfile.TemporaryDirectory(prefix="tpsi5-preflight-plan-") as temp_dir:
            target = Path(temp_dir) / "student-demo"
            plan = adapter.build_plan(
                activity_path=FIRST_ACTIVITY,
                targets=[target],
                platform_root=platform_root,
            )
            if not plan.can_assign:
                add_check(checks, "assignment.plan", "FAIL", "plan not assignable")
                return
            student_targets = {
                item.get("target_path")
                for item in plan.student_assets
                if isinstance(item, dict)
            }
            if not {"index.html", "GUIDA.md"}.issubset(student_targets):
                add_check(checks, "assignment.plan", "FAIL", "expected student targets missing")
                return
            add_check(checks, "assignment.plan", "PASS", "index.html + GUIDA.md planned")
    except Exception as error:
        add_check(checks, "assignment.plan", "FAIL", type(error).__name__)
        return

    try:
        with tempfile.TemporaryDirectory(prefix="tpsi5-preflight-scaffold-") as temp_dir:
            target = Path(temp_dir) / "student-demo"
            results = adapter.assign(
                activity_path=FIRST_ACTIVITY,
                targets=[target],
                platform_root=platform_root,
            )
            if len(results) != 1:
                add_check(checks, "assignment.scaffold", "FAIL", "unexpected scaffold count")
                return

            assignment = target.resolve() / "assignments" / FIRST_ACTIVITY_ID
            expected = {"README.md", "activity.json", "index.html", "GUIDA.md"}
            actual = {
                path.relative_to(assignment).as_posix()
                for path in assignment.rglob("*")
                if path.is_file()
            }
            missing = expected - actual
            if missing:
                add_check(checks, "assignment.scaffold", "FAIL", "required student files missing")
                return

            forbidden_parts = {"solution", "teacher", "NOTES.md"}
            if any(any(part in forbidden_parts for part in Path(item).parts) for item in actual):
                add_check(checks, "assignment.visibility", "FAIL", "teacher/solution file leakage")
                return

            public_activity = json.loads((assignment / "activity.json").read_text(encoding="utf-8"))
            serialized = json.dumps(public_activity, ensure_ascii=False)
            if any(marker in serialized for marker in ("solution/", "teacher/", "teacher_only")):
                add_check(checks, "assignment.visibility", "FAIL", "reserved metadata leakage")
                return

            guide_targets = {
                asset.get("target_path")
                for asset in public_activity.get("assets", [])
                if isinstance(asset, dict) and asset.get("path") == "student/README.md"
            }
            if guide_targets != {"GUIDA.md"}:
                add_check(checks, "assignment.visibility", "FAIL", "student guide target mismatch")
                return

            readme = (assignment / "README.md").read_text(encoding="utf-8")
            guide = (assignment / "GUIDA.md").read_text(encoding="utf-8")
            if "Activity ID" not in readme or "Anatomia di un documento HTML moderno" not in guide:
                add_check(checks, "assignment.scaffold", "FAIL", "generated README/GUIDA content mismatch")
                return

            add_check(checks, "assignment.scaffold", "PASS", "temporary first-lab scaffold verified")
            add_check(checks, "assignment.visibility", "PASS", "no teacher/solution leakage")
    except Exception as error:
        add_check(checks, "assignment.scaffold", "FAIL", type(error).__name__)


def build_report(platform_root: Path, *, skip_docker: bool, expected_tpsi5_sha: str | None) -> tuple[dict[str, Any], int]:
    checks: list[Check] = []
    tpsi5_sha = verify_repository(checks, ROOT, identifier="tpsi5", expected_sha=expected_tpsi5_sha)
    thebitlab_sha = verify_repository(checks, platform_root, identifier="thebitlab", expected_sha=THEBITLAB_REF)
    verify_python(checks)
    verify_docker(checks, skip=skip_docker)

    if thebitlab_sha == THEBITLAB_REF:
        validate_activity(checks, platform_root)
        check_adapter_and_scaffold(checks, platform_root)
    else:
        add_check(checks, "activity.schema", "BLOCKED", "requires accepted TheBitLab pin")
        add_check(checks, "adapter.capability", "BLOCKED", "requires accepted TheBitLab pin")
        add_check(checks, "assignment.plan", "BLOCKED", "requires accepted TheBitLab pin")
        add_check(checks, "assignment.scaffold", "BLOCKED", "requires accepted TheBitLab pin")

    failures = [check.id for check in checks if check.status == "FAIL"]
    blocked = [check.id for check in checks if check.status == "BLOCKED"]
    maximum_decision = "NO-GO" if failures else "GO tecnico demo"

    report = {
        "schema_version": "tpsi5.pilot-preflight.v1",
        "generated_at_utc": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
        "tpsi5_sha": tpsi5_sha,
        "thebitlab_sha": thebitlab_sha,
        "first_activity_id": FIRST_ACTIVITY_ID,
        "checks": [asdict(check) for check in checks],
        "summary": {
            "failures": failures,
            "blocked": blocked,
            "maximum_decision": maximum_decision,
            "go_pilot_possible_from_this_report": False,
            "remaining_real_host_gates": [
                "authoritative data root",
                "auth/authz + pairing/TUI",
                "Docker sandbox policy and immutable runner image",
                "final attempt to teacher report consistency",
                "backup/restore",
                "revocation/incident/shutdown",
                "school governance before real data",
            ],
        },
    }

    if failures:
        return report, 1
    return report, 0


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Sanitized TPSI5/TheBitLab candidate-host preflight. Never declares GO pilot."
    )
    parser.add_argument("--platform", type=Path, required=True, help="Root of the pinned 2cornot2c checkout.")
    parser.add_argument("--report", type=Path, help="Optional JSON report path. The path is not embedded in the report.")
    parser.add_argument("--expected-tpsi5-sha", help="Optional 40-character TPSI5 candidate SHA to enforce.")
    parser.add_argument(
        "--skip-docker",
        action="store_true",
        help="CI-only convenience. Records Docker as BLOCKED; does not satisfy the real-host Docker gate.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    expected = args.expected_tpsi5_sha.lower() if args.expected_tpsi5_sha else None
    if expected is not None and (len(expected) != 40 or any(ch not in "0123456789abcdef" for ch in expected)):
        print("Invalid --expected-tpsi5-sha.")
        return 2

    platform_root = args.platform.resolve()
    report, exit_code = build_report(
        platform_root,
        skip_docker=args.skip_docker,
        expected_tpsi5_sha=expected,
    )
    rendered = json.dumps(report, ensure_ascii=False, indent=2) + "\n"
    print(rendered, end="")

    if args.report is not None:
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_text(rendered, encoding="utf-8")
        print("Sanitized preflight report written.")

    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
