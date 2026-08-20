from __future__ import annotations

from pathlib import Path
import shutil

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "_typescript-frontend"
OVERLAY = ROOT / "activities" / "tpsi5" / "feisbuc_realtime_c" / "solution" / "frontend"
DEST = ROOT / "_realtime-frontend"


def copy_tree(source: Path, destination: Path, *, dirs_exist_ok: bool = False) -> None:
    shutil.copytree(
        source,
        destination,
        dirs_exist_ok=dirs_exist_ok,
        ignore=shutil.ignore_patterns("node_modules", "dist"),
    )


def main() -> None:
    if DEST.exists():
        shutil.rmtree(DEST)
    copy_tree(BASE, DEST)
    copy_tree(OVERLAY, DEST, dirs_exist_ok=True)
    print(DEST)


if __name__ == "__main__":
    main()
