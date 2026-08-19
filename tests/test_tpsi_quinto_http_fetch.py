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


def request(url: str, *, method: str = "GET", payload=None, content_type: str | None = None):
    data = None if payload is None else json.dumps(payload).encode("utf-8")
    headers = {"Content-Type": content_type} if content_type else {}
    req = urllib.request.Request(url, data=data, headers=headers, method=method)
    response = urllib.request.urlopen(req, timeout=5)
    body = response.read()
    media_type = response.headers.get_content_type()
    decoded = json.loads(body.decode("utf-8")) if body and media_type == "application/json" else body.decode("utf-8")
    return response.status, response.headers, decoded


def assert_activity(root: Path, difficulty: str, activity_id: str, automatic: bool) -> dict:
    path = root / "activity.json"
    activity = load(path)
    assert validate_activity(activity, str(path)) == []
    assert activity["id"] == activity_id
    assert activity["difficolta"] == difficulty
    assert sum(entry["punti"] for entry in activity["rubrica"]) == 10
    for asset in activity["assets"]:
        assert (root / asset["path"]).is_file(), asset
        if asset["visibility"] == "student":
            assert asset.get("target_path")
        else:
            assert asset["visibility"] == "teacher"
    if automatic:
        assert activity["correzione"]["test"] is True
        assert activity["correzione"]["sandbox"] is True
    else:
        assert activity["correzione"]["test"] is False
        assert activity["correzione"]["sandbox"] is False
    return activity


def test_uda23_content_item_remains_stable_after_later_backend_increments() -> None:
    pack = load(PACK_PATH)
    design = load(DESIGN_PATH)
    item = next(item for item in pack["content_items"] if item["id"] == "tpsi5-content-http-async-fetch-rest")

    assert pack["version"] == "0.8.0"
    assert item["path"] == "content/tpsi5/05_HTTP_ASYNC_FETCH_REST.md"
    assert item["order"] == 6
    assert item["activity_ids"] == [
        "tpsi5-activity-a-http-microscope-001",
        "tpsi5-activity-b-async-response-policy-001",
        "tpsi5-activity-c-feisbuc-rest-client-001",
        "tpsi5-activity-d-debug-fetch-http-001",
    ]
    assert LESSON_PATH.is_file()

    uda23 = next(uda for uda in design["years"][0]["udas"] if uda["id"] == "uda-23")
    uda24 = next(uda for uda in design["years"][0]["udas"] if uda["id"] == "uda-24")
    assert len(uda23["items"]) == 1
    assert uda23["items"][0]["source"] == "content/tpsi5/05_HTTP_ASYNC_FETCH_REST.md"
    assert uda23["items"][0]["activity_ids"] == item["activity_ids"]
    assert [entry["source"] for entry in uda24["items"]] == [
        "content/tpsi5/06_NODE_EXPRESS_BACKEND.md",
        "content/tpsi5/07_SQL_RAW_PERSISTENCE.md",
    ]

    assert_activity(A_ROOT, "A", "tpsi5-activity-a-http-microscope-001", False)
    b = assert_activity(B_ROOT, "B", "tpsi5-activity-b-async-response-policy-001", True)
    c = assert_activity(C_ROOT, "C", "tpsi5-activity-c-feisbuc-rest-client-001", False)
    assert_activity(D_ROOT, "D", "tpsi5-activity-d-debug-fetch-http-001", False)
    assert b["linguaggio"] == "javascript"
    assert c["project_milestone"] == "feisbuc-04-rest-api-client"


def test_async_response_policy_reference_passes_real_javascript_runner() -> None:
    assert shutil.which("node") is not None
    activity = load(B_ROOT / "activity.json")
    report = grade_activity.grade_activity(activity, B_ROOT / "solution" / "main.js", timeout_seconds=5)
    assert report["passed"] is True, report
    assert report["summary"] == {"passed": len(activity["test_cases"]), "total": len(activity["test_cases"])}


def test_http_microscope_fixture_exposes_status_header_and_method_semantics() -> None:
    with RunningServer(A_ROOT / "starter" / "server.mjs") as server:
        status, headers, posts = request(f"{server.base}/api/posts")
        assert status == 200
        assert headers.get_content_type() == "application/json"
        assert len(posts) == 2

        status, headers, created = request(
            f"{server.base}/api/posts",
            method="POST",
            payload={"text": "CI HTTP"},
            content_type="application/json",
        )
        assert status == 201
        assert headers["Location"] == f"/api/posts/{created['id']}"

        bad = urllib.request.Request(
            f"{server.base}/api/posts",
            data=b"text=bad",
            headers={"Content-Type": "text/plain"},
            method="POST",
        )
        with pytest.raises(urllib.error.HTTPError) as media:
            urllib.request.urlopen(bad, timeout=5)
        assert media.value.code == 415

        delete = urllib.request.Request(f"{server.base}/api/posts", method="DELETE")
        with pytest.raises(urllib.error.HTTPError) as method_error:
            urllib.request.urlopen(delete, timeout=5)
        assert method_error.value.code == 405
        assert "GET" in method_error.value.headers["Allow"]
        assert "POST" in method_error.value.headers["Allow"]


def test_feisbuc_rest_fixture_and_reference_api_adapter_keep_contract() -> None:
    with RunningServer(C_ROOT / "starter" / "server.mjs") as server:
        status, _, before = request(f"{server.base}/api/posts")
        assert status == 200
        assert len(before) == 2

        status, headers, created = request(
            f"{server.base}/api/posts",
            method="POST",
            payload={"text": "Milestone CI"},
            content_type="application/json",
        )
        assert status == 201
        assert headers["Location"].endswith(created["id"])

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

        api_source = (C_ROOT / "solution" / "api.js").read_text(encoding="utf-8")
        with tempfile.TemporaryDirectory() as temp:
            temp_root = Path(temp)
            (temp_root / "api.mjs").write_text(api_source, encoding="utf-8")
            (temp_root / "runner.mjs").write_text(
                "import { createApi } from './api.mjs';\n"
                "const api=createApi(process.argv[2]);\n"
                "const created=await api.createPost('adapter');\n"
                "const updated=await api.setLiked(created.id,true);\n"
                "console.log(JSON.stringify({text:created.text,liked:updated.liked,likes:updated.likes}));\n",
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
            assert json.loads(result.stdout) == {"text": "adapter", "liked": True, "likes": 1}


def test_feisbuc_rest_reference_keeps_http_and_dom_separated() -> None:
    api = (C_ROOT / "solution" / "api.js").read_text(encoding="utf-8")
    app = (C_ROOT / "solution" / "app.js").read_text(encoding="utf-8")
    assert "await fetch" in api
    assert "response.ok" in api
    assert "JSON.stringify" in api
    assert "document." not in api
    assert "localStorage" not in api
    assert "await api.getPosts()" in app
    assert "await api.createPost" in app
    assert "await api.setLiked" in app
    assert "localStorage" not in app


def test_fetch_debug_starter_has_faults_and_solution_fixes_error_taxonomy() -> None:
    broken = (D_ROOT / "starter" / "client.js").read_text(encoding="utf-8")
    fixed = (D_ROOT / "solution" / "client.js").read_text(encoding="utf-8")
    diagnosis = (D_ROOT / "solution" / "DIAGNOSI.md").read_text(encoding="utf-8").lower()

    assert "success: true" in broken
    assert '"Content-Type": "text/plain"' in broken
    assert "body: { text:" in broken
    assert "await response.json()" in broken
    assert "Network error" in broken

    assert "response.ok" in fixed
    assert '"Content-Type": "application/json"' in fixed
    assert "JSON.stringify" in fixed
    assert "response.status === 204" in fixed
    assert 'error.kind = "http"' in fixed

    for concept in ("404", "415", "204", "content-type", "json.stringify", "network"):
        assert concept in diagnosis


def test_uda23_javascript_files_still_parse_with_node() -> None:
    for path in (
        A_ROOT / "starter" / "server.mjs",
        B_ROOT / "solution" / "main.js",
        C_ROOT / "starter" / "server.mjs",
        C_ROOT / "solution" / "api.js",
        C_ROOT / "solution" / "app.js",
        D_ROOT / "starter" / "server.mjs",
        D_ROOT / "solution" / "client.js",
    ):
        result = subprocess.run(["node", "--check", str(path)], capture_output=True, text=True, timeout=10)
        assert result.returncode == 0, f"{path}: {result.stderr}"
