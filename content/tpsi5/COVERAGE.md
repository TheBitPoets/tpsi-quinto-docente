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
| SSR/template | sì, compatto | milestone 8 | Nunjucks, view model, autoescape, PRG, coexistence API/SSR |
| Vue 3 + Vite | **sì, D1 deciso** | milestone 9 | SFC, Composition API, ref/computed, props/emits, API/auth invariati |
| Vue Router / SPA routing | **sì** | milestone 10 | URL/history, named routes, guard, client 404, Express deep-link fallback |
| TypeScript | **sì, D3 deciso** | milestone 11 | targeted boundary typing: dominio, API `unknown`, props/emits, session e route meta |
| WebSocket/realtime | **sì** | **milestone 12** | WebSocket concettuale + Socket.IO 4.8.3, REST commands, session handshake e resync |
| React translation/comparison | **sì, breve non-core** | nessuna milestone nuova | Vue -> React: state, derived values, props/callback, JSX, controlled input; React non diventa secondo frontend core |
| Global state/Pinia | solo se motivato | non introdotto | FeedView ha ancora ownership naturale del feed; sessione resta composable singleton |
| ORM Node | TBD | futuro | confronto solo dopo SQL raw |
| FastAPI mirror/OpenAPI | **sì, D4 deciso** | mirror 01 | FastAPI/Pydantic/OpenAPI/TestClient + MemoryPostStore; stesso dominio HTTP, non secondo backend completo |
| SQLAlchemy mirror | **sì** | **mirror 02** | SQLAlchemy 2.0.51 + SQLite sotto lo stesso contratto FastAPI; repository/Session boundary e restart persistence |
| Testing strategy | **sì** | **mirror 03** | pytest 9.1.1, fixture/tmp_path, repository + HTTP integration, restart/isolation e mock boundary |
| Deploy/capstone | **sì, completato** | **mirror 04** | env config/fail-fast, prestart, health/readiness, live Uvicorn probe, runbook ed evidence SHA-256 |

## Progressione Feisbuc principale

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
9 Vue 3 + Vite SPA shell + stessa API/auth/session/store
10 Vue Router + URL/history + protected navigation + deep-link fallback
11 TypeScript strict sui boundary frontend + stesso backend/API
12 REST commands + Socket.IO realtime + reconnect/resync
```

Il translation lab React **non aggiunge una milestone 13**: confronta un problema UI già risolto e mantiene Feisbuc sul frontend Vue core.

## Track mirror Python UDA26

Il mirror e una progressione separata dal prodotto principale:

```text
Feisbuc HTTP contract gia noto
        ↓
mirror 01
FastAPI + Pydantic + OpenAPI + TestClient
        ↓
MemoryPostStore
        ↓
mirror 02
stessa suite HTTP + SQLAlchemy 2.0.51 + SQLite file
        ↓
restart persistence + repository/transaction evidence
        ↓
mirror 03
pytest fixture + isolation + repository/HTTP contract boundaries
        ↓
mirror 04
runtime config + prestart + liveness/readiness + live Uvicorn + evidence
```

Invariant mirror 01:

- il contratto HTTP viene confrontato con Express, non reinventato da zero;
- route core: `GET /api/posts`, `POST /api/posts`, `PATCH /api/posts/{id}`;
- `PostCreate` e `Post` sono modelli distinti;
- `authorId` non appartiene al command affidabile;
- POST usa `201` e `Location`;
- `response_model` definisce la representation pubblica;
- id inesistente produce `404`;
- validation Pydantic `422` viene resa visibile come differenza di compatibility, non nascosta automaticamente;
- OpenAPI espone path/schema verificabili;
- `TestClient` verifica il contratto senza server TCP;
- MemoryPostStore non importa FastAPI;
- nessun SQLAlchemy, auth/session, Socket.IO o secondo frontend in mirror 01.

Baseline primo slice UDA26:

```text
FastAPI   0.141.1
Pydantic  2.13.4
Uvicorn   0.52.1
HTTPX     0.28.1
Python    3.11 / 3.12 CI
```

Invariant mirror 02:

- SQLAlchemy `2.0.51` e pinned e usa la API moderna `DeclarativeBase` / `Mapped` / `mapped_column` / `select`;
- `PostCreate`/`PostLikePatch`/`Post` restano boundary Pydantic separati dalla entity ORM `PostRow`;
- Engine e SessionFactory nascono nel composition root; le route non costruiscono il database;
- `SqlAlchemyPostStore` non importa FastAPI e usa Session a lifetime corto;
- create/update fanno commit esplicito;
- `session.query(...)` non e baseline del corso;
- `row.__dict__` non diventa representation pubblica;
- seed `seed-1` e idempotente;
- il database SQLite e configurabile e nei test usa un file temporaneo;
- una seconda app sullo stesso file recupera il post creato dalla prima dopo `engine.dispose()`;
- `GET`, `POST 201 + Location`, `PATCH`, `404`, `422` e OpenAPI restano compatibili col mirror 01;
- nessun auth/session Python, Socket.IO, Alembic, async ORM o deploy viene introdotto in questo slice.

Baseline secondo slice UDA26:

```text
FastAPI      0.141.1
Pydantic     2.13.4
Uvicorn      0.52.1
HTTPX        0.28.1
SQLAlchemy   2.0.51
SQLite       file temporaneo/reference
Python       3.11 / 3.12 CI
```

### Milestone 12 — comandi REST, eventi Socket.IO

```text
browser A ── POST/PATCH/DELETE ──► REST API
                                     │
                                     ├─ auth / validation
                                     ├─ SqlPostStore / SQLite
                                     └─ domain event
                                           │
                                           ▼
                                      Socket.IO
                                      ├─ browser A
                                      └─ browser B

connect/reconnect
   ↓
listener realtime attivo
   ↓
GET /api/posts ───────┐
   │                  │ eventi concorrenti
   │                  ▼
   │               coda eventi
   ▼                  │
snapshot autorevole ◄─┘
   ↓
state convergente
```

Invariant:

- Socket.IO non sostituisce la REST API dei comandi;
- il socket anonimo viene rifiutato;
- l'identita del socket deriva dallo stesso cookie/session store server-side;
- nessun `authorId` o `userId` inviato dal socket client viene trusted;
- sessione rivalidata prima del broadcast e socket invalido disconnesso;
- eventi core: `post:created`, `post:updated`, `post:deleted`;
- ogni payload Socket.IO esterno entra nel frontend come `unknown` e diventa `Post`/`RealtimeEvent` solo dopo runtime validation;
- `post:created` e idempotente nel reducer client;
- listener Socket.IO hanno lifecycle start/stop simmetrico;
- il realtime e attivo mentre lo snapshot REST e in volo; gli eventi concorrenti vengono accodati e riapplicati allo snapshot per evitare la race snapshot→connect;
- reconnect non viene confuso con delivery completa: `GET /api/posts` ricostruisce lo snapshot;
- TypeScript strict resta attivo;
- nessun Pinia/ORM introdotto nella milestone 12.

La Quality reference deve verificare almeno:

- Activity B realtime passa il runner JavaScript TheBitLab;
- frontend milestone 11 + overlay realtime passa `vue-tsc` e Vite build;
- backend composto usa Express e Socket.IO sullo stesso HTTP server;
- socket anonimo viene rifiutato;
- due sessioni autentiche ricevono create/update/delete;
- un evento client inventato `post:create` non modifica il dominio;
- autore dei post continua a derivare da `req.auth.user`;
- adapter client conserva i payload remoti come `unknown` fino al parser runtime;
- FeedView implementa resync con listener attivo + coda eventi, non snapshot seguito da connect;
- dopo disconnessione, lo snapshot REST recupera una mutazione avvenuta offline;
- HTTP/SQL/auth/SSR/Vue/Router/TypeScript gates precedenti restano attivi.

## Activity UDA25 — Vue foundations

- [x] `tpsi5-activity-a-vue-reactivity-microscope-001`;
- [x] `tpsi5-activity-b-vue-post-card-001`;
- [x] `tpsi5-activity-c-feisbuc-vue-spa-001` — milestone 9;
- [x] `tpsi5-activity-d-debug-vue-reactivity-001`.

## Activity UDA25 — Vue Router

- [x] `tpsi5-activity-a-vue-router-microscope-001`;
- [x] `tpsi5-activity-b-navigation-policy-001` — automatico JS;
- [x] `tpsi5-activity-c-feisbuc-vue-router-001` — milestone 10;
- [x] `tpsi5-activity-d-debug-vue-router-001`.

## Activity UDA25 — TypeScript mirato

- [x] `tpsi5-activity-a-typescript-contract-microscope-001`;
- [x] `tpsi5-activity-b-typescript-navigation-policy-001`;
- [x] `tpsi5-activity-c-feisbuc-typescript-boundaries-001` — milestone 11;
- [x] `tpsi5-activity-d-debug-typescript-boundaries-001`.

## Activity UDA25 — realtime

- [x] `tpsi5-activity-a-websocket-realtime-microscope-001` — polling/WebSocket/Socket.IO/recovery;
- [x] `tpsi5-activity-b-realtime-event-reducer-001` — reducer idempotente, automatico JS;
- [x] `tpsi5-activity-c-feisbuc-socketio-realtime-001` — milestone 12;
- [x] `tpsi5-activity-d-debug-realtime-boundaries-001` — trust/lifecycle/delivery/architecture.

## Activity UDA25 — React translation/comparison

- [x] `tpsi5-activity-a-react-translation-microscope-001` — `ref/computed` -> `useState`/derived value, manuale;
- [x] `tpsi5-activity-b-react-post-card-translation-001` — props/emits -> props/callback e immutable parent state, manuale.

Boundary:

- React resta un translation lab, non un secondo stack applicativo;
- nessuna nuova milestone Feisbuc;
- nessun React Router, Redux, Next.js, Server Components o React Compiler nel core;
- `computed` viene tradotto prima come valore derivato; `useMemo` non viene introdotto automaticamente;
- la Quality costruisce le reference React/Vite ma non dichiara browser autograding.


Invariant mirror 03:

- nessuna nuova route o feature di prodotto; il nuovo artefatto e il test harness;
- pytest `9.1.1` e pinned nella reference;
- fixture function-scoped e `tmp_path` isolano database/app per test;
- repository integration usa SQLAlchemy + SQLite reali, non mock;
- HTTP integration attraversa FastAPI + Pydantic + repository + SQLite tramite TestClient;
- restart persistence resta un test separato con due app/Engine;
- OpenAPI e verificato con smoke assert su path/schema significativi, non snapshot byte-per-byte;
- test indipendenti dall'ordine e niente `shared-test.db`;
- mock ammessi solo per boundary esterni/costosi/non deterministici, non per l'integrazione sotto test;
- CI mantiene gate reference separati prima della regression suite completa.

Baseline terzo slice UDA26:

```text
pytest        9.1.1
FastAPI       0.141.1
Pydantic      2.13.4
HTTPX         0.28.1
SQLAlchemy    2.0.51
SQLite        file temporanei via tmp_path
Python        3.11 / 3.12 CI
```

## Activity UDA26 — FastAPI/OpenAPI mirror

- [x] `tpsi5-activity-a-fastapi-openapi-microscope-001` — route/OpenAPI/schema/422, manuale;
- [x] `tpsi5-activity-b-fastapi-post-validation-001` — policy Python pura, **automatico Python**;
- [x] `tpsi5-activity-c-feisbuc-fastapi-mirror-001` — mirror 01 con MemoryPostStore e TestClient;
- [x] `tpsi5-activity-d-debug-fastapi-boundaries-001` — status/trust/schema/404/output boundary.

## Activity UDA26 — SQLAlchemy persistence mirror

- [x] `tpsi5-activity-a-sqlalchemy-mapping-microscope-001` — mapping/Engine/Session/SQL echo, manuale;
- [x] `tpsi5-activity-b-sqlalchemy-repository-001` — repository ORM isolato da FastAPI, manuale con reference CI;
- [x] `tpsi5-activity-c-feisbuc-fastapi-sqlalchemy-001` — mirror 02 con SQLite file + restart persistence;
- [x] `tpsi5-activity-d-debug-sqlalchemy-transactions-001` — Engine/Session lifetime, flush/commit/rollback, Query legacy e output boundary.


## Activity UDA26 — Testing strategy e integration boundaries

- [x] `tpsi5-activity-a-testing-boundary-microscope-001` — scegliere il livello minimo che osserva la proprieta, manuale;
- [x] `tpsi5-activity-b-pytest-fixture-boundary-001` — fixture function-scoped, `tmp_path`, teardown e parametrizzazione, manuale con reference CI;
- [x] `tpsi5-activity-c-feisbuc-testing-boundaries-001` — mirror 03 feature-neutral con HTTP/OpenAPI/repository/isolation/restart suite;
- [x] `tpsi5-activity-d-debug-testing-boundaries-001` — shared state, order dependency, over-mocking, internal assert e teardown.


Invariant mirror 04:

- nessuna nuova feature di prodotto: `GET/POST/PATCH /api/posts` resta invariato;
- `FEISBUC_ENV`, `FEISBUC_DATABASE_URL` e `FEISBUC_BUILD_SHA` sono app config; host/port/workers/reload restano process-server config;
- production senza database URL fallisce subito;
- `python -m app.prepare` possiede schema+seed e `create_app()` non prepara implicitamente il DB;
- `/health` e liveness e non interroga SQLite;
- `/ready` attraversa la dipendenza reale `posts` e risponde `503` generico finche non e pronta;
- FastAPI lifespan dispone l'Engine;
- la CI avvia un processo Uvicorn reale con deadline e cleanup;
- l'evidence bundle contiene `manifest.json`, `openapi.json`, `SHA256SUMS.txt` senza timestamp/PID/porta/path/secret;
- runbook production-like usa un processo Uvicorn senza `--reload`;
- nessun auth/session/realtime Python, Alembic, PostgreSQL, async ORM, Docker Compose, Kubernetes, reverse proxy o TLS entra nel closeout.

Baseline quarto slice UDA26:

```text
pytest        9.1.1
FastAPI       0.141.1
Pydantic      2.13.4
Uvicorn       0.52.1
HTTPX         0.28.1
SQLAlchemy    2.0.51
SQLite        file temporaneo / runtime URL
Python        3.11 / 3.12 CI
```

## Activity UDA26 — Runtime deploy e capstone

- [x] `tpsi5-activity-a-runtime-deploy-microscope-001` — config/prestart/liveness/readiness map;
- [x] `tpsi5-activity-b-runtime-config-contract-001` — config policy pura, **automatico Python**;
- [x] `tpsi5-activity-c-health-readiness-001` — probe red/green con SQLite reale;
- [x] `tpsi5-activity-d-debug-runtime-deploy-001` — fallback/leakage/fake readiness/lifecycle debug;
- [x] `tpsi5-activity-e-evidence-bundle-001` — manifest/OpenAPI/SHA-256 deterministici;
- [x] `tpsi5-activity-f-feisbuc-runtime-capstone-001` — mirror 04 integrato con live Uvicorn probe.

## Boundary di grading

Il browser grader TheBitLab non e ancora implementato e il runner deterministico TheBitLab non dichiara ancora TypeScript. Le Activity Vue/TypeScript/realtime/React che richiedono browser o connessioni restano quindi `correzione.test=false`. La Quality docente puo eseguire `tsc`/`vue-tsc`, build Vue/React, backend live e probe Socket.IO a due client; questa evidence non viene spacciata per autograding browser dello studente.

Per UDA26 il runner **Python e implementato**: Activity B FastAPI e Activity B runtime-config usano `correzione.test=true` per policy Python pure. Le Activity framework/database/process/evidence restano manual/rubric-based nella piattaforma; la repository Quality valida SQLAlchemy, HTTP/restart, health/readiness, processo Uvicorn reale ed evidence senza dichiarare un grader deployment specifico.

## Gate prima del freeze del curriculum TPSI5

1. definire/creare il corso SQL separato riusando il blocco SQL;
2. **framework frontend: completato — Vue 3 + Vite**;
3. **SPA routing: completato — Vue Router**;
4. **profondita TypeScript: completata — targeted boundary typing**;
5. **realtime: completato — WebSocket concettuale + Socket.IO applicato**;
6. decidere ORM Node quando serve realmente;
7. verificare ore reali e calendario definitivo;
8. **translation/comparison lab React: completato — breve, non-core, nessuna seconda SPA**;
9. **FastAPI/OpenAPI mirror: primo slice UDA26 implementato**;
10. **SQLAlchemy persistence mirror: secondo slice UDA26 implementato**;
11. **testing strategy/integration boundaries: terzo slice UDA26 implementato**;
12. **runtime deploy/capstone: quarto slice UDA26 completato; UDA26 chiusa**.
