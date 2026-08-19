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
4. `03_BOOTSTRAP_DA_CSS_A_FRAMEWORK.md` — Bootstrap come astrazione sopra CSS nativo, grid/utilities/components, trade-off e Feisbuc milestone 2.

## Activity disponibili

- A — anatomia documento HTML;
- B — Feisbuc semantic skeleton;
- C — Feisbuc responsive shell;
- D — diagnosi di un layout CSS rotto;
- E — Feisbuc Bootstrap UI refactor con mapping CSS nativo -> framework.

## Stato

Versione authoring `0.4.1`, ancora **draft**.

Le fondazioni HTML/CSS/Bootstrap coprono ora Activity A-E e soddisfano il consumer gate usato per validare il Content Pack Standard v1. Questo non congela il corso: framework frontend, ORM Node e profondità TypeScript restano decisioni da prendere e il prossimo blocco e UDA 22 — JavaScript moderno, DOM e Browser APIs.
