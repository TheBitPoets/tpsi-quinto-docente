from unittest.mock import MagicMock
from fastapi.testclient import TestClient

from app.main import create_app

# BUG: database e app globali condivisi da tutta la suite.
app = create_app("sqlite:///./shared-test.db")
client = TestClient(app)


def test_1_create_changes_shared_state():
    response = client.post("/api/posts", json={"text": "global"})
    assert response.status_code == 201


def test_2_depends_on_test_1():
    assert len(client.get("/api/posts").json()) == 2


def test_http_with_everything_mocked():
    # BUG: il test viene chiamato integration ma sostituisce proprio il repository.
    app.state.post_store = MagicMock()
    assert app.state.session_factory is not None  # BUG: dettaglio interno, non contract.


def test_swallow_failure():
    try:
        client.patch("/api/posts/missing", json={"liked": True})
    except Exception:
        pass  # BUG: il test puo diventare verde senza verificare nulla.
