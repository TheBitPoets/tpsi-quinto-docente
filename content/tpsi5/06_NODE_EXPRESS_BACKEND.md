# Node.js ed Express 5: dal protocollo al backend

<table align="center" width="100%"><tr><td>
<details>
<summary>&#128506; <strong>Orientamento della lezione</strong></summary>

<p align="justify"><strong>Contesto:</strong> conosciamo ormai HTTP dal punto di vista del client. Ora JavaScript viene eseguito in un processo server e il flusso della richiesta diventa una pipeline esplicita di middleware, router, validazione e risposta.</p>
<p align="justify"><strong>Domande guida:</strong> che cosa cambia fra browser e runtime Node? In quale ordine attraversa Express una richiesta? Dove devono vivere validation, error handling e dipendenze?</p>
<p align="justify"><strong>Obiettivi osservabili:</strong> avviare un processo Node ESM, leggere una fixture <code>node:http</code>, costruire router e middleware Express 5, propagare errori asincroni e separare applicazione e listener.</p>
<p align="justify"><strong>Prossimo passo:</strong> la lezione 07 sostituirà il <code>MemoryPostStore</code> con una persistenza SQLite mantenendo invariata la API.</p>

</details>
</td></tr></table>

## Perché questa lezione arriva adesso

<p align="justify">In UDA 23 abbiamo usato un server <code>node:http</code> come <strong>fixture trasparente</strong>. Sapevamo cosa chiedergli:</p>

```text
GET   /api/posts
POST  /api/posts
PATCH /api/posts/:id
```

<p align="justify">ma non avevamo ancora studiato come un backend riceve una request, sceglie il codice da eseguire, valida il body e produce una response.</p>

<p align="justify">Adesso apriamo quella scatola.</p>

<p align="justify">L'ordine didattico resta intenzionale:</p>

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

<p align="justify">Express non sostituisce HTTP: organizza codice che deve comunque rispettare il contratto HTTP.</p>

---

## Obiettivi

<p align="justify">Al termine del modulo lo studente deve saper:</p>

<ol>
  <li>distinguere JavaScript, browser e runtime Node.js;</li>
  <li>spiegare il ruolo di <code>package.json</code>, npm, script e dipendenze;</li>
  <li>usare ES modules in Node;</li>
  <li>descrivere a livello concettuale event loop e I/O non bloccante;</li>
  <li>leggere un server minimale costruito con <code>node:http</code>;</li>
  <li>spiegare quali responsabilità Express elimina dal routing manuale;</li>
  <li>costruire una applicazione Express 5 con <code>Router</code>;</li>
  <li>usare e ordinare correttamente middleware;</li>
  <li>distinguere <code>req.params</code>, <code>req.query</code> e <code>req.body</code> come proiezioni della request HTTP;</li>
  <li>validare input al confine dell'applicazione;</li>
  <li>progettare un error model JSON coerente;</li>
  <li>separare avvio server, composizione app, routing, validation e storage;</li>
  <li>usare <code>process.env</code> per configurazione esterna;</li>
  <li>spiegare perché CORS non va abilitato automaticamente in ogni progetto;</li>
  <li>mantenere il contratto HTTP di Feisbuc invariato mentre cambia l'implementazione server.</li>
</ol>

## Prerequisiti

<ul>
  <li>HTTP request/response, metodi, status, header e body;</li>
  <li>Promise, <code>async</code>/<code>await</code> e moduli ES;</li>
  <li>REST API Feisbuc della milestone 4;</li>
  <li>uso essenziale di terminale e file di progetto.</li>
</ul>

## Orientamento nella documentazione

<p align="center">
  <img src="../../assets/tpsi5/lesson-documentation-depth.svg" alt="La dispensa seleziona nelle fonti ufficiali i contenuti da studiare ora, riconoscere, rimandare o dichiarare fuori confine">
</p>

<table align="center"><tr><td>
<details>
<summary>&#128279; <strong>Indice incrociato — Node.js ed Express ↔ documentazione ufficiale</strong></summary>

<table align="center">
<thead><tr><th>Dispensa</th><th>Documentazione ufficiale</th><th>Profondità</th></tr></thead>
<tbody>
<tr><td><a href="#lesson-node-runtime">Runtime, processo, npm ed ESM</a></td><td><a href="https://nodejs.org/api/documentation.html">Node.js documentation</a><br><a href="https://nodejs.org/api/esm.html">ECMAScript modules</a></td><td>&#128994; studiare ora</td></tr>
<tr><td><a href="#lesson-node-http">Server <code>node:http</code></a></td><td><a href="https://nodejs.org/api/http.html">Node.js HTTP</a></td><td>&#128994; leggere l'esempio minimo</td></tr>
<tr><td><a href="#lesson-express-pipeline">Middleware, ordine e Router</a></td><td><a href="https://expressjs.com/en/5x/guide/writing-middleware.html">Express 5 — Writing middleware</a><br><a href="https://expressjs.com/en/guide/routing.html">Express — Routing</a></td><td>&#128994; studiare ora</td></tr>
<tr><td><a href="#lesson-express-boundaries">Validation ed error pipeline</a></td><td><a href="https://expressjs.com/en/5x/guide/error-handling.html">Express 5 — Error handling</a></td><td>&#128994; studiare ora</td></tr>
<tr><td>Streaming, cluster, performance e middleware di terze parti</td><td><a href="https://nodejs.org/api/stream.html">Node.js streams</a><br><a href="https://expressjs.com/en/resources/middleware.html">Express middleware</a></td><td>&#128993; riconoscere o studiare più avanti</td></tr>
</tbody>
</table>

</details>
</td></tr></table>

---

<a id="lesson-node-runtime"></a>
## 1. JavaScript non significa browser

<p align="justify">JavaScript è un linguaggio.</p>

<p align="justify">Il browser è un ambiente che fornisce API come:</p>

```text
document
window
localStorage
fetch
```

<p align="justify">Node.js è un altro runtime JavaScript. Fornisce invece API come:</p>

```text
process
Buffer
node:fs
node:http
node:path
node:crypto
```

<p align="justify">Quindi questo codice:</p>

```js
console.log(document.querySelector("h1"));
```

<p align="justify">ha senso in un browser ma non in un normale processo Node.</p>

<p align="justify">Questo invece:</p>

```js
console.log(process.version);
```

<p align="justify">ha senso in Node.</p>

### Modello mentale

```text
ECMAScript
   |
   +-- Browser runtime -> DOM, Web Storage, Fetch...
   |
   +-- Node.js runtime -> filesystem, process, HTTP server...
```

<p align="justify">Non studiamo quindi un nuovo linguaggio: studiamo un nuovo <strong>runtime</strong> e nuove API.</p>

---

## 2. Il processo Node

<p align="justify">Quando eseguiamo:</p>

```bash
node server.mjs
```

<p align="justify">il sistema operativo avvia un processo Node.</p>

<p align="justify">Nel programma possiamo leggere informazioni dal runtime:</p>

```js
console.log(process.version);
console.log(process.platform);
console.log(process.pid);
```

<p align="justify">E possiamo leggere configurazione esterna:</p>

```js
const port = Number(process.env.PORT ?? 3000);
```

<p align="justify">Questa separazione è importante.</p>

<p align="justify">Evitiamo:</p>

```js
const productionPassword = "segreto";
```

<p align="justify">Preferiamo il principio:</p>

```text
codice       -> repository
configurazione -> environment
segreti      -> secret management / environment protetto
```

<p align="justify">I segreti verranno approfonditi nella parte sicurezza.</p>

---

## 3. npm e package.json

<p align="justify"><code>npm</code> è il package manager normalmente distribuito insieme a Node.js.</p>

<p align="justify">Un progetto può dichiarare la propria identità e le dipendenze in <code>package.json</code>:</p>

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

<p align="justify">Per il corso usiamo una versione Express <strong>pinned</strong> per rendere gli esempi riproducibili.</p>

### dependencies e devDependencies

<p align="justify">In modo semplificato:</p>

```text
dependencies
  -> servono all'applicazione a runtime

devDependencies
  -> strumenti necessari allo sviluppo/test/build
```

<p align="justify">Non aggiungiamo pacchetti senza motivo.</p>

<p align="justify">Ogni dipendenza:</p>

<ul>
  <li>aumenta il codice di terze parti;</li>
  <li>deve essere aggiornata;</li>
  <li>può avere vulnerabilità;</li>
  <li>rende l'applicazione più complessa da riprodurre.</li>
</ul>

---

## 4. ES modules anche nel backend

<p align="justify">Nel corso usiamo ES modules come modello principale.</p>

<p align="justify">Con:</p>

```json
{
  "type": "module"
}
```

<p align="justify">possiamo scrivere:</p>

```js
import express from "express";
import { randomUUID } from "node:crypto";
```

<p align="justify">ed esportare:</p>

```js
export function validatePostInput(value) {
  // ...
}
```

<p align="justify">Perché preferiamo un solo modello iniziale?</p>

<p align="justify">Per ridurre context switching fra browser e backend:</p>

```text
browser modules -> import/export
Node modules    -> import/export
```

<p align="justify">CommonJS (<code>require</code>, <code>module.exports</code>) verrà comunque riconosciuto quando incontreremo codice legacy.</p>

---

## 5. Event loop: quanto ci serve davvero

<p align="justify">Non serve trasformare questa UDA in un corso sugli internals di V8/libuv.</p>

<p align="justify">Serve però capire perché questo server può gestire molte connessioni senza creare un thread JavaScript per ogni request.</p>

<p align="justify">Modello didattico minimo:</p>

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

<p align="justify">Il punto fondamentale è:</p>

<blockquote>
<p align="justify">non bloccare inutilmente il thread JavaScript con lavoro sincrono lungo.</p>
</blockquote>

<p align="justify">Quindi:</p>

```js
const data = await loadSomething();
```

<p align="justify">non significa "Node si ferma completamente".</p>

<p align="justify">La funzione sospende la propria continuazione mentre il runtime può gestire altro lavoro.</p>

---

<a id="lesson-node-http"></a>
## 6. Apriamo la fixture: node:http

<p align="justify">Un server minimale può essere costruito senza Express:</p>

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

<p align="justify">Riconosciamo immediatamente concetti di UDA 23:</p>

```text
req.method       -> HTTP method
req.url          -> target
req.headers      -> request headers
res.statusCode   -> response status
res.setHeader    -> response headers
res.end          -> termina response
```

### Leggere il body

<p align="justify">Nel server HTTP nativo il body arriva come stream.</p>

<p align="justify">Un esempio minimale:</p>

```js
let body = "";

for await (const chunk of req) {
  body += chunk;
}

const value = JSON.parse(body);
```

<p align="justify">Subito emergono problemi reali:</p>

<ul>
  <li>dimensione massima del body;</li>
  <li>JSON invalido;</li>
  <li><code>Content-Type</code> sbagliato;</li>
  <li>routing;</li>
  <li>parametri dinamici;</li>
  <li>static files;</li>
  <li>logging;</li>
  <li>error handling;</li>
  <li>middleware comuni.</li>
</ul>

<p align="justify">Potremmo implementare tutto a mano.</p>

<p align="justify">Ma finiremmo per costruire un framework.</p>

---

## 7. Perché Express

<p align="justify">Express ci fornisce un modello semplice per organizzare il request-response cycle.</p>

<p align="justify">Nel corso usiamo <strong>Express 5.x</strong>.</p>

<p align="justify">Esempio equivalente:</p>

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

<p align="justify">Il protocollo non cambia:</p>

```text
GET /api/health
       -> 200 application/json

GET /missing
       -> 404 application/json
```

<p align="justify">Cambia il modo in cui organizziamo il codice.</p>

---

<a id="lesson-express-pipeline"></a>
## 8. Middleware: la pipeline della request

<p align="justify">Una funzione middleware riceve normalmente:</p>

```js
(req, res, next)
```

<p align="justify">Può:</p>

<ul>
  <li>leggere request;</li>
  <li>modificare request/response;</li>
  <li>terminare il ciclo;</li>
  <li>chiamare <code>next()</code> per continuare.</li>
</ul>

<p align="justify">Esempio:</p>

```js
function requestLogger(req, res, next) {
  console.log(req.method, req.originalUrl);
  next();
}

app.use(requestLogger);
```

<p align="justify">Modello:</p>

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

### L'ordine è comportamento

<p align="justify">Queste due configurazioni non sono equivalenti:</p>

```js
app.use(express.json());
app.use("/api", apiRouter);
```

```js
app.use("/api", apiRouter);
app.use(express.json());
```

<p align="justify">Nel secondo caso le route del router vengono eseguite <strong>prima</strong> del parser JSON.</p>

<p align="justify">Quindi <code>req.body</code> non contiene ciò che ci aspettiamo.</p>

<p align="justify">Questo diventerà parte dell'Activity D.</p>

---

## 9. Middleware built-in utili

### JSON body parser

```js
app.use(express.json({ limit: "32kb" }));
```

<p align="justify">Non significa:</p>

<blockquote>
<p align="justify">ogni request del mondo contiene JSON.</p>
</blockquote>

<p align="justify">Significa:</p>

<blockquote>
<p align="justify">quando la request ha una representation JSON compatibile, Express può produrre <code>req.body</code>.</p>
</blockquote>

### Static files

```js
app.use(express.static("public"));
```

<p align="justify">Possiamo così servire il client Feisbuc dallo stesso origin della API.</p>

<p align="justify">Questo mantiene semplice la prima architettura:</p>

```text
http://localhost:3000/
http://localhost:3000/app.js
http://localhost:3000/api/posts
```

<p align="justify">Stesso scheme + host + port -> stesso origin.</p>

---

## 10. Router: separare le risorse

<p align="justify">Un'applicazione con tutto in <code>server.js</code> cresce male.</p>

<p align="justify">Creiamo un Router:</p>

```js
import { Router } from "express";

export const postsRouter = Router();

postsRouter.get("/", listPosts);
postsRouter.post("/", createPost);
postsRouter.patch("/:id", updatePost);
```

<p align="justify">E lo montiamo:</p>

```js
app.use("/api/posts", postsRouter);
```

<p align="justify">La composizione finale è:</p>

```text
/api/posts       + GET
/api/posts       + POST
/api/posts/:id   + PATCH
```

---

## 11. params, query e body

<p align="justify">UDA 23 ci ha già insegnato dove vivono i dati nella request.</p>

<p align="justify">Express li rende comodi da leggere.</p>

### Path parameter

<p align="justify">Request:</p>

```http
PATCH /api/posts/p-42
```

<p align="justify">Express:</p>

```js
req.params.id
```

### Query string

<p align="justify">Request:</p>

```http
GET /api/posts?liked=true
```

<p align="justify">Express:</p>

```js
req.query.liked
```

### JSON body

<p align="justify">Request:</p>

```http
POST /api/posts
Content-Type: application/json

{"text":"ciao"}
```

<p align="justify">Express:</p>

```js
req.body.text
```

<p align="justify">Questa è una <strong>proiezione conveniente del protocollo</strong>, non una nuova forma di comunicazione.</p>

---

<a id="lesson-express-boundaries"></a>
## 12. Validation: non fidarti del confine esterno

<p align="justify">Il client Feisbuc prova a inviare dati validi.</p>

<p align="justify">Ma il server non può assumere che ogni client sia corretto.</p>

<p align="justify">Una funzione pura di validation può essere:</p>

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

<p align="justify">Notare che questa funzione:</p>

<ul>
  <li>non conosce Express;</li>
  <li>non conosce HTTP;</li>
  <li>può essere testata deterministicamente;</li>
  <li>separa business rule da trasporto.</li>
</ul>

<p align="justify">Questa separazione prepara anche SQL e FastAPI.</p>

---

## 13. Error model

<p align="justify">Evitiamo error response casuali:</p>

```json
{"message":"male"}
```

<p align="justify">poi:</p>

```json
{"error":"qualcosa"}
```

<p align="justify">poi plain text.</p>

<p align="justify">Definiamo un formato semplice:</p>

```json
{
  "error": {
    "code": "post-text-required",
    "message": "Il testo del post e obbligatorio.",
    "requestId": "..."
  }
}
```

<p align="justify">Il codice macchina e il messaggio umano hanno ruoli diversi.</p>

### Status + error body

```text
400 -> request sintatticamente/semanticamente non valida
404 -> risorsa non trovata
415 -> media type non supportato
500 -> errore inatteso server
```

<p align="justify">La scelta precisa dipende dal contratto API, ma deve essere intenzionale.</p>

---

## 14. Error middleware

<p align="justify">Un error middleware Express ha <strong>quattro argomenti</strong>:</p>

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

<p align="justify">Anche se <code>next</code> non viene usato, la firma a quattro argomenti identifica il middleware come error handler.</p>

<p align="justify">Con Express 5, se un route handler <code>async</code> lancia un errore o restituisce una Promise rejected, l'errore può raggiungere automaticamente la pipeline di error handling.</p>

<p align="justify">Esempio:</p>

```js
router.get("/:id", async (req, res) => {
  const post = await repository.findById(req.params.id);

  if (!post) {
    throw new Error("post-not-found");
  }

  res.json(post);
});
```

<p align="justify">Più avanti distingueremo errori applicativi attesi dagli errori inattesi.</p>

---

## 15. Request ID e logging

<p align="justify">Quando una request attraversa più livelli è utile avere una identità.</p>

```js
import { randomUUID } from "node:crypto";

export function requestId(req, res, next) {
  req.requestId = randomUUID();
  res.setHeader("X-Request-Id", req.requestId);
  next();
}
```

<p align="justify">Un logger minimale:</p>

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

<p align="justify">Non è ancora observability completa.</p>

<p align="justify">Ma introduce il concetto:</p>

```text
una request
-> una identita
-> eventi correlabili
```

---

## 16. Configurazione dell'applicazione

<p align="justify">Evitiamo di spargere <code>process.env</code> ovunque.</p>

<p align="justify">Possiamo centralizzare:</p>

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

<p align="justify">Il server startup usa config.</p>

<p align="justify">L'applicazione HTTP non deve conoscere il modo in cui la configurazione è stata caricata.</p>

---

## 17. Separare app e server

<p align="justify">Pattern utile:</p>

```text
src/
  app.js
  server.js
```

### app.js

<p align="justify">Costruisce Express:</p>

```js
export function createApp(dependencies) {
  const app = express();
  // middleware + router
  return app;
}
```

### server.js

<p align="justify">Fa startup:</p>

```js
const app = createApp(...);
app.listen(port);
```

<p align="justify">Perché?</p>

<p align="justify">Perché possiamo testare <code>app</code> senza dover fissare una porta nel modulo che la costruisce.</p>

---

## 18. Dependency injection minimale

<p align="justify">Non serve un framework DI.</p>

<p align="justify">Basta non creare ogni dipendenza dentro ogni route.</p>

```js
export function createPostsRouter({ postStore }) {
  const router = Router();

  router.get("/", (req, res) => {
    res.json(postStore.list());
  });

  return router;
}
```

<p align="justify">Oggi <code>postStore</code> sarà in-memory.</p>

<p align="justify">Più avanti potrà diventare SQL.</p>

<p align="justify">Il router non deve cambiare completamente.</p>

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

<p align="justify">Questo è uno dei passaggi architetturali più importanti del corso.</p>

---

## 19. Feisbuc milestone 5: stessa API, nuovo backend

<p align="justify">In UDA 23 il client usava:</p>

```text
GET   /api/posts
POST  /api/posts
PATCH /api/posts/:id
```

<p align="justify">Questa milestone mantiene lo stesso contratto.</p>

<p align="justify">Cambia il server:</p>

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

<p align="justify">Il client dovrebbe quasi non accorgersene.</p>

<p align="justify">Questa è una proprietà desiderabile.</p>

<p align="justify">Un contratto stabile permette di evolvere l'implementazione.</p>

---

## 20. CORS: non usare cors() come superstizione

<p align="justify">Nel vecchio lab didattico il frontend e il backend potevano essere eseguiti su origin diversi e veniva aggiunto middleware CORS.</p>

<p align="justify">Nel Feisbuc attuale serviamo client e API dallo stesso server:</p>

```text
http://localhost:3000/
http://localhost:3000/api/posts
```

<p align="justify">Quindi il flusso principale è same-origin.</p>

<p align="justify">Non abbiamo bisogno di aggiungere CORS solo perché stiamo costruendo una API.</p>

<p align="justify">Quando frontend e backend saranno realmente cross-origin studieremo una policy esplicita:</p>

```text
quali origin?
quali metodi?
quali header?
credentials sì/no?
```

<p align="justify">Regola:</p>

<blockquote>
<p align="justify">CORS è una policy di accesso cross-origin del browser, non una decorazione obbligatoria delle API.</p>
</blockquote>

---

## 21. Cosa NON facciamo ancora

<p align="justify">Questa prima parte di UDA 24 non introduce ancora:</p>

<ul>
  <li>database;</li>
  <li>ORM;</li>
  <li>password;</li>
  <li>sessioni;</li>
  <li>JWT;</li>
  <li>Nunjucks;</li>
  <li>SSR completo;</li>
  <li>upload;</li>
  <li>deploy production.</li>
</ul>

<p align="justify">Lo storage è volutamente in memoria.</p>

<p align="justify">Perché?</p>

<p align="justify">Perché vogliamo poter attribuire ogni errore a uno strato preciso.</p>

<p align="justify">Se una POST non funziona, dobbiamo sapere se il problema è:</p>

```text
HTTP?
Express routing?
body parsing?
validation?
middleware order?
store?
```

<p align="justify">prima di aggiungere SQL.</p>

---

## 22. Errori frequenti

### 22.1 `express.json()` dopo il router

<p align="justify">Sintomo:</p>

```text
GET funziona
POST ha req.body undefined
```

<p align="justify">Domanda corretta:</p>

<blockquote>
<p align="justify">in quale ordine passa la request nei middleware?</p>
</blockquote>

---

### 22.2 Confondere params e query

<p align="justify">Route:</p>

```text
/api/posts/:id
```

<p align="justify">Errore:</p>

```js
req.query.id
```

<p align="justify">Corretto:</p>

```js
req.params.id
```

---

### 22.3 Error middleware con tre argomenti

<p align="justify">Errore:</p>

```js
function errorHandler(err, req, res) {}
```

<p align="justify">Express lo vede come middleware normale.</p>

<p align="justify">Corretto:</p>

```js
function errorHandler(err, req, res, next) {}
```

---

### 22.4 Non chiamare next()

<p align="justify">Un middleware che non termina la response e non chiama <code>next()</code> lascia il ciclo sospeso.</p>

---

### 22.5 Usare GET per modificare dati

<p align="justify">Se una route crea, modifica o cancella stato, GET è quasi certamente il metodo sbagliato.</p>

<p align="justify">Questo è un punto che correggiamo esplicitamente rispetto ad alcuni lab legacy.</p>

---

### 22.6 Mandare password nei log

<p align="justify">Nel vecchio materiale didattico alcune credenziali venivano stampate per mostrare il flusso.</p>

<p align="justify">Nel nuovo corso questa pratica diventa un anti-pattern esplicito.</p>

<p align="justify">La sicurezza verrà approfondita nella fase auth.</p>

---

## 23. Esercizi A-F

### A — osserva

<p align="justify">Confronta due server equivalenti:</p>

```text
node:http
Express
```

<p align="justify">Individua dove vivono:</p>

<ul>
  <li>method matching;</li>
  <li>path matching;</li>
  <li>JSON parsing;</li>
  <li>status;</li>
  <li>headers;</li>
  <li>404.</li>
</ul>

### B — modifica controllata

<p align="justify">Completa una funzione di validation pura per i post.</p>

<p align="justify">La funzione viene corretta deterministicamente senza avviare un server.</p>

### C — implementazione autonoma

<p align="justify">Costruisci Feisbuc milestone 5:</p>

```text
app.js
server.js
Router
middleware
validator
memory store
```

<p align="justify">mantenendo invariato il contratto REST di UDA 23.</p>

### D — debug

<p align="justify">Diagnostica una app Express in cui:</p>

<ul>
  <li>JSON parser è nell'ordine sbagliato;</li>
  <li>params/query sono confusi;</li>
  <li>l'error handler non ha la firma corretta;</li>
  <li>una route modifica dati con metodo improprio;</li>
  <li>il 404 middleware è posizionato male.</li>
</ul>

### E — mini-progetto futuro

<p align="justify">Sostituire il memory store con repository SQL senza cambiare il contratto HTTP.</p>

### F — prodotto integrato futuro

<p align="justify">Feisbuc con:</p>

<ul>
  <li>API;</li>
  <li>database;</li>
  <li>auth;</li>
  <li>frontend;</li>
  <li>realtime;</li>
  <li>test;</li>
  <li>deployment.</li>
</ul>

---

## 24. Verifica rapida

<ol>
  <li>Qual è la differenza fra ECMAScript e Node.js?</li>
  <li>Cosa indica <code>"type": "module"</code> in <code>package.json</code>?</li>
  <li>Perché <code>process.env</code> è preferibile a una configurazione hard-coded?</li>
  <li>Che cosa fa <code>next()</code>?</li>
  <li>Perché l'ordine dei middleware è importante?</li>
  <li>Qual è la differenza fra <code>req.params</code>, <code>req.query</code> e <code>req.body</code>?</li>
  <li>Perché validation e route handler non devono essere necessariamente la stessa funzione?</li>
  <li>Perché un error middleware Express ha quattro parametri?</li>
  <li>Perché non abilitiamo CORS automaticamente?</li>
  <li>Perché in questa milestone usiamo un memory store invece del database?</li>
</ol>

---

## 25. Sintesi inclusiva

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

<p align="justify">E soprattutto:</p>

```text
Express non inventa HTTP.
Express rende più gestibile implementare HTTP.
```

---

## 26. Fonti e approfondimenti

<p align="justify">Riferimenti tecnici primari:</p>

<ul>
  <li>Node.js documentation — runtime, process, modules, HTTP;</li>
  <li>Express 5.x documentation — application, Router, middleware, error handling;</li>
  <li>RFC 9110 — semantica HTTP già introdotta in UDA 23.</li>
</ul>

<p align="justify">Teacher-reference legacy auditata:</p>

<ul>
  <li><code>kinderp/lab5</code> — Express/fetch/CORS;</li>
  <li><code>kinderp/lab6</code> — form POST;</li>
  <li><code>kinderp/lab7</code> — query/path/body;</li>
  <li><code>kinderp/lab8</code> — Express + SQLite;</li>
  <li><code>kinderp/lab9</code> — register/login;</li>
  <li><code>kinderp/lab10</code> — Express + SQLite + Nunjucks.</li>
</ul>

<p align="justify">Il materiale legacy viene usato come provenance e confronto storico; esempi, architettura e soluzioni canoniche di questo corso sono riscritti.</p>

---

## 27. Prossimo passo

<p align="justify">La seconda parte di UDA 24 sostituirà:</p>

```text
MemoryPostStore
```

<p align="justify">con:</p>

```text
SQL raw repository
```

<p align="justify">mantenendo il più possibile invariati:</p>

```text
client
HTTP contract
Router
validation
error model
```

<p align="justify">Solo dopo aggiungeremo auth sicura e il breve confronto SSR/template.</p>
