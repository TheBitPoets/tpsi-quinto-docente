def test_fixture_starts_with_seed_only(client):
    posts = client.get("/api/posts").json()
    assert [post["id"] for post in posts] == ["seed-1"]
    client.post("/api/posts", json={"text": "local to this test"})
    assert len(client.get("/api/posts").json()) == 2


def test_another_test_also_starts_with_seed_only(client):
    posts = client.get("/api/posts").json()
    assert [post["id"] for post in posts] == ["seed-1"]
