from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_posts_contract_and_openapi():
    response = client.get("/api/posts")
    assert response.status_code == 200
    assert response.json()[0]["id"] == "seed-1"

    created = client.post("/api/posts", json={"text": "  FastAPI mirror  ", "authorId": "spoof"})
    assert created.status_code == 201
    post = created.json()
    assert post["text"] == "FastAPI mirror"
    assert post["authorId"] == "mirror-user"
    assert created.headers["location"] == f"/api/posts/{post['id']}"

    liked = client.patch(f"/api/posts/{post['id']}", json={"liked": True})
    assert liked.status_code == 200
    assert liked.json()["liked"] is True
    assert liked.json()["likes"] == 1

    missing = client.patch("/api/posts/missing", json={"liked": True})
    assert missing.status_code == 404
    assert missing.json()["detail"]["code"] == "post-not-found"

    invalid = client.post("/api/posts", json={"text": "   "})
    assert invalid.status_code == 422

    schema = client.get("/openapi.json").json()
    assert {"get", "post"} <= set(schema["paths"]["/api/posts"])
    assert "patch" in schema["paths"]["/api/posts/{post_id}"]
    assert "PostCreate" in schema["components"]["schemas"]
    assert "PostLikePatch" in schema["components"]["schemas"]
    assert "Post" in schema["components"]["schemas"]
