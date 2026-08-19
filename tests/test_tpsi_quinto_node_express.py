from __future__ import annotations

import json
import os
from pathlib import Path
import shutil
import subprocess
import urllib.error
import urllib.request

import pytest

from scripts import grade_activity
from scripts.validate_activity import validate_activity


ROOT = Path(__file__).resolve().parents[1]
PACK_PATH = ROOT / "content" / "tpsi5" / "content-pack.json"
DESIGN_PATH = ROOT / "doc" / "course_designs" / "tpsi_quinto_2026_2027.json"
LESSON_PATH = ROOT / "content" / "tpsi5" / "06_NODE_EXPRESS_BACKEND.md"

A_ROOT = ROOT / "activities" / "tpsi5" / "node_http_express_a"
B_ROOT = ROOT / "activities" / "tpsi5" / "post_validation_b"
C_ROOT = ROOT / "activities" / "tpsi5" / "feisbuc_express_c"
D_ROOT = ROOT / "activities" / "tpsi5" / "express_debug_d"

EXPRESS_VERSION = "5.2.1"


def load(path: Path) -> dict:
    value = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(value, dict)
    return value


class RunningServer:
    def __init__(self, server: Path):
        env = dict(os.environ)
        env["PORT"] = "0"
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
            raise AssertionError(f"server non pronto: {line!r} stderr={stderr!r}")
        self.base = line.removeprefix("READY ")

    def close(self) -> None:
        if self.process.poll() is not None:
            return
        self.process.terminate()
        try:
            self.process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            self.process.kill()
            self.process.wait(timeout=5)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        self.close()


def request(
    url: str,
    *,
    method: str = "GET",
    payload=None,
    raw: bytes | None = None,
    content_type: str | None = None,
):
    data = raw
    if raw is None and payload is not None:
        data = json.dumps(payload).encode("utf-8")
    headers = {}
    if content_type:
        headers["Content-Type"] = content_type
    req = urllib.request.Request(url, data=data, headers=headers, method=method)
    response = urllib.request.urlopen(req, timeout=5)
    body = response.read()
    media_type = response.headers.get_content_type()
    decoded = json.loads(body.decode("utf-8")) if body and media_type == "application/json" else body.decode("utf-8")
    return response.status, response.headers, decoded


def error_response(error: urllib.error.HTTPError):
    body = error.read()
    media_type = error.headers.get_content_type()
    decoded = json.loads(body.decode("utf-8")) if body and media_type == "application/json" else body.decode("utf-8")
    return error.code, error.headers, decoded


def assert_activity(root: Path, difficulty: str, activity_id: str, automatic: bool) -> dict:
    path = root / "activity.json"
    activity = load(path)
    assert validate_activity(activity, str(path)) == []
    assert activity["id"] == activity_id
    assert activity["difficolta"] == difficulty
    assert sum(entry["punti"] for entry in activity["rubrica"]) == 10

    student_targets: set[str] = set()
    for asset in activity["assets"]:
        asset_path = root / asset["path"]
        assert asset_path.is_file(), asset_path
        if asset["visibility"] == "student":
            assert asset["type"] not in {"teacher_only", "hidden_test"}
            target = asset.get("target_path")
            assert isinstance(target, str) and target
            assert target not in student_targets
            student_targets.add(target)
        else:
            assert asset["visibility"] == "teacher"

    if automatic:
        assert activity["correzione"]["test"] is True
        assert activity["correzione"]["sandbox"] is True
        assert activity["test_cases"]
    else:
        assert activity["correzione"] == {
            "compila": False,
            "test": False,
            "sandbox": False,
            "ai_feedback": False,
        }
    return activity


def test_uda24_content_pack_course_design_and_activity_contracts() -> None:
    pack = load(PACK_PATH)
    design = load(DESIGN_PATH)
    item = next(item for item in pack["content_items"] if item["id"] == "tpsi5-content-node-express-backend")

    assert pack["version"] == "0.7.0"
    assert item["path"] == "content/tpsi5/06_NODE_EXPRESS_BACKEND.md"
    assert item["order"] == 7
    assert item["activity_ids"] == [
        "tpsi5-activity-a-node-http-express-map-001",
        "tpsi5-activity-b-post-validation-001",
        "tpsi5-activity-c-feisbuc-express-api-001",
        "tpsi5-activity-d-debug-express-pipeline-001",
    ]
    assert {
        "tpsi5-source-originali",
        "tpsi5-source-labs-legacy",
        "tpsi5-ref-node",
        "tpsi5-ref-express",
        "tpsi5-ref-rfc9110",
        "tpsi5-ref-lab5-legacy",
        "tpsi5-ref-lab8-legacy",
        "tpsi5-ref-lab9-legacy",
        "tpsi5-ref-lab10-legacy",
    } <= {ref["id"] for ref in item["source_refs"]}
    assert LESSON_PATH.is_file()

    uda24 = next(uda for uda in design["years"][0]["udas"] if uda["id"] == "uda-24")
    assert len(uda24["items"]) == 1
    assert uda24["items"][0]["source"] == "content/tpsi5/06_NODE_EXPRESS_BACKEND.md"
    assert uda24["items"][0]["activity_ids"] == item["activity_ids"]
    assert "SQL raw" in uda24["items"][0]["frame"]["next_step"]

    assert_activity(A_ROOT, "A", "tpsi5-activity-a-node-http-express-map-001", False)
    b = assert_activity(B_ROOT, "B", "tpsi5-activity-b-post-validation-001", True)
    c = assert_activity(C_ROOT, "C", "tpsi5-activity-c-feisbuc-express-api-001", False)
    assert_activity(D_ROOT, "D", "tpsi5-activity-d-debug-express-pipeline-001", False)
    assert b["linguaggio"] == "javascript"
    assert c["project_milestone"] == "feisbuc-05-express-api"


def test_express_version_is_exactly_pinned_and_scope_excludes_later_layers() -> None:
    package_paths = [
        A_ROOT / "starter" / "package.json",
        C_ROOT / "starter" / "package.json",
        C_ROOT / "solution" / "package.json",
        D_ROOT / "starter" / "package.json",
        D_ROOT / "solution" / "package.json",
    ]
    for path in package_paths:
        package = load(path)
        assert package["dependencies"]["express"] == EXPRESS_VERSION
        assert package["type"] == "module"

    solution_text = "\n".join(
        path.read_text(encoding="utf-8")
        for path in (C_ROOT / "solution" / "src").glob("*.js")
    ).lower()
    for forbidden in ("sqlite", "sequelize", "prisma", "drizzle", "nunjucks", "bcrypt", "jsonwebtoken", "cors("):
        assert forbidden not in solution_text


def test_activity_b_validation_solution_passes_real_platform_javascript_runner() -> None:
    assert shutil.which("node") is not None, "Node.js richiesto dalla CI TPSI5"
    activity = load(B_ROOT / "activity.json")
    report = grade_activity.grade_activity(
        activity,
        B_ROOT / "solution" / "main.js",
        timeout_seconds=5,
    )
    assert report["passed"] is True, report
    assert report["summary"] == {
        "passed": len(activity["test_cases"]),
        "total": len(activity["test_cases"]),
    }


def test_node_http_and_express_comparison_servers_preserve_observable_contract() -> None:
    assert shutil.which("node") is not None
    for server_path in (
        A_ROOT / "starter" / "native-server.js",
        A_ROOT / "starter" / "express-server.js",
    ):
        with RunningServer(server_path) as server:
            status, headers, health = request(f"{server.base}/api/health")
            assert status == 200
            assert headers.get_content_type() == "application/json"
            assert health["ok"] is True

            status, _, echo = request(
                f"{server.base}/api/echo",
                method="POST",
                payload={"message": "same-contract"},
                content_type="application/json",
            )
            assert status == 200
            assert echo["received"] == {"message": "same-contract"}

            with pytest.raises(urllib.error.HTTPError) as missing:
                urllib.request.urlopen(f"{server.base}/missing", timeout=5)
            code, headers, payload = error_response(missing.value)
            assert code == 404
            assert headers.get_content_type() == "application/json"
            assert payload["error"] == "not-found"


def test_feisbuc_express_reference_serves_client_and_rest_contract() -> None:
    assert (C_ROOT / "solution" / "node_modules" / "express").is_dir(), "npm install CI mancante"
    with RunningServer(C_ROOT / "solution" / "src" / "server.js") as server:
        status, headers, html = request(f"{server.base}/")
        assert status == 200
        assert headers.get_content_type() == "text/html"
        assert "Feisbuc" in html
        assert headers["X-Request-Id"]
        assert headers.get("X-Powered-By") is None
        assert headers.get("Access-Control-Allow-Origin") is None

        status, headers, posts = request(f"{server.base}/api/posts")
        assert status == 200
        assert headers.get_content_type() == "application/json"
        assert headers["X-Request-Id"]
        assert len(posts) == 1

        status, headers, created = request(
            f"{server.base}/api/posts",
            method="POST",
            payload={"text": "  Express CI  "},
            content_type="application/json",
        )
        assert status == 201
        assert headers["Location"] == f"/api/posts/{created['id']}"
        assert created["text"] == "Express CI"
        assert created["liked"] is False

        status, _, updated = request(
            f"{server.base}/api/posts/{created['id']}",
            method="PATCH",
            payload={"liked": True},
            content_type="application/json",
        )
        assert status == 200
        assert updated["liked"] is True
        assert updated["likes"] == 1

        status, _, liked = request(f"{server.base}/api/posts?liked=true")
        assert status == 200
        assert created["id"] in {post["id"] for post in liked}
        assert all(post["liked"] is True for post in liked)

        bad_media = urllib.request.Request(
            f"{server.base}/api/posts",
            data=b"text=bad",
            headers={"Content-Type": "text/plain"},
            method="POST",
        )
        with pytest.raises(urllib.error.HTTPError) as media_error:
            urllib.request.urlopen(bad_media, timeout=5)
        code, _, payload = error_response(media_error.value)
        assert code == 415
        assert payload["error"]["code"] == "unsupported-media-type"
        assert payload["error"]["requestId"]

        with pytest.raises(urllib.error.HTTPError) as validation_error:
            request(
                f"{server.base}/api/posts",
                method="POST",
                payload={},
                content_type="application/json",
            )
        code, _, payload = error_response(validation_error.value)
        assert code == 400
        assert payload["error"]["code"] == "text-required"

        invalid_json = urllib.request.Request(
            f"{server.base}/api/posts",
            data=b"{broken",
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        with pytest.raises(urllib.error.HTTPError) as parse_error:
            urllib.request.urlopen(invalid_json, timeout=5)
        code, _, payload = error_response(parse_error.value)
        assert code == 400
        assert payload["error"]["code"] == "invalid-json"

        with pytest.raises(urllib.error.HTTPError) as missing_post:
            request(
                f"{server.base}/api/posts/missing",
                method="PATCH",
                payload={"liked": True},
                content_type="application/json",
            )
        code, _, payload = error_response(missing_post.value)
        assert code == 404
        assert payload["error"]["code"] == "post-not-found"

        with pytest.raises(urllib.error.HTTPError) as unknown:
            urllib.request.urlopen(f"{server.base}/api/unknown", timeout=5)
        code, _, payload = error_response(unknown.value)
        assert code == 404
        assert payload["error"]["code"] == "not-found"


def test_feisbuc_express_reference_has_replaceable_store_and_ordered_middleware() -> None:
    app = (C_ROOT / "solution" / "src" / "app.js").read_text(encoding="utf-8")
    router = (C_ROOT / "solution" / "src" / "posts.router.js").read_text(encoding="utf-8")
    validation = (C_ROOT / "solution" / "src" / "validation.js").read_text(encoding="utf-8")
    store = (C_ROOT / "solution" / "src" / "post-store.js").read_text(encoding="utf-8")
    middleware = (C_ROOT / "solution" / "src" / "middleware.js").read_text(encoding="utf-8")

    ordered_fragments = [
        "app.use(requestContext)",
        "app.use(requestLogger)",
        "app.use(express.json",
        "app.use(express.static",
        'app.use("/api/posts"',
        "app.use(notFound)",
        "app.use(errorHandler)",
    ]
    positions = [app.index(fragment) for fragment in ordered_fragments]
    assert positions == sorted(positions)

    assert "Router()" in router
    assert "postStore" in router
    assert "new MemoryPostStore" not in router
    assert "randomUUID" not in router
    assert "express" not in validation.lower()
    assert "express" not in store.lower()
    assert "function errorHandler(error, req, res, next)" in middleware
    assert "X-Request-Id" in middleware


def test_express_debug_solution_fixes_pipeline_without_mutating_get() -> None:
    assert (D_ROOT / "solution" / "node_modules" / "express").is_dir(), "npm install CI mancante"
    broken = (D_ROOT / "starter" / "server.js").read_text(encoding="utf-8")
    fixed = (D_ROOT / "solution" / "server.js").read_text(encoding="utf-8")
    diagnosis = (D_ROOT / "solution" / "DIAGNOSI.md").read_text(encoding="utf-8")

    assert 'app.use("/api/posts", router)' in broken
    assert broken.index('app.use("/api/posts", router)') < broken.index("app.use(express.json())")
    assert "req.query.id" in broken
    assert 'router.get("/create"' in broken
    assert "app.use((error, req, res)" in broken

    assert fixed.index("app.use(express.json())") < fixed.index('app.use("/api/posts", router)')
    assert "req.params.id" in fixed
    assert 'router.get("/create"' not in fixed
    assert "app.use((error, req, res, next)" in fixed

    for concept in ("express.json", "req.params", "GET", "express.static", "quattro argomenti"):
        assert concept.lower() in diagnosis.lower()

    with RunningServer(D_ROOT / "solution" / "server.js") as server:
        status, headers, html = request(f"{server.base}/")
        assert status == 200
        assert headers.get_content_type() == "text/html"
        assert "Express pipeline debug" in html

        status, _, post = request(f"{server.base}/api/posts/p1")
        assert status == 200
        assert post["id"] == "p1"

        status, _, before = request(f"{server.base}/api/posts")
        with pytest.raises(urllib.error.HTTPError) as mutating_get:
            urllib.request.urlopen(f"{server.base}/api/posts/create?text=bad", timeout=5)
        assert mutating_get.value.code == 404
        status, _, after = request(f"{server.base}/api/posts")
        assert len(after) == len(before)

        status, _, created = request(
            f"{server.base}/api/posts",
            method="POST",
            payload={"text": "POST corretto"},
            content_type="application/json",
        )
        assert status == 201
        assert created["text"] == "POST corretto"

        with pytest.raises(urllib.error.HTTPError) as explode:
            urllib.request.urlopen(f"{server.base}/api/posts/explode", timeout=5)
        code, headers, payload = error_response(explode.value)
        assert code == 500
        assert headers.get_content_type() == "application/json"
        assert payload["error"]["code"] == "internal-error"


def test_legacy_audit_records_backend_debts_and_deferred_layers() -> None:
    audit = (ROOT / "doc" / "LEGACY_REUSE_AUDIT.md").read_text(encoding="utf-8")
    for sha in (
        "be9a3988aec8a99b1a0f6776ad8cbeba33d82353",
        "97ee815691e0c985e5216e6f9ed264fd809509ee",
        "7319c0696c8a6f76237e1ef21b4c3c2b535c4958",
    ):
        assert sha in audit
    assert "GET /N2N" in audit
    assert "password" in audit.lower()
    assert "path SQLite assoluto" in audit
    assert "Nunjucks" in audit
    assert "MemoryPostStore" in audit
    assert "SQL raw repository" in audit
