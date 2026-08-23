from __future__ import annotations

import argparse
import importlib.util
import json
import sys
import tempfile
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PLATFORM = ROOT / "_thebitlab-platform"
ADAPTER_PATH = ROOT / "scripts" / "tpsi5_thebitlab_assign.py"
FIRST_ACTIVITY = ROOT / "activities" / "tpsi5" / "html_anatomy_a" / "activity.json"
FIRST_ACTIVITY_ID = "tpsi5-activity-a-html-anatomy-001"


def load_adapter():
    spec = importlib.util.spec_from_file_location("tpsi5_thebitlab_assign", ADAPTER_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError("Impossibile caricare l'adapter TPSI5/TheBitLab.")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


ADAPTER = load_adapter()


def activity_paths() -> list[Path]:
    return sorted((ROOT / "activities" / "tpsi5").glob("*/activity.json"))


def check_assignment_plans() -> None:
    errors: list[str] = []
    supported: list[str] = []
    fallbacks: list[tuple[str, str]] = []
    paths = activity_paths()
    if not paths:
        raise AssertionError("Nessuna Activity TPSI5 trovata.")

    with tempfile.TemporaryDirectory(prefix="tpsi5-plan-smoke-") as temp_dir:
        base = Path(temp_dir)
        for index, activity_path in enumerate(paths):
            relative = activity_path.relative_to(ROOT).as_posix()
            capability = ADAPTER.capability_for(activity_path)
            if not capability.supported:
                if not capability.reason:
                    errors.append(f"{relative}: fallback senza motivazione")
                else:
                    fallbacks.append((relative, capability.reason))
                continue

            target = base / f"student-{index:03d}"
            try:
                plan = ADAPTER.build_plan(
                    activity_path=activity_path,
                    targets=[target],
                    platform_root=PLATFORM,
                )
                if not plan.can_assign:
                    errors.append(f"{relative}: piano dichiarato non assegnabile")
                else:
                    supported.append(relative)
            except Exception as error:  # unknown incompatibilities must fail the gate
                errors.append(f"{relative}: {type(error).__name__}: {error}")

    if errors:
        formatted = "\n".join(f"- {error}" for error in errors)
        raise AssertionError(f"Incompatibilita TheBitLab non classificate:\n{formatted}")

    first_capability = ADAPTER.capability_for(FIRST_ACTIVITY)
    if not first_capability.supported:
        raise AssertionError(f"La prima Activity deve essere scaffoldabile: {first_capability.reason}")

    reasons = Counter(reason for _, reason in fallbacks)
    print(f"Assignment plan smoke passed: {len(supported)} scaffoldabili, {len(fallbacks)} fallback espliciti.")
    for reason, count in sorted(reasons.items()):
        print(f"- fallback {reason}: {count}")


def check_first_scaffold() -> None:
    with tempfile.TemporaryDirectory(prefix="tpsi5-scaffold-smoke-") as temp_dir:
        target = Path(temp_dir) / "student-repo"
        results = ADAPTER.assign(
            activity_path=FIRST_ACTIVITY,
            targets=[target],
            platform_root=PLATFORM,
        )
        if len(results) != 1:
            raise AssertionError(f"Atteso un solo scaffold, ottenuti {len(results)}")

        assignment = target.resolve() / "assignments" / FIRST_ACTIVITY_ID
        if results[0].assignment_dir != assignment:
            raise AssertionError("Il path dello scaffold restituito non coincide con quello atteso.")

        expected = {"README.md", "activity.json", "index.html", "GUIDA.md"}
        actual = {
            path.relative_to(assignment).as_posix()
            for path in assignment.rglob("*")
            if path.is_file()
        }
        missing = expected - actual
        if missing:
            raise AssertionError(f"File studente mancanti: {sorted(missing)}; presenti: {sorted(actual)}")

        forbidden_parts = {"solution", "teacher", "NOTES.md"}
        leaked = [item for item in actual if any(part in forbidden_parts for part in Path(item).parts)]
        if leaked:
            raise AssertionError(f"Asset teacher/solution esposti nello scaffold: {leaked}")

        public_activity = json.loads((assignment / "activity.json").read_text(encoding="utf-8"))
        serialized = json.dumps(public_activity, ensure_ascii=False)
        for forbidden in ("solution/", "teacher/", "teacher_only"):
            if forbidden in serialized:
                raise AssertionError(f"Metadata riservati esposti in activity.json studente: {forbidden}")

        public_assets = public_activity.get("assets", [])
        guide_targets = {
            asset.get("target_path")
            for asset in public_assets
            if isinstance(asset, dict) and asset.get("path") == "student/README.md"
        }
        if guide_targets != {"GUIDA.md"}:
            raise AssertionError(f"Target guida studente inatteso: {guide_targets}")

        readme = (assignment / "README.md").read_text(encoding="utf-8")
        guide = (assignment / "GUIDA.md").read_text(encoding="utf-8")
        if not readme.strip() or "Activity ID" not in readme:
            raise AssertionError("README di scaffold assente o non generato dalla piattaforma.")
        if not guide.strip() or "Anatomia di un documento HTML moderno" not in guide:
            raise AssertionError("Guida Activity studente assente o inattesa.")

        print("First HTML Activity scaffold smoke passed.")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--plans-only", action="store_true")
    mode.add_argument("--first-scaffold", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if not PLATFORM.is_dir():
        raise SystemExit("Pinned TheBitLab checkout missing at _thebitlab-platform.")
    if args.plans_only:
        check_assignment_plans()
    else:
        check_first_scaffold()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
