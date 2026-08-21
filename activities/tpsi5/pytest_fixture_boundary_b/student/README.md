# Pytest fixture boundary

Rifattorizza `tests/test_repository.py`.

Obiettivi:

- `@pytest.fixture` function-scoped;
- `tmp_path / "posts.db"`;
- `yield` + `engine.dispose()` nel teardown;
- ogni test parte da repository vuoto;
- parametrizzazione per le transizioni like;
- nessun database `shared-test.db` nel risultato.
