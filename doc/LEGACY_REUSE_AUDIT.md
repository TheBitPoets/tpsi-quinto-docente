# Audit delle risorse legacy TPSI quinto

Stato: **draft progressivo**. Gli SHA sono snapshot di provenance, non branch mobili. Nessun repository legacy viene copiato integralmente nel corso: ogni elemento riceve una decisione `reuse`, `rewrite`, `replace`, `defer` o `retire`.

## `TheBitPoets/html_css_summary`

Pinned: `d71da420f1aa2ea39b61356e4f9900c6371e7a42`.

Decisione: **REUSE CONCEPTS + MAJOR REWRITE**.

| Frammento | Decisione | Nuova destinazione |
| --- | --- | --- |
| scheletro HTML | rewrite | documento moderno con doctype/lang/charset/viewport |
| p/ol/a | reuse concept | esempi originali e semantici |
| ul | rewrite | corregge il vecchio esempio con `ol` |
| CSS syntax | migrated/rewrite | `02_CSS_MODERNO_RESPONSIVE.md` |
| box model | major update | `border-box`, DevTools e debugging |
| block/inline | rewrite | normal flow, non modello di layout |
| margin/padding/border | reuse | box model moderno |
| JSFiddle | legacy evidence | MDN Playground/browser locale preferiti per i nuovi micro-lab |

Output: HTML/CSS UDA 21 + Feisbuc milestone 0/1.

---

## `TheBitPoets/labs_summary`

Pinned: `36a909f00c9478983a8d1b950440e2abc28b8a55`.

Decisione: **REUSE PROGRESSION + REBUILD ACTIVITIES**.

La progressione storica rimane utile:

```text
statico
 -> storage/JS
 -> fetch/Express
 -> form POST
 -> query/path/body
 -> SQLite
 -> login/register
 -> template
 -> realtime
```

Il nuovo corso cambia l'ordine esplicativo:

```text
Web Platform
 -> JavaScript/DOM
 -> HTTP
 -> fetch/REST
 -> Node
 -> Express
 -> SQL/DB
 -> auth/SSR
 -> framework frontend/realtime
```

Motivo: `fetch`, `req.query`, `sqlite3` o `cors()` non devono apparire prima del modello che stanno implementando.

---

## `kinderp/lab3`

Snapshot: `0deae0eb606bc9c2849ba271bdf03c128910f1ac`.

Decisione: **TEACHER-REFERENCE + SELECTIVE REWRITE**.

| Area legacy | Decisione |
| --- | --- |
| `let`/`const`/`var` | rewrite examples, `const` default e `let` per riassegnazione |
| primitive/object/array | reuse concepts con dati Feisbuc |
| array mutation | contextualize rispetto a trasformazioni prevedibili |
| `map/filter/find` | expand nel core |
| functions/callback/arrow | reuse concept, esempi riscritti |
| error handling | selective reuse |
| Promise/async-await | defer da UDA 22 a UDA 23 |
| CommonJS | defer a Node/backend e contestualizzare come legacy/ecosistema |
| ES module Node/filesystem | replace per browser ES modules |
| advanced internals/classes | advanced/senior |

Output UDA 22: JavaScript/DOM/Web Storage, A/B autograded, milestone 3 e debug browser.

---

## `TheBitPoets/feisbuc`

Pinned: `086995ece4260a3408740b94cfe2701ce24f8b57`.

Decisione: **KEEP AS LONGITUDINAL CAPSTONE**.

### Evoluzione applicata

```text
milestone 0  semantica HTML
milestone 1  Grid/Flexbox responsive
milestone 2  Bootstrap con mapping verso CSS nativo
milestone 3  JavaScript state/render + event delegation + localStorage
milestone 4  HTTP REST API client + node:http fixture
milestone 5  Express 5 modular API + MemoryPostStore
```

### JavaScript legacy

| Pattern | Decisione |
| --- | --- |
| `DOMContentLoaded` + listener | reuse concept, poi confronto con module scripts |
| `event.preventDefault()` con parametro `e` | debug case reale |
| `createElement`/`appendChild` | reuse/modernize con semantica e `textContent` |
| counter globale e `like_button_N` | replace con `post.id` + `data-*` |
| listener individuali sui like iniziali | retire come soluzione finale |
| event delegation sul feed | preserve and deepen |
| like conservato nello stile/disabled del button | replace con state -> render |
| nessuna persistenza strutturata | localStorage/JSON in milestone 3, API da milestone 4 |
| testo utente nel DOM | harden con `textContent` |

Modello corrente:

```text
post object = stato
post.id = identita
DOM = render dello stato
data-action = azione UI
HTTP contract = confine client/backend
```

---

# Audit UDA 23 — lab5/lab6/lab7

## `kinderp/lab5`

Snapshot: `b518922bf346ffe6402d67806acf4c5bc78916b9`.

Decisione: **PRESERVE FIRST CLIENT/SERVER INTUITION, REORDER CONCEPTS**.

Punti utili:

- primo `fetch()` semplice;
- JSON restituito dal server;
- separazione visiva client/server.

Debiti trasformati in materiale didattico:

- Express introdotto prima di rendere esplicito HTTP;
- CORS configurato prima di spiegare origin/policy;
- `fetch().catch()` usato senza una policy esplicita su `response.ok`.

Nel nuovo corso:

```text
HTTP request/response
 -> status/header/content
 -> Promise/async-await
 -> fetch/Response.ok
 -> REST
 -> Node/Express
```

Lab5 resta provenance e diventa anche confronto Express 4 -> Express 5, non baseline di codice.

## `kinderp/lab6`

Snapshot: `79f4d056958b083b70f75b178ef08f00b3f902a8`.

Decisione: **REUSE AS ARCHITECTURAL CONTRAST**.

Valore principale: il browser sa fare una POST con normale `<form>` senza JavaScript. Il parsing Express (`express.json`, `express.urlencoded`) viene spostato dove il framework e oggetto di studio.

## `kinderp/lab7`

Snapshot: `b4ee8a661d0127d5dc92254e5b3bc0a24b6075e5`.

Decisione: **PRESERVE QUERY/PATH/BODY IDEA, MOVE EXPRESS MAPPING LATER**.

```text
GET /users?id=123       -> query
GET /users/123          -> path
POST /users + content   -> body
```

UDA 23 li studia come parti della request; UDA 24 li mappa a `req.query`, `req.params`, `req.body`.

Output UDA 23:

- `05_HTTP_ASYNC_FETCH_REST.md`;
- Activity A–D HTTP/async/fetch;
- Feisbuc `feisbuc-04-rest-api-client`.

---

# Audit UDA 24 — Node/Express e futuri DB/auth/SSR

## Principio della prima parte UDA 24

Il server black-box di UDA 23 viene aperto in due passaggi:

```text
node:http esplicito
      ↓
quali responsabilita stiamo ripetendo?
      ↓
Express 5 Router + middleware + validation + error pipeline
```

La prima API Express usa **solo memoria**. SQL, auth e template vengono intenzionalmente separati per rendere attribuibili gli errori e per poter sostituire una dipendenza alla volta.

## `kinderp/lab5` come baseline Express storica

Lo stesso snapshot UDA 23 diventa qui teacher-reference per confrontare:

```text
legacy
CommonJS + Express 4.18.2 + cors() globale

nuovo
ES modules + Express 5.x pinned + same-origin iniziale + CORS soltanto con policy motivata
```

Decisione: **COMPARE, DO NOT COPY**.

Valore: primo server Express piccolo. Debito: framework e CORS appaiono come setup necessario invece che come scelte con motivazione.

## `kinderp/lab8`

Snapshot: `be9a3988aec8a99b1a0f6776ad8cbeba33d82353`.

Decisione: **PRESERVE SQL-RELATIONSHIP INTUITION; RETIRE MUTATING GET AND TIGHT COUPLING**.

Il lab e utile perché porta finalmente SQLite nel backend e prova a ragionare su relazioni 1:1, 1:N e N:N.

Debiti da non trasferire:

| Pattern legacy | Decisione | Nuovo modello |
| --- | --- | --- |
| Express e SQLite introdotti nello stesso salto | defer/split | prima Express con memory store, poi SQL repository |
| `GET /N2N` crea tabelle e inserisce righe | **retire** | GET resta safe; schema/migrazioni sono operazioni separate |
| route che esegue direttamente DDL/SQL | replace | Router -> repository SQL |
| database file come dettaglio sparso | replace | config/repository boundary |

La futura Activity SQL non copiera quindi le route del lab8: riusera soltanto il problema relazionale e le query come teacher-reference.

## `kinderp/lab9`

Snapshot: `97ee815691e0c985e5216e6f9ed264fd809509ee`.

Decisione: **PRESERVE CRUD/AUTH PROGRESSION; RETIRE CREDENTIAL AND PORTABILITY ANTI-PATTERNS**.

Punti utili:

- CRUD su una risorsa utenti;
- path parameter per l'id;
- register/login come motivazione reale per persistenza e auth;
- query parametrizzate in varie operazioni.

Debiti espliciti:

| Pattern legacy | Decisione | Nuovo modello |
| --- | --- | --- |
| path SQLite assoluto `C:\\Users\\...` | **retire** | path/config relativo o environment, portabile |
| password ricevuta e inserita direttamente | **retire/harden** | password hashing prima della persistenza |
| password stampata/loggata nel client | **retire** | credenziali mai nei log |
| API, validation, SQL e response nello stesso file | replace | Router/service/repository boundaries minime |
| error response eterogenee | replace | error model stabile con code/message/requestId |

La futura fase auth usera il lab9 per mostrare perché "funziona" non significa "e sicuro".

## `kinderp/lab10`

Snapshot: `7319c0696c8a6f76237e1ef21b4c3c2b535c4958`.

Decisione: **DEFER TO SSR COMPARISON; SEPARATE FROM API AND DATABASE FOUNDATIONS**.

Valore:

- introduce Nunjucks e rendering server-side;
- mostra dati SQL trasformati in HTML dinamico;
- offre un contrasto reale con API JSON + client rendering.

Debiti/limiti per il nuovo ordine:

- Express, SQLite, query complesse e template engine entrano insieme;
- le route chiamate `/api/...` restituiscono HTML, confondendo il contratto API con il rendering;
- SQL e presentation logic convivono nello stesso server file.

Nuovo uso didattico:

```text
prima
REST JSON + client render

poi
SSR route + template

confronto
chi produce HTML?
dove vive lo stato UI?
quale navigation model?
```

Nunjucks rimane quindi un modulo compatto di confronto SSR, non la destinazione obbligatoria del progetto.

---

# Output primo blocco UDA 24

- `content/tpsi5/06_NODE_EXPRESS_BACKEND.md`;
- `tpsi5-activity-a-node-http-express-map-001` — mapping native HTTP -> Express;
- `tpsi5-activity-b-post-validation-001` — validation pura autograded;
- `tpsi5-activity-c-feisbuc-express-api-001` — milestone 5 Express modulare + memory store;
- `tpsi5-activity-d-debug-express-pipeline-001` — middleware order, params, safe methods, 404/error pipeline;
- Feisbuc `feisbuc-05-express-api`.

## Prossime migrazioni UDA 24

```text
MemoryPostStore
  -> SQL raw repository
  -> auth sicura con password hashing/sessione
  -> breve confronto SSR/template
```

Ogni passaggio deve preservare il più possibile client, contratto HTTP, validation e error model, cambiando una responsabilita alla volta.

---

# Principio di migrazione

Il valore dei vecchi repo e storico e didattico: mostrano l'evoluzione reale del percorso. Il nuovo corso conserva le idee buone, rende espliciti i debiti e riscrive codice/consegne secondo gli standard correnti, mantenendo sempre snapshot e provenance.
