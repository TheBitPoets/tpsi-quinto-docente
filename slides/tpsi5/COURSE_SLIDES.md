---
marp: true
paginate: true
size: 16:9
title: TPSI quinto anno — Full Stack Web Developer
---

# TPSI quinto anno
## Full Stack Web Developer 2026/27

Content Pack 1.0.0 / approved  
Feisbuc milestone 0–12 + mirror Python 01–04

---

# Narrazione del corso

Dal browser al servizio verificabile:

`HTML/CSS → JS/DOM → HTTP → Express → SQLite → auth → Vue → realtime → FastAPI mirror → deploy capstone`

---

# Metodo d'uso

- Il dettaglio resta nei moduli `content/tpsi5`.
- Le Activity stanno in `activities/tpsi5`.
- Questa è una scaletta proiettabile e modificabile dal docente.
- Ogni sezione ha un anchor `slides-NN` usato dal README.

---

<a id="slides-00"></a>

# 00 — Architettura didattica del corso

- Perché full stack non significa “tutto insieme”.
- Mappa browser → HTTP → backend → database → realtime.
- Feisbuc come progetto longitudinale.
- Output: capire il percorso e i confini.

---

<a id="slides-01"></a>

# 01 — Web Platform e HTML moderno

- HTML come struttura e semantica, non come grafica.
- Metadata, landmark, form e accessibilità.
- DevTools come strumento di lettura del documento.
- Feisbuc: prima pagina semanticamente corretta.

---

<a id="slides-02"></a>

# 02 — CSS moderno e responsive design

- Cascade, specificity, inheritance, box model.
- Flexbox e Grid come strumenti di layout.
- Mobile-first e media query.
- Feisbuc: layout responsive senza framework.

---

<a id="slides-03"></a>

# 03 — Bootstrap da CSS a framework

- Bootstrap come API sopra CSS.
- Grid, componenti e utility class.
- Quando usare il framework e quando capire il CSS sottostante.
- Feisbuc: UI più rapida ma ancora spiegabile.

---

<a id="slides-04"></a>

# 04 — JavaScript, DOM e Browser APIs

- State → render → DOM.
- Eventi, delegation, modules e Web Storage.
- Differenza tra dati, vista e comportamento.
- Feisbuc: feed dinamico nel browser.

---

<a id="slides-05"></a>

# 05 — HTTP, async, fetch e REST

- Request/response, status, header, body.
- `fetch`, `Response`, `async/await` e gestione errori.
- REST come contratto tra client e server.
- Feisbuc: client che parla con API.

---

<a id="slides-06"></a>

# 06 — Node.js ed Express 5

- Dal protocollo HTTP al framework backend.
- Router, middleware, validation ed error pipeline.
- Separare route, dominio e store.
- Feisbuc: prima API Express modulare.

---

<a id="slides-07"></a>

# 07 — SQL raw e persistenza

- Da `MemoryPostStore` a SQLite.
- Tabelle, vincoli, DDL/DML e prepared statement.
- Repository come boundary tra app e database.
- Feisbuc: dati che sopravvivono al riavvio.

---

<a id="slides-08"></a>

# 08 — Auth, sessioni e sicurezza

- Autenticazione vs autorizzazione.
- Password hash, salt, sessione server-side e cookie.
- Non fidarsi di `authorId` dal client.
- Feisbuc: identità affidabile e ownership.

---

<a id="slides-09"></a>

# 09 — SSR e template server-side

- Stesso dominio, altra responsabilità di rendering.
- View model, template, autoescape e PRG.
- Confronto: API JSON + client render vs HTML server-side.
- Feisbuc: SSR senza cambiare auth/store.

---

<a id="slides-10"></a>

# 10 — Vue 3: reattività e componenti

- Componenti, props, emits e state derivato.
- Composition API e reattività osservabile.
- UI come funzione dello stato.
- Feisbuc: prima SPA Vue.

---

<a id="slides-11"></a>

# 11 — Vue Router e navigazione SPA

- URL come stato applicativo.
- Route, parametri, layout, not found e guard.
- Auth lato client come UX, non come sicurezza definitiva.
- Feisbuc: navigazione protetta e feed routed.

---

<a id="slides-12"></a>

# 12 — TypeScript mirato

- Tipare i confini, non tutto per principio.
- DTO, `unknown`, runtime parser e domain type.
- Router policy e payload remoti.
- Feisbuc: TypeScript come rete di sicurezza nei boundary.

---

<a id="slides-13"></a>

# 13 — WebSocket e Socket.IO realtime

- HTTP request/response vs canale persistente.
- REST resta command path; Socket.IO distribuisce eventi.
- Recovery tramite snapshot REST e reducer idempotente.
- Feisbuc: feed realtime multiutente.

---

<a id="slides-14"></a>

# 14 — React translation lab

- Stessi concetti, altra sintassi.
- Vue `ref/computed/emit` ↔ React `state/derived/callback`.
- JSX e controlled input.
- Obiettivo: trasferire concetti, non cambiare framework core.

---

<a id="slides-15"></a>

# 15 — FastAPI e OpenAPI mirror

- Stesso dominio, stack diverso.
- Pydantic, validation, response model e OpenAPI.
- TestClient come prova del contratto HTTP.
- Mirror Python: confrontare senza duplicare il prodotto.

---

<a id="slides-16"></a>

# 16 — SQLAlchemy 2.0 e persistenza

- Engine, Session, mapping ORM e transazioni.
- Repository persistente dietro lo stesso contratto REST.
- Restart test: prova che non è memoria mascherata.
- Feisbuc mirror: stesso HTTP, nuovo data layer.

---

<a id="slides-17"></a>

# 17 — Testing strategy e integration boundaries

- Unit, integration, contract, process smoke.
- Fixture function-scoped e `tmp_path`.
- Quando evitare mock fragili.
- Evidenza: test che dimostrano il boundary giusto.

---

<a id="slides-18"></a>

# 18 — Runtime, deploy, health e capstone

- Configurazione via environment e fail-fast.
- Prestart, liveness, readiness e Uvicorn process probe.
- Evidence bundle deterministico.
- Capstone: da codice funzionante a servizio verificabile.

---

# Chiusura del percorso

Alla fine gli studenti devono saper spiegare e dimostrare:

- dove vive ogni responsabilità;
- quale contratto collega i componenti;
- come si testa un confine;
- come si consegna un servizio riproducibile.
