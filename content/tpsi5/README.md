# TPSI quinto anno — Content Pack

Questo package contiene i contenuti originali del corso **TPSI quinto anno — Full Stack Web Developer**, a.s. 2026/2027.

Contratto di authoring: `thebitlab.content-pack.v1`, pinned alla revisione Accettata `5472eef86568a4e7ce59ad34ba937220df27efd7` di `TheBitPoets/2cornot2c`.

## Principi

- Web Platform prima dei framework;
- HTTP esplicito prima di `fetch`/Express;
- SQL raw prima dell'ORM;
- trasporto, validation, persistence, auth, authorization e presentation separati;
- identita derivata server-side da sessione verificata;
- SSR e client rendering confrontati sopra lo stesso dominio;
- Vue viene introdotto dopo DOM manuale/API/auth/SSR;
- Vue Router entra solo quando l'URL deve rappresentare piu viste;
- TypeScript rende verificabili boundary reali, non sostituisce runtime validation;
- realtime aggiunge un **event path**, ma REST resta il **command path**;
- reconnect non viene confuso con recovery: Feisbuc rilegge uno snapshot REST;
- Node.js + Express backend principale; FastAPI mirror mirato;
- test progettati per boundary osservabili, isolamento e diagnosi, non per percentuali decorative;
- Feisbuc progetto longitudinale;
- documentazioni ufficiali e security guidance come reference;
- Activity A–F con asset student/teacher separati.

## Contenuti disponibili

1. `00_COURSE_ARCHITECTURE.md` — architettura e metodo;
2. `01_WEB_PLATFORM_HTML_MODERNO.md` — HTML; milestone 0;
3. `02_CSS_MODERNO_RESPONSIVE.md` — CSS/responsive; milestone 1;
4. `03_BOOTSTRAP_DA_CSS_A_FRAMEWORK.md` — Bootstrap; milestone 2;
5. `04_JAVASCRIPT_DOM_BROWSER_APIS.md` — JS/DOM/storage; milestone 3;
6. `05_HTTP_ASYNC_FETCH_REST.md` — HTTP/fetch/REST; milestone 4;
7. `06_NODE_EXPRESS_BACKEND.md` — Node/Express; milestone 5;
8. `07_SQL_RAW_PERSISTENCE.md` — SQL raw/SQLite; milestone 6;
9. `08_AUTH_SESSIONI_SICUREZZA.md` — auth/session/authorization; milestone 7;
10. `09_SSR_NUNJUCKS_CONFRONTO.md` — SSR/Nunjucks/PRG; milestone 8;
11. `10_VUE3_COMPONENTI_REATTIVITA.md` — Vue 3/Vite; milestone 9;
12. `11_VUE_ROUTER_NAVIGAZIONE_SPA.md` — Vue Router; milestone 10;
13. `12_TYPESCRIPT_CONTRATTI_FRONTEND.md` — TypeScript mirato; milestone 11;
14. `13_WEBSOCKET_SOCKETIO_REALTIME.md` — WebSocket/Socket.IO, delivery e recovery; milestone 12;
15. `14_REACT_TRANSLATION_COMPARISON.md` — translation lab Vue -> React, non-core;
16. `15_FASTAPI_OPENAPI_MIRROR.md` — mirror 01 HTTP/OpenAPI/TestClient;
17. `16_SQLALCHEMY_PERSISTENCE_MIRROR.md` — mirror 02 SQLAlchemy/SQLite/restart;
18. `17_TESTING_INTEGRATION_BOUNDARIES.md` — mirror 03 pytest, fixture/isolation e integration boundaries;
19. `18_RUNTIME_DEPLOY_HEALTH_CAPSTONE.md` — mirror 04 runtime config, health/readiness, live Uvicorn ed evidence capstone. milestone 12.

## Feisbuc oggi

```text
0 semantic HTML
1 responsive native CSS
2 Bootstrap UI
3 dynamic JS + localStorage
4 HTTP REST client + node:http fixture
5 Express 5 + MemoryPostStore
6 Express 5 + SqlPostStore + SQLite
7 users + scrypt + HttpOnly session + ownership
8 API JSON + SSR Nunjucks sopra stesso auth/store
9 Vue 3 + Vite SPA shell sopra stessa API/auth/store
10 Vue Router + URL/history + protected routes + deep-link fallback
11 TypeScript strict sui boundary frontend + stesso backend/API
12 REST commands + Socket.IO realtime + reconnect/resync
```

Milestone 12 mantiene due flussi distinti:

```text
COMMAND
browser -> REST -> auth/validation -> SQLite -> HTTP response
                                ↓
                              event
                                ↓
EVENT
server -> Socket.IO -> client A / client B

RECOVERY
reconnect -> GET /api/posts -> snapshot autorevole
```


## Track mirror Python UDA26

```text
mirror 01  FastAPI + Pydantic + OpenAPI + TestClient
    ↓
mirror 02  SQLAlchemy 2.0 + SQLite + restart persistence
    ↓
mirror 03  pytest + fixture/tmp_path + repository/HTTP integration + isolation
    ↓
mirror 04  config/prestart + health/readiness + live Uvicorn + capstone/evidence
```

Il mirror non sostituisce il backend principale Node/Express: serve a trasferire concetti e rendere visibili i contratti fra framework diversi.

Baseline testing: `pytest 9.1.1`; niente coverage plugin, xdist, Testcontainers o browser automation in questo slice.

## Decisioni frontend

Le decisioni D1–D5 sono congelate per la release 2026/27:

```text
framework core      = Vue 3 + Vite
router core         = Vue Router
TypeScript depth    = targeted-boundary-typing
realtime core       = WebSocket concettuale + Socket.IO applicato
React               = translation/comparison lab
ORM Node             = fuori dal core 2026/27
corso SQL separato   = integrazione futura non bloccante
```

Baseline reference UDA25:

```text
Vue                  3.5.40
Vue Router           5.2.0
Vite                 8.2.1
@vitejs/plugin-vue   6.0.8
TypeScript           6.0.3
vue-tsc              3.3.8
Socket.IO            4.8.3
socket.io-client     4.8.3
Node                 >=22.18
```

## Activity UDA25 — realtime

- `tpsi5-activity-a-websocket-realtime-microscope-001` — polling, WebSocket, Socket.IO e recovery;
- `tpsi5-activity-b-realtime-event-reducer-001` — reducer idempotente, autograded JS;
- `tpsi5-activity-c-feisbuc-socketio-realtime-001` — milestone 12 multiutente;
- `tpsi5-activity-d-debug-realtime-boundaries-001` — security, lifecycle, delivery e architecture debug.

## Boundary UDA25

Non sono introdotti automaticamente:

```text
Pinia
ORM
backend Express in TypeScript
Socket.IO command handlers per create/update/delete
```

Il feed resta posseduto da `FeedView`; Pinia entra solo se piu feature/route richiederanno una cache condivisa con ownership non piu locale.

## Grading

Il browser grader TheBitLab non e ancora implementato e lo snapshot accettato del runner non dichiara TypeScript. Le Activity browser/TypeScript/realtime rimangono manuali quando richiedono DOM o connessioni. La Quality docente usa `tsc`/`vue-tsc`, build Vite, server live e un probe Socket.IO a due utenti come evidence della reference solution. Activity B realtime resta invece automaticamente verificabile come JavaScript puro.

## Stato

Release authoring **`1.0.0`**, stato editoriale **`approved`**. Curriculum 2026/27 congelato su 33 settimane con UDA20–UDA26 complete.

D2 congela l'ORM Node fuori dal core; D5 rende il futuro corso SQL un'integrazione non bloccante. Dettagli e policy post-freeze: `doc/CURRICULUM_FREEZE_2026_2027.md`.
