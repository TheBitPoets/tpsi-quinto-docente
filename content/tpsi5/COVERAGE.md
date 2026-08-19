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
| Vue 3 + Vite | **sì, D1 deciso** | **milestone 9 disponibile** | SFC, Composition API, ref/computed, props/emits, API/auth invariati |
| SPA routing | sì | prossimo blocco UDA25 | Vue Router solo quando serve URL/navigation |
| TypeScript | TBD | UDA25/advanced | introduzione mirata preferita, profondita da congelare |
| Global state/Pinia | solo se motivato | non ancora | props/emits prima; store solo con requisito condiviso reale |
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
```

### Milestone 9 — framework frontend senza riscrivere il backend

```text
Vue App
  ├── AuthPanel
  ├── PostComposer
  └── PostCard * N
       ↓
      api.js
       ↓
     /api/*
       ↓
loadAuth + Router + stores + SQLite
```

Invariant:

- cookie sessione ancora `HttpOnly`;
- nessun token in `localStorage`/`sessionStorage`/`document.cookie`;
- autore del post ancora derivato da `req.auth.user`;
- delete ancora autorizzata server-side;
- Vue non introduce una seconda persistence strategy.

La Quality reference deve verificare almeno:

- build Vite delle reference A/B/C/D;
- base `/vue/` nella build milestone 9;
- SPA statica servita dallo stesso Express della milestone 7;
- `/api/auth/me` e `/api/posts` mantengono il contratto;
- register/session/API restano utilizzabili con la SPA presente;
- `PostCard` non contiene `fetch` e comunica tramite emits;
- nessun Router/Pinia/TypeScript introdotto prematuramente.

## Activity UDA25 — Vue foundations

- [x] `tpsi5-activity-a-vue-reactivity-microscope-001` — `ref`/`computed`, osservazione + reference build;
- [x] `tpsi5-activity-b-vue-post-card-001` — props/emits, reference build;
- [x] `tpsi5-activity-c-feisbuc-vue-spa-001` — milestone 9, reference build + composed E2E;
- [x] `tpsi5-activity-d-debug-vue-reactivity-001` — debugging reattivita/component boundary, starter+solution build.

## Boundary di grading Vue

Il runtime browser completo resta non disponibile nel grader TheBitLab. Le build e gli E2E della solution sono evidence del **repository docente**, non test automatici della consegna studente.

## Gate prima del freeze del curriculum TPSI5

1. definire/creare il corso SQL separato riusando il blocco SQL;
2. **framework frontend: completato — Vue 3 + Vite**;
3. decidere profondita TypeScript;
4. decidere ORM Node quando serve realmente;
5. verificare ore reali e calendario definitivo;
6. completare UDA25: Vue Router, realtime e translation lab React;
7. completare UDA26: FastAPI mirror, testing, deploy e capstone.
