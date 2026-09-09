from __future__ import annotations

import json
from pathlib import Path
import subprocess
import sys


ROOT = Path(__file__).resolve().parents[1]
ACTIVITIES = ROOT / "activities" / "tpsi5"
ADVANCED = {
    "feisbuc_ssr_c": "feisbuc-07-auth-session",
    "feisbuc_vue_c": "feisbuc-07-auth-session",
    "feisbuc_vue_router_c": "feisbuc-09-vue-spa",
    "feisbuc_typescript_c": "feisbuc-10-vue-router",
    "feisbuc_realtime_c": "feisbuc-11-typescript-boundaries",
}


def load(path: Path) -> dict:
    value = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(value, dict)
    return value


def test_advanced_starters_are_generated_and_current() -> None:
    result = subprocess.run(
        [sys.executable, "scripts/build_feisbuc_starters.py", "--check"],
        cwd=ROOT,
        capture_output=True,
        text=True,
        timeout=20,
        check=False,
    )
    assert result.returncode == 0, result.stdout + result.stderr


def test_advanced_activity_contracts_deliver_one_complete_starter() -> None:
    for name, baseline in ADVANCED.items():
        root = ACTIVITIES / name
        activity = load(root / "activity.json")
        policy = activity["starter_policy"]
        assert policy == {
            "delivery": "complete",
            "baseline": baseline,
            "generated_by": "scripts/build_feisbuc_starters.py",
        }
        student_starters = [
            asset
            for asset in activity["assets"]
            if asset["visibility"] == "student" and asset["type"] == "starter"
        ]
        assert len(student_starters) == 1
        assert student_starters[0]["path"] == "starter"
        assert student_starters[0]["target_path"] == "."
        assert student_starters[0]["description"]
        assert (root / "starter").is_dir()
        assert (root / "starter-overlay").is_dir()

        guide = (root / "student" / "README.md").read_text(encoding="utf-8").lower()
        assert "non devi" in guide
        assert "sovrapponi i file" not in guide
        assert "copia la solution" not in guide
        assert "applica i file overlay" not in guide


def test_every_advanced_starter_contains_the_required_baseline() -> None:
    ssr = ACTIVITIES / "feisbuc_ssr_c" / "starter"
    assert (ssr / "src/auth-store.js").is_file()
    assert (ssr / "src/sql-post-store.js").is_file()
    assert (ssr / "src/ssr.router.js").is_file()

    for name in (
        "feisbuc_vue_c",
        "feisbuc_vue_router_c",
        "feisbuc_typescript_c",
        "feisbuc_realtime_c",
    ):
        starter = ACTIVITIES / name / "starter"
        assert (starter / "package.json").is_file()
        assert (starter / "scripts/start-backend.mjs").is_file()
        assert (starter / "scripts/sync-vue-dist.mjs").is_file()
        assert (starter / "backend/src/auth-store.js").is_file()
        assert (starter / "backend/src/sql-post-store.js").is_file()
        assert (starter / "frontend/index.html").is_file()

    router = ACTIVITIES / "feisbuc_vue_router_c" / "starter"
    assert (router / "frontend/src/api.js").is_file()
    assert (router / "frontend/src/router.js").is_file()
    assert (router / "backend/src/vue-spa.js").is_file()

    typescript = ACTIVITIES / "feisbuc_typescript_c" / "starter"
    for replaced in ("main.js", "api.js", "navigation-policy.js", "session.js", "router.js"):
        assert not (typescript / "frontend/src" / replaced).exists()
    assert (typescript / "frontend/src/main.ts").is_file()
    assert (typescript / "frontend/src/api.ts").is_file()

    realtime = ACTIVITIES / "feisbuc_realtime_c" / "starter"
    assert (realtime / "frontend/src/realtime.ts").is_file()
    assert (realtime / "backend/src/realtime.js").is_file()
    assert (realtime / "backend/src/post-events.js").is_file()


def test_current_milestone_todos_are_preserved_in_complete_starters() -> None:
    expected_todos = (
        ("feisbuc_ssr_c", "src/ssr.router.js"),
        ("feisbuc_vue_c", "frontend/src/App.vue"),
        ("feisbuc_vue_router_c", "frontend/src/router.js"),
        ("feisbuc_typescript_c", "frontend/src/api.ts"),
        ("feisbuc_realtime_c", "frontend/src/realtime.ts"),
    )
    for name, relative in expected_todos:
        source = (ACTIVITIES / name / "starter" / relative).read_text(encoding="utf-8")
        assert "TODO" in source, f"TODO corrente mancante in {name}/{relative}"


def test_workspace_commands_avoid_manual_frontend_copy() -> None:
    ssr_package = load(ACTIVITIES / "feisbuc_ssr_c" / "starter" / "package.json")
    assert ssr_package["scripts"]["start"] == "node src/server.js"

    for milestone, name in enumerate(
        (
            "feisbuc_vue_c",
            "feisbuc_vue_router_c",
            "feisbuc_typescript_c",
            "feisbuc_realtime_c",
        ),
        start=9,
    ):
        package = load(ACTIVITIES / name / "starter" / "package.json")
        assert package["workspaces"] == ["backend", "frontend"]
        assert package["scripts"]["dev:backend"] == "node scripts/start-backend.mjs"
        assert package["scripts"]["dev:frontend"] == "npm run dev --workspace frontend"
        assert "sync-vue-dist.mjs" in package["scripts"]["build"]
        assert package["scripts"]["start"] == "npm run start --workspace backend"
        if milestone >= 11:
            assert package["scripts"]["type-check"] == "npm run type-check --workspace frontend"
