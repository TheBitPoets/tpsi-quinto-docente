# Activity TPSI5

Le Activity usano TheBitLab Activity 1.0 e la tassonomia A–F.

## Estratto UDA24–26

| Livello | ID | Scopo | Grading |
| --- | --- | --- | --- |
| A | `tpsi5-activity-a-node-http-express-map-001` | native HTTP -> Express | manuale + reference CI |
| B | `tpsi5-activity-b-post-validation-001` | validation pura | automatico JS |
| C | `tpsi5-activity-c-feisbuc-express-api-001` | milestone 5 | manuale + E2E |
| D | `tpsi5-activity-d-debug-express-pipeline-001` | Express debug | manuale + E2E |
| A | `tpsi5-activity-a-sql-posts-schema-001` | schema/constraint | automatico SQL |
| B | `tpsi5-activity-b-sql-posts-dml-001` | DML | automatico SQL |
| C | `tpsi5-activity-c-feisbuc-sql-repository-001` | milestone 6 | manuale + E2E |
| D | `tpsi5-activity-d-debug-sql-state-001` | SQL debug | automatico SQL + diagnosi |
| A | `tpsi5-activity-a-auth-credential-policy-001` | credential policy | automatico JS |
| B | `tpsi5-activity-b-auth-post-authorization-001` | ownership/default deny | automatico JS |
| C | `tpsi5-activity-c-feisbuc-auth-session-001` | milestone 7 | manuale + security E2E |
| D | `tpsi5-activity-d-debug-auth-security-001` | security review | manuale |
| A | `tpsi5-activity-a-ssr-view-model-001` | view model | automatico JS |
| B | `tpsi5-activity-b-nunjucks-autoescape-001` | Nunjucks/escape | manuale + reference render CI |
| C | `tpsi5-activity-c-feisbuc-ssr-001` | milestone 8 | manuale + composed E2E CI |
| D | `tpsi5-activity-d-debug-ssr-boundaries-001` | SSR trust-boundary debug | manuale |
| A | `tpsi5-activity-a-vue-reactivity-microscope-001` | `ref`/`computed` observation | manuale + reference Vite build |
| B | `tpsi5-activity-b-vue-post-card-001` | props down / emits up | manuale + reference Vite build |
| C | `tpsi5-activity-c-feisbuc-vue-spa-001` | milestone 9 Vue SPA | manuale + build + composed backend smoke |
| D | `tpsi5-activity-d-debug-vue-reactivity-001` | reactivity/component debugging | manuale + starter/solution build |
| A | `tpsi5-activity-a-vue-router-microscope-001` | URL/history/RouterView/deep link | manuale + Vite build |
| B | `tpsi5-activity-b-navigation-policy-001` | navigation state machine | **automatico JS** |
| C | `tpsi5-activity-c-feisbuc-vue-router-001` | milestone 10 Vue Router | manuale + composed build/deep-link E2E |
| D | `tpsi5-activity-d-debug-vue-router-001` | history/guard/fallback debug | manuale + structural checks |
| A | `tpsi5-activity-a-typescript-contract-microscope-001` | inference/union/unknown/nullability | manuale + `tsc --noEmit` reference |
| B | `tpsi5-activity-b-typescript-navigation-policy-001` | discriminated navigation union | manuale + `tsc --noEmit` reference |
| C | `tpsi5-activity-c-feisbuc-typescript-boundaries-001` | milestone 11 TS boundary overlay | manuale + `vue-tsc` + build + composed E2E |
| D | `tpsi5-activity-d-debug-typescript-boundaries-001` | static type debugging | starter type-check rosso, solution verde |
| A | `tpsi5-activity-a-websocket-realtime-microscope-001` | polling/WebSocket/Socket.IO/recovery | manuale |
| B | `tpsi5-activity-b-realtime-event-reducer-001` | event reducer idempotente | **automatico JS** |
| C | `tpsi5-activity-c-feisbuc-socketio-realtime-001` | milestone 12 realtime multiutente | manuale + type-check/build + two-client E2E |
| D | `tpsi5-activity-d-debug-realtime-boundaries-001` | trust/lifecycle/delivery debug | manuale + structural checks |
| A | `tpsi5-activity-a-fastapi-openapi-microscope-001` | FastAPI/OpenAPI microscope | manuale + TestClient reference |
| B | `tpsi5-activity-b-fastapi-post-validation-001` | validation policy pura | **automatico Python** |
| C | `tpsi5-activity-c-feisbuc-fastapi-mirror-001` | mirror 01 FastAPI | manuale + reference CI |
| D | `tpsi5-activity-d-debug-fastapi-boundaries-001` | FastAPI boundary debug | manuale |
| A | `tpsi5-activity-a-sqlalchemy-mapping-microscope-001` | ORM mapping/Session | manuale + reference CI |
| B | `tpsi5-activity-b-sqlalchemy-repository-001` | repository ORM | manuale + pytest reference |
| C | `tpsi5-activity-c-feisbuc-fastapi-sqlalchemy-001` | mirror 02 persistence | manuale + restart CI |
| D | `tpsi5-activity-d-debug-sqlalchemy-transactions-001` | transaction/session debug | manuale |
| A | `tpsi5-activity-a-testing-boundary-microscope-001` | test-level reasoning | manuale |
| B | `tpsi5-activity-b-pytest-fixture-boundary-001` | fixture/tmp_path/isolation | manuale + pytest reference |
| C | `tpsi5-activity-c-feisbuc-testing-boundaries-001` | mirror 03 testing harness | manuale + integration/restart CI |
| D | `tpsi5-activity-d-debug-testing-boundaries-001` | shared-state/over-mocking debug | manuale |
| A | `tpsi5-activity-a-runtime-deploy-microscope-001` | runtime/config/health map | manuale |
| B | `tpsi5-activity-b-runtime-config-contract-001` | config policy/fail-fast | **automatico Python** |
| C | `tpsi5-activity-c-health-readiness-001` | health/readiness | manuale + reference CI |
| D | `tpsi5-activity-d-debug-runtime-deploy-001` | runtime boundary debug | manuale |
| E | `tpsi5-activity-e-evidence-bundle-001` | evidence mini-project | manuale + reference CI |
| F | `tpsi5-activity-f-feisbuc-runtime-capstone-001` | mirror 04 runtime capstone | manuale + live-process/evidence CI |

## Boundary di grading

```text
linguaggio puro JS/SQL           -> runner deterministico TheBitLab
TypeScript puro/SFC              -> reference tsc/vue-tsc in repository CI
Vue/browser                      -> reference build + smoke/E2E docente
Socket.IO transport/domain       -> reference two-client E2E docente
browser DOM/offline interaction  -> browser grader futuro
Python puro                    -> runner deterministico TheBitLab
pytest/framework/database       -> reference CI docente
backend/persistence/security     -> reference E2E
security/architecture reasoning  -> rubrica + evidence
```

Il browser grader TheBitLab non e ancora implementato e il runner accettato non dichiara TypeScript. Le Activity TS/realtime restano `correzione.test=false` quando richiedono runtime non disponibili nella piattaforma. Activity B realtime e invece autograded perche il reducer e JavaScript puro. In UDA26 le policy Python pure (FastAPI B e runtime-config B) restano automatiche; fixture pytest, FastAPI/SQLAlchemy multi-file, health/readiness, live process ed evidence restano reference CI e rubrica manuale.

La Quality docente puo:

- eseguire `tsc`/`vue-tsc` e Vite build;
- comporre milestone 11 + realtime overlay;
- avviare Express + Socket.IO sullo stesso server;
- verificare socket anonimo rifiutato;
- aprire due socket autenticati e osservare create/update/delete;
- verificare che un command socket inventato non muti il dominio;
- simulare offline e verificare lo snapshot REST di recovery.

Queste evidence dimostrano la reference solution; non sostituiscono il futuro browser grader per DOM, DevTools/offline mode o UI dello studente.


## Quality UDA26

La CI pinna `pytest 9.1.1` e valida fixture repository, mirror 02 persistence, mirror 03 testing harness e mirror 04 runtime capstone. Il closeout aggiunge health/readiness, processo Uvicorn reale ed evidence bundle deterministico prima della regression suite completa.
