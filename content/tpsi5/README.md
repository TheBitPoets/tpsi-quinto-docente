# TPSI quinto anno — Content Pack

Questo package contiene i contenuti originali del corso **TPSI quinto anno — Full Stack Web Developer**, a.s. 2026/2027.

Contratto di authoring: `thebitlab.content-pack.v1`.

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
3. `02_CSS_MODERNO_RESPONSIVE.md` — cascade, specificità, box model, Flexbox, Grid, responsive design, custom properties e metodo di debugging; Feisbuc milestone 1.

## Activity disponibili

- A — anatomia documento HTML;
- B — Feisbuc semantic skeleton;
- C — Feisbuc responsive shell;
- D — diagnosi di un layout CSS rotto.

## Stato

Versione authoring `0.3.0`, ancora **draft**.

Le fondazioni HTML/CSS coprono ora Activity A-D. Framework frontend, ORM Node e profondità TypeScript restano decisioni da congelare. Il prossimo incremento di UDA 21 completera le fondazioni frontend con Bootstrap **dopo** CSS nativo e dovra produrre almeno una Activity E/F per chiudere il gate di adozione del Content Pack v1.
