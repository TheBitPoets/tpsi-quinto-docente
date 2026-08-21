from __future__ import annotations

import http.cookiejar
import json
import os
from pathlib import Path
import subprocess
import tempfile
import urllib.error
import urllib.parse
import urllib.request

import pytest

from scripts import grade_activity
from scripts.validate_activity import validate_activity


ROOT = Path(__file__).resolve().parents[1]
PACK_PATH = ROOT / "content" / "tpsi5" / "content-pack.json"
DESIGN_PATH = ROOT / "doc" / "course_designs" / "tpsi_quinto_2026_2027.json"
LESSON_PATH = ROOT / "content" / "tpsi5" / "09_SSR_NUNJUCKS_CONFRONTO.md"
A_ROOT = ROOT / "activities" / "tpsi5" / "ssr_view_model_a"
B_ROOT = ROOT / "activities" / "tpsi5" / "nunjucks_autoescape_b"
C_ROOT = ROOT / "activities" / "tpsi5" / "feisbuc_ssr_c"
D_ROOT = ROOT / "activities" / "tpsi5" / "ssr_debug_d"
COMPOSED_ROOT = ROOT / "_ssr-reference"
PASSWORD = "una passphrase lunga 2026"


def load(path: Path) -> dict:
    value = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(value, dict)
    return value


def assert_activity(root: Path, difficulty: str, activity_id: str, automatic: bool) -> dict:
    activity = load(root / "activity.json")
    assert validate_activity(activity, str(root / "activity.json")) == []
    assert activity["id"] == activity_id
    assert activity["difficolta"] == difficulty
    assert sum(entry["punti"] for entry in activity["rubrica"]) == 10
    student_targets: set[str] = set()
    for asset in activity["assets"]:
        assert (root / asset["path"]).is_file(), asset
        if asset["visibility"] == "student":
            target = asset.get("target_path")
            assert isinstance(target, str) and target
            assert target not in student_targets
            student_targets.add(target)
        else:
            assert asset["visibility"] == "teacher"
    assert activity["correzione"]["test"] is automatic
    return activity


class RunningServer:
    def __init__(self, *, db_path: Path):
        env = dict(os.environ)
        env.update({
            "PORT": "0",
            "DB_PATH": str(db_path),
            "NODE_ENV": "development",
            "COOKIE_SECURE": "false",
            "SESSION_TTL_MS": str(8 * 60 * 60 * 1000),
        })
        server = COMPOSED_ROOT / "src" / "server.js"
        self.process = subprocess.Popen(
            ["node", server.name],
            cwd=server.parent,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            env=env,
        )
        assert self.process.stdout is not None
        line = self.process.stdout.readline().strip()
        if not line.startswith("READY http://"):
            stderr = self.process.stderr.read() if self.process.stderr else ""
            self.close()
            raise AssertionError(f"SSR server non pronto: {line!r} stderr={stderr!r}")
        self.base = line.removeprefix("READY ")

    def close(self) -> None:
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

    def __exit__(self, exc_type, exc, tb):
        self.close()


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


def new_client(*, follow_redirects: bool = True, jar: http.cookiejar.CookieJar | None = None):
    jar = jar or http.cookiejar.CookieJar()
    handlers = [urllib.request.HTTPCookieProcessor(jar)]
    if not follow_redirects:
        handlers.append(NoRedirect())
    return urllib.request.build_opener(*handlers), jar


def decode_response(response):
    raw = response.read()
    media = response.headers.get_content_type()
    if raw and media == "application/json":
        return json.loads(raw.decode("utf-8"))
    return raw.decode("utf-8")


def request_json(opener, url: str, *, method: str = "GET", payload=None):
    body = None if payload is None else json.dumps(payload).encode("utf-8")
    headers = {"Content-Type": "application/json"} if payload is not None else {}
    req = urllib.request.Request(url, data=body, headers=headers, method=method)
    response = opener.open(req, timeout=15)
    return response.status, response.headers, decode_response(response)


def request_form_no_redirect(jar: http.cookiejar.CookieJar, url: str, *, payload: dict[str, str]):
    opener, _ = new_client(follow_redirects=False, jar=jar)
    body = urllib.parse.urlencode(payload).encode("utf-8")
    req = urllib.request.Request(
        url,
        data=body,
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        method="POST",
    )
    with pytest.raises(urllib.error.HTTPError) as exc:
        opener.open(req, timeout=15)
    return exc.value


def error_json(opener, url: str, *, method: str = "GET", payload=None):
    with pytest.raises(urllib.error.HTTPError) as exc:
        request_json(opener, url, method=method, payload=payload)
    error = exc.value
    raw = error.read()
    media = error.headers.get_content_type()
    value = json.loads(raw.decode("utf-8")) if raw and media == "application/json" else raw.decode("utf-8")
    return error.code, error.headers, value


def test_ssr_content_pack_design_and_activity_contracts_close_uda24() -> None:
    pack = load(PACK_PATH)
    design = load(DESIGN_PATH)
    item = next(x for x in pack["content_items"] if x["id"] == "tpsi5-content-ssr-nunjucks-comparison")

    assert pack["version"] == "0.19.0"
    assert item["order"] == 10
    assert item["path"] == "content/tpsi5/09_SSR_NUNJUCKS_CONFRONTO.md"
    assert item["activity_ids"] == [
        "tpsi5-activity-a-ssr-view-model-001",
        "tpsi5-activity-b-nunjucks-autoescape-001",
        "tpsi5-activity-c-feisbuc-ssr-001",
        "tpsi5-activity-d-debug-ssr-boundaries-001",
    ]
    refs = {ref["id"] for ref in item["source_refs"]}
    assert {"tpsi5-ref-nunjucks", "tpsi5-ref-express", "tpsi5-ref-rfc9110", "tpsi5-ref-lab10-legacy"} <= refs
    assert LESSON_PATH.is_file()

    uda24 = next(u for u in design["years"][0]["udas"] if u["id"] == "uda-24")
    assert uda24["weeks"] == "7"
    assert len(uda24["items"]) == 4
    assert uda24["items"][3]["source"] == item["path"]
    assert uda24["items"][3]["activity_ids"] == item["activity_ids"]
    assert "UDA25" in uda24["items"][3]["frame"]["next_step"]

    a = assert_activity(A_ROOT, "A", "tpsi5-activity-a-ssr-view-model-001", True)
    b = assert_activity(B_ROOT, "B", "tpsi5-activity-b-nunjucks-autoescape-001", False)
    c = assert_activity(C_ROOT, "C", "tpsi5-activity-c-feisbuc-ssr-001", False)
    d = assert_activity(D_ROOT, "D", "tpsi5-activity-d-debug-ssr-boundaries-001", False)
    assert a["linguaggio"] == "javascript"
    assert b["linguaggio"] == c["linguaggio"] == d["linguaggio"] == "nodejs"
    assert c["project_milestone"] == "feisbuc-08-ssr-nunjucks"


def test_view_model_reference_passes_real_javascript_runner() -> None:
    activity = load(A_ROOT / "activity.json")
    report = grade_activity.grade_activity(activity, A_ROOT / "solution" / "main.js", timeout_seconds=5)
    assert report["passed"] is True, report
    assert report["summary"] == {
        "passed": len(activity["test_cases"]),
        "total": len(activity["test_cases"]),
    }


def test_nunjucks_reference_is_pinned_explicit_and_autoescapes_user_text() -> None:
    package = load(B_ROOT / "solution" / "package.json")
    assert package["dependencies"] == {"nunjucks": "3.2.4"}
    assert (B_ROOT / "solution" / "node_modules" / "nunjucks").is_dir(), "npm install Nunjucks CI mancante"

    renderer = (B_ROOT / "solution" / "render.mjs").read_text(encoding="utf-8")
    template = (B_ROOT / "solution" / "templates" / "post.njk").read_text(encoding="utf-8")
    assert "new nunjucks.FileSystemLoader" in renderer
    assert "new nunjucks.Environment" in renderer
    assert "autoescape: true" in renderer
    assert "throwOnUndefined: true" in renderer
    assert "| safe" not in template and "|safe" not in template

    rendered = subprocess.run(
        ["node", "render.mjs"], cwd=B_ROOT / "solution", capture_output=True, text=True, timeout=10, check=False
    )
    assert rendered.returncode == 0, rendered.stderr
    assert "&lt;script&gt;" in rendered.stdout
    assert "<script>" not in rendered.stdout
    assert "Elimina" in rendered.stdout

    hidden = subprocess.run(
        ["node", "render.mjs", "no-delete"], cwd=B_ROOT / "solution", capture_output=True, text=True, timeout=10, check=False
    )
    assert hidden.returncode == 0, hidden.stderr
    assert "Elimina" not in hidden.stdout


def test_composed_feisbuc_ssr_reference_keeps_api_session_store_and_prg() -> None:
    assert COMPOSED_ROOT.is_dir(), "composizione SSR CI mancante"
    assert (COMPOSED_ROOT / "node_modules" / "express").is_dir(), "npm install Express CI mancante"
    assert (COMPOSED_ROOT / "node_modules" / "nunjucks").is_dir(), "npm install Nunjucks CI mancante"

    with tempfile.TemporaryDirectory() as temp:
        db_path = Path(temp) / "ssr-e2e.db"
        alice, alice_jar = new_client()
        bob, bob_jar = new_client()

        with RunningServer(db_path=db_path) as server:
            code, _, anonymous = error_json(alice, f"{server.base}/ssr")
            assert code == 401
            assert anonymous["error"]["code"] == "authentication-required"

            status, _, alice_payload = request_json(
                alice,
                f"{server.base}/api/auth/register",
                method="POST",
                payload={"displayName": "Alice", "email": "alice@example.test", "password": PASSWORD},
            )
            assert status == 201
            alice_id = alice_payload["user"]["id"]

            status, headers, html = request_json(alice, f"{server.base}/ssr")
            assert status == 200
            assert headers.get_content_type() == "text/html"
            assert "Feed SSR" in html and "Alice" in html

            malicious = '<script>alert("ssr")</script>'
            redirect = request_form_no_redirect(alice_jar, f"{server.base}/ssr/posts", payload={"text": malicious})
            assert redirect.code == 303
            assert redirect.headers["Location"] == "/ssr"

            status, _, html = request_json(alice, f"{server.base}/ssr")
            assert status == 200
            assert "&lt;script&gt;" in html
            assert "<script>" not in html

            status, api_headers, posts = request_json(alice, f"{server.base}/api/posts")
            assert status == 200
            assert api_headers.get_content_type() == "application/json"
            created = next(post for post in posts if post["text"] == malicious)
            post_id = created["id"]
            assert created["authorId"] == alice_id

            status, _, bob_payload = request_json(
                bob,
                f"{server.base}/api/auth/register",
                method="POST",
                payload={"displayName": "Bob", "email": "bob@example.test", "password": "altra passphrase lunga 2026"},
            )
            assert status == 201 and bob_payload["user"]["id"] != alice_id

            _, _, bob_html = request_json(bob, f"{server.base}/ssr")
            assert f'/ssr/posts/{post_id}/delete' not in bob_html

            bob_no_redirect, _ = new_client(follow_redirects=False, jar=bob_jar)
            body = urllib.parse.urlencode({}).encode("utf-8")
            req = urllib.request.Request(
                f"{server.base}/ssr/posts/{post_id}/delete",
                data=body,
                headers={"Content-Type": "application/x-www-form-urlencoded"},
                method="POST",
            )
            with pytest.raises(urllib.error.HTTPError) as forbidden:
                bob_no_redirect.open(req, timeout=15)
            assert forbidden.value.code == 403

            owner_redirect = request_form_no_redirect(
                alice_jar, f"{server.base}/ssr/posts/{post_id}/delete", payload={}
            )
            assert owner_redirect.code == 303
            assert owner_redirect.headers["Location"] == "/ssr"

            _, _, remaining = request_json(alice, f"{server.base}/api/posts")
            assert post_id not in {post["id"] for post in remaining}


def test_ssr_overlay_and_debug_reference_preserve_boundaries() -> None:
    package = load(C_ROOT / "solution" / "package.json")
    assert package["dependencies"] == {"express": "5.2.1", "nunjucks": "3.2.4"}

    app = (C_ROOT / "solution" / "src" / "app.js").read_text(encoding="utf-8")
    router = (C_ROOT / "solution" / "src" / "ssr.router.js").read_text(encoding="utf-8")
    engine = (C_ROOT / "solution" / "src" / "view-engine.js").read_text(encoding="utf-8")
    feed = (C_ROOT / "solution" / "views" / "feed.njk").read_text(encoding="utf-8")
    diagnosis = (D_ROOT / "solution" / "DIAGNOSI.md").read_text(encoding="utf-8").lower()

    assert 'app.use("/api/posts"' in app and 'app.use("/ssr"' in app
    assert "express.urlencoded" in app
    assert "res.redirect(303, \"/ssr\")" in router
    assert "deleteOwned(req.params.id, req.auth.user.id)" in router
    assert "req.auth.user.id" in router
    assert "new nunjucks.Environment" in engine and "autoescape: true" in engine
    assert "|safe" not in feed and "| safe" not in feed
    assert "password_hash" not in feed and "session" not in feed.lower()

    for concept in ("safe", "authorization", "get", "303", "secret", "authorid"):
        assert concept in diagnosis