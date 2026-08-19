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
| Web Storage | sì, come passaggio | milestone 3 locale | `localStorage`/JSON solo per dati applicativi non sensibili; sostituito dalla API in milestone 4 |
| JavaScript debugging | sì | diagnosi comportamento client | Activity D UDA 22 usa bug reali del Feisbuc legacy |
| Asincronia | sì | **milestone 4 disponibile** | `05_HTTP_ASYNC_FETCH_REST.md`: Promise, `async`/`await`, error handling e separazione network/HTTP |
| HTTP | sì, approfondito | contratto client/server | request/response, URL/path/query, metodi, safe/idempotent, status, headers, Content-Type, curl e Network panel |
| Fetch | sì | client Feisbuc remoto | `response.ok`, parsing condizionale, error taxonomy |
| REST/API design | sì | **milestone 4–7** | contratto posts evolve senza perdere semantica HTTP; auth aggiunge register/login/me/logout |
| CORS / same-origin | sì, fondamenti | same-origin | niente `cors()` automatico; policy cross-origin soltanto con requisito reale |
| Node.js | sì | **milestone 5–7** | runtime, process/env, npm/package.json, ESM, `node:http`, `node:sqlite`, `node:crypto` |
| Express | sì | **milestone 5–7** | Express 5.2.1 pinned: Router, middleware, static, body parsing, auth pipeline, request ID/logging |
| Backend architecture | sì | boundary sostituibili | `app/server/router/validation/store/middleware`; auth/session e persistence restano separati |
| Modello relazionale / SQLite | sì | **milestone 6/7** | posts, users e sessions; FK/constraint/indici e prepared statements |
| SQL raw | sì, integrato e futuro corso dedicato | **milestone 6/7** | A/B/D autograded dal runner SQL; repository SQL prima dell'ORM |
| Prepared statements / SQL injection prevention | sì | repository SQL/auth | email, user/session/post id e contenuti vengono bindati |
| Transazioni | sì, fondamenti | repository | introdotte quando servono invarianti multi-statement |
| Password policy / hashing | sì | **milestone 7 disponibile** | 15–128, niente composition rule; `scrypt` + salt casuale; niente password plaintext |
| Session management | sì | **milestone 7 disponibile** | token opaco, hash token nel DB, TTL, logout/revoca, cookie `HttpOnly`/`SameSite`/`Secure` in production |
| Authentication | sì | **milestone 7 disponibile** | register/login/me/logout; errore login generico e identità derivata server-side |
| Authorization | sì | **milestone 7 disponibile** | ownership server-side; DELETE proprio 204, altrui 403, anonimo 401 |
| CSRF / same-origin defense | sì, fondamenti | milestone 7 | `SameSite=Strict` + controllo Origin/Sec-Fetch-Site per unsafe methods; defense in depth |
| ORM Node | sì, tecnologia TBD | persistenza evoluta | confronto Drizzle / Prisma / Sequelize **dopo** SQL raw e auth |
| Template/SSR | sì, compatto | **prossimo incremento UDA 24** | confronto SSR vs API/client render; auth model resta invariato |
| Framework frontend | sì, tecnologia TBD | SPA Feisbuc | candidato Vue 3; scelta non congelata |
| SPA e routing | sì | client completo | componenti, stato, form, REST |
| WebSocket/realtime | sì | live feed/chat/notifiche | WebSocket concettuale + Socket.IO applicativo |
| FastAPI mirror track | sì, mirato | API alternativa | stesso contratto HTTP, non doppio corso |
| OpenAPI | sì | documentazione API | naturale nel mirror FastAPI |
| SQLAlchemy | sì nel mirror Python | persistenza Python | mapping SQL ↔ ORM |
| Testing/debugging | sì | test Feisbuc | CSS/JS/HTTP/Express/SQL/auth debugging; JS/SQL puri autograded; auth/session reference E2E |
| Deployment | sì | release finale | env, build, log, HTTPS/reverse proxy concettuali; cookie Secure/proxy ripresi qui |
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
6 Express 5 + SqlPostStore + SQLite file
7 users + scrypt + server-side session + verified author + ownership
```

Il salto 6 → 7 cambia il **trust model**, non soltanto lo schema:

```text
prima
client -> API -> Router -> SqlPostStore
                  author convenzionale

ora
browser -> HttpOnly cookie
        -> loadAuth -> req.auth.user
        -> protected Router
        -> authorization
        -> SqlAuthStore + SqlPostStore
        -> SQLite
```

Il client non sceglie `authorId` e non legge il session token.

## Activity UDA 22

- [x] `tpsi5-activity-a-js-feed-pipeline-001` — JavaScript puro, grading deterministico;
- [x] `tpsi5-activity-b-js-post-refactor-001` — state update `map/spread`, grading deterministico;
- [x] `tpsi5-activity-c-feisbuc-dynamic-feed-001` — milestone 3, DOM/event delegation/localStorage;
- [x] `tpsi5-activity-d-debug-feisbuc-js-001` — debug browser.

## Activity UDA 23

- [x] `tpsi5-activity-a-http-microscope-001` — `curl -i` + DevTools;
- [x] `tpsi5-activity-b-async-response-policy-001` — Promise/async + `Response`, grading JS;
- [x] `tpsi5-activity-c-feisbuc-rest-client-001` — milestone 4, GET/POST/PATCH via `fetch`;
- [x] `tpsi5-activity-d-debug-fetch-http-001` — debug 404/media type/204.

## Activity UDA 24 — Node/Express

- [x] `tpsi5-activity-a-node-http-express-map-001` — confronto stessa API `node:http`/Express;
- [x] `tpsi5-activity-b-post-validation-001` — validation pura, grading JS;
- [x] `tpsi5-activity-c-feisbuc-express-api-001` — milestone 5, Express + MemoryPostStore;
- [x] `tpsi5-activity-d-debug-express-pipeline-001` — debug middleware/params/errors.

## Activity UDA 24 — SQL raw/persistence

- [x] `tpsi5-activity-a-sql-posts-schema-001` — schema/constraint, **grading SQL**;
- [x] `tpsi5-activity-b-sql-posts-dml-001` — DML/view/WHERE, **grading SQL**;
- [x] `tpsi5-activity-c-feisbuc-sql-repository-001` — milestone 6, `node:sqlite` + persistence restart-safe;
- [x] `tpsi5-activity-d-debug-sql-state-001` — constraint + UPDATE/DELETE debugging, **grading SQL + diagnosi**.

## Activity UDA 24 — auth/session/security

- [x] `tpsi5-activity-a-auth-credential-policy-001` — email/password policy, **grading JS**;
- [x] `tpsi5-activity-b-auth-post-authorization-001` — ownership/default deny, **grading JS**;
- [x] `tpsi5-activity-c-feisbuc-auth-session-001` — milestone 7, scrypt + session server-side + cookie + authn/authz;
- [x] `tpsi5-activity-d-debug-auth-security-001` — security review di password/session/identity/IDOR.

## Gate prima del freeze del curriculum TPSI5

1. completare UDA 24 con il breve confronto SSR/template;
2. definire/creare il corso SQL separato riusando il blocco SQL come primo consumer;
3. scelta framework frontend;
4. scelta ORM Node;
5. scelta profondità TypeScript;
6. calendario/UDA definitivo dopo verifica delle ore reali disponibili;
7. completare UDA 25–26: framework frontend, realtime, FastAPI mirror, testing e deploy.
