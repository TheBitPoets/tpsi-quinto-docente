from fastapi.testclient import TestClient

from app.main import create_app


def sqlite_url(path) -> str:
    return f"sqlite:///{path.as_posix()}"


def test_http_contract_openapi_and_restart_persistence(tmp_path):
    db_path = tmp_path / "feisbuc-mirror.db"
    database_url = sqlite_url(db_path)

    app1 = create_app(database_url)
    try:
        with TestClient(app1) as client:
            response = client.get("/api/posts")
            assert response.status_code == 200
            assert {post["id"] for post in response.json()} == {"seed-1"}

            created_response = client.post(
                "/api/posts",
                json={"text": "  SQLAlchemy mirror  ", "authorId": "spoof"},
            )
            assert created_response.status_code == 201
            created = created_response.json()
            assert created["text"] == "SQLAlchemy mirror"
            assert created["authorId"] == "mirror-user"
            assert created_response.headers["location"] == f"/api/posts/{created['id']}"

            liked = client.patch(f"/api/posts/{created['id']}", json={"liked": True})
            assert liked.status_code == 200
            assert liked.json()["liked"] is True
            assert liked.json()["likes"] == 1

            repeated = client.patch(f"/api/posts/{created['id']}", json={"liked": True})
            assert repeated.status_code == 200
            assert repeated.json()["likes"] == 1

            missing = client.patch("/api/posts/missing", json={"liked": True})
            assert missing.status_code == 404
            assert missing.json()["detail"]["code"] == "post-not-found"

            invalid = client.post("/api/posts", json={"text": "   "})
            assert invalid.status_code == 422

            schema = client.get("/openapi.json").json()
            assert {"get", "post"} <= set(schema["paths"]["/api/posts"])
            assert "patch" in schema["paths"]["/api/posts/{post_id}"]
            assert {"PostCreate", "PostLikePatch", "Post"} <= set(schema["components"]["schemas"])
    finally:
        app1.state.engine.dispose()

    assert db_path.is_file()

    app2 = create_app(database_url)
    try:
        with TestClient(app2) as client:
            response = client.get("/api/posts")
            assert response.status_code == 200
            posts = response.json()
            by_id = {post["id"]: post for post in posts}
            assert created["id"] in by_id
            assert by_id[created["id"]]["liked"] is True
            assert by_id[created["id"]]["likes"] == 1
            assert sum(post["id"] == "seed-1" for post in posts) == 1
    finally:
        app2.state.engine.dispose()
