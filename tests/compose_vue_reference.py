from __future__ import annotations

from pathlib import Path
import shutil


ROOT = Path(__file__).resolve().parents[1]
AUTH = ROOT / "activities" / "tpsi5" / "feisbuc_auth_c" / "solution"
VUE_DIST = ROOT / "activities" / "tpsi5" / "feisbuc_vue_c" / "solution" / "frontend" / "dist"
DEST = ROOT / "_vue-reference"


def copy_without_node_modules(source: Path, destination: Path) -> None:
    shutil.copytree(source, destination, ignore=shutil.ignore_patterns("node_modules"))


def main() -> None:
    if not VUE_DIST.is_dir():
        raise SystemExit("Vue dist mancante: eseguire prima npm run build nella solution frontend")
    if DEST.exists():
        shutil.rmtree(DEST)
    copy_without_node_modules(AUTH, DEST)
    vue_target = DEST / "public" / "vue"
    if vue_target.exists():
        shutil.rmtree(vue_target)
    shutil.copytree(VUE_DIST, vue_target)
    print(DEST)


if __name__ == "__main__":
    main()
