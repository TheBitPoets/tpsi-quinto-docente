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

from scripts.validate_activity import validate_activity


ROOT = Path(__file__).resolve().parents[1]
PACK_PATH = ROOT / "content" / "tpsi5" / "content-pack.json"
DESIGN_PATH = ROOT / "doc" / "course_designs" / "tpsi_quinto_2026_2027.json"
LESSON_PATH = ROOT / "content" / "tpsi5" / "10_VUE3_COMPONENTI_REATTIVITA.md"
A_ROOT = ROOT / "activities" / "tpsi5" / "vue_reactivity_a"
B_ROOT = ROOT / "activities" / "tpsi5" / "vue_post_card_b"
C_ROOT = ROOT / "activities" / "tpsi5" / "feisbuc_vue_c"
D_ROOT = ROOT / "activities" / "tpsi5" / "vue_debug_d"
COMPOSED = ROOT / "_vue-reference"
VUE_VERSION = "3.5.40"
VITE_VERSION = "8.2.1"
PLUGIN_VERSION = "6.0.8"


def load(path: Path) -> dict:
    value = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(value, dict)
    return value


def assert_activity(root: Path, difficulty: str, activity_id: str) -> dict:
    activity = load(root / "activity.json")
    assert validate_activity(activity, str(root / "activity.json")) == []
    assert activity["id"] == activity_id
    assert activity["difficolta"] == difficulty
    assert activity["contesto"]["uda"] == "uda-25"
    assert activity["correzione"] == {
        "compila": False,
        "test": False,
        "sandbox": False,
        "ai_feedback": False,
    }
    assert sum(entry["punti"] for entry in activity["rubrica"]) == 10
    for asset in activity["assets"]:
        assert (root / asset["path"]).is_file(), asset
        if asset["visibility"] == "student":
            assert asset.get("target_path")
    return activity


def package_versions(path: Path) -> None:
    package = load(path)
    assert package["dependencies"] == {"vue": VUE_VERSION}
    assert package["devDependencies"] == {
        "@vitejs/plugin-vue": PLUGIN_VERSION,
        "vite": VITE_VERSION,
    }
    assert package["engines"]["node"] == ">=22.18"


def test_vue_content_pack_decision_course_design_and_activity_contracts() -> None:
    pack = load(PACK_PATH)
    design = load(DESIGN_PATH)
    assert pack["version"] == "0.17.0"
    decisions = pack["extensions"]["bootstrap_decisions"]
    assert decisions["frontend_framework"] == "vue3-vite"
    assert decisions["typescript_depth"] == "targeted-boundary-typing"
    assert decisions["node_orm"] == "tbd"

    item = next(x for x in pack["content_items"] if x["id"] == "tpsi5-content-vue3-components-reactivity")
    assert item["path"] == "content/tpsi5/10_VUE3_COMPONENTI_REATTIVITA.md"
    assert item["order"] == 11
    assert item["activity_ids"] == [
        "tpsi5-activity-a-vue-reactivity-microscope-001",
        "tpsi5-activity-b-vue-post-card-001",
        "tpsi5-activity-c-feisbuc-vue-spa-001",
        "tpsi5-activity-d-debug-vue-reactivity-001",
    ]
    refs = {entry["id"] for entry in item["source_refs"]}
    assert {"tpsi5-ref-vue", "tpsi5-ref-vite", "tpsi5-ref-mdn"} <= refs
    assert LESSON_PATH.is_file()

    uda25 = next(u for u in design["years"][0]["udas"] if u["id"] == "uda-25")
    assert uda25["weeks"] == "5"
    assert len(uda25["items"]) == 5
    assert uda25["items"][0]["source"] == item["path"]
    assert uda25["items"][0]["activity_ids"] == item["activity_ids"]
    assert "routing" in uda25["items"][0]["frame"]["next_step"].lower()
    assert uda25["items"][1]["source"] == "content/tpsi5/11_VUE_ROUTER_NAVIGAZIONE_SPA.md"
    assert uda25["items"][2]["source"] == "content/tpsi5/12_TYPESCRIPT_CONTRATTI_FRONTEND.md"
    assert uda25["items"][3]["source"] == "content/tpsi5/13_WEBSOCKET_SOCKETIO_REALTIME.md"
    assert uda25["items"][4]["source"] == "content/tpsi5/14_REACT_TRANSLATION_COMPARISON.md"

    assert_activity(A_ROOT, "A", "tpsi5-activity-a-vue-reactivity-microscope-001")
    assert_activity(B_ROOT, "B", "tpsi5-activity-b-vue-post-card-001")
    c = assert_activity(C_ROOT, "C", "tpsi5-activity-c-feisbuc-vue-spa-001")
    assert_activity(D_ROOT, "D", "tpsi5-activity-d-debug-vue-reactivity-001")
    assert c["project_milestone"] == "feisbuc-09-vue-spa"


def test_vue_reference_toolchain_is_pinned_and_build_outputs_exist() -> None:
    for package in (
        A_ROOT / "starter/package.json",
        B_ROOT / "solution/package.json",
        C_ROOT / "solution/frontend/package.json",
        D_ROOT / "starter/package.json",
        D_ROOT / "solution/package.json",
    ):
        package_versions(package)

    for dist in (
        A_ROOT / "starter/dist/index.html",
        B_ROOT / "solution/dist/index.html",
        C_ROOT / "solution/frontend/dist/index.html",
        D_ROOT / "starter/dist/index.html",
        D_ROOT / "solution/dist/index.html",
    ):
        assert dist.is_file(), f"reference build mancante: {dist}"

    spa_html = (C_ROOT / "solution/frontend/dist/index.html").read_text(encoding="utf-8")
    assert "/vue/assets/" in spa_html


def test_vue_component_and_auth_boundaries_are_explicit() -> None:
    app = (C_ROOT / "solution/frontend/src/App.vue").read_text(encoding="utf-8")
    api = (C_ROOT / "solution/frontend/src/api.js").read_text(encoding="utf-8")
    card = (C_ROOT / "solution/frontend/src/components/PostCard.vue").read_text(encoding="utf-8")
    package = (C_ROOT / "solution/frontend/package.json").read_text(encoding="utf-8").lower()

    for fragment in ("ref(", "computed(", "onMounted(", "PostCard", "api.", "post.authorId===user.id"):
        assert fragment in app
    assert 'credentials:"same-origin"' in api
    for forbidden in ("localStorage", "sessionStorage", "document.cookie", "authorId"):
        assert forbidden not in api
    assert "fetch(" not in card
    assert "defineProps" in card and "defineEmits" in card
    assert "props.post.liked =" not in card
    for forbidden in ("vue-router", "pinia", "typescript"):
        assert forbidden not in package


def test_vue_debug_starter_encodes_real_failures_and_solution_fixes_them() -> None:
    starter_app = (D_ROOT / "starter/src/App.vue").read_text(encoding="utf-8")
    starter_card = (D_ROOT / "starter/src/components/PostCard.vue").read_text(encoding="utf-8")
    fixed_app = (D_ROOT / "solution/src/App.vue").read_text(encoding="utf-8")
    fixed_card = (D_ROOT / "solution/src/components/PostCard.vue").read_text(encoding="utf-8")
    diagnosis = (D_ROOT / "solution/DIAGNOSI.md").read_text(encoding="utf-8").lower()

    assert "const { title } = state" in starter_app
    assert "const postCount = ref(posts.value.length)" in starter_app
    assert ':key="index"' in starter_app
    assert 'defineEmits(["toggle"])' in starter_card
    assert "props.post.liked=!props.post.liked" in starter_card.replace(" ", "")

    assert 'toRef(state,"title")' in fixed_app
    assert "computed(()=>posts.value.length)" in fixed_app
    assert ':key="post.id"' in fixed_app
    assert 'defineEmits(["toggle-like"])' in fixed_card
    assert "props.post.liked=" not in fixed_card.replace(" ", "")
    for concept in ("reattiv", "computed", "prop", "toggle-like", "post.id"):
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


class RunningVueBackend:
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
            raise AssertionError(f"Vue reference backend non pronto: {line!r} {stderr!r}")
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


def test_composed_vue_reference_serves_spa_and_preserves_auth_api_contract() -> None:
    assert (COMPOSED / "node_modules/express").is_dir(), "npm install backend composto mancante"
    assert (COMPOSED / "public/vue/index.html").is_file()

    with tempfile.TemporaryDirectory() as temp:
        client, _ = new_client()
        with RunningVueBackend(Path(temp) / "vue.db") as server:
            html = urllib.request.urlopen(f"{server.base}/vue/", timeout=10)
            page = html.read().decode("utf-8")
            assert html.status == 200 and html.headers.get_content_type() == "text/html"
            assert "/vue/assets/" in page

            with pytest.raises(urllib.error.HTTPError) as anonymous:
                json_call(client, f"{server.base}/api/auth/me")
            assert anonymous.value.code == 401

            status, _, registered = json_call(
                client,
                f"{server.base}/api/auth/register",
                method="POST",
                payload={
                    "displayName": "Vue Student",
                    "email": "vue@example.test",
                    "password": "una passphrase Vue molto lunga 2026",
                },
            )
            assert status == 201 and registered["user"]["email"] == "vue@example.test"

            status, _, posts = json_call(client, f"{server.base}/api/posts")
            assert status == 200 and isinstance(posts, list)
            status, _, created = json_call(
                client,
                f"{server.base}/api/posts",
                method="POST",
                payload={"text": "creato mentre la SPA e servita"},
            )
            assert status == 201 and created["author"] == "Vue Student"