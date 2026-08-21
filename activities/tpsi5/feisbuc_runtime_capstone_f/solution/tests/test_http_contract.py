from fastapi.testclient import TestClient
from app.main import create_app
from app.prepare import prepare_database
from app.settings import RuntimeSettings

def test_posts_contract_is_unchanged(tmp_path):
    s=RuntimeSettings("test",f"sqlite:///{(tmp_path/'posts.db').as_posix()}","contract")
    prepare_database(s); app=create_app(s)
    with TestClient(app) as client:
        created=client.post("/api/posts",json={"text":"  runtime post  ","authorId":"spoof"})
        assert created.status_code==201
        post=created.json(); assert post["text"]=="runtime post" and post["authorId"]=="mirror-user"
        assert created.headers["location"]==f"/api/posts/{post['id']}"
        liked=client.patch(f"/api/posts/{post['id']}",json={"liked":True}); assert liked.status_code==200 and liked.json()["likes"]==1
        assert client.patch("/api/posts/missing",json={"liked":True}).status_code==404
        assert client.post("/api/posts",json={"text":"   "}).status_code==422
