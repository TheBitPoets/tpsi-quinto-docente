from __future__ import annotations

import argparse
import filecmp
import json
import os
from pathlib import Path
import shutil
import tempfile


ROOT = Path(__file__).resolve().parents[1]
ACTIVITIES = ROOT / "activities" / "tpsi5"
IGNORE_NAMES = {"node_modules", "dist", ".DS_Store", "data"}
ADVANCED_MILESTONES = (
    "feisbuc_ssr_c",
    "feisbuc_vue_c",
    "feisbuc_vue_router_c",
    "feisbuc_typescript_c",
    "feisbuc_realtime_c",
)


def copy_tree(source: Path, destination: Path) -> None:
    """Merge a source tree into destination, excluding generated runtime files."""
    for path in sorted(source.rglob("*")):
        relative = path.relative_to(source)
        if any(part in IGNORE_NAMES for part in relative.parts):
            continue
        target = destination / relative
        if path.is_dir():
            target.mkdir(parents=True, exist_ok=True)
        elif path.is_file():
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(path, target)


def remove_paths(root: Path, relative_paths: tuple[str, ...]) -> None:
    for relative in relative_paths:
        path = root / relative
        if path.is_dir():
            shutil.rmtree(path)
        else:
            path.unlink(missing_ok=True)


def rewrite_package_name(path: Path, name: str) -> None:
    package = json.loads(path.read_text(encoding="utf-8"))
    package["name"] = name
    path.write_text(json.dumps(package, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def ensure_package_script(path: Path, name: str, command: str) -> None:
    package = json.loads(path.read_text(encoding="utf-8"))
    package.setdefault("scripts", {})[name] = command
    path.write_text(json.dumps(package, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def write_workspace(root: Path, milestone: int) -> None:
    scripts = {
        "dev:backend": "node scripts/start-backend.mjs",
        "dev:frontend": "npm run dev --workspace frontend",
        "build": "npm run build --workspace frontend && node scripts/sync-vue-dist.mjs",
        "start": "npm run start --workspace backend",
    }
    if milestone >= 11:
        scripts["type-check"] = "npm run type-check --workspace frontend"
    package = {
        "name": f"feisbuc-milestone-{milestone:02d}-starter",
        "private": True,
        "version": "0.0.0",
        "type": "module",
        "engines": {"node": ">=22.18"},
        "workspaces": ["backend", "frontend"],
        "scripts": scripts,
    }
    (root / "package.json").write_text(
        json.dumps(package, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    scripts = root / "scripts"
    scripts.mkdir(parents=True, exist_ok=True)
    (scripts / "start-backend.mjs").write_text(
        """import { spawn } from "node:child_process";
import path from "node:path";

const backendRoot = path.resolve("backend");
const child = spawn(process.execPath, ["src/server.js"], {
  cwd: backendRoot,
  env: { ...process.env, PORT: process.env.PORT ?? "3333" },
  stdio: "inherit",
});

for (const signal of ["SIGINT", "SIGTERM"]) {
  process.once(signal, () => child.kill(signal));
}

child.once("exit", (code, signal) => {
  if (signal) process.kill(process.pid, signal);
  else process.exitCode = code ?? 1;
});
""",
        encoding="utf-8",
    )
    (scripts / "sync-vue-dist.mjs").write_text(
        """import { cpSync, existsSync, mkdirSync, rmSync } from "node:fs";
import path from "node:path";

const source = path.resolve("frontend", "dist");
const destination = path.resolve("backend", "public", "vue");

if (!existsSync(source)) {
  throw new Error("Build frontend mancante: esegui npm run build dalla root dello starter.");
}

rmSync(destination, { recursive: true, force: true });
mkdirSync(path.dirname(destination), { recursive: true });
cpSync(source, destination, { recursive: true });
console.log(`Frontend integrato in ${destination}`);
""",
        encoding="utf-8",
    )


def compose_auth_backend(destination: Path) -> None:
    copy_tree(ACTIVITIES / "feisbuc_auth_c" / "solution", destination)


def compose_router_backend(destination: Path, *, variant: str) -> None:
    compose_auth_backend(destination)
    copy_tree(
        ACTIVITIES / "feisbuc_vue_router_c" / variant / "backend",
        destination / "src",
    )


def compose_vue_frontend(destination: Path, *, router_variant: str | None = None) -> None:
    copy_tree(ACTIVITIES / "feisbuc_vue_c" / "solution" / "frontend", destination)
    if router_variant is not None:
        copy_tree(
            ACTIVITIES / "feisbuc_vue_router_c" / router_variant / "frontend",
            destination,
        )


def compose_typescript_frontend(destination: Path, *, variant: str) -> None:
    compose_vue_frontend(destination, router_variant="solution")
    remove_paths(
        destination,
        (
            "src/main.js",
            "src/api.js",
            "src/navigation-policy.js",
            "src/session.js",
            "src/router.js",
        ),
    )
    copy_tree(
        ACTIVITIES / "feisbuc_typescript_c" / variant / "frontend",
        destination,
    )


def build_ssr_starter(destination: Path) -> None:
    compose_auth_backend(destination)
    copy_tree(ACTIVITIES / "feisbuc_ssr_c" / "starter-overlay", destination)
    ensure_package_script(destination / "package.json", "start", "node src/server.js")


def build_vue_starter(destination: Path) -> None:
    write_workspace(destination, 9)
    compose_auth_backend(destination / "backend")
    rewrite_package_name(destination / "backend" / "package.json", "feisbuc-vue-backend-starter")
    copy_tree(
        ACTIVITIES / "feisbuc_vue_c" / "starter-overlay" / "frontend",
        destination / "frontend",
    )


def build_vue_router_starter(destination: Path) -> None:
    write_workspace(destination, 10)
    compose_router_backend(destination / "backend", variant="starter-overlay")
    rewrite_package_name(destination / "backend" / "package.json", "feisbuc-vue-router-backend-starter")
    compose_vue_frontend(destination / "frontend")
    copy_tree(
        ACTIVITIES / "feisbuc_vue_router_c" / "starter-overlay" / "frontend",
        destination / "frontend",
    )


def build_typescript_starter(destination: Path) -> None:
    write_workspace(destination, 11)
    compose_router_backend(destination / "backend", variant="solution")
    rewrite_package_name(destination / "backend" / "package.json", "feisbuc-typescript-backend-starter")
    compose_vue_frontend(destination / "frontend", router_variant="solution")
    remove_paths(
        destination / "frontend",
        (
            "src/main.js",
            "src/api.js",
            "src/navigation-policy.js",
            "src/session.js",
            "src/router.js",
        ),
    )
    copy_tree(
        ACTIVITIES / "feisbuc_typescript_c" / "starter-overlay" / "frontend",
        destination / "frontend",
    )


def build_realtime_starter(destination: Path) -> None:
    write_workspace(destination, 12)
    compose_router_backend(destination / "backend", variant="solution")
    compose_typescript_frontend(destination / "frontend", variant="solution")
    copy_tree(
        ACTIVITIES / "feisbuc_realtime_c" / "starter-overlay" / "backend",
        destination / "backend",
    )
    copy_tree(
        ACTIVITIES / "feisbuc_realtime_c" / "starter-overlay" / "frontend",
        destination / "frontend",
    )


BUILDERS = {
    "feisbuc_ssr_c": build_ssr_starter,
    "feisbuc_vue_c": build_vue_starter,
    "feisbuc_vue_router_c": build_vue_router_starter,
    "feisbuc_typescript_c": build_typescript_starter,
    "feisbuc_realtime_c": build_realtime_starter,
}


def tree_files(root: Path) -> list[Path]:
    return sorted(path.relative_to(root) for path in root.rglob("*") if path.is_file())


def trees_match(expected: Path, actual: Path) -> bool:
    expected_files = tree_files(expected)
    actual_files = tree_files(actual) if actual.is_dir() else []
    if expected_files != actual_files:
        return False
    return all(filecmp.cmp(expected / path, actual / path, shallow=False) for path in expected_files)


def build_one(name: str, *, check: bool) -> bool:
    activity = ACTIVITIES / name
    target = activity / "starter"
    with tempfile.TemporaryDirectory(prefix=f"{name}-", dir=activity) as temp_dir:
        expected = Path(temp_dir) / "starter"
        expected.mkdir()
        BUILDERS[name](expected)
        if check:
            if not trees_match(expected, target):
                print(f"STALE {target.relative_to(ROOT)}")
                return False
            print(f"OK    {target.relative_to(ROOT)}")
            return True

        replacement = activity / ".starter-next"
        if replacement.exists():
            shutil.rmtree(replacement)
        shutil.copytree(expected, replacement)
        if target.exists():
            shutil.rmtree(target)
        os.replace(replacement, target)
        print(f"BUILT {target.relative_to(ROOT)} ({len(tree_files(target))} file)")
        return True


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Genera starter Feisbuc completi per le milestone 8-12."
    )
    parser.add_argument("--check", action="store_true", help="Verifica che gli starter versionati siano aggiornati.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    results = [build_one(name, check=args.check) for name in ADVANCED_MILESTONES]
    return 0 if all(results) else 1


if __name__ == "__main__":
    raise SystemExit(main())
