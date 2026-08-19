# TPSI quinto 2026/27 — matrice di copertura iniziale

Stato: **draft**.

| Area | Core 2026/27 | Progetto Feisbuc | Note |
| --- | --- | --- | --- |
| Web Platform/HTML/CSS | sì | milestone 0–1 | semantica, responsive, Flexbox/Grid |
| Bootstrap | sì, dopo CSS | milestone 2 | framework come astrazione |
| JavaScript/DOM/Storage | sì | milestone 3 | state/render, delegation, localStorage temporaneo |
| HTTP/Fetch/REST | sì | milestone 4 | request/response, status, errors, REST |
| Node/Express | sì | milestone 5 | Express 5.2.1, Router/middleware/validation/error model |
| SQL raw/SQLite | sì | milestone 6 | `node:sqlite`, constraint, prepared statement, persistence |
| Auth/session/authz | sì | milestone 7 | scrypt, HttpOnly cookie, session server-side, ownership |
| SSR/template | sì, compatto | **milestone 8 disponibile** | Nunjucks 3.2.4, view model, autoescape, PRG, coexistence API/SSR |
| ORM Node | TBD | futuro | confronto solo dopo SQL raw |
| Framework frontend | TBD | UDA25 | candidato Vue 3; decisione da congelare |
| TypeScript | TBD | UDA25/advanced | profondita da congelare |
| WebSocket/realtime | sì | UDA25 | WebSocket concettuale + Socket.IO applicato |
| FastAPI mirror/OpenAPI/SQLAlchemy | sì, mirato | UDA26 | stesso contratto HTTP come mirror |
| Testing/deploy/capstone | sì | UDA26 | release finale e osservabilita base |

## Progressione Feisbuc

```text
0 semantic HTML
1 native responsive CSS
2 Bootstrap UI
3 JavaScript DOM + localStorage
4 HTTP REST API client + node:http fixture
5 Express 5 + MemoryPostStore
6 Express 5 + SqlPostStore + SQLite file
7 users + scrypt + server-side session + ownership
8 Nunjucks SSR + stessa API/auth/session/store
```

### Milestone 8 — due presentation adapter

```text
                         +-> JSON -> JS -> DOM
SqlPostStore + session --|
                         +-> view model -> Nunjucks -> HTML
```

La Quality reference deve verificare:

- anonimo `/ssr` -> 401;
- utente autenticato `/ssr` -> `text/html`;
- POST form -> 303 -> GET;
- body utente con `<script>` viene escapato;
- non-owner non vede delete e riceve 403 se forza la route;
- owner delete -> 303 e rimozione;
- `/api/posts` continua a essere JSON e vede le stesse righe.

## Activity UDA24 — SSR

- [x] `tpsi5-activity-a-ssr-view-model-001` — grading JS;
- [x] `tpsi5-activity-b-nunjucks-autoescape-001` — template lab + reference CI;
- [x] `tpsi5-activity-c-feisbuc-ssr-001` — milestone 8 overlay;
- [x] `tpsi5-activity-d-debug-ssr-boundaries-001` — escaping/authz/PRG review.

## Gate prima del freeze del curriculum TPSI5

1. definire/creare il corso SQL separato riusando il blocco SQL;
2. congelare framework frontend;
3. decidere profondita TypeScript;
4. decidere ORM Node quando serve realmente;
5. verificare ore reali e calendario definitivo;
6. completare UDA25–26: framework frontend/realtime, FastAPI mirror, testing e deploy.
