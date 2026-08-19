# Audit iniziale delle risorse legacy

Stato: draft. Gli SHA indicati sono snapshot di partenza, non branch mobili.

## `TheBitPoets/html_css_summary`

Pinned: `d71da420f1aa2ea39b61356e4f9900c6371e7a42`.

**Decisione iniziale: REUSE + MAJOR UPDATE.**

Da conservare: progressione molto semplice, esempi piccoli, box model, block/inline, collegamenti playground.

Da aggiornare: scheletro HTML moderno (`DOCTYPE`, `lang`, charset, viewport), semantica, form, accessibilità, cascade/specificità, Flexbox, Grid, media query, custom properties e responsive design. Gli esempi vanno revisionati: per esempio la sezione dedicata a `<ul>` contiene attualmente un esempio con `<ol>`. JSFiddle resta materiale legacy utile, ma i nuovi micro-esempi dovrebbero privilegiare MDN Playground quando possibile.

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

## Principio di migrazione

Nessun repository legacy viene copiato integralmente nel nuovo corso. Ogni frammento deve ricevere una decisione esplicita `reuse`, `rewrite`, `replace` o `retire`, conservando provenance e snapshot originario.
