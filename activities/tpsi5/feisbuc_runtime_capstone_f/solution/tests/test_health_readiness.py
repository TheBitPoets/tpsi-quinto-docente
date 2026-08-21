from fastapi.testclient import TestClient
from app.main import create_app
from app.prepare import prepare_database
from app.settings import RuntimeSettings

def settings(tmp_path): return RuntimeSettings("test", f"sqlite:///{(tmp_path/'runtime.db').as_posix()}", "test-sha")

def test_liveness_does_not_require_prepared_database(tmp_path):
    app=create_app(settings(tmp_path))
    with TestClient(app) as client:
        r=client.get("/health"); assert r.status_code==200; assert r.json()=={"status":"ok","build":"test-sha"}
        r=client.get("/ready"); assert r.status_code==503; assert r.json()["detail"]=={"code":"not-ready"}

def test_readiness_turns_green_after_explicit_prepare(tmp_path):
    s=settings(tmp_path); prepare_database(s); app=create_app(s)
    with TestClient(app) as client:
        assert client.get("/ready").status_code==200
        assert client.get("/api/posts").json()[0]["id"]=="seed-1"
