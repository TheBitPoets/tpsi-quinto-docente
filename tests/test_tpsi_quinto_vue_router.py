from __future__ import annotations

import http.cookiejar
import json
import os
from pathlib import Path
import subprocess
import tempfile
import urllib.error
import urllib.request

import pytest

from scripts import grade_activity
from scripts.validate_activity import validate_activity


ROOT = Path(__file__).resolve().parents[1]
PACK_PATH = ROOT / "content" / "tpsi5" / "content-pack.json"
DESIGN_PATH = ROOT / "doc" / "course_designs" / "tpsi_quinto_2026_2027.json"
LESSON_PATH = ROOT / "content" / "tpsi5" / "11_VUE_ROUTER_NAVIGAZIONE_SPA.md"
A_ROOT = ROOT / "activities" / "tpsi5" / "vue_router_microscope_a"
B_ROOT = ROOT / "activities" / "tpsi5" / "navigation_policy_b"
C_ROOT = ROOT / "activities" / "tpsi5" / "feisbuc_vue_router_c"
D_ROOT = ROOT / "activities" / "tpsi5" / "vue_router_debug_d"
FRONTEND = ROOT / "_vue-router-frontend"
COMPOSED = ROOT / "_vue-router-reference"
VUE_VERSION = "3.5.40"
ROUTER_VERSION = "5.2.0"
VITE_VERSION = "8.2.1"
PLUGIN_VERSION = "6.0.8"


def load(path: Path) -> dict:
    value = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(value, dict)
    return value


def assert_activity(root: Path, difficulty: str, activity_id: str, *, automatic: bool) -> dict:
    activity = load(root / "activity.json")
    assert validate_activity(activity, str(root / "activity.json")) == []
    assert activity["id"] == activity_id
    assert activity["difficolta"] == difficulty
    assert activity["contesto"]["uda"] == "uda-25"
    assert sum(entry["punti"] for entry in activity["rubrica"]) == 10
    for asset in activity["assets"]:
        assert (root / asset["path"]).is_file(), asset
        if asset["visibility"] == "student":
            assert asset.get("target_path")
    assert activity["correzione"]["test"] is automatic
    return activity


def test_vue_router_pack_design_and_activity_contracts() -> None:
    pack = load(PACK_PATH)
    design = load(DESIGN_PATH)
    assert pack["version"] == "0.12.0"
    assert pack["extensions"]["bootstrap_decisions"] == {
        "frontend_framework": "vue3-vite",
        "node_orm": "tbd",
        "typescript_depth": "tbd",
        "python_mirror": "fastapi",
        "main_backend": "node-express",
    }

    refs = {entry["id"]: entry for entry in pack["references"]}
    assert refs["tpsi5-ref-vue-router"]["role"] == "technical-reference"
    assert "5.2.0" in refs["tpsi5-ref-vue-router"]["notes"]

    item = next(x for x in pack["content_items"] if x["id"] == "tpsi5-content-vue-router-navigation")
    assert item["order"] == 12
    assert item["path"] == "content/tpsi5/11_VUE_ROUTER_NAVIGAZIONE_SPA.md"
    assert item["activity_ids"] == [
        "tpsi5-activity-a-vue-router-microscope-001",
        "tpsi5-activity-b-navigation-policy-001",
        "tpsi5-activity-c-feisbuc-vue-router-001",
        "tpsi5-activity-d-debug-vue-router-001",
    ]
    assert LESSON_PATH.is_file()

    uda25 = next(u for u in design["years"][0]["udas"] if u["id"] == "uda-25")
    assert uda25["weeks"] == "5"
    assert [entry["source"] for entry in uda25["items"]] == [
        "content/tpsi5/10_VUE3_COMPONENTI_REATTIVITA.md",
        "content/tpsi5/11_VUE_ROUTER_NAVIGAZIONE_SPA.md",
    ]
    assert uda25["items"][1]["activity_ids"] == item["activity_ids"]

    assert_activity(A_ROOT, "A", "tpsi5-activity-a-vue-router-microscope-001", automatic=False)
    b = assert_activity(B_ROOT, "B", "tpsi5-activity-b-navigation-policy-001", automatic=True)
    c = assert_activity(C_ROOT, "C", "tpsi5-activity-c-feisbuc-vue-router-001", automatic=False)
    assert_activity(D_ROOT, "D", "tpsi5-activity-d-debug-vue-router-001", automatic=False)
    assert b["linguaggio"] == "javascript"
    assert c["project_milestone"] == "feisbuc-10-vue-router"


def test_navigation_policy_passes_real_javascript_runner() -> None:
    activity = load(B_ROOT / "activity.json")
    report = grade_activity.grade_activity(activity, B_ROOT / "solution/main.js", timeout_seconds=5)
    assert report["passed"] is True, report
    assert report["summary"] == {
        "passed": len(activity["test_cases"]),
        "total": len(activity["test_cases"]),
    }


def test_router_toolchain_and_reference_builds_are_pinned() -> None:
    microscope = load(A_ROOT / "starter/package.json")
    routed = load(FRONTEND / "package.json")
    for package in (microscope, routed):
        assert package["dependencies"] == {
            "vue": VUE_VERSION,
            "vue-router": ROUTER_VERSION,
        }
        assert package["devDependencies"] == {
            "@vitejs/plugin-vue": PLUGIN_VERSION,
            "vite": VITE_VERSION,
        }
        assert package["engines"]["node"] == ">=22.18"

    assert (A_ROOT / "starter/dist/index.html").is_file(), "build microscope mancante"
    assert (FRONTEND / "dist/index.html").is_file(), "build routed frontend mancante"
    built = (FRONTEND / "dist/index.html").read_text(encoding="utf-8")
    assert "/vue/assets/" in built


def test_router_guard_session_and_deep_link_boundaries_are_explicit() -> None:
    router = (C_ROOT / "solution/frontend/src/router.js").read_text(encoding="utf-8")
    session = (C_ROOT / "solution/frontend/src/session.js").read_text(encoding="utf-8")
    login = (C_ROOT / "solution/frontend/src/views/LoginView.vue").read_text(encoding="utf-8")
    app = (C_ROOT / "solution/frontend/src/App.vue").read_text(encoding="utf-8")
    fallback = (C_ROOT / "solution/backend/vue-spa.js").read_text(encoding="utf-8")
    backend_app = (C_ROOT / "solution/backend/app.js").read_text(encoding="utf-8")

    assert "createWebHistory(import.meta.env.BASE_URL)" in router
    for name in ('name: "login"', 'name: "feed"', 'name: "about"', 'name: "not-found"'):
        assert name in router
    assert 'meta: { requiresAuth: true }' in router
    assert '/:pathMatch(.*)' in router
    assert "router.beforeEach" in router
    assert "decideNavigation" in router
    assert "session.ensureKnown()" in router

    for state in ('ref("unknown")', '"anonymous"', '"authenticated"'):
        assert state in session
    assert "localStorage" not in session and "sessionStorage" not in session and "document.cookie" not in session

    assert 'value.startsWith("//")' in login
    assert "router.replace" in login
    assert "<RouterView" in app and "<RouterLink" in app

    assert 'app.get("/vue/{*splat}"' in fallback
    assert 'app.use("/vue", express.static(vueRoot))' in fallback
    assert backend_app.index('app.use("/api/posts"') < backend_app.index("installVueSpa(app") < backend_app.index("app.use(notFound)")


def test_router_debug_starter_contains_real_defects_and_reference_fixes_them() -> None:
    broken_router = (D_ROOT / "starter/router.js").read_text(encoding="utf-8")
    broken_app = (D_ROOT / "starter/App.vue").read_text(encoding="utf-8")
    broken_server = (D_ROOT / "starter/server-fallback.js").read_text(encoding="utf-8")
    fixed_router = (D_ROOT / "solution/router.js").read_text(encoding="utf-8")
    fixed_app = (D_ROOT / "solution/App.vue").read_text(encoding="utf-8")
    fixed_server = (D_ROOT / "solution/server-fallback.js").read_text(encoding="utf-8")
    diagnosis = (D_ROOT / "solution/DIAGNOSI.md").read_text(encoding="utf-8").lower()

    compact_broken = broken_router.replace(" ", "")
    assert "createWebHistory()" in broken_router
    assert "requireAuth:true" in compact_broken
    assert 'return{name:"login"}' in compact_broken
    assert "pathMatch" not in broken_router
    assert "window.location.assign" in broken_app
    assert 'app.get("/vue/*"' in broken_server

    assert "createWebHistory(import.meta.env.BASE_URL)" in fixed_router
    assert "requiresAuth:true" in fixed_router.replace(" ", "")
    assert "pathMatch" in fixed_router
    assert "decideNavigation" in fixed_router
    assert "RouterLink" in fixed_app and "window.location" not in fixed_app
    assert 'app.get("/vue/{*splat}"' in fixed_server
    for concept in ("http server", "route match", "guard", "navigation", "redirect", "wildcard"):
        assert concept in diagnosis


def new_client():
    jar = http.cookiejar.CookieJar()
    opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(jar))
    return opener, jar


def json_call(opener, url: str, *, method: str = "GET", payload=None):
    body = None if payload is None else json.dumps(payload).encode("utf-8")
    headers = {} if payload is None else {"Content-Type": "application/json"}
    req = urllib.request.Request(url, data=body, headers=headers, method=method)
    response = opener.open(req, timeout=20)
    raw = response.read()
    media = response.headers.get_content_type()
    value = json.loads(raw.decode("utf-8")) if raw and media == "application/json" else raw.decode("utf-8")
    return response.status, response.headers, value


class RunningRouterBackend:
    def __init__(self, db_path: Path):
        env = {
            **os.environ,
            "PORT": "0",
            "DB_PATH": str(db_path),
            "NODE_ENV": "development",
            "COOKIE_SECURE": "false",
        }
        server = COMPOSED / "src/server.js"
        self.process = subprocess.Popen(
            ["node", server.name], cwd=server.parent,
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, env=env,
        )
        assert self.process.stdout is not None
        line = self.process.stdout.readline().strip()
        if not line.startswith("READY http://"):
            stderr = self.process.stderr.read() if self.process.stderr else ""
            self.close()
            raise AssertionError(f"Vue Router reference backend non pronto: {line!r} {stderr!r}")
        self.base = line.removeprefix("READY ")

    def close(self):
        if self.process.poll() is not None:
            return
        self.process.terminate()
        try:
            self.process.wait(timeout=8)
        except subprocess.TimeoutExpired:
            self.process.kill()
            self.process.wait(timeout=5)

    def __enter__(self):
        return self

    def __exit__(self, *_):
        self.close()


def test_composed_router_reference_supports_deep_links_and_preserves_api_security() -> None:
    assert (COMPOSED / "node_modules/express").is_dir(), "npm install routed backend mancante"
    assert (COMPOSED / "public/vue/index.html").is_file()

    with tempfile.TemporaryDirectory() as temp:
        client, _ = new_client()
        with RunningRouterBackend(Path(temp) / "router.db") as server:
            for path in ("/vue/", "/vue/feed", "/vue/about", "/vue/route-che-non-esiste"):
                response = urllib.request.urlopen(f"{server.base}{path}", timeout=10)
                page = response.read().decode("utf-8")
                assert response.status == 200
                assert response.headers.get_content_type() == "text/html"
                assert "/vue/assets/" in page

            with pytest.raises(urllib.error.HTTPError) as anonymous:
                json_call(client, f"{server.base}/api/posts")
            assert anonymous.value.code == 401

            status, _, registered = json_call(
                client,
                f"{server.base}/api/auth/register",
                method="POST",
                payload={
                    "displayName": "Router Student",
                    "email": "router@example.test",
                    "password": "una passphrase Router molto lunga 2026",
                },
            )
            assert status == 201 and registered["user"]["email"] == "router@example.test"

            status, _, posts = json_call(client, f"{server.base}/api/posts")
            assert status == 200 and isinstance(posts, list)
            status, _, created = json_call(
                client,
                f"{server.base}/api/posts",
                method="POST",
                payload={"text": "creato con Vue Router presente"},
            )
            assert status == 201
            assert created["author"] == "Router Student"
