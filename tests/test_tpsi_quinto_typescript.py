from __future__ import annotations

import http.cookiejar
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import urllib.error
import urllib.request

import pytest

from scripts.grade_activity import SUPPORTED_LANGUAGES
from scripts.validate_activity import validate_activity

ROOT = Path(__file__).resolve().parents[1]
PACK_PATH = ROOT / "content" / "tpsi5" / "content-pack.json"
DESIGN_PATH = ROOT / "doc" / "course_designs" / "tpsi_quinto_2026_2027.json"
LESSON_PATH = ROOT / "content" / "tpsi5" / "12_TYPESCRIPT_CONTRATTI_FRONTEND.md"
A_ROOT = ROOT / "activities" / "tpsi5" / "typescript_contract_microscope_a"
B_ROOT = ROOT / "activities" / "tpsi5" / "typescript_navigation_policy_b"
C_ROOT = ROOT / "activities" / "tpsi5" / "feisbuc_typescript_c"
D_ROOT = ROOT / "activities" / "tpsi5" / "typescript_debug_d"
FRONTEND = ROOT / "_typescript-frontend"
COMPOSED = ROOT / "_typescript-reference"
TS_VERSION = "6.0.3"
VUE_TSC_VERSION = "3.3.8"


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
    assert activity["linguaggio"] == "typescript"
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


def test_typescript_content_pack_decision_and_course_design() -> None:
    pack = load(PACK_PATH)
    design = load(DESIGN_PATH)

    assert pack["version"] == "0.13.0"
    assert pack["extensions"]["bootstrap_decisions"]["typescript_depth"] == "targeted-boundary-typing"

    refs = {entry["id"]: entry for entry in pack["references"]}
    assert refs["tpsi5-ref-typescript"]["role"] == "technical-reference"
    assert refs["tpsi5-ref-vue-typescript"]["role"] == "technical-reference"
    assert "6.0.3" in refs["tpsi5-ref-typescript"]["notes"]
    assert "3.3.8" in refs["tpsi5-ref-vue-typescript"]["notes"]

    item = next(x for x in pack["content_items"] if x["id"] == "tpsi5-content-typescript-boundary-typing")
    assert item["path"] == "content/tpsi5/12_TYPESCRIPT_CONTRATTI_FRONTEND.md"
    assert item["order"] == 13
    assert item["activity_ids"] == [
        "tpsi5-activity-a-typescript-contract-microscope-001",
        "tpsi5-activity-b-typescript-navigation-policy-001",
        "tpsi5-activity-c-feisbuc-typescript-boundaries-001",
        "tpsi5-activity-d-debug-typescript-boundaries-001",
    ]
    assert LESSON_PATH.is_file()

    uda25 = next(u for u in design["years"][0]["udas"] if u["id"] == "uda-25")
    assert uda25["weeks"] == "5"
    assert [entry["source"] for entry in uda25["items"]] == [
        "content/tpsi5/10_VUE3_COMPONENTI_REATTIVITA.md",
        "content/tpsi5/11_VUE_ROUTER_NAVIGAZIONE_SPA.md",
        "content/tpsi5/12_TYPESCRIPT_CONTRATTI_FRONTEND.md",
    ]
    assert uda25["items"][2]["activity_ids"] == item["activity_ids"]
    assert "realtime" in uda25["items"][2]["frame"]["next_step"].lower()

    assert_activity(A_ROOT, "A", "tpsi5-activity-a-typescript-contract-microscope-001")
    assert_activity(B_ROOT, "B", "tpsi5-activity-b-typescript-navigation-policy-001")
    c = assert_activity(C_ROOT, "C", "tpsi5-activity-c-feisbuc-typescript-boundaries-001")
    assert_activity(D_ROOT, "D", "tpsi5-activity-d-debug-typescript-boundaries-001")
    assert c["project_milestone"] == "feisbuc-11-typescript-boundaries"


def test_platform_boundary_does_not_claim_typescript_runner() -> None:
    assert "typescript" not in SUPPORTED_LANGUAGES


def test_typescript_toolchain_is_pinned_and_strict() -> None:
    packages = [
        load(A_ROOT / "starter/package.json"),
        load(B_ROOT / "starter/package.json"),
        load(C_ROOT / "solution/frontend/package.json"),
        load(D_ROOT / "starter/package.json"),
        load(D_ROOT / "solution/package.json"),
    ]
    assert packages[0]["devDependencies"]["typescript"] == TS_VERSION
    assert packages[1]["devDependencies"]["typescript"] == TS_VERSION
    for package in packages[2:]:
        assert package["devDependencies"]["typescript"] == TS_VERSION
        assert package["devDependencies"]["vue-tsc"] == VUE_TSC_VERSION

    for config_path in (
        A_ROOT / "starter/tsconfig.json",
        B_ROOT / "starter/tsconfig.json",
        C_ROOT / "solution/frontend/tsconfig.json",
        D_ROOT / "starter/tsconfig.json",
        D_ROOT / "solution/tsconfig.json",
    ):
        options = load(config_path)["compilerOptions"]
        assert options["strict"] is True
        assert options["noUncheckedIndexedAccess"] is True
        assert options["exactOptionalPropertyTypes"] is True
        assert options["noEmit"] is True


def test_reference_typechecks_and_typed_build_exist() -> None:
    assert (A_ROOT / "starter/node_modules/typescript").is_dir(), "npm install A mancante"
    assert (B_ROOT / "starter/node_modules/typescript").is_dir(), "npm install B mancante"
    assert (D_ROOT / "solution/node_modules/vue-tsc").is_dir(), "npm install D solution mancante"
    assert (FRONTEND / "node_modules/vue-tsc").is_dir(), "npm install typed frontend mancante"
    assert (FRONTEND / "dist/index.html").is_file(), "build typed frontend mancante"
    built = (FRONTEND / "dist/index.html").read_text(encoding="utf-8")
    assert "/vue/assets/" in built


def test_typescript_boundary_source_is_explicit_and_no_any_shortcuts() -> None:
    domain = (C_ROOT / "solution/frontend/src/domain.ts").read_text(encoding="utf-8")
    api = (C_ROOT / "solution/frontend/src/api.ts").read_text(encoding="utf-8")
    policy = (C_ROOT / "solution/frontend/src/navigation-policy.ts").read_text(encoding="utf-8")
    session = (C_ROOT / "solution/frontend/src/session.ts").read_text(encoding="utf-8")
    router = (C_ROOT / "solution/frontend/src/router.ts").read_text(encoding="utf-8")
    card = (C_ROOT / "solution/frontend/src/components/PostCard.vue").read_text(encoding="utf-8")
    feed = (C_ROOT / "solution/frontend/src/views/FeedView.vue").read_text(encoding="utf-8")

    for fragment in ("interface User", "interface Post", 'type AuthStatus = "unknown" | "anonymous" | "authenticated"'):
        assert fragment in domain
    assert "Promise<unknown>" in api
    assert "const payload: unknown" in api
    assert "parsePost" in api and "parseUser" in api
    assert "as Post" not in api and "as User" not in api
    assert ": any" not in api and "<any>" not in api
    assert 'action: "redirect"; name: RouteName' in policy
    assert "ref<User | null>(null)" in session
    assert "ref<AuthStatus>(\"unknown\")" in session
    assert 'interface RouteMeta' in router and "requiresAuth?: boolean" in router
    assert 'satisfies RouteMeta' in router
    assert '<script setup lang="ts">' in card and "defineProps" in card and "defineEmits" in card
    assert "ref<Post[]>([])" in feed


def test_debug_starter_fails_and_solution_passes_without_weakening_strict() -> None:
    npm = shutil.which("npm")
    assert npm is not None
    assert (D_ROOT / "starter/node_modules/vue-tsc").is_dir(), "npm install D starter mancante"

    broken = subprocess.run(
        [npm, "run", "type-check"],
        cwd=D_ROOT / "starter",
        capture_output=True,
        text=True,
        timeout=30,
        check=False,
    )
    assert broken.returncode != 0
    combined = broken.stdout + broken.stderr
    assert "error TS" in combined

    fixed = subprocess.run(
        [npm, "run", "type-check"],
        cwd=D_ROOT / "solution",
        capture_output=True,
        text=True,
        timeout=30,
        check=False,
    )
    assert fixed.returncode == 0, fixed.stdout + fixed.stderr

    diagnosis = (D_ROOT / "solution/DIAGNOSI.md").read_text(encoding="utf-8").lower()
    for concept in ("union", "undefined", "unknown", "emit", "routemeta", "strict"):
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


class RunningTypedBackend:
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
            raise AssertionError(f"typed reference backend non pronto: {line!r} {stderr!r}")
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


def test_composed_typed_reference_preserves_deep_link_and_api_security() -> None:
    assert (COMPOSED / "node_modules/express").is_dir(), "npm install typed backend mancante"
    assert (COMPOSED / "public/vue/index.html").is_file()

    with tempfile.TemporaryDirectory() as temp:
        client, _ = new_client()
        with RunningTypedBackend(Path(temp) / "typescript.db") as server:
            for path in ("/vue/", "/vue/feed", "/vue/about"):
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
                    "displayName": "Typed Student",
                    "email": "typed@example.test",
                    "password": "una passphrase TypeScript molto lunga 2026",
                },
            )
            assert status == 201 and registered["user"]["email"] == "typed@example.test"

            status, _, created = json_call(
                client,
                f"{server.base}/api/posts",
                method="POST",
                payload={"text": "creato con frontend TypeScript presente"},
            )
            assert status == 201 and created["author"] == "Typed Student"
