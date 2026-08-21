# Feisbuc mirror 02 — FastAPI + SQLAlchemy

Questo milestone cambia **solo il data layer** del mirror 01.

## Contratto da non cambiare

```text
GET   /api/posts
POST  /api/posts
PATCH /api/posts/{post_id}
```

Success semantics:

- GET -> 200 + `list[Post]`;
- POST -> 201 + `Location` + `Post`;
- PATCH esistente -> 200 + `Post`;
- PATCH mancante -> 404;
- body Pydantic invalido -> 422;
- `/openapi.json` continua a descrivere gli stessi model HTTP.

## Architettura target

```text
FastAPI route
    ↓
Pydantic command/response
    ↓
SqlAlchemyPostStore
    ↓
SessionFactory
    ↓
SQLAlchemy 2.0
    ↓
SQLite
```

## Lavoro

1. confronta `models.py` e `entities.py`;
2. completa `SqlAlchemyPostStore.list()`;
3. completa `create()` con `add + commit`;
4. completa `set_liked()` con `Session.get`, transizione idempotente e commit;
5. esegui l'app con un database file;
6. verifica `/docs` e `/openapi.json`;
7. con TestClient o curl crea e modifica un post;
8. riavvia l'app e verifica che il post esista ancora.

## Regole

- non importare FastAPI in `store.py`;
- non mettere `HTTPException` nel repository;
- non usare una Session globale;
- non creare Engine dentro le route;
- non usare `session.query`;
- non restituire `row.__dict__`;
- non aggiungere auth, Socket.IO o Alembic.

## Check finale

La domanda piu importante non e “funziona SQLAlchemy?”.

E:

> Il client puo distinguere, dal contratto HTTP, se dietro FastAPI c'e MemoryPostStore o SQLAlchemy?

Per le response di successo e i casi governati del milestone, la risposta deve essere **no**.
