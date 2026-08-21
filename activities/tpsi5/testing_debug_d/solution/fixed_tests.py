import pytest
from fastapi.testclient import TestClient

from app.main import create_app


def sqlite_url(path) -> str:
    return f"sqlite:///{path.as_posix()}"


@pytest.fixture
def client(tmp_path):
    app = create_app(sqlite_url(tmp_path / "test.db"))
    try:
        with TestClient(app) as test_client:
            yield test_client
    finally:
        app.state.engine.dispose()


def test_create_is_observable_through_http(client):
    response = client.post("/api/posts", json={"text": "isolated"})
    assert response.status_code == 201
    body = response.json()
    assert response.headers["location"] == f"/api/posts/{body['id']}"


def test_each_test_has_fresh_state(client):
    assert [post["id"] for post in client.get("/api/posts").json()] == ["seed-1"]


def test_missing_is_explicit_404(client):
    response = client.patch("/api/posts/missing", json={"liked": True})
    assert response.status_code == 404
    assert response.json()["detail"]["code"] == "post-not-found"
