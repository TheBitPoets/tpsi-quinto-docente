# Slide TPSI quinto anno — 2026/27

Questa directory contiene le slide Markdown docente derivate dal Content Pack **1.0.0 / approved**.

- Deck overview del corso: [`COURSE_SLIDES.md`](COURSE_SLIDES.md)
- Deck modulari completi: [`modules/`](modules/)
- Formato: Markdown compatibile con Marp (`---` separa le slide)
- Uso previsto: proiezione, spiegazione, checkpoint, handoff al laboratorio, conversione PDF/PPTX/HTML
- Stato: materiale di delivery docente; può migliorare durante l'anno senza cambiare silenziosamente il curriculum

## Regola di authoring

Il deck overview resta una mappa rapida. I deck modulari sono la **narrazione da usare in classe** e contengono richiamo, obiettivi, modello mentale, esempi progressivi, errori tipici, checkpoint, collegamento Feisbuc, handoff al lab e recap.

Quando una slide viene corretta o chiarita durante l'anno, registrare la modifica in [`../../doc/DELIVERY_CHANGELOG.md`](../../doc/DELIVERY_CHANGELOG.md).

## Indice slide

| Modulo | UDA | Deck da lezione | Overview | Lezione canonica |
|---:|---|---|---|---|
| 00 | UDA-20 | [Architettura del corso](modules/00_COURSE_ARCHITECTURE.md) | [overview](COURSE_SLIDES.md#slides-00) | [lesson](../../content/tpsi5/00_COURSE_ARCHITECTURE.md) |
| 01 | UDA-21 | [Web Platform e HTML moderno](modules/01_WEB_PLATFORM_HTML_MODERNO.md) | [overview](COURSE_SLIDES.md#slides-01) | [lesson](../../content/tpsi5/01_WEB_PLATFORM_HTML_MODERNO.md) |
| 02 | UDA-21 | [CSS moderno e responsive](modules/02_CSS_MODERNO_RESPONSIVE.md) | [overview](COURSE_SLIDES.md#slides-02) | [lesson](../../content/tpsi5/02_CSS_MODERNO_RESPONSIVE.md) |
| 03 | UDA-21 | [Bootstrap: da CSS a framework](modules/03_BOOTSTRAP_DA_CSS_A_FRAMEWORK.md) | [overview](COURSE_SLIDES.md#slides-03) | [lesson](../../content/tpsi5/03_BOOTSTRAP_DA_CSS_A_FRAMEWORK.md) |
| 04 | UDA-22 | [JavaScript, DOM e Browser APIs](modules/04_JAVASCRIPT_DOM_BROWSER_APIS.md) | [overview](COURSE_SLIDES.md#slides-04) | [lesson](../../content/tpsi5/04_JAVASCRIPT_DOM_BROWSER_APIS.md) |
| 05 | UDA-23 | [HTTP, async, Fetch e REST](modules/05_HTTP_ASYNC_FETCH_REST.md) | [overview](COURSE_SLIDES.md#slides-05) | [lesson](../../content/tpsi5/05_HTTP_ASYNC_FETCH_REST.md) |
| 06 | UDA-24 | [Node.js ed Express 5](modules/06_NODE_EXPRESS_BACKEND.md) | [overview](COURSE_SLIDES.md#slides-06) | [lesson](../../content/tpsi5/06_NODE_EXPRESS_BACKEND.md) |
| 07 | UDA-24 | [SQL raw e persistenza](modules/07_SQL_RAW_PERSISTENCE.md) | [overview](COURSE_SLIDES.md#slides-07) | [lesson](../../content/tpsi5/07_SQL_RAW_PERSISTENCE.md) |
| 08 | UDA-24 | [Auth, sessioni e sicurezza](modules/08_AUTH_SESSIONI_SICUREZZA.md) | [overview](COURSE_SLIDES.md#slides-08) | [lesson](../../content/tpsi5/08_AUTH_SESSIONI_SICUREZZA.md) |
| 09 | UDA-24 | [SSR e Nunjucks](modules/09_SSR_NUNJUCKS_CONFRONTO.md) | [overview](COURSE_SLIDES.md#slides-09) | [lesson](../../content/tpsi5/09_SSR_NUNJUCKS_CONFRONTO.md) |
| 10 | UDA-25 | [Vue 3: reattività e componenti](modules/10_VUE3_COMPONENTI_REATTIVITA.md) | [overview](COURSE_SLIDES.md#slides-10) | [lesson](../../content/tpsi5/10_VUE3_COMPONENTI_REATTIVITA.md) |
| 11 | UDA-25 | [Vue Router](modules/11_VUE_ROUTER_NAVIGAZIONE_SPA.md) | [overview](COURSE_SLIDES.md#slides-11) | [lesson](../../content/tpsi5/11_VUE_ROUTER_NAVIGAZIONE_SPA.md) |
| 12 | UDA-25 | [TypeScript mirato](modules/12_TYPESCRIPT_CONTRATTI_FRONTEND.md) | [overview](COURSE_SLIDES.md#slides-12) | [lesson](../../content/tpsi5/12_TYPESCRIPT_CONTRATTI_FRONTEND.md) |
| 13 | UDA-25 | [Socket.IO realtime](modules/13_WEBSOCKET_SOCKETIO_REALTIME.md) | [overview](COURSE_SLIDES.md#slides-13) | [lesson](../../content/tpsi5/13_WEBSOCKET_SOCKETIO_REALTIME.md) |
| 14 | UDA-25 | [React translation lab](modules/14_REACT_TRANSLATION_COMPARISON.md) | [overview](COURSE_SLIDES.md#slides-14) | [lesson](../../content/tpsi5/14_REACT_TRANSLATION_COMPARISON.md) |
| 15 | UDA-26 | [FastAPI/OpenAPI mirror](modules/15_FASTAPI_OPENAPI_MIRROR.md) | [overview](COURSE_SLIDES.md#slides-15) | [lesson](../../content/tpsi5/15_FASTAPI_OPENAPI_MIRROR.md) |
| 16 | UDA-26 | [SQLAlchemy persistence](modules/16_SQLALCHEMY_PERSISTENCE_MIRROR.md) | [overview](COURSE_SLIDES.md#slides-16) | [lesson](../../content/tpsi5/16_SQLALCHEMY_PERSISTENCE_MIRROR.md) |
| 17 | UDA-26 | [Testing boundaries](modules/17_TESTING_INTEGRATION_BOUNDARIES.md) | [overview](COURSE_SLIDES.md#slides-17) | [lesson](../../content/tpsi5/17_TESTING_INTEGRATION_BOUNDARIES.md) |
| 18 | UDA-26 | [Runtime/deploy/capstone](modules/18_RUNTIME_DEPLOY_HEALTH_CAPSTONE.md) | [overview](COURSE_SLIDES.md#slides-18) | [lesson](../../content/tpsi5/18_RUNTIME_DEPLOY_HEALTH_CAPSTONE.md) |

## Produzione completata

- **Batch A — 00–05:** foundations + HTTP — completato.
- **Batch B — 06–09:** backend, SQL, auth, SSR — completato.
- **Batch C — 10–14:** Vue, routing, TypeScript, realtime, React comparison — completato.
- **Batch D — 15–18:** FastAPI mirror, SQLAlchemy, testing, runtime/deploy — completato.

Ogni deck resta indipendente così da poter essere corretto e migliorato durante l'anno senza rigenerare un monolite.