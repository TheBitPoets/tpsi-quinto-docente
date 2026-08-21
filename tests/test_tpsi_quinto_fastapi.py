from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import subprocess
import sys

from fastapi.testclient import TestClient

from scripts import grade_activity
from scripts.validate_activity import validate_activity


ROOT = Path(__file__).resolve().parents[1]
PACK_PATH = ROOT / "content/tpsi5/content-pack.json"
DESIGN_PATH = ROOT / "doc/course_designs/tpsi_quinto_2026_2027.json"
DECISIONS_PATH = ROOT / "doc/OPEN_DECISIONS.md"
LESSON_PATH = ROOT / "content/tpsi5/15_FASTAPI_OPENAPI_MIRROR.md"
A_ROOT = ROOT / "activities/tpsi5/fastapi_openapi_microscope_a"
B_ROOT = ROOT / "activities/tpsi5/fastapi_post_validation_b"
C_ROOT = ROOT / "activities/tpsi5/feisbuc_fastapi_mirror_c"
D_ROOT = ROOT / "activities/tpsi5/fastapi_debug_d"

FASTAPI_VERSION = "0.141.1"
PYDANTIC_VERSION = "2.13.4"
UVICORN_VERSION = "0.52.1"
HTTPX_VERSION = "0.28.1"


def load(path: Path) -> dict:
    value = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(value, dict)
    return value


def assert_activity(root: Path, difficulty: str, activity_id: str, automatic: bool) -> dict:
    activity = load(root / "activity.json")
    assert validate_activity(activity, str(root / "activity.json")) == []
    assert activity["id"] == activity_id
    assert activity["difficolta"] == difficulty
    assert activity["contesto"]["uda"] == "uda-26"
    assert activity["linguaggio"] == "python"
    assert activity["correzione"]["test"] is automatic
    assert sum(item["punti"] for item in activity["rubrica"]) == 10
    for asset in activity["assets"]:
        assert (root / asset["path"]).is_file(), asset
        if asset["visibility"] == "student":
            assert asset.get("target_path")
    return activity


def assert_requirements(path: Path) -> None:
    text = path.read_text(encoding="utf-8")
    for pin in (
        f"fastapi=={FASTAPI_VERSION}",
        f"pydantic=={PYDANTIC_VERSION}",
        f"uvicorn=={UVICORN_VERSION}",
        f"httpx=={HTTPX_VERSION}",
    ):
        assert pin in text
    assert "sqlalchemy" not in text.lower()


def import_module(path: Path, module_name: str):
    spec = importlib.util.spec_from_file_location(module_name, path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_fastapi_content_pack_course_design_and_activity_contracts() -> None:
    pack = load(PACK_PATH)
    design = load(DESIGN_PATH)

    assert pack["version"] == "0.19.0"
    assert pack["extensions"]["bootstrap_decisions"]["python_mirror"] == "fastapi"

    refs = {item["id"]: item for item in pack["references"]}
    assert refs["tpsi5-ref-fastapi"]["role"] == "technical-reference"
    assert FASTAPI_VERSION in refs["tpsi5-ref-fastapi"]["notes"]
    assert PYDANTIC_VERSION in refs["tpsi5-ref-fastapi"]["notes"]
    assert UVICORN_VERSION in refs["tpsi5-ref-fastapi"]["notes"]
    assert HTTPX_VERSION in refs["tpsi5-ref-fastapi"]["notes"]
    assert "2.0.51" in refs["tpsi5-ref-sqlalchemy"]["notes"]

    item = next(x for x in pack["content_items"] if x["id"] == "tpsi5-content-fastapi-openapi-mirror")
    assert item["order"] == 16
    assert item["path"] == "content/tpsi5/15_FASTAPI_OPENAPI_MIRROR.md"
    assert item["activity_ids"] == [
        "tpsi5-activity-a-fastapi-openapi-microscope-001",
        "tpsi5-activity-b-fastapi-post-validation-001",
        "tpsi5-activity-c-feisbuc-fastapi-mirror-001",
        "tpsi5-activity-d-debug-fastapi-boundaries-001",
    ]
    assert LESSON_PATH.is_file()

    uda26 = next(u for u in design["years"][0]["udas"] if u["id"] == "uda-26")
    assert uda26["weeks"] == "4"
    assert len(uda26["items"]) == 4
    assert uda26["items"][0]["source"] == item["path"]
    assert uda26["items"][0]["activity_ids"] == item["activity_ids"]
    assert "SQLAlchemy" in uda26["items"][0]["frame"]["next_step"]
    assert uda26["items"][1]["source"] == "content/tpsi5/16_SQLALCHEMY_PERSISTENCE_MIRROR.md"
    assert uda26["items"][2]["source"] == "content/tpsi5/17_TESTING_INTEGRATION_BOUNDARIES.md"
    assert uda26["items"][3]["source"] == "content/tpsi5/18_RUNTIME_DEPLOY_HEALTH_CAPSTONE.md"

    a = assert_activity(A_ROOT, "A", "tpsi5-activity-a-fastapi-openapi-microscope-001", False)
    b = assert_activity(B_ROOT, "B", "tpsi5-activity-b-fastapi-post-validation-001", True)
    c = assert_activity(C_ROOT, "C", "tpsi5-activity-c-feisbuc-fastapi-mirror-001", False)
    d = assert_activity(D_ROOT, "D", "tpsi5-activity-d-debug-fastapi-boundaries-001", False)
    assert a["tipo"] == b["tipo"] == c["tipo"] == "laboratorio"
    assert d["tipo"] == "debug-didattico"
    assert c["project_milestone"] == "feisbuc-mirror-01-fastapi-openapi"


def test_d4_freezes_mirror_before_sqlalchemy() -> None:
    decisions = DECISIONS_PATH.read_text(encoding="utf-8")
    assert "## D4 — Mirror Python" in decisions
    assert "Stato: `DECIDED`" in decisions
    assert "FastAPI + Pydantic + OpenAPI + TestClient + MemoryPostStore" in decisions
    assert "SQLAlchemy" in decisions
    assert "secondo slice" in decisions


def test_python_runner_is_real_and_validation_activity_passes() -> None:
    assert grade_activity.SUPPORTED_LANGUAGES["python"] == "implemented"
    activity = load(B_ROOT / "activity.json")
    report = grade_activity.grade_activity(activity, B_ROOT / "solution/main.py", timeout_seconds=5)
    assert report["passed"] is True, report
    assert report["summary"] == {
        "passed": len(activity["test_cases"]),
        "total": len(activity["test_cases"]),
    }

    too_long = next(case for case in activity["test_cases"] if case["name"] == "too-long")
    payload = json.loads(too_long["stdin"])
    assert len(payload["text"]) > 280


def test_fastapi_microscope_exposes_openapi_201_location_and_422() -> None:
    assert_requirements(A_ROOT / "starter/requirements.txt")
    module = import_module(A_ROOT / "starter/app.py", "tpsi5_fastapi_microscope")
    client = TestClient(module.app)

    initial = client.get("/api/posts")
    assert initial.status_code == 200
    assert initial.json()[0]["id"] == "p1"

    created = client.post("/api/posts", json={"text": "  microscope  "})
    assert created.status_code == 201
    assert created.json()["text"] == "microscope"
    assert created.headers["location"] == f"/api/posts/{created.json()['id']}"

    invalid = client.post("/api/posts", json={"text": "   "})
    assert invalid.status_code == 422

    schema = client.get("/openapi.json").json()
    assert {"get", "post"} <= set(schema["paths"]["/api/posts"])
    assert "PostCreate" in schema["components"]["schemas"]
    assert "Post" in schema["components"]["schemas"]


def test_fastapi_mirror_reference_preserves_contract_and_boundaries() -> None:
    assert_requirements(C_ROOT / "solution/requirements.txt")

    result = subprocess.run(
        [sys.executable, "-m", "pytest", "-q", "tests"],
        cwd=C_ROOT / "solution",
        capture_output=True,
        text=True,
        timeout=30,
        check=False,
    )
    assert result.returncode == 0, result.stdout + result.stderr

    models = (C_ROOT / "solution/app/models.py").read_text(encoding="utf-8")
    store = (C_ROOT / "solution/app/store.py").read_text(encoding="utf-8")
    app = (C_ROOT / "solution/app/main.py").read_text(encoding="utf-8")
    requirements = (C_ROOT / "solution/requirements.txt").read_text(encoding="utf-8").lower()

    post_create = models.split("class PostCreate", 1)[1].split("class PostLikePatch", 1)[0]
    assert "authorId" not in post_create and "userId" not in post_create
    assert "fastapi" not in store.lower()
    assert "sqlalchemy" not in store.lower()
    assert "response_model=Post" in app
    assert "status.HTTP_201_CREATED" in app
    assert 'response.headers["Location"]' in app
    assert "HTTPException(status_code=404" in app
    for forbidden in ("sqlalchemy", "socket.io", "jwt", "session"):
        assert forbidden not in requirements


def test_fastapi_debug_fixture_covers_status_trust_error_and_output_boundaries() -> None:
    broken = (D_ROOT / "starter/broken_app.py").read_text(encoding="utf-8")
    fixed = (D_ROOT / "solution/fixed_app.py").read_text(encoding="utf-8")
    diagnosis = (D_ROOT / "solution/DIAGNOSI.md").read_text(encoding="utf-8").lower()

    assert "payload: dict" in broken
    assert 'payload["authorId"]' in broken
    assert "internalSecret" in broken
    assert "return posts[post_id]" in broken
    assert "status_code" not in broken

    assert "class PostCreate" in fixed
    assert "response_model=Post" in fixed
    assert "status.HTTP_201_CREATED" in fixed
    assert '"authorId": "server-user"' in fixed
    assert "HTTPException(status_code=404" in fixed

    for concept in ("201", "schema", "spoof", "404", "intern", "authorization"):
        assert concept in diagnosis
