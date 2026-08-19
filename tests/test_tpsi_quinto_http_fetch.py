from __future__ import annotations

import json
import os
from pathlib import Path
import shutil
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
LESSON_PATH = ROOT / "content" / "tpsi5" / "05_HTTP_ASYNC_FETCH_REST.md"

A_ROOT = ROOT / "activities" / "tpsi5" / "http_microscope_a"
B_ROOT = ROOT / "activities" / "tpsi5" / "async_response_b"
C_ROOT = ROOT / "activities" / "tpsi5" / "feisbuc_rest_c"
D_ROOT = ROOT / "activities" / "tpsi5" / "fetch_debug_d"


def load(path: Path) -> dict:
    value = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(value, dict)
    return value


def read_json_response(url: str, *, method: str = "GET", payload=None, content_type: str | None = None):
    data = None if payload is None else (
        payload if isinstance(payload, bytes) else json.dumps(payload).encode("utf-8")
    )
    headers = {}
    if content_type:
        headers["Content-Type"] = content_type
    request = urllib.request.Request(url, data=data, headers=headers, method=method)
    response = urllib.request.urlopen(request, timeout=5)
    body = response.read()
    decoded = json.loads(body.decode("utf-8")) if body else None
    return response.status, response.headers, decoded


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


def assert_activity_assets(root: Path, difficulty: str, activity_id: str, automatic: bool) -> dict:
    activity_path = root / "activity.json"
    activity = load(activity_path)
    assert validate_activity(activity, str(activity_path)) == []
    assert activity["id"] == activity_id
    assert activity["difficolta"] == difficulty
    assert activity["linguaggio"] == "javascript"
    assert sum(item["punti"] for item in activity["rubrica"]) == 10

    for asset in activity["assets"]:
        assert (root / asset["path"]).is_file(), asset
        if asset["visibility"] == "student":
            assert asset["type"] not in {"teacher_only", "hidden_test"}
            assert asset.get("target_path")
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


def test_uda23_content_pack_and_course_design_links() -> None:
    pack = load(PACK_PATH)
    design = load(DESIGN_PATH)
    item = next(item for item in pack["content_items"] if item["id"] == "tpsi5-content-http-async-fetch-rest")

    assert pack["version"] == "0.6.0"
    assert item["path"] == "content/tpsi5/05_HTTP_ASYNC_FETCH_REST.md"
    assert item["order"] == 6
    assert item["activity_ids"] == [
        "tpsi5-activity-a-http-microscope-001",
        "tpsi5-activity-b-async-response-policy-001",
        "tpsi5-activity-c-feisbuc-rest-client-001",
        "tpsi5-activity-d-debug-fetch-http-001",
    ]
    refs = {ref["id"] for ref in item["source_refs"]}
    assert {
        "tpsi5-source-originali",
        "tpsi5-source-labs-legacy",
        "tpsi5-ref-lab5-legacy",
        "tpsi5-ref-lab6-legacy",
        "tpsi5-ref-lab7-legacy",
        "tpsi5-ref-rfc9110",
        "tpsi5-ref-fetch",
        "tpsi5-ref-node",
        "tpsi5-ref-mdn",
    } <= refs
    assert LESSON_PATH.is_file()

    year = design["years"][0]
    uda23 = next(uda for uda in year["udas"] if uda["id"] == "uda-23")
    uda24 = next(uda for uda in year["udas"] if uda["id"] == "uda-24")
    assert len(uda23["items"]) == 1
    assert uda23["items"][0]["source"] == "content/tpsi5/05_HTTP_ASYNC_FETCH_REST.md"
    assert uda23["items"][0]["activity_ids"] == item["activity_ids"]
    assert "Express" in uda23["items"][0]["frame"]["next_step"]
    assert uda24["items"] == []


def test_uda23_activity_contracts_and_grading_boundary() -> None:
    assert_activity_assets(A_ROOT, "A", "tpsi5-activity-a-http-microscope-001", False)
    b = assert_activity_assets(B_ROOT, "B", "tpsi5-activity-b-async-response-policy-001", True)
    c = assert_activity_assets(C_ROOT, "C", "tpsi5-activity-c-feisbuc-rest-client-001", False)
    assert_activity_assets(D_ROOT, "D", "tpsi5-activity-d-debug-fetch-http-001", False)

    assert c["project_milestone"] == "feisbuc-04-rest-api-client"
    assert grade_activity.SUPPORTED_LANGUAGES["javascript"] == "implemented"
    assert b["correzione"]["test"] is True
    assert c["correzione"]["test"] is False


@pytest.mark.skipif(shutil.which("node") is None, reason="Node.js richiesto")
def test_activity_b_reference_solution_passes_real_javascript_grader() -> None:
    activity = load(B_ROOT / "activity.json")
    report = grade_activity.grade_activity(activity, B_ROOT / "solution" / "main.js", timeout_seconds=5)
    assert report["passed"] is True, report
    assert report["summary"] == {"passed": 4, "total": 4}


@pytest.mark.skipif(shutil.which("node") is None, reason="Node.js richiesto")
def test_http_microscope_fixture_exposes_declared_semantics() -> None:
    with RunningServer(A_ROOT / "starter" / "server.mjs") as server:
        status, headers, posts = read_json_response(f"{server.base}/api/posts")
        assert status == 200
        assert headers.get_content_type() == "application/json"
        assert len(posts) == 2

        with pytest.raises(urllib.error.HTTPError) as missing:
            urllib.request.urlopen(f"{server.base}/api/posts/missing", timeout=5)
        assert missing.value.code == 404
        missing_payload = json.loads(missing.value.read().decode("utf-8"))
        assert missing_payload["error"] == "post-not-found"

        status, headers, created = read_json_response(
            f"{server.base}/api/posts",
            method="POST",
            payload={"text": "CI HTTP"},
            content_type="application/json",
        )
        assert status == 201
        assert headers["Location"] == f"/api/posts/{created['id']}"
        assert created["text"] == "CI HTTP"

        request = urllib.request.Request(
            f"{server.base}/api/posts",
            data=b"text=bad",
            headers={"Content-Type": "text/plain"},
            method="POST",
        )
        with pytest.raises(urllib.error.HTTPError) as media_type:
            urllib.request.urlopen(request, timeout=5)
        assert media_type.value.code == 415

        delete = urllib.request.Request(f"{server.base}/api/posts", method="DELETE")
        with pytest.raises(urllib.error.HTTPError) as method_error:
            urllib.request.urlopen(delete, timeout=5)
        assert method_error.value.code == 405
        assert "GET" in method_error.value.headers["Allow"]
        assert "POST" in method_error.value.headers["Allow"]


@pytest.mark.skipif(shutil.which("node") is None, reason="Node.js richiesto")
def test_feisbuc_rest_fixture_get_post_patch_and_filter() -> None:
    with RunningServer(C_ROOT / "starter" / "server.mjs") as server:
        status, _, before = read_json_response(f"{server.base}/api/posts")
        assert status == 200
        assert len(before) == 2

        status, headers, created = read_json_response(
            f"{server.base}/api/posts",
            method="POST",
            payload={"text": "Milestone CI"},
            content_type="application/json",
        )
        assert status == 201
        assert headers["Location"].endswith(created["id"])
        assert created["liked"] is False

        status, _, updated = read_json_response(
            f"{server.base}/api/posts/{created['id']}",
            method="PATCH",
            payload={"liked": True},
            content_type="application/json",
        )
        assert status == 200
        assert updated["liked"] is True
        assert updated["likes"] == 1

        status, _, liked = read_json_response(f"{server.base}/api/posts?liked=true")
        assert status == 200
        assert all(post["liked"] is True for post in liked)
        assert created["id"] in {post["id"] for post in liked}


@pytest.mark.skipif(shutil.which("node") is None, reason="Node.js richiesto")
def test_feisbuc_api_reference_runs_against_real_fixture() -> None:
    api_source = (C_ROOT / "solution" / "api.js").read_text(encoding="utf-8")

    with RunningServer(C_ROOT / "starter" / "server.mjs") as server, tempfile.TemporaryDirectory() as temp:
        temp_root = Path(temp)
        (temp_root / "api.mjs").write_text(api_source, encoding="utf-8")
        (temp_root / "runner.mjs").write_text(
            "import { createApi } from './api.mjs';\n"
            "const api = createApi(process.argv[2]);\n"
            "const before = await api.getPosts();\n"
            "const created = await api.createPost('API adapter CI');\n"
            "const updated = await api.setLiked(created.id, true);\n"
            "console.log(JSON.stringify({before: before.length, text: created.text, liked: updated.liked, likes: updated.likes}));\n",
            encoding="utf-8",
        )
        result = subprocess.run(
            ["node", "runner.mjs", server.base],
            cwd=temp_root,
            capture_output=True,
            text=True,
            timeout=10,
            check=False,
        )
        assert result.returncode == 0, result.stderr
        payload = json.loads(result.stdout)
        assert payload == {"before": 2, "text": "API adapter CI", "liked": True, "likes": 1}


def test_feisbuc_rest_reference_keeps_http_dom_boundary() -> None:
    api = (C_ROOT / "solution" / "api.js").read_text(encoding="utf-8")
    app = (C_ROOT / "solution" / "app.js").read_text(encoding="utf-8")

    assert "await fetch" in api
    assert "response.ok" in api
    assert "content-type" in api
    assert "JSON.stringify" in api
    assert 'method: "POST"' in api
    assert 'method: "PATCH"' in api
    assert "document." not in api
    assert "localStorage" not in api
    assert "sessionStorage" not in api

    assert 'addEventListener("submit"' in app
    assert 'postList.addEventListener("click"' in app
    assert "await api.getPosts()" in app
    assert "await api.createPost" in app
    assert "await api.setLiked" in app
    assert "textContent" in app
    assert "localStorage" not in app


def test_fetch_debug_starter_has_faults_and_solution_fixes_them() -> None:
    broken = (D_ROOT / "starter" / "client.js").read_text(encoding="utf-8")
    fixed = (D_ROOT / "solution" / "client.js").read_text(encoding="utf-8")
    diagnosis = (D_ROOT / "solution" / "DIAGNOSI.md").read_text(encoding="utf-8")

    assert "success: true" in broken
    assert '"Content-Type": "text/plain"' in broken
    assert "body: { text:" in broken
    assert 'fetch("/api/no-content")' in broken
    assert "await response.json()" in broken
    assert "Network error" in broken

    assert "response.ok" in fixed
    assert '"Content-Type": "application/json"' in fixed
    assert "JSON.stringify" in fixed
    assert "response.status === 204" in fixed
    assert 'error.kind = "http"' in fixed
    assert 'kind: "network-or-runtime"' in fixed

    for concept in ("404", "415", "204", "Content-Type", "JSON.stringify", "Network"):
        assert concept.lower() in diagnosis.lower()


@pytest.mark.skipif(shutil.which("node") is None, reason="Node.js richiesto")
def test_all_uda23_javascript_files_parse_with_node_22() -> None:
    files = [
        A_ROOT / "starter" / "server.mjs",
        B_ROOT / "starter" / "main.js",
        B_ROOT / "solution" / "main.js",
        C_ROOT / "starter" / "server.mjs",
        C_ROOT / "starter" / "api.js",
        C_ROOT / "starter" / "app.js",
        C_ROOT / "solution" / "api.js",
        C_ROOT / "solution" / "app.js",
        D_ROOT / "starter" / "server.mjs",
        D_ROOT / "starter" / "client.js",
        D_ROOT / "solution" / "client.js",
    ]
    for path in files:
        result = subprocess.run(["node", "--check", str(path)], capture_output=True, text=True, timeout=10)
        assert result.returncode == 0, f"{path}: {result.stderr}"
