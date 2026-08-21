import pytest
from fastapi.testclient import TestClient

from app.main import create_app


def sqlite_url(path) -> str:
    return f"sqlite:///{path.as_posix()}"


@pytest.fixture
def client(tmp_path):
    db_path = tmp_path / "feisbuc-test.db"
    app = create_app(sqlite_url(db_path))
    try:
        with TestClient(app) as test_client:
            yield test_client
    finally:
        app.state.engine.dispose()
