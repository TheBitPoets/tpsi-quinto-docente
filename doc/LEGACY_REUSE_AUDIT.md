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

Il nuovo corso cambia però l'ordine esplicativo:

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

Motivo: non vogliamo che `fetch`, `req.query` o `cors()` appaiano prima del modello che stanno implementando.

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
| Promise/async-await | **defer da UDA 22 a UDA 23** |
| CommonJS | defer a Node/backend |
| ES module Node/filesystem | replace per browser ES modules |
| advanced internals/classes | advanced/senior |

L'esempio ES module Node legacy non viene reso canonico: e Node-specifico e contiene riferimenti incompleti. UDA 22 parte da `type=module`, `import`/`export` nel browser.

Output UDA 22:

- `04_JAVASCRIPT_DOM_BROWSER_APIS.md`;
- A/B JavaScript puro autograded;
- C Feisbuc DOM/event delegation/localStorage;
- D debug browser;
- milestone `feisbuc-03-dynamic-local-feed`.

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
milestone 4  HTTP REST API client
```

### JavaScript legacy

| Pattern | Decisione |
| --- | --- |
| `DOMContentLoaded` + listener | reuse concept, poi confronto con module scripts |
| `event.preventDefault()` con parametro `e` | debug case reale |
| `createElement`/`appendChild` | reuse/modernize con semantica e `textContent` |
| counter globale e `like_button_N` | replace con `post.id` + `data-*` |
| listener individuali sui like iniziali | retire come soluzione finale |
| event delegation sul feed | **preserve and deepen** |
| like conservato nello stile/disabled del button | replace con state -> render |
| nessuna persistenza strutturata | localStorage/JSON in milestone 3 |
| testo utente nel DOM | harden con `textContent` |

Modello nuovo:

```text
post object = stato
post.id = identita
DOM = render dello stato
data-action = azione UI
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

- Express viene introdotto immediatamente, prima di rendere esplicito HTTP;
- CORS viene configurato come libreria prima di spiegare origin/policy;
- il client fa `response.json()` e `catch()` ma non controlla `response.ok`.

Nel nuovo corso:

```text
HTTP request/response
 -> status/header/content
 -> Promise/async-await
 -> fetch/Response.ok
 -> REST
 -> solo dopo Express/CORS middleware
```

Quindi lab5 resta provenance, non baseline di codice.

## `kinderp/lab6`

Snapshot: `79f4d056958b083b70f75b178ef08f00b3f902a8`.

Decisione: **REUSE AS ARCHITECTURAL CONTRAST**.

Valore principale: mostra che il browser sa fare una request `POST` anche con una normale `<form>` senza JavaScript.

Nel nuovo corso il confronto diventa:

```text
HTML form navigation/submission
vs
fetch API request + client-side state update
```

Il parsing Express (`express.json`, `express.urlencoded`) viene spostato a UDA 24, dove sara finalmente possibile spiegare che cosa astrae.

## `kinderp/lab7`

Snapshot: `b4ee8a661d0127d5dc92254e5b3bc0a24b6075e5`.

Decisione: **PRESERVE QUERY/PATH/BODY IDEA, MOVE EXPRESS MAPPING LATER**.

Il lab storico mostra bene tre modi di trasportare dati:

```text
query string
path segment
request body
```

Nel nuovo corso questi vengono prima descritti come parti della request HTTP:

```text
GET /users?id=123
GET /users/123
POST /users + content
```

Solo in UDA 24 verranno mappati a:

```text
req.query
req.params
req.body
```

Il POST legacy `application/x-www-form-urlencoded` resta utile per confrontare representation diverse; Feisbuc milestone 4 sceglie invece JSON e rende esplicito `Content-Type` + `JSON.stringify`.

---

# Output UDA 23

- `content/tpsi5/05_HTTP_ASYNC_FETCH_REST.md`;
- `tpsi5-activity-a-http-microscope-001` — protocollo osservato con curl/DevTools;
- `tpsi5-activity-b-async-response-policy-001` — status/ok/Content-Type, autograded JS;
- `tpsi5-activity-c-feisbuc-rest-client-001` — GET/POST/PATCH, milestone 4;
- `tpsi5-activity-d-debug-fetch-http-001` — diagnosi di 404, media type, serialization e 204;
- Feisbuc `feisbuc-04-rest-api-client`.

## Server fixture UDA 23

La fixture usa `node:http`, memoria e same-origin **ma non e ancora un laboratorio Node/Express**.

Serve a rendere osservabile il contratto:

```text
browser -> HTTP -> server fixture
```

senza introdurre routing/middleware/persistenza prima del momento didattico corretto. UDA 24 aprira il black box e sostituira progressivamente la fixture con il backend strutturato.

---

# Principio di migrazione

Il valore dei vecchi repo e storico e didattico: mostrano l'evoluzione reale del percorso. Il nuovo corso conserva le idee buone, rende espliciti i debiti e riscrive codice/consegne secondo gli standard correnti, mantenendo sempre snapshot e provenance.
