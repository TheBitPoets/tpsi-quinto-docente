# TPSI quinto anno — Content Pack

Questo package contiene i contenuti originali del corso **TPSI quinto anno — Full Stack Web Developer**, a.s. 2026/2027.

Contratto di authoring: `thebitlab.content-pack.v1`.

Il consumer e pinned alla revisione **Accettata** del contratto in `TheBitPoets/2cornot2c`: `5472eef86568a4e7ce59ad34ba937220df27efd7`.

## Principi

- partire dalla Web Platform prima dei framework;
- rendere HTTP un argomento esplicito e non un dettaglio nascosto di `fetch`/Express;
- usare SQL raw prima dell'ORM e mantenere visibile il mapping SQL ↔ ORM;
- usare Node.js + Express come backend principale;
- mantenere Python/FastAPI come mirror track mirato, non come duplicazione integrale;
- usare Feisbuc come progetto longitudinale;
- usare MDN e le documentazioni ufficiali per insegnare a leggere la documentazione professionale;
- usare Manning/Pluralsight come riferimenti docente licensed, senza copiarne o ingerirne automaticamente i contenuti;
- mantenere Activity e laboratori nella tassonomia TheBitLab A–F.

## Contenuti disponibili

1. `00_COURSE_ARCHITECTURE.md` — architettura del percorso Full Stack e metodo;
2. `01_WEB_PLATFORM_HTML_MODERNO.md` — HTML come struttura/semantica, documento moderno, metadata, MDN/DevTools e Feisbuc milestone 0;
3. `02_CSS_MODERNO_RESPONSIVE.md` — cascade, specificità, box model, Flexbox, Grid, responsive design, custom properties e metodo di debugging; Feisbuc milestone 1;
4. `03_BOOTSTRAP_DA_CSS_A_FRAMEWORK.md` — Bootstrap come astrazione sopra CSS nativo, grid/utilities/components, trade-off e Feisbuc milestone 2;
5. `04_JAVASCRIPT_DOM_BROWSER_APIS.md` — JavaScript moderno, array/object/functions, ES modules, DOM, form/eventi, event delegation, state/render, Web Storage e debugging; Feisbuc milestone 3.

## Activity disponibili

UDA 21 porta dalla struttura HTML alla UI responsive/Bootstrap con Activity A-E. UDA 22 aggiunge:

- `tpsi5-activity-a-js-feed-pipeline-001` — pipeline `filter/map`, **autograded JavaScript**;
- `tpsi5-activity-b-js-post-refactor-001` — state update `map/spread`, **autograded JavaScript**;
- `tpsi5-activity-c-feisbuc-dynamic-feed-001` — Feisbuc milestone 3 con DOM/event delegation/localStorage;
- `tpsi5-activity-d-debug-feisbuc-js-001` — debug browser basato su bug e pattern del Feisbuc legacy.

## Confine UDA 22 / UDA 23

UDA 22 studia il comportamento client senza rete. `Promise`, `async`/`await` e `fetch` sono intenzionalmente rinviati a UDA 23, dove vengono introdotti insieme a HTTP e REST. La milestone 3 usa quindi `localStorage` come persistenza locale temporanea: il passaggio successivo renderà visibile la sostituzione `storage locale -> API HTTP`.

## Stato

Versione authoring `0.5.0`, ancora **draft**.

Il Content Pack Standard v1 resta congelato; il corso no. Framework frontend, ORM Node e profondità TypeScript rimangono decisioni da prendere. Il prossimo blocco previsto è UDA 23 — **HTTP, asincronia, Fetch e REST**.
