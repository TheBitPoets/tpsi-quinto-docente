# Node.js ed Express 5: dal protocollo al backend

## Perché questa lezione arriva adesso

In UDA 23 abbiamo usato un server `node:http` come **fixture trasparente**. Sapevamo cosa chiedergli:

```text
GET   /api/posts
POST  /api/posts
PATCH /api/posts/:id
```

ma non avevamo ancora studiato come un backend riceve una request, sceglie il codice da eseguire, valida il body e produce una response.

Adesso apriamo quella scatola.

L'ordine didattico resta intenzionale:

```text
HTTP
  -> Node.js runtime
  -> node:http
  -> routing manuale
  -> problema della complessità
  -> Express 5
  -> middleware
  -> Router
  -> validation
  -> error handling
  -> API Feisbuc
```

Express non sostituisce HTTP: organizza codice che deve comunque rispettare il contratto HTTP.

---

## Obiettivi

Al termine del modulo lo studente deve saper:

1. distinguere JavaScript, browser e runtime Node.js;
2. spiegare il ruolo di `package.json`, npm, script e dipendenze;
3. usare ES modules in Node;
4. descrivere a livello concettuale event loop e I/O non bloccante;
5. leggere un server minimale costruito con `node:http`;
6. spiegare quali responsabilità Express elimina dal routing manuale;
7. costruire una applicazione Express 5 con `Router`;
8. usare e ordinare correttamente middleware;
9. distinguere `req.params`, `req.query` e `req.body` come proiezioni della request HTTP;
10. validare input al confine dell'applicazione;
11. progettare un error model JSON coerente;
12. separare avvio server, composizione app, routing, validation e storage;
13. usare `process.env` per configurazione esterna;
14. spiegare perché CORS non va abilitato automaticamente in ogni progetto;
15. mantenere il contratto HTTP di Feisbuc invariato mentre cambia l'implementazione server.

---

# 1. JavaScript non significa browser

JavaScript è un linguaggio.

Il browser è un ambiente che fornisce API come:

```text
document
window
localStorage
fetch
```

Node.js è un altro runtime JavaScript. Fornisce invece API come:

```text
process
Buffer
node:fs
node:http
node:path
node:crypto
```

Quindi questo codice:

```js
console.log(document.querySelector("h1"));
```

ha senso in un browser ma non in un normale processo Node.

Questo invece:

```js
console.log(process.version);
```

ha senso in Node.

## Modello mentale

```text
ECMAScript
   |
   +-- Browser runtime -> DOM, Web Storage, Fetch...
   |
   +-- Node.js runtime -> filesystem, process, HTTP server...
```

Non studiamo quindi un nuovo linguaggio: studiamo un nuovo **runtime** e nuove API.

---

# 2. Il processo Node

Quando eseguiamo:

```bash
node server.mjs
```

il sistema operativo avvia un processo Node.

Nel programma possiamo leggere informazioni dal runtime:

```js
console.log(process.version);
console.log(process.platform);
console.log(process.pid);
```

E possiamo leggere configurazione esterna:

```js
const port = Number(process.env.PORT ?? 3000);
```

Questa separazione è importante.

Evitiamo:

```js
const productionPassword = "segreto";
```

Preferiamo il principio:

```text
codice       -> repository
configurazione -> environment
segreti      -> secret management / environment protetto
```

I segreti verranno approfonditi nella parte sicurezza.

---

# 3. npm e package.json

`npm` è il package manager normalmente distribuito insieme a Node.js.

Un progetto può dichiarare la propria identità e le dipendenze in `package.json`:

```json
{
  "name": "feisbuc-api",
  "private": true,
  "type": "module",
  "engines": {
    "node": ">=22"
  },
  "scripts": {
    "start": "node src/server.js",
    "check": "node --check src/server.js"
  },
  "dependencies": {
    "express": "5.2.1"
  }
}
```

Per il corso usiamo una versione Express **pinned** per rendere gli esempi riproducibili.

## dependencies e devDependencies

In modo semplificato:

```text
dependencies
  -> servono all'applicazione a runtime

devDependencies
  -> strumenti necessari allo sviluppo/test/build
```

Non aggiungiamo pacchetti senza motivo.

Ogni dipendenza:

- aumenta il codice di terze parti;
- deve essere aggiornata;
- può avere vulnerabilità;
- rende l'applicazione più complessa da riprodurre.

---

# 4. ES modules anche nel backend

Nel corso usiamo ES modules come modello principale.

Con:

```json
{
  "type": "module"
}
```

possiamo scrivere:

```js
import express from "express";
import { randomUUID } from "node:crypto";
```

ed esportare:

```js
export function validatePostInput(value) {
  // ...
}
```

Perché preferiamo un solo modello iniziale?

Per ridurre context switching fra browser e backend:

```text
browser modules -> import/export
Node modules    -> import/export
```

CommonJS (`require`, `module.exports`) verrà comunque riconosciuto quando incontreremo codice legacy.

---

# 5. Event loop: quanto ci serve davvero

Non serve trasformare questa UDA in un corso sugli internals di V8/libuv.

Serve però capire perché questo server può gestire molte connessioni senza creare un thread JavaScript per ogni request.

Modello didattico minimo:

```text
JavaScript call stack
        |
        | avvia operazione I/O
        v
runtime / sistema operativo
        |
        | operazione completata
        v
queue
        |
        v
event loop
        |
        v
callback / continuation
```

Il punto fondamentale è:

> non bloccare inutilmente il thread JavaScript con lavoro sincrono lungo.

Quindi:

```js
const data = await loadSomething();
```

non significa "Node si ferma completamente".

La funzione sospende la propria continuazione mentre il runtime può gestire altro lavoro.

---

# 6. Apriamo la fixture: node:http

Un server minimale può essere costruito senza Express:

```js
import { createServer } from "node:http";

const server = createServer((req, res) => {
  if (req.method === "GET" && req.url === "/api/health") {
    res.writeHead(200, {
      "Content-Type": "application/json; charset=utf-8"
    });
    res.end(JSON.stringify({ ok: true }));
    return;
  }

  res.writeHead(404, {
    "Content-Type": "application/json; charset=utf-8"
  });
  res.end(JSON.stringify({ error: "not-found" }));
});

server.listen(3000);
```

Riconosciamo immediatamente concetti di UDA 23:

```text
req.method       -> HTTP method
req.url          -> target
req.headers      -> request headers
res.statusCode   -> response status
res.setHeader    -> response headers
res.end          -> termina response
```

## Leggere il body

Nel server HTTP nativo il body arriva come stream.

Un esempio minimale:

```js
let body = "";

for await (const chunk of req) {
  body += chunk;
}

const value = JSON.parse(body);
```

Subito emergono problemi reali:

- dimensione massima del body;
- JSON invalido;
- `Content-Type` sbagliato;
- routing;
- parametri dinamici;
- static files;
- logging;
- error handling;
- middleware comuni.

Potremmo implementare tutto a mano.

Ma finiremmo per costruire un framework.

---

# 7. Perché Express

Express ci fornisce un modello semplice per organizzare il request-response cycle.

Nel corso usiamo **Express 5.x**.

Esempio equivalente:

```js
import express from "express";

const app = express();

app.get("/api/health", (req, res) => {
  res.json({ ok: true });
});

app.use((req, res) => {
  res.status(404).json({ error: "not-found" });
});

app.listen(3000);
```

Il protocollo non cambia:

```text
GET /api/health
       -> 200 application/json

GET /missing
       -> 404 application/json
```

Cambia il modo in cui organizziamo il codice.

---

# 8. Middleware: la pipeline della request

Una funzione middleware riceve normalmente:

```js
(req, res, next)
```

Può:

- leggere request;
- modificare request/response;
- terminare il ciclo;
- chiamare `next()` per continuare.

Esempio:

```js
function requestLogger(req, res, next) {
  console.log(req.method, req.originalUrl);
  next();
}

app.use(requestLogger);
```

Modello:

```text
request
  |
  v
middleware A
  |
 next()
  v
middleware B
  |
 next()
  v
route handler
  |
  v
response
```

## L'ordine è comportamento

Queste due configurazioni non sono equivalenti:

```js
app.use(express.json());
app.use("/api", apiRouter);
```

```js
app.use("/api", apiRouter);
app.use(express.json());
```

Nel secondo caso le route del router vengono eseguite **prima** del parser JSON.

Quindi `req.body` non contiene ciò che ci aspettiamo.

Questo diventerà parte dell'Activity D.

---

# 9. Middleware built-in utili

## JSON body parser

```js
app.use(express.json({ limit: "32kb" }));
```

Non significa:

> ogni request del mondo contiene JSON.

Significa:

> quando la request ha una representation JSON compatibile, Express può produrre `req.body`.

## Static files

```js
app.use(express.static("public"));
```

Possiamo così servire il client Feisbuc dallo stesso origin della API.

Questo mantiene semplice la prima architettura:

```text
http://localhost:3000/
http://localhost:3000/app.js
http://localhost:3000/api/posts
```

Stesso scheme + host + port -> stesso origin.

---

# 10. Router: separare le risorse

Un'applicazione con tutto in `server.js` cresce male.

Creiamo un Router:

```js
import { Router } from "express";

export const postsRouter = Router();

postsRouter.get("/", listPosts);
postsRouter.post("/", createPost);
postsRouter.patch("/:id", updatePost);
```

E lo montiamo:

```js
app.use("/api/posts", postsRouter);
```

La composizione finale è:

```text
/api/posts       + GET
/api/posts       + POST
/api/posts/:id   + PATCH
```

---

# 11. params, query e body

UDA 23 ci ha già insegnato dove vivono i dati nella request.

Express li rende comodi da leggere.

## Path parameter

Request:

```http
PATCH /api/posts/p-42
```

Express:

```js
req.params.id
```

## Query string

Request:

```http
GET /api/posts?liked=true
```

Express:

```js
req.query.liked
```

## JSON body

Request:

```http
POST /api/posts
Content-Type: application/json

{"text":"ciao"}
```

Express:

```js
req.body.text
```

Questa è una **proiezione conveniente del protocollo**, non una nuova forma di comunicazione.

---

# 12. Validation: non fidarti del confine esterno

Il client Feisbuc prova a inviare dati validi.

Ma il server non può assumere che ogni client sia corretto.

Una funzione pura di validation può essere:

```js
export function validateNewPost(input) {
  if (!input || typeof input !== "object" || Array.isArray(input)) {
    return { ok: false, error: "body-invalid" };
  }

  const text = typeof input.text === "string"
    ? input.text.trim()
    : "";

  if (text.length === 0) {
    return { ok: false, error: "text-required" };
  }

  if (text.length > 280) {
    return { ok: false, error: "text-too-long" };
  }

  return {
    ok: true,
    value: { text }
  };
}
```

Notare che questa funzione:

- non conosce Express;
- non conosce HTTP;
- può essere testata deterministicamente;
- separa business rule da trasporto.

Questa separazione prepara anche SQL e FastAPI.

---

# 13. Error model

Evitiamo error response casuali:

```json
{"message":"male"}
```

poi:

```json
{"error":"qualcosa"}
```

poi plain text.

Definiamo un formato semplice:

```json
{
  "error": {
    "code": "post-text-required",
    "message": "Il testo del post e obbligatorio.",
    "requestId": "..."
  }
}
```

Il codice macchina e il messaggio umano hanno ruoli diversi.

## Status + error body

```text
400 -> request sintatticamente/semanticamente non valida
404 -> risorsa non trovata
415 -> media type non supportato
500 -> errore inatteso server
```

La scelta precisa dipende dal contratto API, ma deve essere intenzionale.

---

# 14. Error middleware

Un error middleware Express ha **quattro argomenti**:

```js
function errorHandler(error, req, res, next) {
  console.error(error);

  res.status(500).json({
    error: {
      code: "internal-error",
      message: "Errore interno",
      requestId: req.requestId
    }
  });
}
```

Anche se `next` non viene usato, la firma a quattro argomenti identifica il middleware come error handler.

Con Express 5, se un route handler `async` lancia un errore o restituisce una Promise rejected, l'errore può raggiungere automaticamente la pipeline di error handling.

Esempio:

```js
router.get("/:id", async (req, res) => {
  const post = await repository.findById(req.params.id);

  if (!post) {
    throw new Error("post-not-found");
  }

  res.json(post);
});
```

Più avanti distingueremo errori applicativi attesi dagli errori inattesi.

---

# 15. Request ID e logging

Quando una request attraversa più livelli è utile avere una identità.

```js
import { randomUUID } from "node:crypto";

export function requestId(req, res, next) {
  req.requestId = randomUUID();
  res.setHeader("X-Request-Id", req.requestId);
  next();
}
```

Un logger minimale:

```js
export function requestLogger(req, res, next) {
  const startedAt = Date.now();

  res.on("finish", () => {
    console.log(
      req.requestId,
      req.method,
      req.originalUrl,
      res.statusCode,
      Date.now() - startedAt
    );
  });

  next();
}
```

Non è ancora observability completa.

Ma introduce il concetto:

```text
una request
-> una identita
-> eventi correlabili
```

---

# 16. Configurazione dell'applicazione

Evitiamo di spargere `process.env` ovunque.

Possiamo centralizzare:

```js
export function loadConfig(env = process.env) {
  const port = Number(env.PORT ?? 3000);

  if (!Number.isInteger(port) || port < 0 || port > 65535) {
    throw new Error("PORT non valida");
  }

  return {
    port,
    nodeEnv: env.NODE_ENV ?? "development"
  };
}
```

Il server startup usa config.

L'applicazione HTTP non deve conoscere il modo in cui la configurazione è stata caricata.

---

# 17. Separare app e server

Pattern utile:

```text
src/
  app.js
  server.js
```

## app.js

Costruisce Express:

```js
export function createApp(dependencies) {
  const app = express();
  // middleware + router
  return app;
}
```

## server.js

Fa startup:

```js
const app = createApp(...);
app.listen(port);
```

Perché?

Perché possiamo testare `app` senza dover fissare una porta nel modulo che la costruisce.

---

# 18. Dependency injection minimale

Non serve un framework DI.

Basta non creare ogni dipendenza dentro ogni route.

```js
export function createPostsRouter({ postStore }) {
  const router = Router();

  router.get("/", (req, res) => {
    res.json(postStore.list());
  });

  return router;
}
```

Oggi `postStore` sarà in-memory.

Più avanti potrà diventare SQL.

Il router non deve cambiare completamente.

```text
Router
  |
  v
postStore interface
  |
  +-- memory store      <- adesso
  |
  +-- SQL repository    <- prossima fase
```

Questo è uno dei passaggi architetturali più importanti del corso.

---

# 19. Feisbuc milestone 5: stessa API, nuovo backend

In UDA 23 il client usava:

```text
GET   /api/posts
POST  /api/posts
PATCH /api/posts/:id
```

Questa milestone mantiene lo stesso contratto.

Cambia il server:

```text
prima
node:http fixture monolitica

ora
Express app
  -> middleware
  -> posts Router
  -> validation
  -> memory store
  -> error middleware
```

Il client dovrebbe quasi non accorgersene.

Questa è una proprietà desiderabile.

Un contratto stabile permette di evolvere l'implementazione.

---

# 20. CORS: non usare cors() come superstizione

Nel vecchio lab didattico il frontend e il backend potevano essere eseguiti su origin diversi e veniva aggiunto middleware CORS.

Nel Feisbuc attuale serviamo client e API dallo stesso server:

```text
http://localhost:3000/
http://localhost:3000/api/posts
```

Quindi il flusso principale è same-origin.

Non abbiamo bisogno di aggiungere CORS solo perché stiamo costruendo una API.

Quando frontend e backend saranno realmente cross-origin studieremo una policy esplicita:

```text
quali origin?
quali metodi?
quali header?
credentials sì/no?
```

Regola:

> CORS è una policy di accesso cross-origin del browser, non una decorazione obbligatoria delle API.

---

# 21. Cosa NON facciamo ancora

Questa prima parte di UDA 24 non introduce ancora:

- database;
- ORM;
- password;
- sessioni;
- JWT;
- Nunjucks;
- SSR completo;
- upload;
- deploy production.

Lo storage è volutamente in memoria.

Perché?

Perché vogliamo poter attribuire ogni errore a uno strato preciso.

Se una POST non funziona, dobbiamo sapere se il problema è:

```text
HTTP?
Express routing?
body parsing?
validation?
middleware order?
store?
```

prima di aggiungere SQL.

---

# 22. Errori frequenti

## 22.1 `express.json()` dopo il router

Sintomo:

```text
GET funziona
POST ha req.body undefined
```

Domanda corretta:

> in quale ordine passa la request nei middleware?

---

## 22.2 Confondere params e query

Route:

```text
/api/posts/:id
```

Errore:

```js
req.query.id
```

Corretto:

```js
req.params.id
```

---

## 22.3 Error middleware con tre argomenti

Errore:

```js
function errorHandler(err, req, res) {}
```

Express lo vede come middleware normale.

Corretto:

```js
function errorHandler(err, req, res, next) {}
```

---

## 22.4 Non chiamare next()

Un middleware che non termina la response e non chiama `next()` lascia il ciclo sospeso.

---

## 22.5 Usare GET per modificare dati

Se una route crea, modifica o cancella stato, GET è quasi certamente il metodo sbagliato.

Questo è un punto che correggiamo esplicitamente rispetto ad alcuni lab legacy.

---

## 22.6 Mandare password nei log

Nel vecchio materiale didattico alcune credenziali venivano stampate per mostrare il flusso.

Nel nuovo corso questa pratica diventa un anti-pattern esplicito.

La sicurezza verrà approfondita nella fase auth.

---

# 23. Esercizi A-F

## A — osserva

Confronta due server equivalenti:

```text
node:http
Express
```

Individua dove vivono:

- method matching;
- path matching;
- JSON parsing;
- status;
- headers;
- 404.

## B — modifica controllata

Completa una funzione di validation pura per i post.

La funzione viene corretta deterministicamente senza avviare un server.

## C — implementazione autonoma

Costruisci Feisbuc milestone 5:

```text
app.js
server.js
Router
middleware
validator
memory store
```

mantenendo invariato il contratto REST di UDA 23.

## D — debug

Diagnostica una app Express in cui:

- JSON parser è nell'ordine sbagliato;
- params/query sono confusi;
- l'error handler non ha la firma corretta;
- una route modifica dati con metodo improprio;
- il 404 middleware è posizionato male.

## E — mini-progetto futuro

Sostituire il memory store con repository SQL senza cambiare il contratto HTTP.

## F — prodotto integrato futuro

Feisbuc con:

- API;
- database;
- auth;
- frontend;
- realtime;
- test;
- deployment.

---

# 24. Verifica rapida

1. Qual è la differenza fra ECMAScript e Node.js?
2. Cosa indica `"type": "module"` in `package.json`?
3. Perché `process.env` è preferibile a una configurazione hard-coded?
4. Che cosa fa `next()`?
5. Perché l'ordine dei middleware è importante?
6. Qual è la differenza fra `req.params`, `req.query` e `req.body`?
7. Perché validation e route handler non devono essere necessariamente la stessa funzione?
8. Perché un error middleware Express ha quattro parametri?
9. Perché non abilitiamo CORS automaticamente?
10. Perché in questa milestone usiamo un memory store invece del database?

---

# 25. Sintesi inclusiva

```text
Node.js
= runtime JavaScript server-side

npm/package.json
= progetto + dipendenze + script

node:http
= server HTTP nativo

Express
= organizzazione di routing/middleware/response

middleware
= funzione nella pipeline request-response

Router
= gruppo di route

validation
= controllare input al confine

memory store
= persistenza temporanea didattica

error handler
= punto comune per error response
```

E soprattutto:

```text
Express non inventa HTTP.
Express rende più gestibile implementare HTTP.
```

---

# 26. Fonti e approfondimenti

Riferimenti tecnici primari:

- Node.js documentation — runtime, process, modules, HTTP;
- Express 5.x documentation — application, Router, middleware, error handling;
- RFC 9110 — semantica HTTP già introdotta in UDA 23.

Teacher-reference legacy auditata:

- `kinderp/lab5` — Express/fetch/CORS;
- `kinderp/lab6` — form POST;
- `kinderp/lab7` — query/path/body;
- `kinderp/lab8` — Express + SQLite;
- `kinderp/lab9` — register/login;
- `kinderp/lab10` — Express + SQLite + Nunjucks.

Il materiale legacy viene usato come provenance e confronto storico; esempi, architettura e soluzioni canoniche di questo corso sono riscritti.

---

# 27. Prossimo passo

La seconda parte di UDA 24 sostituirà:

```text
MemoryPostStore
```

con:

```text
SQL raw repository
```

mantenendo il più possibile invariati:

```text
client
HTTP contract
Router
validation
error model
```

Solo dopo aggiungeremo auth sicura e il breve confronto SSR/template.