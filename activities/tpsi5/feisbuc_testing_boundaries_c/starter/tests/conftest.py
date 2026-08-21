import pytest
from fastapi.testclient import TestClient

from app.main import create_app


def sqlite_url(path) -> str:
    return f"sqlite:///{path.as_posix()}"


@pytest.fixture
def client(tmp_path):
    # TODO: crea app con DB sotto tmp_path, usa TestClient come context manager,
    # yield del client e dispose dell'Engine nel finally.
    raise NotImplementedError
