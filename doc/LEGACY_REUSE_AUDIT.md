# Audit delle risorse legacy TPSI quinto

Stato: **draft progressivo**. Gli SHA sono snapshot di provenance, non branch mobili. Nessun repository legacy viene copiato integralmente nel corso: ogni elemento riceve una decisione `reuse`, `rewrite`, `replace`, `defer` o `retire`.

## `TheBitPoets/html_css_summary`

Pinned: `d71da420f1aa2ea39b61356e4f9900c6371e7a42`.

Decisione: **REUSE CONCEPTS + MAJOR REWRITE**.

| Frammento | Decisione | Nuova destinazione |
| --- | --- | --- |
| scheletro HTML | rewrite | documento moderno doctype/lang/charset/viewport |
| p/ol/a | reuse concept | esempi originali e semantici |
| ul | rewrite | corregge il vecchio esempio con `ol` |
| CSS syntax | migrated/rewrite | `02_CSS_MODERNO_RESPONSIVE.md` |
| box model | major update | `border-box`, DevTools e debugging |
| block/inline | rewrite | normal flow, non modello di layout |
| margin/padding/border | reuse | box model moderno |
| JSFiddle | legacy evidence | MDN Playground/browser locale per nuovi micro-lab |

Output: UDA21 + Feisbuc milestone 0/1.

---

## `TheBitPoets/labs_summary`

Pinned: `36a909f00c9478983a8d1b950440e2abc28b8a55`.

Decisione: **REUSE PROGRESSION + REBUILD ACTIVITIES**.

Progressione storica utile:

```text
statico -> storage/JS -> fetch/Express -> form POST
-> query/path/body -> SQLite -> login/register -> template -> realtime
```

Nuovo ordine:

```text
Web Platform -> JavaScript/DOM -> HTTP -> fetch/REST
-> Node -> Express -> SQL -> auth -> SSR
-> framework frontend -> realtime
```

Motivo: una API o libreria non deve apparire prima del modello che sta astraendo.

---

## `kinderp/lab3`

Snapshot: `0deae0eb606bc9c2849ba271bdf03c128910f1ac`.

Decisione: **TEACHER-REFERENCE + SELECTIVE REWRITE**.

| Area legacy | Decisione |
| --- | --- |
| `let`/`const`/`var` | rewrite; `const` default, `let` per riassegnazione |
| primitive/object/array | reuse concepts con Feisbuc |
| `map/filter/find` | expand nel core |
| functions/callback/arrow | reuse concept, esempi riscritti |
| error handling | selective reuse |
| Promise/async-await | spostato UDA22 -> UDA23 |
| CommonJS | contestualizzato in Node/backend |
| ES module Node/filesystem | replace per browser ES modules |
| advanced internals/classes | advanced/senior |

Output UDA22: JavaScript/DOM/Web Storage, A/B autograded, milestone 3 e debug browser.

---

## `TheBitPoets/feisbuc`

Pinned: `086995ece4260a3408740b94cfe2701ce24f8b57`.

Decisione: **KEEP AS LONGITUDINAL CAPSTONE**.

### Evoluzione applicata

```text
0  semantica HTML
1  Grid/Flexbox responsive
2  Bootstrap mappato a CSS nativo
3  JavaScript state/render + event delegation + localStorage
4  HTTP REST API client + node:http fixture
5  Express 5 modular API + MemoryPostStore
6  SqlPostStore + SQLite file
7  users + scrypt + session server-side + ownership
```

### Pattern JavaScript legacy

| Pattern | Decisione |
| --- | --- |
| `DOMContentLoaded` + listener | reuse concept / confronto module script |
| `event.preventDefault()` con parametro `e` | debug case reale |
| `createElement`/`appendChild` | reuse/modernize con `textContent` |
| counter globale / `like_button_N` | replace con `post.id` + `data-*` |
| listener individuali ai like | retire come soluzione finale |
| event delegation sul feed | preserve and deepen |
| like nello stile/disabled del button | replace con state -> render |
| testo utente nel DOM | harden con `textContent` |
| identita autore convenzionale/client-side | replace con `req.auth.user.id` |

Modello attuale:

```text
post.id        = identita risorsa
post.authorId  = identita verificata dal server
DOM            = render dello stato
data-action    = intenzione UI
HTTP contract  = confine client/backend
session cookie = credential opaca non letta dal JS
```

---

# Audit UDA23 — lab5/lab6/lab7

## `kinderp/lab5`

Snapshot: `b518922bf346ffe6402d67806acf4c5bc78916b9`.

Decisione: **PRESERVE FIRST CLIENT/SERVER INTUITION, REORDER CONCEPTS**.

Valore: primo `fetch`, JSON e separazione visiva client/server.

Debiti trasformati:

- Express prima del modello HTTP;
- CORS come setup automatico;
- `catch()` senza `response.ok`.

Nuovo ordine:

```text
HTTP -> status/header/content -> Promise/async-await
-> fetch/Response.ok -> REST -> Node/Express
```

Lab5 resta provenance e confronto Express 4 -> Express 5.

## `kinderp/lab6`

Snapshot: `79f4d056958b083b70f75b178ef08f00b3f902a8`.

Decisione: **REUSE AS ARCHITECTURAL CONTRAST**.

Valore: una normale `<form>` puo produrre POST senza JavaScript. Il parsing Express viene spiegato solo quando il framework diventa oggetto di studio.

## `kinderp/lab7`

Snapshot: `b4ee8a661d0127d5dc92254e5b3bc0a24b6075e5`.

Decisione: **PRESERVE QUERY/PATH/BODY IDEA, MOVE EXPRESS MAPPING LATER**.

```text
GET /users?id=123       -> query
GET /users/123          -> path
POST /users + content   -> body
```

UDA23 descrive la request; UDA24 la mappa a `req.query`, `req.params`, `req.body`.

Output UDA23: `05_HTTP_ASYNC_FETCH_REST.md`, Activity A-D e Feisbuc milestone 4.

---

# Audit UDA24 — Node/Express, SQL, auth e SSR

## Strategia

UDA24 cambia **una responsabilita alla volta**:

```text
node:http fixture
  -> Express + MemoryPostStore
  -> SqlPostStore + SQLite
  -> users/session/authz
  -> breve confronto SSR
```

Questo rende attribuibili gli errori e permette di verificare se i boundary progettati nel passaggio precedente erano davvero sostituibili.

## `kinderp/lab5` come baseline Express storica

Decisione: **COMPARE, DO NOT COPY**.

```text
legacy
CommonJS + Express 4.18.2 + cors() globale

nuovo
ES modules + Express 5.x pinned + same-origin iniziale
+ CORS soltanto con policy motivata
```

Output primo blocco UDA24:

- `06_NODE_EXPRESS_BACKEND.md`;
- Activity A-D Node/Express;
- Feisbuc milestone 5.

---

## `kinderp/lab8`

Snapshot: `be9a3988aec8a99b1a0f6776ad8cbeba33d82353`.

Decisione: **MIGRATED SQL CONCEPTS; RETIRE MUTATING GET AND TIGHT COUPLING**.

| Pattern legacy | Decisione | Nuovo modello |
| --- | --- | --- |
| Express + SQLite nello stesso salto | split | Express milestone 5, SQL milestone 6 |
| `GET /N2N` crea tabelle/righe | **retire** | GET safe; schema fuori dalle route |
| route con DDL/SQL diretto | replace | Router -> repository SQL |
| DB path sparso | replace | `DB_PATH`/config/repository |
| relazioni e query SQLite | reuse concept | modulo SQL e futuro corso SQL |

Output secondo blocco UDA24:

- `07_SQL_RAW_PERSISTENCE.md`;
- Activity A/B/D SQL autograded;
- Activity C `SqlPostStore`;
- Feisbuc milestone 6.

La provenance di lab8 ha quindi prodotto materiale reale, ma nessuna route legacy e stata copiata come baseline.

---

## `kinderp/lab9`

Snapshot: `97ee815691e0c985e5216e6f9ed264fd809509ee`.

Decisione: **MIGRATED AUTH MOTIVATION; RETIRE CREDENTIAL/PORTABILITY/TRUST ANTI-PATTERNS**.

Valore conservato:

- register/login come problema applicativo reale;
- utenti persistenti;
- CRUD e path parameter;
- query parametrizzate come intuizione iniziale.

Debiti trasformati:

| Pattern legacy | Decisione | Nuovo modello milestone 7 |
| --- | --- | --- |
| path SQLite assoluto Windows | **retire** | `DB_PATH` configurabile e portabile |
| password ricevuta e salvata direttamente | **retire** | scrypt + salt casuale |
| password/log credential nel client | **retire** | secret mai restituito/loggato |
| nessuna vera sessione revocabile | replace | token opaco + hash token DB + TTL/logout |
| identita affidata al client | **retire** | `req.auth.user` da sessione verificata |
| authorization implicita/assente | replace | ownership server-side, 401/403/404 distinti |
| errori login distinguono account/cause | harden | `invalid-credentials` generico |
| API/validation/SQL nello stesso file | replace | Router/auth-store/post-store/middleware boundary |

Output terzo blocco UDA24:

- `08_AUTH_SESSIONI_SICUREZZA.md`;
- `tpsi5-activity-a-auth-credential-policy-001`;
- `tpsi5-activity-b-auth-post-authorization-001`;
- `tpsi5-activity-c-feisbuc-auth-session-001`;
- `tpsi5-activity-d-debug-auth-security-001`;
- Feisbuc `feisbuc-07-auth-session`.

Nuovo trust model:

```text
browser
  -> HttpOnly cookie
  -> hash(token)
  -> session DB non scaduta
  -> user verificato
  -> authorization server-side
  -> prepared SQL
```

Il client puo scegliere il testo e l'azione richiesta; non puo scegliere l'identita usata per autorizzarla.

---

## `kinderp/lab10`

Snapshot: `7319c0696c8a6f76237e1ef21b4c3c2b535c4958`.

Decisione: **DEFER TO SSR COMPARISON; SEPARATE FROM API/DATABASE/AUTH FOUNDATIONS**.

Valore:

- introduce Nunjucks e rendering server-side;
- mostra dati SQL trasformati in HTML;
- offre un contrasto reale con API JSON + client rendering.

Debiti/limiti:

- Express, SQLite, query e template entrano insieme;
- route `/api/...` restituiscono HTML e confondono API/rendering;
- SQL e presentation logic convivono nello stesso server file.

Nuovo uso didattico:

```text
prima
REST JSON + client render + auth/session stabile

poi
SSR route + template usando lo stesso user/session model

confronto
chi produce HTML?
dove vive lo stato UI?
quale navigation model?
```

Nunjucks rimane un modulo compatto di confronto SSR, non la destinazione obbligatoria del progetto.

---

# Prossima migrazione UDA24

```text
milestone 7 auth/session
      ↓
breve SSR/template comparison (lab10 provenance)
      ↓
UDA25 frontend framework/SPA/realtime
```

ORM resta deliberatamente fuori da questa catena finche non viene presa la decisione tecnologica e finche SQL raw non e sufficientemente consolidato.

---

# Principio di migrazione

Il valore dei vecchi repo e storico e didattico: mostrano l'evoluzione reale del percorso. Il nuovo corso conserva le idee buone, rende espliciti i debiti e riscrive codice/consegne secondo gli standard correnti, mantenendo sempre snapshot e provenance.
