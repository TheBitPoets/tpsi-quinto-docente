from fastapi.testclient import TestClient

from app.main import create_app


def sqlite_url(path) -> str:
    return f"sqlite:///{path.as_posix()}"


def test_restart_preserves_created_and_liked_post(tmp_path):
    db_path = tmp_path / "restart.db"
    database_url = sqlite_url(db_path)

    app_a = create_app(database_url)
    try:
        with TestClient(app_a) as client:
            created = client.post("/api/posts", json={"text": "survive restart"}).json()
            liked = client.patch(f"/api/posts/{created['id']}", json={"liked": True})
            assert liked.status_code == 200
    finally:
        app_a.state.engine.dispose()

    app_b = create_app(database_url)
    try:
        with TestClient(app_b) as client:
            posts = {post["id"]: post for post in client.get("/api/posts").json()}
            assert created["id"] in posts
            assert posts[created["id"]]["liked"] is True
            assert posts[created["id"]]["likes"] == 1
            assert sum(post["id"] == "seed-1" for post in posts.values()) == 1
    finally:
        app_b.state.engine.dispose()
