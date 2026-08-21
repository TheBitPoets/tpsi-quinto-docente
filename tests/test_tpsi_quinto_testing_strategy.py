from __future__ import annotations

import json
from pathlib import Path
import subprocess
import sys

from scripts.validate_activity import validate_activity

ROOT = Path(__file__).resolve().parents[1]
PACK_PATH = ROOT / "content/tpsi5/content-pack.json"
DESIGN_PATH = ROOT / "doc/course_designs/tpsi_quinto_2026_2027.json"
LESSON_PATH = ROOT / "content/tpsi5/17_TESTING_INTEGRATION_BOUNDARIES.md"
A_ROOT = ROOT / "activities/tpsi5/testing_boundary_microscope_a"
B_ROOT = ROOT / "activities/tpsi5/pytest_fixture_boundary_b"
C_ROOT = ROOT / "activities/tpsi5/feisbuc_testing_boundaries_c"
D_ROOT = ROOT / "activities/tpsi5/testing_debug_d"

PYTEST_VERSION = "9.1.1"


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
    assert sum(entry["punti"] for entry in activity["rubrica"]) == 10
    for asset in activity["assets"]:
        assert (root / asset["path"]).is_file(), asset
        if asset["visibility"] == "student":
            assert asset.get("target_path")
    return activity


def test_testing_slice_is_registered_without_changing_week_budget() -> None:
    pack = load(PACK_PATH)
    design = load(DESIGN_PATH)
    assert pack["version"] == "0.18.0"
    refs = {item["id"]: item for item in pack["references"]}
    assert refs["tpsi5-ref-pytest"]["role"] == "technical-reference"
    assert PYTEST_VERSION in refs["tpsi5-ref-pytest"]["notes"]

    item = next(x for x in pack["content_items"] if x["id"] == "tpsi5-content-testing-integration-boundaries")
    assert item["order"] == 18
    assert item["path"] == "content/tpsi5/17_TESTING_INTEGRATION_BOUNDARIES.md"
    assert item["activity_ids"] == [
        "tpsi5-activity-a-testing-boundary-microscope-001",
        "tpsi5-activity-b-pytest-fixture-boundary-001",
        "tpsi5-activity-c-feisbuc-testing-boundaries-001",
        "tpsi5-activity-d-debug-testing-boundaries-001",
    ]
    assert LESSON_PATH.is_file()

    uda26 = next(u for u in design["years"][0]["udas"] if u["id"] == "uda-26")
    assert uda26["weeks"] == "4"
    assert [entry["source"] for entry in uda26["items"]] == [
        "content/tpsi5/15_FASTAPI_OPENAPI_MIRROR.md",
        "content/tpsi5/16_SQLALCHEMY_PERSISTENCE_MIRROR.md",
        "content/tpsi5/17_TESTING_INTEGRATION_BOUNDARIES.md",
    ]
    assert uda26["items"][2]["activity_ids"] == item["activity_ids"]
    assert "deploy" in uda26["items"][2]["frame"]["next_step"].lower()

    assert_activity(A_ROOT, "A", "tpsi5-activity-a-testing-boundary-microscope-001")
    assert_activity(B_ROOT, "B", "tpsi5-activity-b-pytest-fixture-boundary-001")
    c = assert_activity(C_ROOT, "C", "tpsi5-activity-c-feisbuc-testing-boundaries-001")
    assert_activity(D_ROOT, "D", "tpsi5-activity-d-debug-testing-boundaries-001")
    assert c["project_milestone"] == "feisbuc-mirror-03-testing-boundaries"


def test_pytest_is_pinned_and_scope_stays_small() -> None:
    for path in (
        B_ROOT / "starter/requirements.txt",
        B_ROOT / "solution/requirements.txt",
        C_ROOT / "starter/requirements.txt",
        C_ROOT / "solution/requirements.txt",
    ):
        text = path.read_text(encoding="utf-8")
        assert f"pytest=={PYTEST_VERSION}" in text
        for forbidden in ("pytest-cov", "xdist", "testcontainers", "factory-boy"):
            assert forbidden not in text.lower()


def test_fixture_reference_is_function_scoped_isolated_and_real() -> None:
    source = (B_ROOT / "solution/tests/test_repository.py").read_text(encoding="utf-8")
    assert "@pytest.fixture" in source
    assert "tmp_path" in source
    assert "yield SqlAlchemyPostStore" in source
    assert "engine.dispose()" in source
    assert "shared-test.db" not in source
    assert "MagicMock" not in source
    assert "pytest.mark.parametrize" in source

    result = subprocess.run(
        [sys.executable, "-m", "pytest", "-q", "tests"],
        cwd=B_ROOT / "solution",
        capture_output=True,
        text=True,
        timeout=45,
        check=False,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    assert "5 passed" in result.stdout


def test_mirror03_splits_contract_repository_isolation_and_restart_evidence() -> None:
    conftest = (C_ROOT / "solution/tests/conftest.py").read_text(encoding="utf-8")
    http_test = (C_ROOT / "solution/tests/test_http_contract.py").read_text(encoding="utf-8")
    openapi_test = (C_ROOT / "solution/tests/test_openapi_contract.py").read_text(encoding="utf-8")
    repo_test = (C_ROOT / "solution/tests/test_repository_integration.py").read_text(encoding="utf-8")
    isolation_test = (C_ROOT / "solution/tests/test_isolation.py").read_text(encoding="utf-8")
    restart_test = (C_ROOT / "solution/tests/test_restart_persistence.py").read_text(encoding="utf-8")

    assert "@pytest.fixture" in conftest and "tmp_path" in conftest
    assert "with TestClient(app)" in conftest and "engine.dispose()" in conftest
    assert "201" in http_test and 'headers["location"]' in http_test
    assert "404" in http_test and "422" in http_test
    assert 'schema["paths"]' in openapi_test and 'schema["components"]["schemas"]' in openapi_test
    assert "create_engine" in repo_test and "SqlAlchemyPostStore" in repo_test
    assert "MagicMock" not in repo_test
    assert "starts_with_seed_only" in isolation_test
    assert "app_a.state.engine.dispose()" in restart_test
    assert "app_b = create_app(database_url)" in restart_test

    result = subprocess.run(
        [sys.executable, "-m", "pytest", "-q", "tests"],
        cwd=C_ROOT / "solution",
        capture_output=True,
        text=True,
        timeout=60,
        check=False,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    assert "8 passed" in result.stdout


def test_debug_fixture_names_real_test_smells_and_reference_removes_them() -> None:
    broken = (D_ROOT / "starter/broken_tests.py").read_text(encoding="utf-8")
    fixed = (D_ROOT / "solution/fixed_tests.py").read_text(encoding="utf-8")
    diagnosis = (D_ROOT / "solution/DIAGNOSI.md").read_text(encoding="utf-8").lower()

    assert "shared-test.db" in broken
    assert "MagicMock" in broken
    assert "app.state.session_factory" in broken
    assert "except Exception" in broken and "pass" in broken

    assert "tmp_path" in fixed
    assert "@pytest.fixture" in fixed
    assert "engine.dispose()" in fixed
    assert "MagicMock" not in fixed
    assert "shared-test.db" not in fixed

    for concept in ("shared state", "order dependency", "over-mocking", "implementation detail", "teardown", "swallowed"):
        assert concept in diagnosis
