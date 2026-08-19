# Audit iniziale delle risorse legacy

Stato: draft. Gli SHA indicati sono snapshot di partenza, non branch mobili.

## `TheBitPoets/html_css_summary`

Pinned: `d71da420f1aa2ea39b61356e4f9900c6371e7a42`.

**Decisione iniziale: REUSE + MAJOR UPDATE.**

Da conservare: progressione molto semplice, esempi piccoli, box model, block/inline, collegamenti playground.

Da aggiornare: scheletro HTML moderno (`DOCTYPE`, `lang`, charset, viewport), semantica, form, accessibilità, cascade/specificità, Flexbox, Grid, media query, custom properties e responsive design. Gli esempi vanno revisionati: per esempio la sezione dedicata a `<ul>` contiene attualmente un esempio con `<ol>`. JSFiddle resta materiale legacy utile, ma i nuovi micro-esempi dovrebbero privilegiare MDN Playground quando possibile.

### Decisioni per frammento — primo modulo HTML

| Frammento legacy | Decisione | Destinazione / motivazione |
| --- | --- | --- |
| `Scheletro html` | **rewrite** | sostituito da `01_WEB_PLATFORM_HTML_MODERNO.md`: doctype moderno, `lang`, UTF-8, viewport, `title`, distinzione `head/header` |
| `Tag p` | **reuse concept / new example** | il concetto resta, ma viene spiegato come semantica del testo e non come effetto grafico |
| `Tag ol` | **reuse concept / new example** | mantenere liste ordinate con esempi originali |
| `Tag ul` | **rewrite** | correggere l'esempio legacy che usa `ol`; nuovo esempio originale nel corso |
| `Tag a` | **reuse concept / update** | mantenere il collegamento ipertestuale e aggiungere contesto semantico/accessibilità quando serve |
| `CSS sintassi` | **migrated/rewrite** | ora coperto da `02_CSS_MODERNO_RESPONSIVE.md` con terminologia selettore/proprietà/valore e workflow MDN |
| `Box Model` | **migrated/major update** | ora integrato con `box-sizing: border-box`, DevTools e debugging reale |
| `Block/Inline` | **rewrite** | ricollocato nel normal flow e nei concetti di display, senza usarlo come modello centrale del layout moderno |
| Padding/Margin/Border | **reuse concepts / new examples** | conservati dentro il box model con esempi originali e Activity nuove |
| JSFiddle links | **keep as legacy evidence** | non diventano dipendenza obbligatoria; MDN Playground/browser locale sono preferiti nei nuovi micro-lab |

### Output del primo incremento

- `content/tpsi5/01_WEB_PLATFORM_HTML_MODERNO.md`;
- Activity A `tpsi5-activity-a-html-anatomy-001`;
- Activity B `tpsi5-activity-b-feisbuc-semantic-001`;
- Feisbuc milestone `feisbuc-00-semantic-skeleton`.

### Output del secondo incremento CSS

- `content/tpsi5/02_CSS_MODERNO_RESPONSIVE.md`;
- cascade, specificità, inheritance e box model riscritti con approccio moderno;
- Flexbox e Grid aggiunti come strumenti principali di layout;
- responsive design e media query introdotti con strategia mobile-first;
- custom properties introdotte come fondamento di manutenzione;
- Activity C `tpsi5-activity-c-feisbuc-responsive-layout-001`;
- Activity D `tpsi5-activity-d-debug-responsive-css-001`;
- Feisbuc milestone `feisbuc-01-responsive-shell`.

Il nuovo testo non copia la spiegazione legacy: conserva i concetti utili, riscrive esempi e struttura e collega esplicitamente MDN come riferimento professionale. *CSS in Depth, Second Edition* resta teacher-reference licensed e non viene riprodotto.

## `TheBitPoets/labs_summary`

Pinned: `36a909f00c9478983a8d1b950440e2abc28b8a55`.

**Decisione iniziale: REUSE PROGRESSION + REBUILD ACTIVITIES.**

La sequenza storica è preziosa: statico → storage/JS → Express/fetch → form/POST → parametri HTTP → SQLite → register/login/CRUD → template → Socket.IO.

Da cambiare: rendere HTTP esplicito prima di Express/fetch; trasformare i lab in Activity A–F; rivedere dipendenze Node/DB; introdurre password hashing, session/authn/authz e sicurezza; usare Nunjucks come confronto SSR anziché architettura finale; correggere la descrizione di Socket.IO, che non va presentato semplicemente come wrapper WebSocket.

## `TheBitPoets/feisbuc`

Pinned: `086995ece4260a3408740b94cfe2701ce24f8b57`.

**Decisione iniziale: KEEP AS LONGITUDINAL CAPSTONE.**

Il progetto ha valore perché cresce insieme al corso. Il README e gli esempi sono sorgente didattica; i file HTML/CSS/JS sono invece asset/progetto e non vengono ingeriti come Markdown dalla Course Board.

Da modernizzare: layout basati su float → Flexbox/Grid; semantica/accessibilità; gestione degli asset esterni; separazione progressiva dei moduli JS; REST/backend/DB/auth; framework frontend; realtime; test e deploy.

### Decisioni applicate

**Milestone 0** non copia il vecchio `home.html`: ricostruisce uno scheletro Feisbuc minimale e richiede allo studente di passare da contenitori generici a `header`, `nav`, `main`, `section`, `article` e `footer`.

**Milestone 1** sostituisce il modello legacy a colonne basato su `float` con:

```text
Grid    → macro-layout profilo/feed/tendenze
Flexbox → navigazione e azioni del post
```

Il layout di base è mobile-first e la versione ampia usa colonne Grid flessibili. Il vecchio uso di float rimane utile come evidenza storica da confrontare, non come soluzione canonica del nuovo corso.

## Principio di migrazione

Nessun repository legacy viene copiato integralmente nel nuovo corso. Ogni frammento deve ricevere una decisione esplicita `reuse`, `rewrite`, `replace` o `retire`, conservando provenance e snapshot originario.
