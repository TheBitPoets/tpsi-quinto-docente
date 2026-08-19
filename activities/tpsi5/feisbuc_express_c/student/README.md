# Feisbuc milestone 5 — Express API

## Obiettivo

Il client di UDA 23 deve continuare a usare:

```text
GET   /api/posts
POST  /api/posts
PATCH /api/posts/:id
```

La differenza e solo il backend.

## Setup

```bash
npm install
npm start
```

Il server deve stampare:

```text
READY http://127.0.0.1:<porta>
```

Poi apri quell'URL nel browser.

## Architettura attesa

```text
src/server.js
   -> config + listen

src/app.js
   -> middleware + static + router + errors

src/posts.router.js
   -> mapping HTTP della risorsa posts

src/validation.js
   -> funzioni pure

src/post-store.js
   -> memoria, nessuna dipendenza Express

src/middleware.js
   -> requestId/logger/404/error handler

public/
   -> client gia funzionante da UDA 23
```

## Smoke request

```bash
curl -i http://127.0.0.1:3000/api/posts
```

```bash
curl -i \
  -H "Content-Type: application/json" \
  -d '{"text":"Express senza magia"}' \
  http://127.0.0.1:3000/api/posts
```

Usa l'id restituito:

```bash
curl -i \
  -X PATCH \
  -H "Content-Type: application/json" \
  -d '{"liked":true}' \
  http://127.0.0.1:3000/api/posts/<id>
```

## Errori da verificare

- POST senza `Content-Type: application/json` -> 415;
- POST con `{}` -> 400;
- PATCH id inesistente -> 404;
- route inesistente -> 404;
- JSON invalido -> 400.

Ogni error response deve avere:

```json
{
  "error": {
    "code": "...",
    "message": "...",
    "requestId": "..."
  }
}
```

## Definition of done

- il client browser continua a funzionare;
- `X-Request-Id` compare nelle response;
- il router non crea direttamente lo store;
- la validation non importa Express;
- non compare SQLite/ORM/auth/Nunjucks;
- non viene aggiunto `cors()` senza un caso cross-origin reale.
