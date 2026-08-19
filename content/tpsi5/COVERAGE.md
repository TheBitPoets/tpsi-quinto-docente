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
| HTTP | sì, approfondito | **contratto client/server implementato** | request/response, URL/path/query, metodi, safe/idempotent, status, header/content, Content-Type, curl e DevTools Network |
| Fetch | sì | client Feisbuc remoto | `response.ok`, Content-Type, parsing condizionale, `AbortController` concettuale, error taxonomy |
| REST/API design | sì | **milestone 4 disponibile** | `GET /api/posts`, `POST /api/posts`, `PATCH /api/posts/:id`, representation/error model |
| CORS / same-origin | sì, fondamenti | micro-esperimento | prima same-origin; poi origin/preflight/header CORS; middleware Express soltanto in UDA 24 |
| Node.js | sì | fixture server in UDA23, backend in UDA24 | in UDA23 `node:http` è una fixture trasparente; runtime/npm/server diventano oggetto di studio nella UDA successiva |
| Express | sì | API/SSR | **UDA 24**, dopo HTTP nativo: routing, Router, middleware, validation/error handling, static, CORS, auth |
| SQL | integrazione col corso SQL | persistenza | SQL raw prima dell'ORM |
| ORM Node | sì, tecnologia TBD | persistenza evoluta | confronto Drizzle / Prisma / Sequelize |
| Auth e sicurezza web | sì | login/sessione | password hashing, authn/authz, XSS/CSRF/SQLi, secret, cookie |
| Template/SSR | sì, compatto | confronto architetturale | Nunjucks o equivalente come passaggio concettuale |
| Framework frontend | sì, tecnologia TBD | SPA Feisbuc | candidato Vue 3; scelta non congelata |
| SPA e routing | sì | client completo | componenti, stato, form, REST |
| WebSocket/realtime | sì | live feed/chat/notifiche | WebSocket concettuale + Socket.IO applicativo |
| FastAPI mirror track | sì, mirato | API alternativa | stesso contratto HTTP, non doppio corso |
| OpenAPI | sì | documentazione API | naturale nel mirror FastAPI |
| SQLAlchemy | sì nel mirror Python | persistenza Python | mapping SQL ↔ ORM |
| Testing/debugging | sì | test Feisbuc | CSS/JS/HTTP debugging; JS puro autograded; fixture API smoke-testate in CI |
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
4 HTTP REST API client
```

Milestone 4 sostituisce esplicitamente:

```text
app.js -> localStorage
```

con:

```text
app.js -> api.js -> fetch -> HTTP -> server fixture
```

senza ancora introdurre Express o database.

## Activity UDA 22

- [x] `tpsi5-activity-a-js-feed-pipeline-001` — JavaScript puro, grading deterministico;
- [x] `tpsi5-activity-b-js-post-refactor-001` — state update `map/spread`, grading deterministico;
- [x] `tpsi5-activity-c-feisbuc-dynamic-feed-001` — milestone 3, DOM/event delegation/localStorage;
- [x] `tpsi5-activity-d-debug-feisbuc-js-001` — debug browser.

## Activity UDA 23

- [x] `tpsi5-activity-a-http-microscope-001` — `curl -i` + DevTools, request/response/status/header/content;
- [x] `tpsi5-activity-b-async-response-policy-001` — Promise/async + semantica `Response`, **grading deterministico JS**;
- [x] `tpsi5-activity-c-feisbuc-rest-client-001` — milestone 4, GET/POST/PATCH via `fetch`;
- [x] `tpsi5-activity-d-debug-fetch-http-001` — 404 vs network error, JSON/Content-Type, 204 e parsing.

## Gate prima del freeze del curriculum TPSI5

1. completare l'audit progressivo di `labs_summary`/Feisbuc durante UDA 24–26;
2. scelta framework frontend;
3. scelta ORM Node;
4. scelta profondità TypeScript;
5. definizione operativa del confine col corso SQL separato;
6. calendario/UDA definitivo dopo verifica delle ore reali disponibili;
7. proseguire con Node/Express, DB, auth/SSR, framework frontend, realtime, FastAPI mirror, testing e deploy.
