from __future__ import annotations

import argparse
import copy
import importlib
import json
import shutil
import subprocess
import sys
import tempfile
from contextlib import contextmanager
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterator

THEBITLAB_REF = "5472eef86568a4e7ce59ad34ba937220df27efd7"
STUDENT_ASSET_TYPES = {"starter", "example", "fixture", "visible_test"}


@dataclass(frozen=True)
class Capability:
    supported: bool
    reason: str | None = None


def load_activity(path: Path) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError("La Activity deve essere un oggetto JSON.")
    return data


def asset_is_student_visible(asset: dict[str, Any]) -> bool:
    visibility = asset.get("visibility")
    if visibility is None:
        visibility = "teacher" if asset.get("type") in {"hidden_test", "runner", "teacher_only"} else "student"
    return asset.get("type") in STUDENT_ASSET_TYPES and visibility == "student"


def capability_for(activity_path: Path) -> Capability:
    activity = load_activity(activity_path)
    language = str(activity.get("language") or activity.get("linguaggio") or "").strip().lower()
    if language == "typescript":
        return Capability(False, "typescript-runner/scaffold-not-supported-by-pinned-thebitlab")

    for asset in activity.get("assets", []):
        if not isinstance(asset, dict) or not asset_is_student_visible(asset):
            continue
        raw_path = asset.get("path")
        if not isinstance(raw_path, str) or not raw_path:
            continue
        source = activity_path.parent / raw_path
        if source.is_dir():
            return Capability(False, "directory-asset-not-supported-by-pinned-thebitlab")

    return Capability(True)


def verify_platform_revision(platform_root: Path) -> None:
    try:
        completed = subprocess.run(
            ["git", "-C", str(platform_root), "rev-parse", "HEAD"],
            check=False,
            capture_output=True,
            text=True,
        )
    except OSError as error:
        raise ValueError(f"Impossibile verificare il pin TheBitLab: {error}") from error

    if completed.returncode != 0:
        detail = completed.stderr.strip() or "git rev-parse fallito"
        raise ValueError(f"Checkout TheBitLab non verificabile: {detail}")

    actual = completed.stdout.strip().lower()
    if actual != THEBITLAB_REF:
        raise ValueError(
            "Revisione TheBitLab diversa dal pin accettato: "
            f"attesa {THEBITLAB_REF}, trovata {actual or '<vuota>'}."
        )


def load_platform(platform_root: Path):
    platform_root = platform_root.resolve()
    if not (platform_root / "scripts" / "assign_activity.py").is_file():
        raise ValueError(f"Checkout TheBitLab non valido: {platform_root}")
    verify_platform_revision(platform_root)
    platform_string = str(platform_root)
    if platform_string not in sys.path:
        sys.path.insert(0, platform_string)
    assign_activity = importlib.import_module("scripts.assign_activity")
    return assign_activity


@contextmanager
def adapted_activity(activity_path: Path) -> Iterator[Path]:
    """Create an ephemeral bundle compatible with the pinned scaffold contract.

    The canonical TPSI5 Activity is never modified. The platform owns README.md
    in a student scaffold, so a student guide targeting README.md is exposed as
    GUIDA.md only in the temporary delivery bundle.
    """

    activity_path = activity_path.resolve()
    activity = load_activity(activity_path)
    capability = capability_for(activity_path)
    if not capability.supported:
        raise ValueError(f"Capability TheBitLab non disponibile: {capability.reason}")

    adapted = copy.deepcopy(activity)
    assets = adapted.get("assets", [])
    if isinstance(assets, list):
        for asset in assets:
            if not isinstance(asset, dict) or not asset_is_student_visible(asset):
                continue
            if asset.get("target_path") == "README.md":
                asset["target_path"] = "GUIDA.md"

    with tempfile.TemporaryDirectory(prefix="tpsi5-thebitlab-") as temp_dir:
        bundle_root = Path(temp_dir)
        for asset in assets if isinstance(assets, list) else []:
            if not isinstance(asset, dict) or not asset_is_student_visible(asset):
                continue
            raw_path = asset.get("path")
            if not isinstance(raw_path, str) or not raw_path:
                continue
            source = activity_path.parent / raw_path
            if not source.is_file():
                raise ValueError(f"Asset studente non trovato o non file: {raw_path}")
            destination = bundle_root / raw_path
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source, destination)

        adapted_path = bundle_root / "activity.json"
        adapted_path.write_text(json.dumps(adapted, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        yield adapted_path


def build_plan(
    *,
    activity_path: Path,
    targets: list[Path],
    platform_root: Path,
    source_name: str | None = None,
    language: str | None = None,
    overwrite: bool = False,
):
    capability = capability_for(activity_path)
    if not capability.supported:
        raise ValueError(f"Capability TheBitLab non disponibile: {capability.reason}")
    assign_activity = load_platform(platform_root)
    with adapted_activity(activity_path) as adapted_path:
        return assign_activity.build_assignment_plan(
            activity_path=adapted_path,
            targets=targets,
            source_name=source_name,
            language=language,
            thebitlab_ref=THEBITLAB_REF,
            overwrite=overwrite,
        )


def assign(
    *,
    activity_path: Path,
    targets: list[Path],
    platform_root: Path,
    source_name: str | None = None,
    language: str | None = None,
    overwrite: bool = False,
    overwrite_source: bool = False,
):
    capability = capability_for(activity_path)
    if not capability.supported:
        raise ValueError(f"Capability TheBitLab non disponibile: {capability.reason}")
    assign_activity = load_platform(platform_root)
    with adapted_activity(activity_path) as adapted_path:
        return assign_activity.assign_activity_to_targets(
            activity_path=adapted_path,
            targets=targets,
            source_name=source_name,
            language=language,
            thebitlab_ref=THEBITLAB_REF,
            overwrite=overwrite,
            overwrite_source=overwrite_source,
        )


def targets_from_args(targets: list[Path] | None, targets_file: Path | None) -> list[Path]:
    result = list(targets or [])
    if targets_file is not None:
        for line in targets_file.read_text(encoding="utf-8").splitlines():
            clean = line.strip()
            if clean and not clean.startswith("#"):
                path = Path(clean)
                if not path.is_absolute():
                    path = targets_file.parent / path
                result.append(path)
    if not result:
        raise ValueError("Indica almeno un repository studente con --target o --targets-file.")
    return result


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Adapter TPSI5 per assegnare Activity al pin TheBitLab senza modificare il Content Pack canonico."
    )
    parser.add_argument("--activity", type=Path, required=True)
    parser.add_argument("--platform", type=Path, required=True, help="Root del checkout 2cornot2c/TheBitLab pinned.")
    parser.add_argument("--target", type=Path, action="append")
    parser.add_argument("--targets-file", type=Path)
    parser.add_argument("--source-name")
    parser.add_argument("--language")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--force", action="store_true")
    parser.add_argument("--overwrite-source", action="store_true")
    parser.add_argument("--capability-only", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    activity_path = args.activity.resolve()
    capability = capability_for(activity_path)
    if args.capability_only:
        print(json.dumps({"supported": capability.supported, "reason": capability.reason}, ensure_ascii=False))
        return 0 if capability.supported else 2

    if not capability.supported:
        print(f"Activity non assegnabile tramite lo scaffold pinned: {capability.reason}")
        return 2

    try:
        targets = targets_from_args(args.target, args.targets_file)
        if args.dry_run:
            plan = build_plan(
                activity_path=activity_path,
                targets=targets,
                platform_root=args.platform,
                source_name=args.source_name,
                language=args.language,
                overwrite=args.force,
            )
            payload = plan.to_dict()
            payload["tpsi5_delivery_adapter"] = {
                "thebitlab_ref": THEBITLAB_REF,
                "canonical_activity_unchanged": True,
                "student_readme_target": "GUIDA.md",
            }
            print(json.dumps(payload, ensure_ascii=False, indent=2))
            return 0

        results = assign(
            activity_path=activity_path,
            targets=targets,
            platform_root=args.platform,
            source_name=args.source_name,
            language=args.language,
            overwrite=args.force,
            overwrite_source=args.overwrite_source,
        )
    except ValueError as error:
        print(f"Activity non assegnata: {error}")
        return 1

    for result in results:
        print(f"Consegna creata per {result.target}: {result.assignment_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
