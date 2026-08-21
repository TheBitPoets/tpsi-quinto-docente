from fastapi.testclient import TestClient
from app.main import create_app
from app.prepare import prepare_database
from app.settings import RuntimeSettings

def test_post_survives_new_app_and_engine(tmp_path):
    s=RuntimeSettings("test",f"sqlite:///{(tmp_path/'restart.db').as_posix()}","restart")
    prepare_database(s)
    app_a=create_app(s)
    with TestClient(app_a) as client:
        post=client.post("/api/posts",json={"text":"persist me"}).json()
        client.patch(f"/api/posts/{post['id']}",json={"liked":True})
    app_b=create_app(s)
    with TestClient(app_b) as client:
        posts={p["id"]:p for p in client.get("/api/posts").json()}
        assert posts[post["id"]]["text"]=="persist me"
        assert posts[post["id"]]["liked"] is True
        assert posts[post["id"]]["likes"]==1
