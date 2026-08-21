# Diagnosi

1. **Shared state**: app/client/database globali rendono la suite dipendente dal processo e lasciano dati fra test.
2. **Order dependency**: `test_2` passa solo se `test_1` ha gia creato un post.
3. **Over-mocking**: sostituire il repository in un test dichiarato integration elimina SQLAlchemy e SQLite, cioe il boundary da provare.
4. **Implementation detail assertion**: controllare `app.state.session_factory` non verifica il contratto osservabile dal client.
5. **Missing teardown**: l'Engine globale non ha ownership/cleanup esplicito.
6. **Swallowed failure**: `except Exception: pass` trasforma un errore in un falso verde.

La soluzione usa fixture function-scoped, `tmp_path`, database reale, TestClient context manager, dispose dell'Engine e assert su status/header/body.
