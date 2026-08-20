from __future__ import annotations

from pathlib import Path
import shutil

ROOT = Path(__file__).resolve().parents[1]
AUTH = ROOT / "activities" / "tpsi5" / "feisbuc_auth_c" / "solution"
ROUTER_BACKEND = ROOT / "activities" / "tpsi5" / "feisbuc_vue_router_c" / "solution" / "backend"
FRONTEND_DIST = ROOT / "_typescript-frontend" / "dist"
DEST = ROOT / "_typescript-reference"


def copy_tree(source: Path, destination: Path, *, dirs_exist_ok: bool = False) -> None:
    shutil.copytree(
        source,
        destination,
        dirs_exist_ok=dirs_exist_ok,
        ignore=shutil.ignore_patterns("node_modules"),
    )


def main() -> None:
    if DEST.exists():
        shutil.rmtree(DEST)
    copy_tree(AUTH, DEST)
    copy_tree(ROUTER_BACKEND, DEST / "src", dirs_exist_ok=True)
    vue_dest = DEST / "public" / "vue"
    if vue_dest.exists():
        shutil.rmtree(vue_dest)
    copy_tree(FRONTEND_DIST, vue_dest)
    print(DEST)


if __name__ == "__main__":
    main()
