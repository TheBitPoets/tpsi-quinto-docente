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
LESSON_PATH = ROOT / "content" / "tpsi5" / "07_SQL_RAW_PERSISTENCE.md"
A_ROOT = ROOT / "activities" / "tpsi5" / "sql_posts_schema_a"
B_ROOT = ROOT / "activities" / "tpsi5" / "sql_posts_dml_b"
C_ROOT = ROOT / "activities" / "tpsi5" / "feisbuc_sql_c"
D_ROOT = ROOT / "activities" / "tpsi5" / "sql_debug_d"


def load(path: Path) -> dict:
    value = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(value, dict)
    return value


class RunningServer:
    def __init__(self, server: Path, *, extra_env: dict[str, str] | None = None):
        env = dict(os.environ)
        env["PORT"] = "0"
        if extra_env:
            env.update(extra_env)
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

    targets: set[str] = set()
    for asset in activity["assets"]:
        assert (root / asset["path"]).is_file(), asset
        if asset["visibility"] == "student":
            target = asset.get("target_path")
            assert isinstance(target, str) and target
            assert target not in targets
            targets.add(target)
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


def test_sql_content_pack_item_course_design_and_activity_contracts() -> None:
    pack = load(PACK_PATH)
    design = load(DESIGN_PATH)
    item = next(item for item in pack["content_items"] if item["id"] == "tpsi5-content-sql-raw-persistence")

    assert pack["version"] == "0.8.0"
    assert item["path"] == "content/tpsi5/07_SQL_RAW_PERSISTENCE.md"
    assert item["order"] == 8
    assert item["activity_ids"] == [
        "tpsi5-activity-a-sql-posts-schema-001",
        "tpsi5-activity-b-sql-posts-dml-001",
        "tpsi5-activity-c-feisbuc-sql-repository-001",
        "tpsi5-activity-d-debug-sql-state-001",
    ]
    assert {
        "tpsi5-source-originali",
        "tpsi5-source-labs-legacy",
        "tpsi5-ref-lab8-legacy",
        "tpsi5-ref-node",
        "tpsi5-ref-sqlite",
    } <= {ref["id"] for ref in item["source_refs"]}
    assert LESSON_PATH.is_file()

    uda24 = next(uda for uda in design["years"][0]["udas"] if uda["id"] == "uda-24")
    assert len(uda24["items"]) == 2
    sql_item = uda24["items"][1]
    assert sql_item["source"] == "content/tpsi5/07_SQL_RAW_PERSISTENCE.md"
    assert sql_item["activity_ids"] == item["activity_ids"]
    assert "auth" in sql_item["frame"]["next_step"].lower()

    a = assert_activity(A_ROOT, "A", "tpsi5-activity-a-sql-posts-schema-001", True)
    b = assert_activity(B_ROOT, "B", "tpsi5-activity-b-sql-posts-dml-001", True)
    c = assert_activity(C_ROOT, "C", "tpsi5-activity-c-feisbuc-sql-repository-001", False)
    d = assert_activity(D_ROOT, "D", "tpsi5-activity-d-debug-sql-state-001", True)
    assert a["linguaggio"] == b["linguaggio"] == d["linguaggio"] == "sql"
    assert c["linguaggio"] == "nodejs"
    assert c["project_milestone"] == "feisbuc-06-sql-persistence"


def test_sql_reference_solutions_pass_real_thebitlab_sql_runner() -> None:
    assert grade_activity.SUPPORTED_LANGUAGES["sql"] == "implemented"
    for root in (A_ROOT, B_ROOT, D_ROOT):
        activity = load(root / "activity.json")
        report = grade_activity.grade_activity(
            activity,
            root / "solution" / "main.sql",
            timeout_seconds=5,
        )
        assert report["passed"] is True, report
        assert report["language"] == "sql"
        assert report["summary"] == {
            "passed": len(activity["test_cases"]),
            "total": len(activity["test_cases"]),
        }


def test_schema_and_debug_solutions_preserve_persistent_invariants() -> None:
    schema = (A_ROOT / "solution" / "main.sql").read_text(encoding="utf-8").lower()
    debug = (D_ROOT / "solution" / "main.sql").read_text(encoding="utf-8").lower()
    diagnosis = (D_ROOT / "solution" / "DIAGNOSI.md").read_text(encoding="utf-8").lower()

    assert ") strict;" in schema
    assert "check (length(trim(text)) between 1 and 280)" in schema
    assert "check (likes >= 0)" in schema
    assert "check (liked in (0, 1))" in schema
    assert "idx_posts_liked_created" in schema

    assert "where id = 'p2'" in debug
    assert "where id = 'remove-me'" in debug
    for concept in ("constraint", "update", "where", "delete"):
        assert concept in diagnosis


def test_node_22_runtime_exposes_builtin_sqlite_module() -> None:
    assert shutil.which("node") is not None
    result = subprocess.run(
        [
            "node",
            "--input-type=module",
            "-e",
            "import { DatabaseSync } from 'node:sqlite'; const db=new DatabaseSync(':memory:'); db.exec('SELECT 1'); db.close(); console.log('ok');",
        ],
        capture_output=True,
        text=True,
        timeout=10,
        check=False,
    )
    assert result.returncode == 0, result.stderr
    assert result.stdout.strip() == "ok"


def test_feisbuc_sql_package_and_store_keep_database_behind_repository_boundary() -> None:
    package = load(C_ROOT / "solution" / "package.json")
    assert package["dependencies"] == {"express": "5.2.1"}
    assert package["engines"]["node"] == ">=22.13"

    store = (C_ROOT / "solution" / "src" / "sql-post-store.js").read_text(encoding="utf-8")
    router = (C_ROOT / "solution" / "src" / "posts.router.js").read_text(encoding="utf-8")
    config = (C_ROOT / "solution" / "src" / "config.js").read_text(encoding="utf-8")
    schema = (C_ROOT / "solution" / "src" / "schema.sql").read_text(encoding="utf-8")

    assert 'from "node:sqlite"' in store
    assert "DatabaseSync" in store
    assert ".prepare(" in store
    assert "VALUES(?, ?, ?, 0, 0)" in store
    assert "WHERE id = ?" in store
    assert "INSERT OR IGNORE" in store
    assert "Boolean(row.liked)" in store
    assert "express" not in store.lower()
    assert "req." not in store and "res." not in store
    assert "DatabaseSync" not in router
    assert "node:sqlite" not in router
    assert "DB_PATH" in config
    assert "C:\\" not in config
    assert "CHECK (liked IN (0, 1))" in schema
    assert "CHECK (likes >= 0)" in schema


def test_feisbuc_sql_client_router_and_validation_remain_storage_agnostic() -> None:
    sql_app = (C_ROOT / "solution" / "src" / "app.js").read_text(encoding="utf-8")
    sql_router = (C_ROOT / "solution" / "src" / "posts.router.js").read_text(encoding="utf-8")
    sql_validation = (C_ROOT / "solution" / "src" / "validation.js").read_text(encoding="utf-8")
    api = (C_ROOT / "solution" / "public" / "api.js").read_text(encoding="utf-8")

    assert "SqlPostStore" not in sql_app
    assert "SqlPostStore" not in sql_router
    assert "sqlite" not in sql_router.lower()
    assert "sqlite" not in sql_validation.lower()
    assert "sqlite" not in api.lower()
    assert 'requestJson("/api/posts")' in api
    assert 'method: "POST"' in api
    assert 'method: "PATCH"' in api


def test_feisbuc_sql_reference_persists_across_process_restart() -> None:
    assert (C_ROOT / "solution" / "node_modules" / "express").is_dir(), "npm install CI mancante"

    with tempfile.TemporaryDirectory() as temp:
        db_path = Path(temp) / "feisbuc-test.db"
        env = {"DB_PATH": str(db_path)}
        created_id = None

        with RunningServer(C_ROOT / "solution" / "src" / "server.js", extra_env=env) as server:
            status, _, before = request(f"{server.base}/api/posts")
            assert status == 200
            assert len(before) == 1
            assert before[0]["id"] == "seed-1"

            status, headers, created = request(
                f"{server.base}/api/posts",
                method="POST",
                payload={"text": "  Persistenza CI  "},
                content_type="application/json",
            )
            assert status == 201
            created_id = created["id"]
            assert headers["Location"] == f"/api/posts/{created_id}"
            assert created["text"] == "Persistenza CI"

            status, _, updated = request(
                f"{server.base}/api/posts/{created_id}",
                method="PATCH",
                payload={"liked": True},
                content_type="application/json",
            )
            assert status == 200
            assert updated["liked"] is True
            assert updated["likes"] == 1

        assert db_path.is_file()
        assert created_id is not None

        with RunningServer(C_ROOT / "solution" / "src" / "server.js", extra_env=env) as restarted:
            status, _, posts = request(f"{restarted.base}/api/posts")
            assert status == 200
            by_id = {post["id"]: post for post in posts}
            assert set(by_id) == {"seed-1", created_id}
            assert by_id[created_id]["text"] == "Persistenza CI"
            assert by_id[created_id]["liked"] is True
            assert by_id[created_id]["likes"] == 1
            assert sum(post["id"] == "seed-1" for post in posts) == 1

            status, _, liked = request(f"{restarted.base}/api/posts?liked=true")
            assert status == 200
            assert created_id in {post["id"] for post in liked}

            with pytest.raises(urllib.error.HTTPError) as missing:
                request(
                    f"{restarted.base}/api/posts/missing",
                    method="PATCH",
                    payload={"liked": True},
                    content_type="application/json",
                )
            code, _, payload = error_response(missing.value)
            assert code == 404
            assert payload["error"]["code"] == "post-not-found"


def test_memory_database_mode_is_isolated_between_processes() -> None:
    assert (C_ROOT / "solution" / "node_modules" / "express").is_dir(), "npm install CI mancante"
    env = {"DB_PATH": ":memory:"}

    with RunningServer(C_ROOT / "solution" / "src" / "server.js", extra_env=env) as server:
        _, _, created = request(
            f"{server.base}/api/posts",
            method="POST",
            payload={"text": "volatile"},
            content_type="application/json",
        )
        volatile_id = created["id"]

    with RunningServer(C_ROOT / "solution" / "src" / "server.js", extra_env=env) as restarted:
        _, _, posts = request(f"{restarted.base}/api/posts")
        assert {post["id"] for post in posts} == {"seed-1"}
        assert volatile_id not in {post["id"] for post in posts}


def test_sql_solution_files_parse_and_do_not_add_orm_dependencies() -> None:
    for path in (C_ROOT / "solution" / "src").glob("*.js"):
        result = subprocess.run(["node", "--check", str(path)], capture_output=True, text=True, timeout=10)
        assert result.returncode == 0, f"{path}: {result.stderr}"

    text = "\n".join(path.read_text(encoding="utf-8").lower() for path in (C_ROOT / "solution" / "src").glob("*.js"))
    for forbidden in ("sequelize", "prisma", "drizzle", "typeorm", "sqlalchemy"):
        assert forbidden not in text
