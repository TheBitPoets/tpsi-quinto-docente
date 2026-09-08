# HTTP, asincronia, Fetch e REST

<table align="center" width="100%"><tr><td>
<details>
<summary>&#128506; <strong>Orientamento della lezione</strong></summary>

<p align="justify"><strong>Contesto:</strong> il Feisbuc dinamico conserva ancora lo stato in un solo browser. Per condividerlo dobbiamo comprendere il contratto request/response prima dei framework che lo rendono più comodo da programmare.</p>
<p align="justify"><strong>Domande guida:</strong> quali informazioni viaggiano in request e response? Come esprimono intento e risultato metodi e status? Perché <code>fetch()</code> non tratta automaticamente uno status 4xx/5xx come errore di rete?</p>
<p align="justify"><strong>Obiettivi osservabili:</strong> leggere uno scambio HTTP nei DevTools, progettare endpoint orientati a risorse, usare Promise e <code>async</code>/<code>await</code> e gestire correttamente una <code>Response</code>.</p>
<p align="justify"><strong>Prossimo passo:</strong> la lezione 06 aprirà il server e implementerà lo stesso contratto con Node.js ed Express 5.</p>

</details>
</td></tr></table>

## Obiettivi

<p align="justify">Al termine del modulo lo studente deve saper:</p>

<ul>
  <li>leggere una richiesta e una risposta HTTP distinguendo metodo, target, header, content e status;</li>
  <li>spiegare che HTTP definisce semantica request/response indipendentemente dal framework server;</li>
  <li>scegliere metodi e status code coerenti con l'intento dell'operazione;</li>
  <li>distinguere path, query string, header e body;</li>
  <li>interpretare <code>Content-Type</code> e JSON come rappresentazione, non come sinonimi di HTTP;</li>
  <li>spiegare statelessness, safe/idempotent in modo operativo;</li>
  <li>leggere una chiamata asincrona come <code>Promise</code> e riscriverla con <code>async</code>/<code>await</code>;</li>
  <li>usare <code>fetch()</code> senza confondere errore HTTP con errore di rete;</li>
  <li>controllare <code>response.ok</code>, status e content type prima di interpretare la risposta;</li>
  <li>progettare una piccola API REST orientata a risorse;</li>
  <li>usare DevTools Network e <code>curl</code> per osservare il protocollo;</li>
  <li>distinguere same-origin e cross-origin e spiegare il ruolo di CORS;</li>
  <li>trasformare Feisbuc da applicazione con <code>localStorage</code> a client di una API HTTP.</li>
</ul>

## Prerequisiti

<ul>
  <li>UDA 21: HTML, CSS, Bootstrap;</li>
  <li>UDA 22: JavaScript, moduli ES, DOM, eventi, stato e <code>localStorage</code>;</li>
  <li>concetto generale di client e server.</li>
</ul>

## Orientamento nella documentazione

<p align="center">
  <img src="../../assets/tpsi5/lesson-documentation-depth.svg" alt="La dispensa seleziona nelle fonti ufficiali i contenuti da studiare ora, riconoscere, rimandare o dichiarare fuori confine">
</p>

<table align="center"><tr><td>
<p align="justify"><strong><span style="font-size: 1.15em;">&#128279;</span> Percorso MDN — HTTP e Fetch:</strong> usa la <a href="GUIDA_USO_MDN.md#mdn-guide-http">checklist per le reference HTTP</a> e la <a href="GUIDA_USO_MDN.md#mdn-guide-js-api">checklist per le Web API</a>. Qui MDN serve a collegare ciò che osservi nel pannello Network con il contratto usato da JavaScript.</p>
<ul>
  <li><strong>Studia:</strong> <a href="https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Methods">metodi HTTP</a> e <a href="https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Status">status code</a>, aprendo le singole schede quando serve un dettaglio;</li>
  <li><strong>studia:</strong> <a href="https://developer.mozilla.org/en-US/docs/Web/API/Fetch_API/Using_Fetch">Using the Fetch API</a>, in particolare richiesta, risposta, controllo dello status e lettura del body;</li>
  <li><strong>consulta:</strong> le reference di <a href="https://developer.mozilla.org/en-US/docs/Web/API/Window/fetch"><code>fetch()</code></a>, <a href="https://developer.mozilla.org/en-US/docs/Web/API/Request"><code>Request</code></a> e <a href="https://developer.mozilla.org/en-US/docs/Web/API/Response"><code>Response</code></a> per sintassi, proprietà e valori restituiti.</li>
</ul>
<p align="justify"><strong>Prodotto atteso:</strong> scegli una richiesta del Feisbuc, annota metodo, URL, header, body, status e rappresentazione; collega ogni campo alla sezione MDN che ne chiarisce il significato.</p>
</td></tr></table>

<table align="center"><tr><td>
<details>
<summary>&#128279; <strong>Indice incrociato — HTTP, Fetch e REST ↔ fonti ufficiali</strong></summary>

<table align="center">
<thead><tr><th>Dispensa</th><th>Documentazione ufficiale</th><th>Profondità</th></tr></thead>
<tbody>
<tr><td><a href="#lesson-http-messages">Request, response e messaggi</a></td><td><a href="https://developer.mozilla.org/en-US/docs/Web/HTTP/Guides/Overview">MDN — Overview of HTTP</a><br><a href="https://www.rfc-editor.org/rfc/rfc9110">RFC 9110</a></td><td>&#128994; MDN ora; RFC come riferimento</td></tr>
<tr><td><a href="#lesson-http-semantics">Metodi, status e rappresentazioni</a></td><td><a href="https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Methods">HTTP methods</a><br><a href="https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Status">HTTP status codes</a></td><td>&#128994; studiare ora</td></tr>
<tr><td><a href="#lesson-fetch-api">Promise, Fetch e Response</a></td><td><a href="https://developer.mozilla.org/en-US/docs/Web/API/Fetch_API/Using_Fetch">Using the Fetch API</a><br><a href="https://fetch.spec.whatwg.org/">Fetch Standard</a></td><td>&#128994; MDN ora; standard per precisione</td></tr>
<tr><td><a href="#lesson-rest-resources">Risorse e REST API</a></td><td><a href="https://developer.mozilla.org/en-US/docs/Glossary/REST">MDN — REST</a></td><td>&#128994; studiare ora</td></tr>
<tr><td>Streaming, service worker e cache avanzata</td><td><a href="https://developer.mozilla.org/en-US/docs/Web/API/Fetch_API">Fetch API</a></td><td>&#128993; riconoscere o studiare più avanti</td></tr>
</tbody>
</table>

</details>
</td></tr></table>

## Problema iniziale

<p align="justify">Nella milestone precedente Feisbuc conserva i post nel browser:</p>

```text
browser
   |
   +-- JavaScript state
   |
   +-- localStorage
```

<p align="justify">Funziona, ma solo su quel browser.</p>

<p align="justify">Se apriamo Feisbuc da un altro computer non vediamo gli stessi dati.</p>

<p align="justify">Per condividere lo stato serve un altro componente:</p>

```text
browser                         server
   |                               |
   | ------ richiesta HTTP ------> |
   |                               |
   | <------ risposta HTTP ------- |
```

<p align="justify">La domanda di questa UDA è:</p>

<blockquote>
<p align="justify">Che cosa viene realmente scambiato fra client e server prima ancora di parlare di Express, FastAPI o Vue?</p>
</blockquote>

<p align="justify">La risposta è il contratto HTTP.</p>

---

<a id="lesson-http-messages"></a>
## 1. HTTP prima dei framework

<p align="justify">HTTP è un protocollo request/response.</p>

<p align="justify">Un client invia una richiesta che esprime un intento verso una risorsa; il server interpreta quell'intento e produce una risposta.</p>

<p align="justify">Modello mentale:</p>

```text
REQUEST
method + target + headers + content
                |
                v
              SERVER
                |
                v
RESPONSE
status + headers + content
```

<p align="justify">Express non crea questo modello: lo rende più comodo da programmare.</p>

### 1.1 Una richiesta osservabile

<p align="justify">Esempio concettuale:</p>

```http
POST /api/posts HTTP/1.1
Host: localhost:3000
Content-Type: application/json
Accept: application/json

{"text":"Primo post via API"}
```

<p align="justify">La stessa informazione può essere costruita dal browser con <code>fetch()</code> o da <code>curl</code>.</p>

### 1.2 Una risposta osservabile

```http
HTTP/1.1 201 Created
Content-Type: application/json
Location: /api/posts/p3

{"id":"p3","text":"Primo post via API","likes":0,"liked":false}
```

<p align="justify">Non bisogna leggere solo il JSON: anche <code>201</code>, <code>Content-Type</code> e <code>Location</code> fanno parte del contratto.</p>

---

## 2. URL, path, query, header, body

<p align="justify">Questi canali non sono intercambiabili.</p>

```text
http://localhost:3000/api/posts?author=ada&limit=10
|---- origin --------| |-- path -| |---- query -------|
```

### 2.1 Path

<p align="justify">Il path identifica normalmente la risorsa o la collezione:</p>

```text
/api/posts
/api/posts/p42
```

### 2.2 Query string

<p align="justify">La query modifica la vista o la selezione senza cambiare l'identità di base della risorsa:</p>

```text
/api/posts?author=ada
/api/posts?limit=10
```

### 2.3 Header

<p align="justify">Gli header trasportano metadati e controllo del protocollo:</p>

```text
Accept: application/json
Content-Type: application/json
Authorization: ...        # verra approfondito piu avanti
```

### 2.4 Body/content

<p align="justify">Il content contiene una rappresentazione da elaborare:</p>

```json
{
  "text": "Nuovo post"
}
```

<p align="justify">Nel vecchio <code>lab7</code> query, path parameter e body erano gia presenti; nel nuovo corso vengono prima letti come parti della request HTTP e solo dopo verranno mappati a <code>req.query</code>, <code>req.params</code> e <code>req.body</code> in Express.</p>

---

<a id="lesson-http-semantics"></a>
## 3. Metodi HTTP: intento, non CRUD meccanico

<p align="justify">Per il core del corso:</p>

<table align="center">
<thead>
<tr>
<th>Metodo</th>
<th>Intenzione tipica</th>
</tr>
</thead>
<tbody>
<tr>
<td><code>GET</code></td>
<td>leggere una rappresentazione</td>
</tr>
<tr>
<td><code>POST</code></td>
<td>creare/processare secondo la semantica della risorsa</td>
</tr>
<tr>
<td><code>PUT</code></td>
<td>sostituire la rappresentazione di una risorsa</td>
</tr>
<tr>
<td><code>PATCH</code></td>
<td>applicare una modifica parziale</td>
</tr>
<tr>
<td><code>DELETE</code></td>
<td>rimuovere una risorsa</td>
</tr>
<tr>
<td><code>HEAD</code></td>
<td>come GET, ma senza trasferire il content della rappresentazione</td>
</tr>
<tr>
<td><code>OPTIONS</code></td>
<td>descrivere opzioni di comunicazione</td>
</tr>
</tbody>
</table>

<p align="justify">Non insegniamo la falsa regola:</p>

```text
GET = SELECT
POST = INSERT
PUT = UPDATE
DELETE = DELETE SQL
```

<p align="justify">HTTP non e SQL.</p>

### 3.1 Safe e idempotent

<p align="justify">Due concetti utili per ragionare sulle API:</p>

<ul>
  <li><strong>safe</strong>: il client non richiede un cambiamento di stato sul server;</li>
  <li><strong>idempotent</strong>: ripetere la stessa richiesta intenzionale una o piu volte deve avere lo stesso effetto previsto della singola richiesta.</li>
</ul>

<p align="justify">Esempi operativi:</p>

```text
GET     safe + idempotent
PUT     non safe + idempotent
DELETE  non safe + idempotent nella semantica dell'intento
POST    non e garantito idempotent
```

<p align="justify">Questa distinzione diventa importante con retry, cache e sistemi distribuiti.</p>

---

## 4. Status code: il risultato appartiene al protocollo

<p align="justify">Lo status code non e decorazione.</p>

<p align="justify">Le classi principali:</p>

```text
1xx  informational
2xx  successo
3xx  redirezione
4xx  problema attribuito alla richiesta/client
5xx  errore del server nell'elaborare una richiesta apparentemente valida
```

<p align="justify">Per Feisbuc useremo soprattutto:</p>

<table align="center">
<thead>
<tr>
<th>Status</th>
<th>Uso didattico</th>
</tr>
</thead>
<tbody>
<tr>
<td><code>200 OK</code></td>
<td>lettura o modifica con representation in risposta</td>
</tr>
<tr>
<td><code>201 Created</code></td>
<td>nuova risorsa creata</td>
</tr>
<tr>
<td><code>204 No Content</code></td>
<td>successo senza content</td>
</tr>
<tr>
<td><code>400 Bad Request</code></td>
<td>request non interpretabile/valida</td>
</tr>
<tr>
<td><code>404 Not Found</code></td>
<td>risorsa non trovata</td>
</tr>
<tr>
<td><code>405 Method Not Allowed</code></td>
<td>metodo noto ma non ammesso sulla risorsa</td>
</tr>
<tr>
<td><code>415 Unsupported Media Type</code></td>
<td>representation inviata con media type non supportato</td>
</tr>
<tr>
<td><code>500 Internal Server Error</code></td>
<td>errore non gestito lato server</td>
</tr>
</tbody>
</table>

<p align="justify">Regola didattica:</p>

<blockquote>
<p align="justify">Prima interpretiamo lo status, poi il payload.</p>
</blockquote>

---

## 5. Representation e Content-Type

<p align="justify">HTTP trasferisce representation.</p>

<p align="justify">JSON e una possibile representation, non il protocollo.</p>

```http
Content-Type: application/json
```

<p align="justify">significa che il content della message e JSON.</p>

<p align="justify">Se inviamo JSON con <code>fetch</code>:</p>

```js
await fetch("/api/posts", {
  method: "POST",
  headers: {
    "Content-Type": "application/json"
  },
  body: JSON.stringify({ text: "Ciao" })
});
```

<p align="justify">Le due parti hanno ruoli diversi:</p>

```text
Content-Type       descrive i byte inviati
JSON.stringify()   produce una stringa JSON
```

<p align="justify">Dimenticarne una delle due e un bug diverso.</p>

---

## 6. Statelessness

<p align="justify">HTTP e stateless a livello di semantica del protocollo: ogni request deve poter essere interpretata nel proprio contesto senza assumere una conversazione nascosta nel protocollo stesso.</p>

<p align="justify">Questo non significa che una applicazione non possa mantenere stato.</p>

<p align="justify">Lo stato puo vivere, per esempio:</p>

```text
database
sessione server
cookie/token
cache
browser state
```

<p align="justify">Cookie e session verranno approfonditi nell'UDA backend/auth.</p>

---

## 7. Osservare HTTP con DevTools e curl

<p align="justify">Prima di programmare <code>fetch</code>, osserviamo richieste vere.</p>

<p align="justify">Esempio:</p>

```bash
curl -i http://localhost:3000/api/posts
```

<p align="justify">Per inviare JSON:</p>

```bash
curl -i \
  -X POST \
  -H "Content-Type: application/json" \
  -H "Accept: application/json" \
  -d '{"text":"Post da curl"}' \
  http://localhost:3000/api/posts
```

<p align="justify">Nel pannello <strong>Network</strong> del browser cerchiamo sempre:</p>

```text
Request URL
Request Method
Status Code
Request Headers
Request Payload
Response Headers
Response / Preview
Timing
```

<p align="justify">Il browser diventa uno strumento di protocol analysis, non solo un visualizzatore della pagina.</p>

---

<a id="lesson-fetch-api"></a>
## 8. Dal callback alla Promise

<p align="justify">Una operazione asincrona termina in futuro.</p>

<p align="justify">Invece di bloccare il programma:</p>

```text
start request
   |
   +---- il programma continua
   |
response disponibile
   |
callback/promise continuation
```

<p align="justify">Una <code>Promise</code> rappresenta un risultato futuro.</p>

<p align="justify">Stati concettuali:</p>

```text
pending
  |
  +--> fulfilled
  |
  +--> rejected
```

<p align="justify">Esempio:</p>

```js
fetch("/api/posts")
  .then((response) => response.json())
  .then((posts) => console.log(posts))
  .catch((error) => console.error(error));
```

<p align="justify">Il problema non e che <code>.then()</code> sia sbagliato: il problema e leggere pipeline lunghe senza rendere evidente il flusso e la gestione errori.</p>

---

## 9. async/await

<p align="justify">Una funzione <code>async</code> restituisce una Promise.</p>

```js
const loadPosts = async () => {
  const response = await fetch("/api/posts");
  return response.json();
};
```

<p align="justify">Con <code>try/catch</code>:</p>

```js
const loadPosts = async () => {
  try {
    const response = await fetch("/api/posts");
    // qui manca ancora un controllo fondamentale
    return await response.json();
  } catch (error) {
    console.error(error);
    throw error;
  }
};
```

<p align="justify">Quale controllo manca?</p>

<p align="justify"><code>response.ok</code>.</p>

---

## 10. fetch(): errore di rete != errore HTTP

<p align="justify">Questa e una delle idee piu importanti dell'UDA.</p>

```js
const response = await fetch("/api/posts/manca");
```

<p align="justify">Se il server risponde <code>404</code>, abbiamo comunque ricevuto una risposta HTTP.</p>

<p align="justify">Per questo il codice robusto controlla:</p>

```js
if (!response.ok) {
  throw new Error(`HTTP ${response.status}`);
}
```

<p align="justify">Poi interpreta il content.</p>

### 10.1 Helper minimo

```js
const requestJson = async (url, options = {}) => {
  const response = await fetch(url, options);

  const contentType = response.headers.get("content-type") ?? "";
  const isJson = contentType.includes("application/json");
  const payload = isJson ? await response.json() : null;

  if (!response.ok) {
    const message = payload?.error ?? `HTTP ${response.status}`;
    throw new Error(message);
  }

  return payload;
};
```

<p align="justify">Notare l'ordine:</p>

```text
fetch
 -> response
 -> content type
 -> payload
 -> response.ok
 -> risultato oppure errore applicativo
```

---

## 11. Abort e timeout applicativo

<p align="justify">Una request non dovrebbe necessariamente restare pendente per sempre.</p>

<p align="justify">Pattern:</p>

```js
const controller = new AbortController();
const timer = setTimeout(() => controller.abort(), 5000);

try {
  const response = await fetch("/api/posts", {
    signal: controller.signal
  });
  // ...
} finally {
  clearTimeout(timer);
}
```

<p align="justify">Per il core basta capire:</p>

<ul>
  <li>abort e timeout applicativo sono decisioni del client;</li>
  <li>un timeout non e uno status HTTP;</li>
  <li>non va confuso <code>500</code> con una mancata connessione.</li>
</ul>

---

<a id="lesson-rest-resources"></a>
## 12. REST: modellare risorse

<p align="justify">REST non significa soltanto usare JSON con quattro verbi.</p>

<p align="justify">Nel core usiamo una regola pratica:</p>

<blockquote>
<p align="justify">URL descrive la risorsa; metodo descrive l'intento; status descrive il risultato; representation descrive i dati.</p>
</blockquote>

<p align="justify">Per Feisbuc:</p>

```text
GET   /api/posts
POST  /api/posts
GET   /api/posts/p42
PATCH /api/posts/p42
```

<p align="justify">Esempi:</p>

```text
GET /api/posts
-> lista dei post

POST /api/posts
{ "text": "Ciao" }
-> 201 + nuova representation

PATCH /api/posts/p42
{ "liked": true }
-> 200 + representation aggiornata
```

### 12.1 Endpoint orientati alle azioni

<p align="justify">Un endpoint come:</p>

```text
POST /api/likePost42
```

<p align="justify">lega URL e azione in modo rigido.</p>

<p align="justify">Per il nostro modello preferiamo:</p>

```text
PATCH /api/posts/p42
{ "liked": true }
```

<p align="justify">Non e una legge universale: e una scelta di design coerente con una risorsa <code>post</code>.</p>

---

## 13. Query e filtri

<p align="justify">Per leggere subset di una collezione:</p>

```text
GET /api/posts?author=ada
GET /api/posts?limit=10
```

<p align="justify">Non useremo un body GET per passare filtri ordinari.</p>

---

## 14. Error model della API

<p align="justify">Una API didattica deve avere errori prevedibili.</p>

<p align="justify">Formato scelto:</p>

```json
{
  "error": "post-not-found",
  "message": "Il post richiesto non esiste"
}
```

<p align="justify">Il client non deve cercare stringhe casuali nell'HTML di errore.</p>

---

## 15. Same-origin e CORS

<p align="justify">Origin comprende schema, host e porta.</p>

<p align="justify">Quindi:</p>

```text
http://localhost:3000
http://localhost:5173
```

<p align="justify">sono origin diverse perche cambia la porta.</p>

<p align="justify">Il protocollo CORS appartiene al modello Fetch/browser e decide quando una risposta cross-origin puo essere esposta allo script chiamante.</p>

<p align="justify">Strategia didattica:</p>

<ol>
  <li>prima Feisbuc e API sono same-origin, cosi HTTP resta il problema principale;</li>
  <li>poi facciamo un micro-esperimento cross-origin;</li>
  <li>osserviamo <code>Origin</code>, eventuale preflight <code>OPTIONS</code> e header <code>Access-Control-Allow-*</code>;</li>
  <li>solo dopo, in Express, vedremo middleware/librerie che configurano CORS.</li>
</ol>

<p align="justify">Non insegniamo:</p>

```text
CORS = problema del server che blocca Internet
```

<p align="justify">ma:</p>

```text
browser + origin policy + protocol CORS
```

---

## 16. Caching: concetto minimo

<p align="justify">HTTP prevede meccanismi di caching.</p>

<p align="justify">In questa UDA ci basta riconoscere che header come:</p>

```text
Cache-Control
ETag
If-None-Match
```

<p align="justify">possono cambiare se e quando una representation viene riusata.</p>

<p align="justify">La progettazione avanzata della cache resta nel track advanced/senior.</p>

---

## 17. Feisbuc milestone 4: da localStorage a API

<p align="justify">Prima:</p>

```text
UI
 |
app.js
 |
posts.js
 |
localStorage
```

<p align="justify">Dopo:</p>

```text
UI
 |
app.js
 |
api.js
 |
HTTP
 |
fixture server Node/http
 |
in-memory posts
```

<p align="justify">Il server e volutamente una fixture: in questa UDA non vogliamo ancora studiare routing e middleware server-side.</p>

### 17.1 Contratto

```text
GET /api/posts
-> 200 application/json

POST /api/posts
Content-Type: application/json
{ "text": "..." }
-> 201 + Location

PATCH /api/posts/:id
Content-Type: application/json
{ "liked": true|false }
-> 200
```

### 17.2 Responsabilita client

<p align="justify"><code>api.js</code>:</p>

```text
requestJson
getPosts
createPost
setLiked
```

<p align="justify"><code>app.js</code>:</p>

```text
DOM
loading state
submit
click delegation
render
error feedback
```

<p align="justify">Lo stato persistente non vive piu nel browser.</p>

---

## 18. Errori frequenti

### 18.1 `catch()` come unico controllo

```js
try {
  const response = await fetch(url);
  return await response.json();
} catch (error) {
  // pensa di avere gestito anche 404 e 500
}
```

<p align="justify">Manca <code>response.ok</code>.</p>

### 18.2 JSON senza stringify

```js
body: { text: "ciao" }
```

<p align="justify">non e un body JSON valido per <code>fetch</code>.</p>

### 18.3 Stringify senza Content-Type

<p align="justify">Il server riceve bytes JSON ma il metadata non dichiara correttamente il media type.</p>

### 18.4 Content-Type senza JSON

```js
headers: { "Content-Type": "application/json" },
body: new URLSearchParams(...)
```

<p align="justify">metadata e content non concordano.</p>

### 18.5 Parsing cieco

```js
const body = await response.json();
```

<p align="justify">non tutte le response devono avere JSON o content.</p>

### 18.6 Usare `200` per tutto

<p align="justify">Status code diversi esprimono semantica diversa.</p>

### 18.7 Confondere CORS con autenticazione

<p align="justify">CORS non e un sistema di login e non protegge una API da client non-browser.</p>

---

## 19. Metodo di debug HTTP/fetch

<p align="justify">Quando una richiesta fallisce:</p>

```text
1. La request e partita?
2. URL e method sono corretti?
3. Quali request headers?
4. Quale payload?
5. Quale status e arrivato?
6. Quale response Content-Type?
7. Quale response body?
8. response.ok e stato controllato?
9. C'e un errore di rete/CORS distinto dall'errore HTTP?
10. La UI rappresenta loading/error/success in modo coerente?
```

<p align="justify">DevTools Network viene prima delle modifiche casuali al codice.</p>

---

## 20. Esercizi A-F

### A — osserva

<p align="justify">Avvia la fixture HTTP e confronta con <code>curl -i</code>:</p>

<ul>
  <li><code>GET /api/posts</code>;</li>
  <li><code>GET /api/posts/missing</code>;</li>
  <li><code>POST /api/posts</code> JSON;</li>
  <li>richiesta con <code>Content-Type</code> sbagliato.</li>
</ul>

<p align="justify">Annota method, status, header e body.</p>

### B — modifica controllata

<p align="justify">Completa una funzione asincrona che interpreta metadata di una Response distinguendo:</p>

<ul>
  <li><code>ok</code>;</li>
  <li>classe status;</li>
  <li>presenza di content;</li>
  <li>JSON/non JSON.</li>
</ul>

### C — implementazione autonoma

<p align="justify">Porta Feisbuc milestone 3 da <code>localStorage</code> a API HTTP.</p>

### D — debug

<p align="justify">Correggi un client che:</p>

<ul>
  <li>non controlla <code>response.ok</code>;</li>
  <li>invia object senza <code>JSON.stringify</code>;</li>
  <li>usa <code>Content-Type</code> incoerente;</li>
  <li>interpreta qualunque response come JSON;</li>
  <li>confonde errore HTTP e network error.</li>
</ul>

### E — mini-progetto

<p align="justify">Estendi API/client con filtro <code>?liked=true</code> o <code>?limit=n</code>, documentando contract e status.</p>

### F — prodotto integrato

<p align="justify">Verrà completato nelle UDA successive quando la fixture server verra sostituita dal backend Express con database e auth.</p>

---

## 21. Verifica rapida

<ol>
  <li>Quali sono le quattro parti che vogliamo riconoscere in una request HTTP?</li>
  <li>Perche <code>GET /posts?id=7</code> e <code>GET /posts/7</code> non esprimono necessariamente lo stesso design?</li>
  <li>Che cosa comunica <code>Content-Type</code>?</li>
  <li>Perche <code>fetch()</code> con response 404 non deve essere trattato come una semplice eccezione di rete?</li>
  <li>Quando <code>response.ok</code> e vero?</li>
  <li>Differenza fra <code>201</code> e <code>200</code> nel nostro POST <code>/api/posts</code>?</li>
  <li>Che cosa significa idempotent?</li>
  <li>Perche CORS entra in gioco con <code>localhost:3000</code> e <code>localhost:5173</code>?</li>
  <li>Perche <code>JSON.stringify</code> e <code>Content-Type: application/json</code> servono a problemi diversi?</li>
  <li>Quale componente sostituisce <code>localStorage</code> nella milestone 4 di Feisbuc?</li>
</ol>

---

## 22. Sintesi inclusiva

```text
HTTP
 |
 +-- request
 |    +-- method
 |    +-- target
 |    +-- headers
 |    +-- content
 |
 +-- response
      +-- status
      +-- headers
      +-- content

Promise / async-await
        |
        v
      fetch
        |
        +-- network error -> reject
        |
        +-- HTTP response -> Response
                               |
                               +-- status
                               +-- ok
                               +-- headers
                               +-- body

REST
URL = risorsa
method = intento
status = risultato
representation = dati
```

---

## 23. Fonti e provenance

<p align="justify">Fonti tecniche/professionali:</p>

<ul>
  <li>RFC 9110 — HTTP Semantics;</li>
  <li>WHATWG Fetch Standard;</li>
  <li>Node.js HTTP documentation per la fixture didattica;</li>
  <li>MDN Web Docs come documentazione professionale per studenti;</li>
  <li>ECMAScript Language Specification per Promise/async functions quando serve risalire allo standard.</li>
</ul>

<p align="justify">Teacher-reference legacy auditate:</p>

<ul>
  <li><code>kinderp/lab5</code> snapshot <code>b518922bf346ffe6402d67806acf4c5bc78916b9</code>;</li>
  <li><code>kinderp/lab6</code> snapshot <code>79f4d056958b083b70f75b178ef08f00b3f902a8</code>;</li>
  <li><code>kinderp/lab7</code> snapshot <code>b4ee8a661d0127d5dc92254e5b3bc0a24b6075e5</code>;</li>
  <li><code>TheBitPoets/labs_summary</code> snapshot gia registrato nel Content Pack.</li>
</ul>

<p align="justify">I lab legacy sono usati come provenance e confronto storico; codice, esempi e struttura del nuovo modulo sono riscritti.</p>

---

## 24. Activity correlate

<ul>
  <li><code>tpsi5-activity-a-http-microscope-001</code>;</li>
  <li><code>tpsi5-activity-b-async-response-policy-001</code>;</li>
  <li><code>tpsi5-activity-c-feisbuc-rest-client-001</code>;</li>
  <li><code>tpsi5-activity-d-debug-fetch-http-001</code>.</li>
</ul>

## Prossimo passo

<p align="justify">UDA 24 prende il server-fixture che qui trattiamo come black box e lo apre:</p>

```text
Node.js runtime
 -> native http server
 -> npm/package.json
 -> Express
 -> routing
 -> middleware
 -> validation/error handling
 -> persistence
 -> auth / SSR
```
