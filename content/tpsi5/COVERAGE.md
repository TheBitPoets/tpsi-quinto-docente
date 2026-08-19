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
| Vue Router / SPA routing | **sì** | **milestone 10 disponibile** | URL/history, named routes, guard, client 404, Express deep-link fallback |
| TypeScript | TBD | UDA25/advanced | introduzione mirata preferita, profondita da congelare |
| Global state/Pinia | solo se motivato | non ancora | session composable sufficiente; store solo con requisito condiviso reale |
| ORM Node | TBD | futuro | confronto solo dopo SQL raw |
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
9 Vue 3 + Vite SPA shell + stessa API/auth/session/store
10 Vue Router + URL/history + protected navigation + deep-link fallback
```

### Milestone 10 — navigazione sopra lo stesso dominio

```text
App layout
  ↓
RouterView
  ├── LoginView
  ├── FeedView
  ├── AboutView
  └── NotFoundView
       ↓
small session composable
       ↓
api.js
       ↓
/api/*
       ↓
loadAuth + Router Express + stores + SQLite
```

Invariant:

- cookie sessione ancora `HttpOnly`;
- navigation guard e UX, non authorization API;
- feed route usa `meta.requiresAuth`;
- auth state distingue `unknown`, `anonymous`, `authenticated`;
- `/vue/{*splat}` serve `index.html` per i deep link HTML5 history;
- catch-all Vue Router gestisce la 404 client-side;
- autore del post continua a derivare da `req.auth.user`;
- delete continua a essere autorizzata server-side;
- nessun Pinia/TypeScript/ORM introdotto in questa verticale.

La Quality reference deve verificare almeno:

- build Vite del microscope router;
- navigation policy B passa il runner JS TheBitLab;
- frontend milestone 9 + routing overlay produce una build con Vue Router pinned;
- `GET /vue/` e **deep link `GET /vue/feed`** restituiscono l'entry HTML dal backend composto;
- `/api/posts` anonimo continua a produrre 401;
- register/session/posts API restano operativi;
- fallback SPA viene installato dopo `/api/*` e prima di `notFound`;
- starter D contiene realmente loop/base/meta/wildcard defects e la solution li rimuove.

## Activity UDA25 — Vue foundations

- [x] `tpsi5-activity-a-vue-reactivity-microscope-001`;
- [x] `tpsi5-activity-b-vue-post-card-001`;
- [x] `tpsi5-activity-c-feisbuc-vue-spa-001` — milestone 9;
- [x] `tpsi5-activity-d-debug-vue-reactivity-001`.

## Activity UDA25 — Vue Router

- [x] `tpsi5-activity-a-vue-router-microscope-001` — osservazione URL/history/deep link;
- [x] `tpsi5-activity-b-navigation-policy-001` — **automatico JS**;
- [x] `tpsi5-activity-c-feisbuc-vue-router-001` — milestone 10 overlay;
- [x] `tpsi5-activity-d-debug-vue-router-001` — debug multilivello.

## Boundary di grading Vue

Il runtime browser completo resta non disponibile nel grader TheBitLab. Build, fallback HTTP ed E2E della solution sono evidence del **repository docente**, non test automatici di RouterLink/back-forward/guard rendering nella consegna studente.

## Gate prima del freeze del curriculum TPSI5

1. definire/creare il corso SQL separato riusando il blocco SQL;
2. **framework frontend: completato — Vue 3 + Vite**;
3. **SPA routing: completato — Vue Router**;
4. decidere profondita TypeScript;
5. decidere ORM Node quando serve realmente;
6. verificare ore reali e calendario definitivo;
7. completare UDA25: TypeScript boundary, realtime e translation lab React;
8. completare UDA26: FastAPI mirror, testing, deploy e capstone.
