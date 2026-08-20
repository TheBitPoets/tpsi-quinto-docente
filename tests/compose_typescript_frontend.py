from __future__ import annotations

from pathlib import Path
import shutil

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "activities" / "tpsi5" / "feisbuc_vue_c" / "solution" / "frontend"
ROUTER = ROOT / "activities" / "tpsi5" / "feisbuc_vue_router_c" / "solution" / "frontend"
TYPESCRIPT = ROOT / "activities" / "tpsi5" / "feisbuc_typescript_c" / "solution" / "frontend"
DEST = ROOT / "_typescript-frontend"


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
    copy_tree(ROUTER, DEST, dirs_exist_ok=True)

    for replaced in (
        "src/main.js",
        "src/api.js",
        "src/navigation-policy.js",
        "src/session.js",
        "src/router.js",
    ):
        (DEST / replaced).unlink(missing_ok=True)

    copy_tree(TYPESCRIPT, DEST, dirs_exist_ok=True)
    print(DEST)


if __name__ == "__main__":
    main()
