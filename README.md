# TPSI quinto anno — Full Stack Web Developer

Repository docente del corso **TPSI quinto anno — Full Stack Web Developer** per l'a.s. **2026/2027**.

Il curriculum è congelato nella release authoring **Content Pack 1.0.0 / approved**, conforme a `thebitlab.content-pack.v1` e pinned alla revisione accettata `5472eef86568a4e7ce59ad34ba937220df27efd7` di TheBitLab/2cornot2c.

## Presentazione del corso

Il corso accompagna una classe quinta dalla lettura consapevole della Web Platform alla costruzione, messa in sicurezza, test e consegna di una piccola applicazione full stack. Il filo conduttore è **Feisbuc**, un social didattico che cresce per milestone: prima pagine HTML/CSS, poi JavaScript, API REST, backend Express, SQLite, autenticazione, SPA Vue, realtime Socket.IO e infine un mirror Python con FastAPI/SQLAlchemy usato per confrontare architetture e confini.

L'obiettivo non è “fare tante tecnologie”, ma far vedere agli studenti **dove passano i confini**: browser/server, protocollo/framework, memoria/database, utente/sessione, JSON/tipo, stato locale/realtime, app funzionante/app verificabile.

### Ingressi rapidi

- **Docente:** [`teacher/README.md`](teacher/README.md) — conduzione della lezione, demo, debugging, gestione delle modifiche in-year.
- **Studente:** [`student/README.md`](student/README.md) — workflow leggi/esegui/modifica/test/debug/consegna, setup e troubleshooting.
- **Slide:** [`slides/tpsi5/README.md`](slides/tpsi5/README.md) — indice delle presentazioni.
- **Activity/lab:** [`activities/tpsi5/`](activities/tpsi5/) — esercitazioni, debug, milestone e reference solution.
- **Modifiche durante l'anno:** [`doc/DELIVERY_CHANGELOG.md`](doc/DELIVERY_CHANGELOG.md).

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

Il freeze editoriale è documentato in [`doc/CURRICULUM_FREEZE_2026_2027.md`](doc/CURRICULUM_FREEZE_2026_2027.md). Il materiale di delivery può essere corretto e migliorato durante l'anno senza cambiare silenziosamente il curriculum: ogni revisione classroom-facing va registrata nel [`Delivery Change Log`](doc/DELIVERY_CHANGELOG.md).

## Come usare i materiali in classe

1. Parti dall'indice qui sotto e apri il modulo della settimana.
2. Usa le [slide Markdown del corso](slides/tpsi5/COURSE_SLIDES.md) o i deck modulari come narrazione della lezione.
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

## Pianificazione annuale, docenti e consuntivo

Il piano usa le **132 ore nominali** della disciplina (`33 settimane × 4 ore`) senza separare rigidamente teoria e laboratorio. Le lezioni sono affidate alternativamente al prof. **Antonio Caristia** e all'ITP **Antonino Pirri**; se una lezione richiede più tempo del previsto, viene conclusa dal docente responsabile. Gli scostamenti vengono compensati su ore future o sulla riserva, senza passare una lezione incompleta all'altro docente.

La previsione mantiene **16 ore non vincolate a nuovi contenuti**: 4 ore per almeno un compito scritto o pratico di due ore in ciascun quadrimestre e 12 ore per recuperi, consolidamento, ulteriori verifiche, ritardi o sospensioni. Le date nella tabella dettagliata vengono inserite soltanto dopo lo svolgimento effettivo; gli eventi che non producono ore di lezione sono registrati separatamente.

### Distribuzione delle ore per UDA

| UDA | Settimane | Lezioni e Activity | Compiti | Riserva flessibile | Totale UDA | Antonio Caristia | Antonino Pirri |
|---|---:|---:|---:|---:|---:|---:|---:|
| UDA-20 — Avvio e architettura | 1 | 4 | 0 | 0 | 4 | 4 | 0 |
| UDA-21 — Web Platform, HTML, CSS e Bootstrap | 6 | 22 | 0 | 2 | 24 | 7 | 17 |
| UDA-22 — JavaScript, DOM e Browser API | 6 | 19 | 0 | 5 | 24 | 22 | 2 |
| UDA-23 — HTTP, Fetch e REST | 4 | 13 | 2 | 1 | 16 | 2 | 14 |
| UDA-24 — Node, Express, SQL, autenticazione e SSR | 7 | 26 | 0 | 2 | 28 | 14 | 14 |
| UDA-25 — Vue, TypeScript, realtime e React | 5 | 18 | 0 | 2 | 20 | 11 | 9 |
| UDA-26 — Mirror Python, testing e deploy | 4 | 14 | 2 | 0 | 16 | 6 | 10 |
| **Totale** | **33** | **116** | **4** | **12** | **132** | **66** | **66** |

Le ore nelle ultime due colonne comprendono lezioni, compiti e quote di riserva. La distribuzione per singola lezione riportata sotto assegna 58 ore di contenuto a ciascun docente; un compito da 2 ore e 6 ore di riserva completano le 66 ore individuali.

### Lezioni e Activity associate

Ogni titolo di lezione apre la dispensa corrispondente. Ogni Activity apre direttamente la consegna dello studente; quando il bundle non possiede ancora una pagina studente autonoma, il collegamento conduce al relativo `activity.json` canonico.

| UDA | Lezione | Activity associate | Ore | Docente responsabile | Date e ore svolte |
|---|---|---|---:|---|---|
| UDA-20 | [00 — Architettura didattica del corso Full Stack](content/tpsi5/00_COURSE_ARCHITECTURE.md) | — | 4 | prof. Antonio Caristia | 07/09/2026 — 2/4 ore, in corso |
| UDA-21 | [01 — Web Platform e HTML moderno](content/tpsi5/01_WEB_PLATFORM_HTML_MODERNO.md) | [A — Anatomia di un documento HTML moderno](activities/tpsi5/html_anatomy_a/student/README.md)<br>[B — Feisbuc: da div generici a HTML semantico](activities/tpsi5/feisbuc_semantic_b/student/README.md) | 10 | ITP Antonino Pirri | — |
| UDA-21 | [02 — CSS moderno, layout e responsive design](content/tpsi5/02_CSS_MODERNO_RESPONSIVE.md) | [C — Shell responsive Feisbuc](activities/tpsi5/feisbuc_responsive_c/student/README.md)<br>[D — Debug del layout responsive](activities/tpsi5/css_debug_d/student/README.md) | 6 | prof. Antonio Caristia | — |
| UDA-21 | [03 — Bootstrap: dal CSS nativo a un framework](content/tpsi5/03_BOOTSTRAP_DA_CSS_A_FRAMEWORK.md) | [E — Interfaccia Bootstrap Feisbuc](activities/tpsi5/feisbuc_bootstrap_e/student/README.md) | 6 | ITP Antonino Pirri | — |
| UDA-22 | [04 — JavaScript moderno, DOM e Browser API](content/tpsi5/04_JAVASCRIPT_DOM_BROWSER_APIS.md) | [A — Pipeline JavaScript del feed](activities/tpsi5/js_feed_pipeline_a/student/README.md)<br>[B — Refactoring dello stato di un post](activities/tpsi5/js_post_refactor_b/student/README.md)<br>[C — Feed dinamico Feisbuc](activities/tpsi5/feisbuc_dynamic_c/student/README.md)<br>[D — Debug JavaScript, DOM e storage](activities/tpsi5/js_debug_d/student/README.md) | 19 | prof. Antonio Caristia | — |
| UDA-23 | [05 — HTTP, asincronia, Fetch e REST](content/tpsi5/05_HTTP_ASYNC_FETCH_REST.md) | [A — HTTP al microscopio](activities/tpsi5/http_microscope_a/student/README.md)<br>[B — Interpretare una response asincrona](activities/tpsi5/async_response_b/student/README.md)<br>[C — Client REST Feisbuc](activities/tpsi5/feisbuc_rest_c/student/README.md)<br>[D — Debug Fetch e HTTP](activities/tpsi5/fetch_debug_d/student/README.md) | 13 | ITP Antonino Pirri | — |
| UDA-24 | [06 — Node.js ed Express 5](content/tpsi5/06_NODE_EXPRESS_BACKEND.md) | [A — Dal server nativo a Express](activities/tpsi5/node_http_express_a/student/README.md)<br>[B — Validazione di un nuovo post](activities/tpsi5/post_validation_b/student/README.md)<br>[C — API Express Feisbuc](activities/tpsi5/feisbuc_express_c/student/README.md)<br>[D — Debug della pipeline Express](activities/tpsi5/express_debug_d/student/README.md) | 7 | prof. Antonio Caristia | — |
| UDA-24 | [07 — SQL raw e persistenza SQLite](content/tpsi5/07_SQL_RAW_PERSISTENCE.md) | [A — Schema SQL dei post](activities/tpsi5/sql_posts_schema_a/student/README.md)<br>[B — DML sui post](activities/tpsi5/sql_posts_dml_b/student/README.md)<br>[C — Repository SQLite Feisbuc](activities/tpsi5/feisbuc_sql_c/student/README.md)<br>[D — Debug dello stato SQL](activities/tpsi5/sql_debug_d/student/README.md) | 7 | ITP Antonino Pirri | — |
| UDA-24 | [08 — Autenticazione, sessioni e autorizzazione](content/tpsi5/08_AUTH_SESSIONI_SICUREZZA.md) | [A — Policy delle credenziali](activities/tpsi5/auth_credential_policy_a/student/README.md)<br>[B — Autorizzazione server-side sui post](activities/tpsi5/auth_post_authorization_b/student/README.md)<br>[C — Sessioni e ownership Feisbuc](activities/tpsi5/feisbuc_auth_c/student/README.md)<br>[D — Security review e debug](activities/tpsi5/auth_debug_d/student/README.md) | 6 | prof. Antonio Caristia | — |
| UDA-24 | [09 — SSR e template Nunjucks](content/tpsi5/09_SSR_NUNJUCKS_CONFRONTO.md) | [A — View model SSR](activities/tpsi5/ssr_view_model_a/student/README.md)<br>[B — Autoescape Nunjucks](activities/tpsi5/nunjucks_autoescape_b/student/README.md)<br>[C — SSR Feisbuc](activities/tpsi5/feisbuc_ssr_c/student/README.md)<br>[D — Debug dei boundary SSR](activities/tpsi5/ssr_debug_d/student/README.md) | 6 | ITP Antonino Pirri | — |
| UDA-25 | [10 — Vue 3, componenti e reattività](content/tpsi5/10_VUE3_COMPONENTI_REATTIVITA.md) | [A — Reattività Vue](activities/tpsi5/vue_reactivity_a/student/OBSERVATIONS.md)<br>[B — Componente Vue PostCard](activities/tpsi5/vue_post_card_b/student/README.md)<br>[C — SPA Vue Feisbuc](activities/tpsi5/feisbuc_vue_c/student/README.md)<br>[D — Debug Vue](activities/tpsi5/vue_debug_d/student/DIAGNOSI.md) | 5 | prof. Antonio Caristia | — |
| UDA-25 | [11 — Vue Router e navigazione SPA](content/tpsi5/11_VUE_ROUTER_NAVIGAZIONE_SPA.md) | [A — Microscopio Vue Router](activities/tpsi5/vue_router_microscope_a/student/OBSERVATIONS.md)<br>[B — Navigation policy](activities/tpsi5/navigation_policy_b/student/README.md)<br>[C — Vue Router in Feisbuc](activities/tpsi5/feisbuc_vue_router_c/student/README.md)<br>[D — Debug Vue Router](activities/tpsi5/vue_router_debug_d/activity.json) | 4 | ITP Antonino Pirri | — |
| UDA-25 | [12 — TypeScript nei boundary frontend](content/tpsi5/12_TYPESCRIPT_CONTRATTI_FRONTEND.md) | [A — Contratti TypeScript](activities/tpsi5/typescript_contract_microscope_a/student/README.md)<br>[B — Navigation policy tipizzata](activities/tpsi5/typescript_navigation_policy_b/student/README.md)<br>[C — Boundary TypeScript Feisbuc](activities/tpsi5/feisbuc_typescript_c/student/README.md)<br>[D — Debug TypeScript](activities/tpsi5/typescript_debug_d/activity.json) | 3 | prof. Antonio Caristia | — |
| UDA-25 | [13 — WebSocket e Socket.IO](content/tpsi5/13_WEBSOCKET_SOCKETIO_REALTIME.md) | [A — Microscopio realtime](activities/tpsi5/websocket_realtime_microscope_a/student/OSSERVAZIONI.md)<br>[B — Event reducer realtime](activities/tpsi5/realtime_event_reducer_b/student/README.md)<br>[C — Socket.IO in Feisbuc](activities/tpsi5/feisbuc_realtime_c/student/README.md)<br>[D — Debug dei boundary realtime](activities/tpsi5/realtime_debug_d/student/DIAGNOSI.md) | 4 | ITP Antonino Pirri | — |
| UDA-25 | [14 — React translation lab](content/tpsi5/14_REACT_TRANSLATION_COMPARISON.md) | [A — Traduzione da Vue a React](activities/tpsi5/react_translation_microscope_a/student/MAPPING.md)<br>[B — Componente React PostCard](activities/tpsi5/react_post_card_b/student/README.md) | 2 | prof. Antonio Caristia | — |
| UDA-26 | [15 — FastAPI e OpenAPI](content/tpsi5/15_FASTAPI_OPENAPI_MIRROR.md) | [A — Microscopio FastAPI e OpenAPI](activities/tpsi5/fastapi_openapi_microscope_a/student/OBSERVATIONS.md)<br>[B — Validazione Python dei post](activities/tpsi5/fastapi_post_validation_b/student/README.md)<br>[C — Mirror FastAPI Feisbuc](activities/tpsi5/feisbuc_fastapi_mirror_c/student/README.md)<br>[D — Debug dei boundary FastAPI](activities/tpsi5/fastapi_debug_d/student/DIAGNOSI.md) | 4 | ITP Antonino Pirri | — |
| UDA-26 | [16 — SQLAlchemy e persistenza ORM](content/tpsi5/16_SQLALCHEMY_PERSISTENCE_MIRROR.md) | [A — Mapping e Session SQLAlchemy](activities/tpsi5/sqlalchemy_mapping_microscope_a/student/OBSERVATIONS.md)<br>[B — Repository SQLAlchemy](activities/tpsi5/sqlalchemy_repository_b/student/README.md)<br>[C — FastAPI con SQLAlchemy](activities/tpsi5/feisbuc_fastapi_sqlalchemy_c/student/README.md)<br>[D — Debug di Session e transazioni](activities/tpsi5/sqlalchemy_debug_d/student/DIAGNOSI.md) | 3 | prof. Antonio Caristia | — |
| UDA-26 | [17 — Testing e integration boundary](content/tpsi5/17_TESTING_INTEGRATION_BOUNDARIES.md) | [A — Microscopio dei livelli di test](activities/tpsi5/testing_boundary_microscope_a/student/TEST_MATRIX.md)<br>[B — Fixture pytest e isolamento](activities/tpsi5/pytest_fixture_boundary_b/student/README.md)<br>[C — Test d'integrazione Feisbuc](activities/tpsi5/feisbuc_testing_boundaries_c/student/README.md)<br>[D — Debug della strategia di test](activities/tpsi5/testing_debug_d/activity.json) | 4 | ITP Antonino Pirri | — |
| UDA-26 | [18 — Runtime, deploy, health e capstone](content/tpsi5/18_RUNTIME_DEPLOY_HEALTH_CAPSTONE.md) | [A — Microscopio runtime e deploy](activities/tpsi5/runtime_deploy_microscope_a/student/RUNTIME_MAP.md)<br>[B — Contratto di configurazione runtime](activities/tpsi5/runtime_config_contract_b/student/README.md)<br>[C — Health e readiness](activities/tpsi5/health_readiness_c/student/README.md)<br>[D — Debug runtime e deploy](activities/tpsi5/runtime_debug_d/activity.json)<br>[E — Evidence bundle](activities/tpsi5/evidence_bundle_e/student/README.md)<br>[F — Runtime capstone Feisbuc](activities/tpsi5/feisbuc_runtime_capstone_f/student/README.md) | 3 | prof. Antonio Caristia | — |

### Ripartizione complessiva fra i docenti

| Docente | Lezioni e Activity | Compito assegnato | Riserva flessibile | Totale annuale | Ore svolte | Ore ancora da svolgere |
|---|---:|---:|---:|---:|---:|---:|
| prof. Antonio Caristia | 58 | 2 | 6 | **66** | 2 | 64 |
| ITP Antonino Pirri | 58 | 2 | 6 | **66** | 0 | 66 |
| **Totale** | **116** | **4** | **12** | **132** | **2** | **130** |

La verifica del primo quadrimestre è affidata ad Antonio Caristia; quella del secondo quadrimestre ad Antonino Pirri. Ulteriori prove da due ore vengono assorbite dalla riserva e devono essere distribuite in coppia o compensate, così da conservare il 50% esatto del carico assegnato.

### Registro iniziale delle ore e degli imprevisti

| Data | Lezione | Docente previsto | Ore previste | Ore svolte | Esito |
|---|---|---|---:|---:|---|
| 07/09/2026 | [00 — Introduzione al corso](content/tpsi5/00_COURSE_ARCHITECTURE.md) | prof. Antonio Caristia | 2 | 2 | Svolta; lezione 00 ancora in corso. |
| 08/09/2026 | [00 — Continuazione](content/tpsi5/00_COURSE_ARCHITECTURE.md) | prof. Antonio Caristia | 1 | 0 | Annullata per rottura della conduttura dell'acqua; consumata 1 ora della riserva annuale. |

Situazione dopo l'8 settembre: **2 ore svolte**, **2 ore ancora necessarie per concludere la lezione 00** e **11 ore di riserva flessibile residue**. Le sospensioni non vengono attribuite come ore svolte al docente; il controllo del 50% riguarda il carico annuale assegnato, mentre il consuntivo effettivo resta separato.

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
- [`content/tpsi5/GUIDA_USO_MDN.md`](content/tpsi5/GUIDA_USO_MDN.md) — tutorial trasversale per orientarsi in MDN, leggere le reference e verificare ciò che si apprende;
- [`content/tpsi5/STYLE_GUIDE.md`](content/tpsi5/STYLE_GUIDE.md) — standard HTML/Markdown, callout, icone e pannelli espandibili delle dispense;
- [`doc/course_designs/tpsi_quinto_2026_2027.json`](doc/course_designs/tpsi_quinto_2026_2027.json) — Course Design di 33 settimane;
- [`doc/OPEN_DECISIONS.md`](doc/OPEN_DECISIONS.md) — decisioni D1–D5 congelate;
- [`doc/CURRICULUM_FREEZE_2026_2027.md`](doc/CURRICULUM_FREEZE_2026_2027.md) — baseline, confini e policy post-freeze;
- [`doc/DELIVERY_CHANGELOG.md`](doc/DELIVERY_CHANGELOG.md) — correzioni e revisioni classroom-facing durante l'anno;
- [`doc/LEGACY_REUSE_AUDIT.md`](doc/LEGACY_REUSE_AUDIT.md) — provenance e audit dei materiali legacy;
- [`teacher/`](teacher/) — guida docente;
- [`student/`](student/) — guida operativa studenti;
- [`slides/tpsi5/`](slides/tpsi5/) — slide Markdown per la conduzione delle lezioni;
- [`activities/tpsi5/`](activities/tpsi5/) — Activity e reference solution;
- [`.github/workflows/quality.yml`](.github/workflows/quality.yml) — Quality del consumer reale.

## Confini deliberati

Non fanno parte del core 2026/27: ORM Node, Pinia senza requisito concreto, TypeScript avanzato/backend TypeScript, un secondo framework frontend core, duplicazione auth/session/realtime nel mirror Python, Alembic/PostgreSQL/async ORM, Kubernetes/cloud/scaling e CI/CD avanzata.

Il futuro corso SQL separato potrà approfondire e riusare milestone condivise, ma **non è un prerequisito bloccante** per questa release: TPSI5 contiene il minimo SQL raw necessario prima delle astrazioni.

Le capability di piattaforma #729 (browser/HTML grader) e #731 (TypeScript Activity runner) restano follow-up indipendenti e non bloccano il curriculum freeze.

Umbrella di progetto: `TheBitPoets/2cornot2c#728`. Standard authoring cross-course accettato: `TheBitPoets/2cornot2c#723`. Delivery standard cross-course in rollout: `TheBitPoets/2cornot2c#737`.

## Rigenerare gli starter Feisbuc avanzati

Le milestone 8–12 distribuiscono uno **starter completo e autonomo**. Ogni starter contiene la baseline funzionante richiesta dalla milestone precedente e soltanto i TODO del nuovo argomento: lo studente non deve copiare solution, sovrapporre cartelle o integrare manualmente la build Vue.

I file specifici della nuova milestone vivono nelle cartelle interne di authoring `starter-overlay/`, che non vengono consegnate agli studenti; gli starter completi sotto `starter/` sono generati in modo deterministico. Dopo avere modificato una baseline o uno starter overlay, eseguire dalla root del repository:

```bash
python3 scripts/build_feisbuc_starters.py
python3 scripts/build_feisbuc_starters.py --check
```

Il primo comando ricostruisce gli starter completi delle milestone 8–12. Il secondo non modifica file e verifica che le copie versionate siano aggiornate. Per le milestone Vue 9–12, dalla root dello starter bastano `npm install`, i comandi `npm run dev:backend` e `npm run dev:frontend` durante lo sviluppo, oppure `npm run build` e `npm start` per la versione integrata. La build copia automaticamente gli asset in `backend/public/vue/`.

## Generare manualmente le slide

La build converte esclusivamente le presentazioni Marp presenti in `slides/tpsi5/`. I file in `content/tpsi5/` sono le lezioni/dispense canoniche e non vengono trasformati in HTML o PDF da questo processo.

I diagrammi condividono il sistema grafico documentato in [`assets/tpsi5/visual-system/`](assets/tpsi5/visual-system/). Quando viene modificato un componente o una scena, rigenerare prima gli SVG autonomi:

```bash
python3 scripts/build_course_diagrams.py
python3 scripts/build_course_diagrams.py --check
```

Il primo comando rigenera cataloghi e diagrammi; il secondo verifica che gli SVG versionati coincidano con le scene e i componenti sorgente.

### Prerequisiti

- Python 3.11 o successivo;
- Node.js 18 o successivo, con `npx` disponibile;
- Google Chrome o Chromium per generare PDF e PowerPoint.

I comandi devono essere eseguiti dalla directory principale del repository. Lo script usa automaticamente `@marp-team/marp-cli` nella versione fissata dal progetto; al primo utilizzo `npx` potrebbe doverla scaricare.

### Controllare i sorgenti senza generare file

```bash
python3 scripts/build_slides.py --check-only
```

Controlla che siano presenti l'overview e i 19 deck modulari, che il front matter Marp sia valido e che ogni modulo sia collegato al contenuto canonico. Non genera slide e non richiede Chrome.

### Generare le slide HTML

```bash
python3 scripts/build_slides.py --formats html
```

Genera presentazioni navigabili nel browser. Questo formato è utile per una verifica rapida e non richiede Chrome.

### Generare le slide PDF

```bash
python3 scripts/build_slides.py --formats pdf --browser chrome
```

Genera un PDF per l'overview e per ciascun modulo. Richiede Chrome o Chromium perché Marp deve renderizzare le pagine.

### Generare le slide PowerPoint

```bash
python3 scripts/build_slides.py --formats pptx --browser chrome
```

Genera un file `.pptx` per l'overview e per ciascun modulo. Anche questa conversione richiede Chrome o Chromium.

### Generare tutti i formati

```bash
python3 scripts/build_slides.py --formats html,pdf,pptx --browser chrome
```

Esegue la validazione e genera tutti i formati supportati. HTML e PDF possono essere elaborati in parallelo; la generazione PowerPoint è intenzionalmente seriale per evitare timeout del browser.

### Cartella di output

Per impostazione predefinita i file vengono scritti in:

```text
build/tpsi5-slides/
├── html/
├── pdf/
├── pptx/
├── MANIFEST.json
└── SHA256SUMS.txt
```

`MANIFEST.json` registra sorgenti, formati, dimensioni e hash degli artifact. `SHA256SUMS.txt` permette di verificarne l'integrità.

Per usare una destinazione differente:

```bash
python3 scripts/build_slides.py --formats html --output /percorso/destinazione
```

La cartella di output viene rigenerata a ogni build. Gli artifact sotto `build/tpsi5-slides/` sono derivati e ignorati da Git: eventuali correzioni devono essere applicate ai file Markdown o agli asset sorgente, non agli HTML, PDF o PPTX generati.

## Generare manualmente le immagini del corso

Le immagini architetturali del corso non sono disegni isolati: vengono costruite con il **TPSI Visual System**, un pack di componenti SVG condivisi. Questo permette di rappresentare laptop, browser, rete, server, API, database e tecnologie sempre con lo stesso stile.

Il sistema grafico è composto da questi elementi:

- [`assets/tpsi5/visual-system/README.md`](assets/tpsi5/visual-system/README.md) — **guida del Visual System**. Documenta principi grafici, significato dei colori, grammatica delle frecce, dimensioni del canvas, regole di accessibilità e procedura per aggiungere nuovi componenti.
- [`assets/tpsi5/visual-system/components.svg`](assets/tpsi5/visual-system/components.svg) — **libreria dei 30 componenti SVG riutilizzabili**. Contiene le definizioni vettoriali di laptop, browser, smartphone, utente, server, rete, cloud, database, API, servizi, repository, route, documenti, sicurezza, test, artifact e badge tecnologici. È un file sorgente: i simboli vengono richiamati dalle scene tramite il loro identificatore `tpsi-*`.
- [`assets/tpsi5/visual-system/tokens.json`](assets/tpsi5/visual-system/tokens.json) — **token grafici e colori semantici**. Definisce canvas, griglia, margini, font, dimensioni, raggi, spessori e colori canonici. Per esempio, blu indica il client, verde il backend, viola il realtime e indaco la persistenza.
- [`assets/tpsi5/visual-system/catalog/component-catalog.svg`](assets/tpsi5/visual-system/catalog/component-catalog.svg) — **catalogo visuale dei componenti**. È la tavola da consultare per vedere rapidamente gli oggetti generici disponibili. È un file generato e non deve essere modificato direttamente.
- [`assets/tpsi5/visual-system/catalog/technology-badges.svg`](assets/tpsi5/visual-system/catalog/technology-badges.svg) — **catalogo visuale delle tecnologie**. Mostra i badge didattici disponibili per HTML, CSS, JavaScript, Node.js, Express, SQLite, Vue, React, TypeScript e Python. Anche questo file è generato.
- [`assets/tpsi5/visual-system/scenes/`](assets/tpsi5/visual-system/scenes) — **scene sorgente componibili**. Ogni file `.scene.svg` descrive una figura completa: posiziona i componenti, aggiunge testi e connettori e indica il percorso dello SVG finale. Questi sono i file da modificare quando cambia la composizione di un'immagine.
- [`scripts/build_course_diagrams.py`](scripts/build_course_diagrams.py) — **generatore deterministico**. Legge la libreria e le scene, incorpora le definizioni condivise e produce SVG finali autonomi. A parità di sorgenti genera sempre lo stesso risultato e controlla che le scene non richiamino componenti inesistenti o destinazioni esterne all'area degli asset TPSI5.

Le due immagini della lezione 00 sono già costruite realmente con questo sistema:

- [`assets/tpsi5/00-client-server-roles.svg`](assets/tpsi5/00-client-server-roles.svg);
- [`assets/tpsi5/00-full-stack-architecture.svg`](assets/tpsi5/00-full-stack-architecture.svg).

Laptop e browser, per esempio, sono due componenti distinti: la scena colloca il browser nello spazio dello schermo del laptop. Lo stesso laptop potrà quindi contenere in futuro un editor, un terminale, DevTools o l'interfaccia di Feisbuc senza essere ridisegnato.

### Rigenerare le immagini

Dalla directory principale del repository eseguire:

```bash
python3 scripts/build_course_diagrams.py
```

Il comando legge `components.svg` e tutti i file `scenes/*.scene.svg`, quindi rigenera:

- i cataloghi del Visual System;
- le immagini autonome utilizzate nelle dispense;
- le immagini autonome utilizzate dalle slide Marp.

Gli SVG finali incorporano le definizioni dei componenti e non dipendono da CDN, connessioni Internet o riferimenti esterni durante la proiezione e l'esportazione.

### Controllare che le immagini siano aggiornate

```bash
python3 scripts/build_course_diagrams.py --check
```

Questa modalità non modifica file. Rigenera il risultato in memoria e lo confronta con gli SVG presenti nel repository. Il controllo fallisce se un'immagine manca o non corrisponde più ai componenti e alle scene sorgente.

### Flusso di lavoro consigliato

1. modificare `components.svg` se cambia un oggetto condiviso, per esempio l'icona della rete;
2. modificare o aggiungere un file `.scene.svg` se cambia la composizione di una figura;
3. eseguire `python3 scripts/build_course_diagrams.py`;
4. controllare visivamente gli SVG generati;
5. eseguire `python3 scripts/build_course_diagrams.py --check`;
6. eseguire `python3 scripts/build_slides.py --check-only` prima di generare HTML, PDF o PPTX.

Non modificare direttamente i cataloghi o gli SVG finali della lezione: alla rigenerazione verrebbero sovrascritti. Le modifiche permanenti devono essere applicate alla libreria dei componenti o alle scene sorgente.
