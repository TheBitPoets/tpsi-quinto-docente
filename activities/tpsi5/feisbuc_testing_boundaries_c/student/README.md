# Feisbuc mirror 03 — testing boundaries

L'applicazione e gia il mirror 02. Non aggiungere route.

Completa la suite in `tests/` separando:

- fixture/lifecycle in `conftest.py`;
- HTTP contract;
- OpenAPI smoke;
- repository integration con SQLite reale;
- test di isolamento;
- restart persistence.

Regole: `tmp_path`, DB per test, dispose dell'Engine, nessun mock di SQLAlchemy/SQLite/FastAPI, niente assert su dettagli privati dell'app.
