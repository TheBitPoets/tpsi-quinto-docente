from __future__ import annotations

import json
from pathlib import Path
import subprocess
import sys

from scripts.validate_activity import validate_activity


ROOT = Path(__file__).resolve().parents[1]
PACK_PATH = ROOT / "content/tpsi5/content-pack.json"
DESIGN_PATH = ROOT / "doc/course_designs/tpsi_quinto_2026_2027.json"
LESSON_PATH = ROOT / "content/tpsi5/16_SQLALCHEMY_PERSISTENCE_MIRROR.md"
A_ROOT = ROOT / "activities/tpsi5/sqlalchemy_mapping_microscope_a"
B_ROOT = ROOT / "activities/tpsi5/sqlalchemy_repository_b"
C_ROOT = ROOT / "activities/tpsi5/feisbuc_fastapi_sqlalchemy_c"
D_ROOT = ROOT / "activities/tpsi5/sqlalchemy_debug_d"

SQLALCHEMY_VERSION = "2.0.51"
FASTAPI_VERSION = "0.141.1"
PYDANTIC_VERSION = "2.13.4"
UVICORN_VERSION = "0.52.1"
HTTPX_VERSION = "0.28.1"


def load(path: Path) -> dict:
    value = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(value, dict)
    return value


def assert_activity(root: Path, difficulty: str, activity_id: str) -> dict:
    activity = load(root / "activity.json")
    assert validate_activity(activity, str(root / "activity.json")) == []
    assert activity["id"] == activity_id
    assert activity["difficolta"] == difficulty
    assert activity["contesto"]["uda"] == "uda-26"
    assert activity["linguaggio"] == "python"
    assert activity["correzione"] == {
        "compila": False,
        "test": False,
        "sandbox": False,
        "ai_feedback": False,
    }
    assert sum(item["punti"] for item in activity["rubrica"]) == 10
    for asset in activity["assets"]:
        assert (root / asset["path"]).is_file(), asset
        if asset["visibility"] == "student":
            assert asset.get("target_path")
    return activity


def test_sqlalchemy_content_pack_course_design_and_activity_contracts() -> None:
    pack = load(PACK_PATH)
    design = load(DESIGN_PATH)

    assert pack["version"] == "0.17.0"
    refs = {item["id"]: item for item in pack["references"]}
    sqlalchemy_ref = refs["tpsi5-ref-sqlalchemy"]
    assert sqlalchemy_ref["role"] == "technical-reference"
    assert SQLALCHEMY_VERSION in sqlalchemy_ref["notes"]
    assert "second mirror slice" in sqlalchemy_ref["notes"].lower()

    item = next(
        x for x in pack["content_items"]
        if x["id"] == "tpsi5-content-sqlalchemy-persistence-mirror"
    )
    assert item["order"] == 17
    assert item["path"] == "content/tpsi5/16_SQLALCHEMY_PERSISTENCE_MIRROR.md"
    assert item["activity_ids"] == [
        "tpsi5-activity-a-sqlalchemy-mapping-microscope-001",
        "tpsi5-activity-b-sqlalchemy-repository-001",
        "tpsi5-activity-c-feisbuc-fastapi-sqlalchemy-001",
        "tpsi5-activity-d-debug-sqlalchemy-transactions-001",
    ]
    assert LESSON_PATH.is_file()

    uda26 = next(u for u in design["years"][0]["udas"] if u["id"] == "uda-26")
    assert uda26["weeks"] == "4"
    assert len(uda26["items"]) == 2
    assert uda26["items"][0]["source"] == "content/tpsi5/15_FASTAPI_OPENAPI_MIRROR.md"
    assert "SQLAlchemy" in uda26["items"][0]["frame"]["next_step"]
    assert uda26["items"][1]["source"] == item["path"]
    assert uda26["items"][1]["activity_ids"] == item["activity_ids"]
    assert "testing" in uda26["items"][1]["frame"]["next_step"].lower()

    a = assert_activity(A_ROOT, "A", "tpsi5-activity-a-sqlalchemy-mapping-microscope-001")
    b = assert_activity(B_ROOT, "B", "tpsi5-activity-b-sqlalchemy-repository-001")
    c = assert_activity(C_ROOT, "C", "tpsi5-activity-c-feisbuc-fastapi-sqlalchemy-001")
    d = assert_activity(D_ROOT, "D", "tpsi5-activity-d-debug-sqlalchemy-transactions-001")
    assert a["tipo"] == b["tipo"] == c["tipo"] == "laboratorio"
    assert d["tipo"] == "debug-didattico"
    assert c["project_milestone"] == "feisbuc-mirror-02-sqlalchemy-persistence"


def test_sqlalchemy_toolchain_is_pinned_without_scope_creep() -> None:
    requirement_paths = (
        A_ROOT / "starter/requirements.txt",
        B_ROOT / "starter/requirements.txt",
        B_ROOT / "solution/requirements.txt",
        C_ROOT / "starter/requirements.txt",
        C_ROOT / "solution/requirements.txt",
        D_ROOT / "starter/requirements.txt",
        D_ROOT / "solution/requirements.txt",
    )
    for path in requirement_paths:
        text = path.read_text(encoding="utf-8")
        assert f"SQLAlchemy=={SQLALCHEMY_VERSION}" in text
        assert "alembic" not in text.lower()

    c_requirements = (C_ROOT / "solution/requirements.txt").read_text(encoding="utf-8")
    for pin in (
        f"fastapi=={FASTAPI_VERSION}",
        f"pydantic=={PYDANTIC_VERSION}",
        f"uvicorn=={UVICORN_VERSION}",
        f"httpx=={HTTPX_VERSION}",
    ):
        assert pin in c_requirements


def test_mapping_microscope_uses_modern_sqlalchemy_20_api() -> None:
    source = (A_ROOT / "starter/app.py").read_text(encoding="utf-8")
    for fragment in (
        "DeclarativeBase",
        "Mapped",
        "mapped_column",
        "create_engine",
        "Session(engine)",
        "select(PostRow)",
        "echo=True",
        "StaticPool",
    ):
        assert fragment in source
    assert ".query(" not in source


def test_repository_reference_runs_without_fastapi() -> None:
    source = (B_ROOT / "solution/repository.py").read_text(encoding="utf-8")
    lower = source.lower()
    assert "fastapi" not in lower
    assert "select(PostRow)" in source
    assert "session.scalars" in source
    assert "session.get(PostRow" in source
    assert source.count("session.commit()") >= 2
    assert "session.query" not in source
    assert ".__dict__" not in source

    result = subprocess.run(
        [sys.executable, "-m", "pytest", "-q", "tests"],
        cwd=B_ROOT / "solution",
        capture_output=True,
        text=True,
        timeout=30,
        check=False,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    assert "1 passed" in result.stdout


def test_feisbuc_sqlalchemy_reference_preserves_boundary_and_restart_contract() -> None:
    entities = (C_ROOT / "solution/app/entities.py").read_text(encoding="utf-8")
    database = (C_ROOT / "solution/app/database.py").read_text(encoding="utf-8")
    store = (C_ROOT / "solution/app/store.py").read_text(encoding="utf-8")
    main = (C_ROOT / "solution/app/main.py").read_text(encoding="utf-8")
    contract_test = (C_ROOT / "solution/tests/test_contract.py").read_text(encoding="utf-8")

    assert "DeclarativeBase" in entities
    assert "Mapped" in entities and "mapped_column" in entities
    assert "CheckConstraint" in entities
    assert "create_engine(database_url" in database
    assert "Base.metadata.create_all(engine)" in database
    assert "sessionmaker(bind=engine, expire_on_commit=False)" in database

    assert "fastapi" not in store.lower()
    assert "select(PostRow)" in store
    assert "session.get(PostRow" in store
    assert "ensure_seed" in store
    assert "to_public_post" in store
    assert "session.query" not in store
    assert ".__dict__" not in store
    assert store.count("session.commit()") >= 3

    assert "def create_app(database_url: str)" in main
    assert "build_database(database_url)" in main
    assert "app.state.engine = engine" in main
    assert "status.HTTP_201_CREATED" in main
    assert 'response.headers["Location"]' in main
    assert "SQLAlchemy" not in main.replace("FastAPI SQLAlchemy mirror", "")

    assert "app1.state.engine.dispose()" in contract_test
    assert "app2 = create_app(database_url)" in contract_test
    assert "assert db_path.is_file()" in contract_test
    assert "created[\"id\"] in by_id" in contract_test
    assert "sum(post[\"id\"] == \"seed-1\" for post in posts) == 1" in contract_test

    result = subprocess.run(
        [sys.executable, "-m", "pytest", "-q", "tests"],
        cwd=C_ROOT / "solution",
        capture_output=True,
        text=True,
        timeout=45,
        check=False,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    assert "1 passed" in result.stdout


def test_sqlalchemy_debug_fixture_covers_distinct_failure_classes() -> None:
    broken = (D_ROOT / "starter/broken_repository.py").read_text(encoding="utf-8")
    fixed = (D_ROOT / "solution/fixed_repository.py").read_text(encoding="utf-8")
    diagnosis = (D_ROOT / "solution/DIAGNOSI.md").read_text(encoding="utf-8").lower()

    assert "create_engine(database_url)" in broken
    assert "session = Session(engine)" in broken
    assert "session.query(PostRow)" in broken
    assert "session.flush()" in broken
    assert "row.__dict__" in broken
    assert "except IntegrityError" in broken

    assert "sessionmaker" in fixed
    assert "session.scalars(select(PostRow))" in fixed
    assert "session.commit()" in fixed
    assert "session.rollback()" in fixed
    assert "row.__dict__" not in fixed
    assert "session.query" not in fixed

    for concept in (
        "engine",
        "session globale",
        "identity map",
        "flush",
        "commit",
        "rollback",
        "query legacy",
        "__dict__",
        "representation",
    ):
        assert concept in diagnosis
