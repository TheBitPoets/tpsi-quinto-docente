from __future__ import annotations

from pathlib import Path
import shutil


ROOT = Path(__file__).resolve().parents[1]
AUTH = ROOT / "activities" / "tpsi5" / "feisbuc_auth_c" / "solution"
OVERLAY = ROOT / "activities" / "tpsi5" / "feisbuc_ssr_c" / "solution"
DEST = ROOT / "_ssr-reference"


def copy_without_node_modules(source: Path, destination: Path, *, dirs_exist_ok: bool = False) -> None:
    shutil.copytree(
        source,
        destination,
        dirs_exist_ok=dirs_exist_ok,
        ignore=shutil.ignore_patterns("node_modules"),
    )


def main() -> None:
    if DEST.exists():
        shutil.rmtree(DEST)
    copy_without_node_modules(AUTH, DEST)
    copy_without_node_modules(OVERLAY, DEST, dirs_exist_ok=True)
    print(DEST)


if __name__ == "__main__":
    main()
