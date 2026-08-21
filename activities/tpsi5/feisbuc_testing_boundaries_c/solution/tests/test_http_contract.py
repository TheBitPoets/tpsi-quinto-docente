def test_create_post_contract(client):
    response = client.post(
        "/api/posts",
        json={"text": "  testing boundary  ", "authorId": "spoof"},
    )
    assert response.status_code == 201
    body = response.json()
    assert body["text"] == "testing boundary"
    assert body["authorId"] == "mirror-user"
    assert response.headers["location"] == f"/api/posts/{body['id']}"


def test_like_is_idempotent_and_missing_is_404(client):
    created = client.post("/api/posts", json={"text": "like"}).json()
    first = client.patch(f"/api/posts/{created['id']}", json={"liked": True})
    second = client.patch(f"/api/posts/{created['id']}", json={"liked": True})
    assert first.status_code == second.status_code == 200
    assert first.json()["likes"] == second.json()["likes"] == 1

    missing = client.patch("/api/posts/missing", json={"liked": True})
    assert missing.status_code == 404
    assert missing.json()["detail"]["code"] == "post-not-found"


def test_invalid_payload_is_422(client):
    response = client.post("/api/posts", json={"text": "   "})
    assert response.status_code == 422
