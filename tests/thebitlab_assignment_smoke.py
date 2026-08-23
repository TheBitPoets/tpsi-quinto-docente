from __future__ import annotations

import argparse
import json
import shutil
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PLATFORM = ROOT / "_thebitlab-platform"
THEBITLAB_REF = "5472eef86568a4e7ce59ad34ba937220df27efd7"
FIRST_ACTIVITY = ROOT / "activities" / "tpsi5" / "html_anatomy_a" / "activity.json"
FIRST_ACTIVITY_ID = "tpsi5-activity-a-html-anatomy-001"

if str(PLATFORM) not in sys.path:
    sys.path.insert(0, str(PLATFORM))

from scripts.assign_activity import assign_activity_to_targets, build_assignment_plan  # noqa: E402


def activity_paths() -> list[Path]:
    return sorted((ROOT / "activities" / "tpsi5").glob("*/activity.json"))


def check_assignment_plans() -> None:
    errors: list[str] = []
    paths = activity_paths()
    if not paths:
        raise AssertionError("Nessuna Activity TPSI5 trovata.")

    with tempfile.TemporaryDirectory(prefix="tpsi5-plan-smoke-") as temp_dir:
        base = Path(temp_dir)
        for index, activity_path in enumerate(paths):
            target = base / f"student-{index:03d}"
            try:
                plan = build_assignment_plan(
                    activity_path=activity_path,
                    targets=[target],
                    thebitlab_ref=THEBITLAB_REF,
                )
                if not plan.can_assign:
                    errors.append(f"{activity_path}: piano non assegnabile")
            except Exception as error:  # report all incompatible Activities in one run
                errors.append(f"{activity_path.relative_to(ROOT)}: {type(error).__name__}: {error}")

    if errors:
        formatted = "\n".join(f"- {error}" for error in errors)
        raise AssertionError(f"Activity incompatibili con assign_activity.py pinned:\n{formatted}")

    print(f"Assignment plan smoke passed for {len(paths)} TPSI5 Activities.")


def check_first_scaffold() -> None:
    with tempfile.TemporaryDirectory(prefix="tpsi5-scaffold-smoke-") as temp_dir:
        target = Path(temp_dir) / "student-repo"
        results = assign_activity_to_targets(
            activity_path=FIRST_ACTIVITY,
            targets=[target],
            thebitlab_ref=THEBITLAB_REF,
        )
        if len(results) != 1:
            raise AssertionError(f"Atteso un solo scaffold, ottenuti {len(results)}")

        assignment = target / "assignments" / FIRST_ACTIVITY_ID
        if results[0].assignment_dir != assignment:
            raise AssertionError("Il path dello scaffold restituito non coincide con quello atteso.")

        expected = {
            "README.md",
            "activity.json",
            "index.html",
            "GUIDA.md",
        }
        actual = {
            path.relative_to(assignment).as_posix()
            for path in assignment.rglob("*")
            if path.is_file()
        }
        missing = expected - actual
        if missing:
            raise AssertionError(f"File studente mancanti: {sorted(missing)}; presenti: {sorted(actual)}")

        forbidden_parts = {"solution", "teacher", "NOTES.md"}
        leaked = [
            item
            for item in actual
            if any(part in forbidden_parts for part in Path(item).parts)
        ]
        if leaked:
            raise AssertionError(f"Asset teacher/solution esposti nello scaffold: {leaked}")

        public_activity = json.loads((assignment / "activity.json").read_text(encoding="utf-8"))
        serialized = json.dumps(public_activity, ensure_ascii=False)
        for forbidden in ("solution/", "teacher/", "teacher_only"):
            if forbidden in serialized:
                raise AssertionError(f"Metadata riservati esposti in activity.json studente: {forbidden}")

        if (assignment / "README.md").read_text(encoding="utf-8").strip() == "":
            raise AssertionError("README scaffold vuoto.")
        if (assignment / "GUIDA.md").read_text(encoding="utf-8").strip() == "":
            raise AssertionError("Guida Activity studente vuota.")

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
