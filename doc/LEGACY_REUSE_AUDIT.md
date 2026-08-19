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

### Decisione UDA 22

La progressione `lab2`/`lab3`/`lab4` viene riutilizzata come **ordine concettuale**, non come importazione dei repository esterni:

```text
JavaScript language
  -> DOM/events
  -> Web Storage
  -> mini-app/browser
```

La parte async del vecchio `lab3` viene separata:

- callback come concetto di funzione/evento: **UDA 22**;
- Promise, `async`/`await` e `fetch`: **UDA 23**, insieme a HTTP e REST.

Questo evita di presentare asincronia e rete come sintassi isolate.

## `kinderp/lab3`

Snapshot auditato: `0deae0eb606bc9c2849ba271bdf03c128910f1ac`.

**Decisione: TEACHER-REFERENCE + SELECTIVE REWRITE.**

Il repository contiene un buon inventario di concetti JavaScript (variabili/tipi, controllo di flusso, array/loop, funzioni, async/errori, moduli), ma non viene promosso a sorgente canonica senza revisione.

| Area legacy | Decisione | Motivo / destinazione |
| --- | --- | --- |
| `let` / `const` / `var` | **reuse concept / rewrite example** | `const` come default e `let` per riassegnazione; l'assegnazione successiva a una `const` diventa esperimento controllato, non codice canonico |
| primitive / object / array | **reuse concepts / new Feisbuc data** | esempi generici sostituiti da post, likes, tag e stato della UI |
| array mutation (`push`, `splice`...) | **reuse + contextualize** | mantenere la distinzione fra operazioni mutanti e trasformazioni che producono nuove collezioni |
| `map` / `filter` / `find` / `some` / `every` | **add/expand** | diventano parte del core UDA 22 e alimentano Activity A/B |
| funzioni / callback / arrow | **reuse concept / rewrite examples** | conservare funzioni come valori e callback; riscrivere esempi eliminando rumore/dead code e collegandoli a array/events |
| error handling | **reuse selectively** | `try/catch` usato per recovery motivato (es. JSON storage), non per nascondere errori |
| callback async / Promise / async-await | **defer to UDA 23** | studiarli insieme a HTTP/fetch per dare un motivo concreto all'asincronia |
| CommonJS | **defer to Node/backend** | e un modello dell'ecosistema Node, non il primo module system del browser |
| ES module Node + filesystem | **replace for UDA 22** | l'esempio legacy e Node-specifico e contiene riferimenti incompleti; il browser parte da `type=module`, `import`/`export` e moduli locali |
| advanced internals/classes/metaprogramming | **defer/advanced** | entrano solo se richiesti dal core o nel futuro track advanced/senior |

### Output UDA 22

- `content/tpsi5/04_JAVASCRIPT_DOM_BROWSER_APIS.md`;
- Activity A `tpsi5-activity-a-js-feed-pipeline-001` — JavaScript puro autograded;
- Activity B `tpsi5-activity-b-js-post-refactor-001` — state update autograded;
- Activity C `tpsi5-activity-c-feisbuc-dynamic-feed-001` — DOM/event delegation/localStorage;
- Activity D `tpsi5-activity-d-debug-feisbuc-js-001` — diagnosi browser;
- Feisbuc milestone `feisbuc-03-dynamic-local-feed`.

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

**Milestone 2** rifattorizza la UI con Bootstrap soltanto dopo avere costruito il layout nativo. `MAPPING.md` obbliga a collegare ogni astrazione del framework ai concetti CSS sottostanti.

### Audit JavaScript legacy applicato in UDA 22

`add_post.js` e `like_button_pressed.js` contengono intuizioni didattiche preziose ma anche debiti da rendere espliciti:

| Pattern legacy | Decisione |
| --- | --- |
| `DOMContentLoaded` + listener | **reuse concept**, poi confrontare con `type=module` e caricamento differito |
| `event.preventDefault()` con parametro `e` | **turn into debug case** nell'Activity D |
| creazione DOM con `createElement`/`appendChild` | **reuse concept / modernize** con semantica, `textContent`, `append`, funzioni di render |
| `counter` globale + id `like_button_N` | **replace** con identita del dato (`post.id`) e `data-post-id`/`data-action` |
| listener individuali sui like iniziali | **retire as final solution**; resta utile come step del problema |
| event delegation sul `.feed` | **preserve and deepen**: bubbling, `target/currentTarget`, `closest`, contenitore stabile |
| like rappresentato modificando stile/disabled del button | **replace** con `state -> render`; likes/liked sono dati |
| nessuna persistenza strutturata | **add** adapter `localStorage` + JSON + recovery |
| testo utente inserito nel DOM | **harden**: `textContent` come default; XSS verra approfondito nel modulo security |

La milestone 3 conserva quindi l'idea migliore del legacy — **event delegation** — ma cambia il modello architetturale:

```text
legacy
DOM = stato
button id = identita

nuovo
post object = stato
post.id = identita
DOM = render dello stato
data-action = azione UI
```

## Principio di migrazione

Nessun repository legacy viene copiato integralmente nel nuovo corso. Ogni frammento deve ricevere una decisione esplicita `reuse`, `rewrite`, `replace`, `defer` o `retire`, conservando provenance e snapshot originario.
