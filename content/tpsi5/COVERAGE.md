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
| Global state/Pinia | solo se motivato | non introdotto | FeedView ha ancora ownership naturale del feed; sessione resta composable singleton |
| ORM Node | TBD | futuro | confronto solo dopo SQL raw |
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
9 Vue 3 + Vite SPA shell + stessa API/auth/session/store
10 Vue Router + URL/history + protected navigation + deep-link fallback
11 TypeScript strict sui boundary frontend + stesso backend/API
12 REST commands + Socket.IO realtime + reconnect/resync
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

- Activity B passa il runner JavaScript TheBitLab;
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

## Boundary di grading UDA25

Il browser grader TheBitLab non e ancora implementato e il runner deterministico TheBitLab non dichiara ancora TypeScript. Le Activity Vue/TypeScript/realtime che richiedono browser o connessioni restano quindi `correzione.test=false`. La Quality docente puo eseguire `tsc`/`vue-tsc`, build, backend live e probe Socket.IO a due client; questa evidence non viene spacciata per autograding browser dello studente.

## Gate prima del freeze del curriculum TPSI5

1. definire/creare il corso SQL separato riusando il blocco SQL;
2. **framework frontend: completato — Vue 3 + Vite**;
3. **SPA routing: completato — Vue Router**;
4. **profondita TypeScript: completata — targeted boundary typing**;
5. **realtime: completato — WebSocket concettuale + Socket.IO applicato**;
6. decidere ORM Node quando serve realmente;
7. verificare ore reali e calendario definitivo;
8. completare il breve translation/comparison lab React;
9. completare UDA26: FastAPI mirror, testing, deploy e capstone.
