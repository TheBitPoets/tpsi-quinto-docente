# TPSI quinto 2026/27 — matrice di copertura iniziale

Stato: **draft**. Questa matrice descrive il perimetro del corso mentre i moduli vengono progressivamente trasformati in contenuti e Activity TheBitLab.

| Area | Core 2026/27 | Progetto Feisbuc | Note |
| --- | --- | --- | --- |
| Web Platform e browser | sì | struttura iniziale | documenti, metadata, DevTools e distinzione sorgente/DOM in `01_WEB_PLATFORM_HTML_MODERNO.md` |
| HTML moderno e semantica | sì | **milestone 0 disponibile** | Activity A/B UDA 21 |
| CSS moderno | sì | **milestone 1 disponibile** | cascade, specificità, box model, Flexbox, Grid, custom properties |
| Responsive design | sì | shell mobile-first | costruzione autonoma + debug/diagnosi |
| Bootstrap | sì, dopo CSS nativo | **milestone 2 disponibile** | framework come astrazione sopra CSS, mapping obbligatorio |
| JavaScript moderno | sì | comportamento client | `04_JAVASCRIPT_DOM_BROWSER_APIS.md`; array/object, map/filter/find, functions, ES modules; A/B autograded |
| DOM e Browser APIs | sì | **milestone 3 disponibile** | state/render, form, eventi, event delegation, dataset, textContent |
| Web Storage | sì, come passaggio | milestone 3 locale | `localStorage`/JSON come persistenza temporanea, poi sostituita dalla API in milestone 4 |
| JavaScript debugging | sì | diagnosi comportamento client | Activity D UDA 22 usa bug reali del Feisbuc legacy |
| Asincronia | sì | **milestone 4 disponibile** | `05_HTTP_ASYNC_FETCH_REST.md`: Promise, `async`/`await`, error handling e separazione network/HTTP |
| HTTP | sì, approfondito | contratto client/server | request/response, URL/path/query, metodi, safe/idempotent, status, headers, Content-Type, curl e Network panel |
| Fetch | sì | client Feisbuc remoto | `response.ok`, parsing condizionale, error taxonomy |
| REST/API design | sì | **milestone 4/5** | contratto `GET/POST/PATCH /api/posts` mantenuto mentre cambia il backend |
| CORS / same-origin | sì, fondamenti | same-origin | niente `cors()` automatico: policy cross-origin solo quando esiste un vero secondo origin |
| Node.js | sì | **milestone 5 disponibile** | `06_NODE_EXPRESS_BACKEND.md`: runtime, process/env, npm/package.json, ESM, event loop concettuale, `node:http` |
| Express | sì | **milestone 5 disponibile** | Express 5.2.1 pinned: Router, middleware, static, body parsing, validation, error pipeline, request ID/logging |
| Backend architecture | sì | memory store sostituibile | `app/server/router/validation/store/middleware`; Router dipende dallo store, non dalla memoria concreta |
| SQL | integrazione col corso SQL | **prossimo incremento UDA 24** | SQL raw repository prima dell'ORM; sostituirà `MemoryPostStore` mantenendo il contratto HTTP |
| ORM Node | sì, tecnologia TBD | persistenza evoluta | confronto Drizzle / Prisma / Sequelize dopo SQL raw |
| Auth e sicurezza web | sì | fase successiva UDA 24 | password hashing, session/authn/authz, cookie, secret; password in chiaro dei legacy è anti-pattern esplicito |
| Template/SSR | sì, compatto | fase successiva UDA 24 | Nunjucks/equivalente come confronto SSR vs API/SPA, non architettura finale obbligatoria |
| Framework frontend | sì, tecnologia TBD | SPA Feisbuc | candidato Vue 3; scelta non congelata |
| SPA e routing | sì | client completo | componenti, stato, form, REST |
| WebSocket/realtime | sì | live feed/chat/notifiche | WebSocket concettuale + Socket.IO applicativo |
| FastAPI mirror track | sì, mirato | API alternativa | stesso contratto HTTP, non doppio corso |
| OpenAPI | sì | documentazione API | naturale nel mirror FastAPI |
| SQLAlchemy | sì nel mirror Python | persistenza Python | mapping SQL ↔ ORM |
| Testing/debugging | sì | test Feisbuc | CSS/JS/HTTP/Express debugging; JS puro autograded; API reference E2E in CI |
| Deployment | sì | release finale | env, build, log, HTTPS/reverse proxy concettuali |
| Capstone | sì | Feisbuc | milestone progressive e prodotto finale |
| TypeScript | da decidere | eventuale fase avanzata | breve core o track advanced |
| Senior track | no, previsto | prosecuzione futura | architecture, perf, cache/queue, observability, CI/CD, scaling |

## Progressione Feisbuc disponibile

```text
0 semantic HTML
1 native responsive CSS
2 Bootstrap UI
3 JavaScript DOM + localStorage
4 HTTP REST API client + node:http fixture
5 Express 5 modular API + MemoryPostStore
```

La milestone 5 mantiene intenzionalmente il contratto di milestone 4:

```text
client
  -> api.js
  -> GET/POST/PATCH /api/posts
  -> Express Router
  -> validation
  -> MemoryPostStore
```

La prossima sostituzione desiderata è quindi locale al backend:

```text
MemoryPostStore
      ↓
SQL raw repository
```

senza riscrivere client, route semantics o error model.

## Activity UDA 22

- [x] `tpsi5-activity-a-js-feed-pipeline-001` — JavaScript puro, grading deterministico;
- [x] `tpsi5-activity-b-js-post-refactor-001` — state update `map/spread`, grading deterministico;
- [x] `tpsi5-activity-c-feisbuc-dynamic-feed-001` — milestone 3, DOM/event delegation/localStorage;
- [x] `tpsi5-activity-d-debug-feisbuc-js-001` — debug browser.

## Activity UDA 23

- [x] `tpsi5-activity-a-http-microscope-001` — `curl -i` + DevTools, request/response/status/header/content;
- [x] `tpsi5-activity-b-async-response-policy-001` — Promise/async + semantica `Response`, grading deterministico JS;
- [x] `tpsi5-activity-c-feisbuc-rest-client-001` — milestone 4, GET/POST/PATCH via `fetch`;
- [x] `tpsi5-activity-d-debug-fetch-http-001` — 404 vs network error, JSON/Content-Type, 204 e parsing.

## Activity UDA 24 — primo blocco Node/Express

- [x] `tpsi5-activity-a-node-http-express-map-001` — confronto stessa API `node:http`/Express;
- [x] `tpsi5-activity-b-post-validation-001` — validation pura, grading deterministico JS;
- [x] `tpsi5-activity-c-feisbuc-express-api-001` — milestone 5, Express Router/middleware/memory store;
- [x] `tpsi5-activity-d-debug-express-pipeline-001` — ordine middleware, params, safe methods, 404/error pipeline.

## Gate prima del freeze del curriculum TPSI5

1. completare UDA 24 con SQL raw, auth sicura e confronto SSR;
2. definire operativamente il confine col corso SQL separato;
3. scelta framework frontend;
4. scelta ORM Node;
5. scelta profondità TypeScript;
6. calendario/UDA definitivo dopo verifica delle ore reali disponibili;
7. completare UDA 25–26: framework frontend, realtime, FastAPI mirror, testing e deploy.
