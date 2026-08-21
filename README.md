# TPSI quinto anno — Full Stack Web Developer

Repository docente del corso **TPSI quinto anno — Full Stack Web Developer** per l'a.s. **2026/2027**.

Il curriculum è congelato nella release authoring **Content Pack 1.0.0 / approved**, conforme a `thebitlab.content-pack.v1` e pinned alla revisione accettata `5472eef86568a4e7ce59ad34ba937220df27efd7` di TheBitLab/2cornot2c.

## Presentazione del corso

Il corso accompagna una classe quinta dalla lettura consapevole della Web Platform alla costruzione, messa in sicurezza, test e consegna di una piccola applicazione full stack. Il filo conduttore è **Feisbuc**, un social didattico che cresce per milestone: prima pagine HTML/CSS, poi JavaScript, API REST, backend Express, SQLite, autenticazione, SPA Vue, realtime Socket.IO e infine un mirror Python con FastAPI/SQLAlchemy usato per confrontare architetture e confini.

L'obiettivo non è “fare tante tecnologie”, ma far vedere agli studenti **dove passano i confini**: browser/server, protocollo/framework, memoria/database, utente/sessione, JSON/tipo, stato locale/realtime, app funzionante/app verificabile.

### A chi serve questo repository

- **Docente**: indice del percorso, lezioni, attività, reference solution, Quality gate e slide Markdown da usare in classe.
- **Studenti**: mappa degli argomenti, collegamenti ai materiali e progressione del progetto Feisbuc.
- **TheBitLab / piattaforma**: Content Pack 1.0.0 approved, Activity schema, runner e regression test.

## Stato della release

- **33 settimane** di Course Design;
- UDA **20–26** complete;
- **19 moduli** originali, da architettura/metodo a runtime deploy/capstone;
- progetto longitudinale **Feisbuc milestone 0–12**;
- mirror Python **01–04**: FastAPI/OpenAPI → SQLAlchemy/SQLite → testing boundaries → runtime/deploy/evidence;
- Activity A–F e reference solution collegate ai content item;
- Quality cross-platform su Ubuntu Python 3.11/3.12 e Windows Python 3.11.

Il freeze editoriale è documentato in [`doc/CURRICULUM_FREEZE_2026_2027.md`](doc/CURRICULUM_FREEZE_2026_2027.md).

## Come usare i materiali in classe

1. Parti dall'indice qui sotto e apri il modulo della settimana.
2. Usa le [slide Markdown del corso](slides/tpsi5/COURSE_SLIDES.md) come scaletta di lezione.
3. Apri le Activity corrispondenti in [`activities/tpsi5/`](activities/tpsi5/) per esercitazione, debug o milestone Feisbuc.
4. Usa la Quality come prova che reference solution e contratti restano riproducibili.

Le slide sono in formato **Markdown compatibile con Marp**: possono essere lette direttamente su GitHub, proiettate come scaletta o convertite in PDF/PPTX con un renderer Markdown/Marp. Sono materiale docente derivato dal Content Pack approvato e **non modificano** il curriculum congelato.

## Indice cliccabile: argomenti, moduli e slide

| UDA | Modulo | Lezione | Slide | Nucleo didattico |
|---|---:|---|---|---|
| UDA-20 | 00 | [Architettura didattica del corso Full Stack](content/tpsi5/00_COURSE_ARCHITECTURE.md) | [Slide 00](slides/tpsi5/COURSE_SLIDES.md#slides-00) | Browser, HTTP, backend, database e progetto Feisbuc come filo conduttore. |
| UDA-21 | 01 | [Web Platform e HTML moderno](content/tpsi5/01_WEB_PLATFORM_HTML_MODERNO.md) | [Slide 01](slides/tpsi5/COURSE_SLIDES.md#slides-01) | Documento HTML, semantica, metadata, accessibilità e DevTools. |
| UDA-21 | 02 | [CSS moderno, layout e responsive design](content/tpsi5/02_CSS_MODERNO_RESPONSIVE.md) | [Slide 02](slides/tpsi5/COURSE_SLIDES.md#slides-02) | Cascade, box model, Flexbox/Grid, media query e mobile-first. |
| UDA-21 | 03 | [Bootstrap: dal CSS nativo a un framework frontend](content/tpsi5/03_BOOTSTRAP_DA_CSS_A_FRAMEWORK.md) | [Slide 03](slides/tpsi5/COURSE_SLIDES.md#slides-03) | Grid, utility e componenti come API sopra CSS. |
| UDA-22 | 04 | [JavaScript moderno, DOM e Browser APIs](content/tpsi5/04_JAVASCRIPT_DOM_BROWSER_APIS.md) | [Slide 04](slides/tpsi5/COURSE_SLIDES.md#slides-04) | State/render, eventi, delegation, modules e Web Storage. |
| UDA-23 | 05 | [HTTP, asincronia, Fetch e REST](content/tpsi5/05_HTTP_ASYNC_FETCH_REST.md) | [Slide 05](slides/tpsi5/COURSE_SLIDES.md#slides-05) | Request/response, status, header, fetch, async/await e REST. |
| UDA-24 | 06 | [Node.js ed Express 5: dal protocollo al backend](content/tpsi5/06_NODE_EXPRESS_BACKEND.md) | [Slide 06](slides/tpsi5/COURSE_SLIDES.md#slides-06) | Dal protocollo HTTP a Router, middleware, validation ed error pipeline. |
| UDA-24 | 07 | [SQL raw e persistenza: dal MemoryPostStore al database](content/tpsi5/07_SQL_RAW_PERSISTENCE.md) | [Slide 07](slides/tpsi5/COURSE_SLIDES.md#slides-07) | Schema, vincoli, DDL/DML, prepared statement e repository SQLite. |
| UDA-24 | 08 | [Autenticazione, sessioni e autorizzazione](content/tpsi5/08_AUTH_SESSIONI_SICUREZZA.md) | [Slide 08](slides/tpsi5/COURSE_SLIDES.md#slides-08) | Password hash, sessioni server-side, cookie, ownership e CSRF boundary. |
| UDA-24 | 09 | [SSR e template server-side](content/tpsi5/09_SSR_NUNJUCKS_CONFRONTO.md) | [Slide 09](slides/tpsi5/COURSE_SLIDES.md#slides-09) | View model, Nunjucks, autoescape, PRG e confronto API/SSR. |
| UDA-25 | 10 | [Vue 3: reattività, componenti e prima SPA Feisbuc](content/tpsi5/10_VUE3_COMPONENTI_REATTIVITA.md) | [Slide 10](slides/tpsi5/COURSE_SLIDES.md#slides-10) | Composition API, props/emits, state derivato e prima SPA. |
| UDA-25 | 11 | [Vue Router: URL, navigazione e route protette](content/tpsi5/11_VUE_ROUTER_NAVIGAZIONE_SPA.md) | [Slide 11](slides/tpsi5/COURSE_SLIDES.md#slides-11) | URL come stato, route, guard, layout e not found. |
| UDA-25 | 12 | [TypeScript mirato: contratti statici nei boundary frontend](content/tpsi5/12_TYPESCRIPT_CONTRATTI_FRONTEND.md) | [Slide 12](slides/tpsi5/COURSE_SLIDES.md#slides-12) | Tipi nei confini, DTO, unknown, parser e policy di navigazione. |
| UDA-25 | 13 | [WebSocket e Socket.IO: dal request/response al realtime](content/tpsi5/13_WEBSOCKET_SOCKETIO_REALTIME.md) | [Slide 13](slides/tpsi5/COURSE_SLIDES.md#slides-13) | Canale bidirezionale, eventi, recovery REST e payload unknown. |
| UDA-25 | 14 | [React translation lab: stessi concetti, altra sintassi](content/tpsi5/14_REACT_TRANSLATION_COMPARISON.md) | [Slide 14](slides/tpsi5/COURSE_SLIDES.md#slides-14) | Mapping Vue↔React: state, props, callback, JSX e derived values. |
| UDA-26 | 15 | [FastAPI e OpenAPI: mirror del contratto REST](content/tpsi5/15_FASTAPI_OPENAPI_MIRROR.md) | [Slide 15](slides/tpsi5/COURSE_SLIDES.md#slides-15) | Pydantic, OpenAPI, TestClient e stesso contratto HTTP. |
| UDA-26 | 16 | [SQLAlchemy 2.0 e persistenza](content/tpsi5/16_SQLALCHEMY_PERSISTENCE_MIRROR.md) | [Slide 16](slides/tpsi5/COURSE_SLIDES.md#slides-16) | Engine, Session, repository, transazioni e persistenza SQLite. |
| UDA-26 | 17 | [Testing strategy e integration boundaries](content/tpsi5/17_TESTING_INTEGRATION_BOUNDARIES.md) | [Slide 17](slides/tpsi5/COURSE_SLIDES.md#slides-17) | Fixture, tmp_path, integration test reali, HTTP contract e restart test. |
| UDA-26 | 18 | [Runtime configuration, health/readiness, deploy e capstone](content/tpsi5/18_RUNTIME_DEPLOY_HEALTH_CAPSTONE.md) | [Slide 18](slides/tpsi5/COURSE_SLIDES.md#slides-18) | Config fail-fast, prestart, liveness/readiness, Uvicorn e evidence bundle. |

## Stack core congelato

```text
Web Platform / HTML / CSS / Bootstrap
        ↓
JavaScript / DOM / Browser APIs
        ↓
HTTP / async / fetch / REST
        ↓
Node.js / Express 5
        ↓
SQL raw / SQLite
        ↓
auth / session / authorization / security
        ↓
SSR comparison / Nunjucks
        ↓
Vue 3 / Vite / Vue Router
        ↓
TypeScript targeted boundary typing
        ↓
Socket.IO realtime + REST recovery
        ↓
React translation/comparison lab
        ↓
FastAPI mirror / SQLAlchemy / pytest / deploy capstone
```

## Documenti principali

- [`content/tpsi5/content-pack.json`](content/tpsi5/content-pack.json) — manifest Content Pack **1.0.0 approved**;
- [`content/tpsi5/COVERAGE.md`](content/tpsi5/COVERAGE.md) — matrice di copertura congelata;
- [`content/tpsi5/00_COURSE_ARCHITECTURE.md`](content/tpsi5/00_COURSE_ARCHITECTURE.md) — architettura didattica;
- [`doc/course_designs/tpsi_quinto_2026_2027.json`](doc/course_designs/tpsi_quinto_2026_2027.json) — Course Design di 33 settimane;
- [`doc/OPEN_DECISIONS.md`](doc/OPEN_DECISIONS.md) — decisioni D1–D5 congelate;
- [`doc/CURRICULUM_FREEZE_2026_2027.md`](doc/CURRICULUM_FREEZE_2026_2027.md) — baseline, confini e policy post-freeze;
- [`doc/LEGACY_REUSE_AUDIT.md`](doc/LEGACY_REUSE_AUDIT.md) — provenance e audit dei materiali legacy;
- [`slides/tpsi5/`](slides/tpsi5/) — slide Markdown per la conduzione delle lezioni;
- [`activities/tpsi5/`](activities/tpsi5/) — Activity e reference solution;
- [`.github/workflows/quality.yml`](.github/workflows/quality.yml) — Quality del consumer reale.

## Confini deliberati

Non fanno parte del core 2026/27: ORM Node, Pinia senza requisito concreto, TypeScript avanzato/backend TypeScript, un secondo framework frontend core, duplicazione auth/session/realtime nel mirror Python, Alembic/PostgreSQL/async ORM, Kubernetes/cloud/scaling e CI/CD avanzata.

Il futuro corso SQL separato potrà approfondire e riusare milestone condivise, ma **non è un prerequisito bloccante** per questa release: TPSI5 contiene il minimo SQL raw necessario prima delle astrazioni.

Le capability di piattaforma #729 (browser/HTML grader) e #731 (TypeScript Activity runner) restano follow-up indipendenti e non bloccano il curriculum freeze.

Umbrella di progetto: `TheBitPoets/2cornot2c#728`. Standard cross-course accettato: `TheBitPoets/2cornot2c#723`.
