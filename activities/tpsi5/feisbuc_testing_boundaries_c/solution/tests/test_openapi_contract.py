def test_openapi_exposes_core_paths_and_schemas(client):
    schema = client.get("/openapi.json").json()
    assert {"get", "post"} <= set(schema["paths"]["/api/posts"])
    assert "patch" in schema["paths"]["/api/posts/{post_id}"]
    assert {"PostCreate", "PostLikePatch", "Post"} <= set(schema["components"]["schemas"])
