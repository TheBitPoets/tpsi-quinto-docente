# TPSI quinto anno — Content Pack

Questo package contiene i contenuti originali del corso **TPSI quinto anno — Full Stack Web Developer**, a.s. 2026/2027.

Contratto di authoring: `thebitlab.content-pack.v1`.

Il consumer e pinned alla revisione **Accettata** del contratto in `TheBitPoets/2cornot2c`: `5472eef86568a4e7ce59ad34ba937220df27efd7`.

## Principi

- partire dalla Web Platform prima dei framework;
- rendere HTTP esplicito prima di `fetch`/Express;
- usare SQL raw prima dell'ORM;
- usare Node.js + Express come backend principale, ma soltanto dopo avere studiato il protocollo;
- mantenere Python/FastAPI come mirror track mirato;
- usare Feisbuc come progetto longitudinale;
- usare MDN, specifiche e documentazioni ufficiali come reference professionali;
- usare Manning/Pluralsight come teacher-reference licensed senza ingestione;
- mantenere Activity A–F e separazione studente/docente/grading.

## Contenuti disponibili

1. `00_COURSE_ARCHITECTURE.md` — architettura del percorso e metodo;
2. `01_WEB_PLATFORM_HTML_MODERNO.md` — HTML moderno; Feisbuc milestone 0;
3. `02_CSS_MODERNO_RESPONSIVE.md` — CSS/Flexbox/Grid/responsive; milestone 1;
4. `03_BOOTSTRAP_DA_CSS_A_FRAMEWORK.md` — Bootstrap come astrazione sopra CSS; milestone 2;
5. `04_JAVASCRIPT_DOM_BROWSER_APIS.md` — JavaScript, DOM, eventi, modules, Web Storage; milestone 3;
6. `05_HTTP_ASYNC_FETCH_REST.md` — HTTP semantics, Promise/async-await, Fetch/Response, REST, same-origin/CORS e network debugging; milestone 4.

## Feisbuc oggi

```text
milestone 0  semantic HTML
milestone 1  responsive native CSS
milestone 2  Bootstrap UI
milestone 3  dynamic local JS + localStorage
milestone 4  HTTP REST API client
```

La milestone 4 rende visibile la sostituzione:

```text
localStorage
     ↓
api.js -> fetch -> HTTP -> server fixture
```

Il server UDA 23 usa `node:http` ed e deliberatamente trattato come fixture/black box. Node runtime, native HTTP server ed Express diventano oggetto di studio in UDA 24.

## Activity UDA 22

- `tpsi5-activity-a-js-feed-pipeline-001` — **autograded JavaScript**;
- `tpsi5-activity-b-js-post-refactor-001` — **autograded JavaScript**;
- `tpsi5-activity-c-feisbuc-dynamic-feed-001` — browser/manuale;
- `tpsi5-activity-d-debug-feisbuc-js-001` — browser/manuale.

## Activity UDA 23

- `tpsi5-activity-a-http-microscope-001` — request/response con `curl -i` + Network panel;
- `tpsi5-activity-b-async-response-policy-001` — status/ok/Content-Type + Promise/await, **autograded JavaScript**;
- `tpsi5-activity-c-feisbuc-rest-client-001` — Feisbuc milestone 4, GET/POST/PATCH via HTTP;
- `tpsi5-activity-d-debug-fetch-http-001` — debug 404 vs network, serialization/Content-Type e 204.

## Stato

Versione authoring **`0.6.0`**, ancora `draft`.

Il Content Pack Standard v1 resta congelato; il curriculum continua a evolvere. Framework frontend, ORM Node e profondita TypeScript sono ancora decisioni aperte. Il prossimo blocco e UDA 24: **Node.js, Express, persistenza, auth e SSR**.
