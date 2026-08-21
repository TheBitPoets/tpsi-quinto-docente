# Feisbuc mirror 01 — FastAPI/OpenAPI

## Scope

Implementa solo:

```text
GET   /api/posts
POST  /api/posts
PATCH /api/posts/{id}
```

Mantieni:
- public Post shape;
- POST 201;
- header Location;
- PATCH liked;
- 404 per id inesistente.

Il command create contiene solo `text`: non fidarti di `authorId` dal client.

Usa un autore fixture del mirror (`mirror-user` / `Mirror Student`): **non inventare una seconda autenticazione**.

## Evidence

Con `TestClient` verifica:
- GET iniziale;
- POST valida;
- trim del testo;
- Location;
- PATCH;
- 404;
- body invalido -> 422;
- `/openapi.json` contiene GET/POST/PATCH e gli schema Pydantic.

SQLAlchemy, SQLite, sessioni e realtime sono fuori da questo slice.
