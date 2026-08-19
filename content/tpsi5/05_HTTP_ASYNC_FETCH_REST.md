# HTTP, asincronia, Fetch e REST

## Obiettivi

Al termine del modulo lo studente deve saper:

- leggere una richiesta e una risposta HTTP distinguendo metodo, target, header, content e status;
- spiegare che HTTP definisce semantica request/response indipendentemente dal framework server;
- scegliere metodi e status code coerenti con l'intento dell'operazione;
- distinguere path, query string, header e body;
- interpretare `Content-Type` e JSON come rappresentazione, non come sinonimi di HTTP;
- spiegare statelessness, safe/idempotent in modo operativo;
- leggere una chiamata asincrona come `Promise` e riscriverla con `async`/`await`;
- usare `fetch()` senza confondere errore HTTP con errore di rete;
- controllare `response.ok`, status e content type prima di interpretare la risposta;
- progettare una piccola API REST orientata a risorse;
- usare DevTools Network e `curl` per osservare il protocollo;
- distinguere same-origin e cross-origin e spiegare il ruolo di CORS;
- trasformare Feisbuc da applicazione con `localStorage` a client di una API HTTP.

## Prerequisiti

- UDA 21: HTML, CSS, Bootstrap;
- UDA 22: JavaScript, moduli ES, DOM, eventi, stato e `localStorage`;
- concetto generale di client e server.

## Problema iniziale

Nella milestone precedente Feisbuc conserva i post nel browser:

```text
browser
   |
   +-- JavaScript state
   |
   +-- localStorage
```

Funziona, ma solo su quel browser.

Se apriamo Feisbuc da un altro computer non vediamo gli stessi dati.

Per condividere lo stato serve un altro componente:

```text
browser                         server
   |                               |
   | ------ richiesta HTTP ------> |
   |                               |
   | <------ risposta HTTP ------- |
```

La domanda di questa UDA è:

> Che cosa viene realmente scambiato fra client e server prima ancora di parlare di Express, FastAPI o Vue?

La risposta è il contratto HTTP.

---

# 1. HTTP prima dei framework

HTTP è un protocollo request/response.

Un client invia una richiesta che esprime un intento verso una risorsa; il server interpreta quell'intento e produce una risposta.

Modello mentale:

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

Express non crea questo modello: lo rende più comodo da programmare.

## 1.1 Una richiesta osservabile

Esempio concettuale:

```http
POST /api/posts HTTP/1.1
Host: localhost:3000
Content-Type: application/json
Accept: application/json

{"text":"Primo post via API"}
```

La stessa informazione può essere costruita dal browser con `fetch()` o da `curl`.

## 1.2 Una risposta osservabile

```http
HTTP/1.1 201 Created
Content-Type: application/json
Location: /api/posts/p3

{"id":"p3","text":"Primo post via API","likes":0,"liked":false}
```

Non bisogna leggere solo il JSON: anche `201`, `Content-Type` e `Location` fanno parte del contratto.

---

# 2. URL, path, query, header, body

Questi canali non sono intercambiabili.

```text
http://localhost:3000/api/posts?author=ada&limit=10
|---- origin --------| |-- path -| |---- query -------|
```

## 2.1 Path

Il path identifica normalmente la risorsa o la collezione:

```text
/api/posts
/api/posts/p42
```

## 2.2 Query string

La query modifica la vista o la selezione senza cambiare l'identità di base della risorsa:

```text
/api/posts?author=ada
/api/posts?limit=10
```

## 2.3 Header

Gli header trasportano metadati e controllo del protocollo:

```text
Accept: application/json
Content-Type: application/json
Authorization: ...        # verra approfondito piu avanti
```

## 2.4 Body/content

Il content contiene una rappresentazione da elaborare:

```json
{
  "text": "Nuovo post"
}
```

Nel vecchio `lab7` query, path parameter e body erano gia presenti; nel nuovo corso vengono prima letti come parti della request HTTP e solo dopo verranno mappati a `req.query`, `req.params` e `req.body` in Express.

---

# 3. Metodi HTTP: intento, non CRUD meccanico

Per il core del corso:

| Metodo | Intenzione tipica |
| --- | --- |
| `GET` | leggere una rappresentazione |
| `POST` | creare/processare secondo la semantica della risorsa |
| `PUT` | sostituire la rappresentazione di una risorsa |
| `PATCH` | applicare una modifica parziale |
| `DELETE` | rimuovere una risorsa |
| `HEAD` | come GET, ma senza trasferire il content della rappresentazione |
| `OPTIONS` | descrivere opzioni di comunicazione |

Non insegniamo la falsa regola:

```text
GET = SELECT
POST = INSERT
PUT = UPDATE
DELETE = DELETE SQL
```

HTTP non e SQL.

## 3.1 Safe e idempotent

Due concetti utili per ragionare sulle API:

- **safe**: il client non richiede un cambiamento di stato sul server;
- **idempotent**: ripetere la stessa richiesta intenzionale una o piu volte deve avere lo stesso effetto previsto della singola richiesta.

Esempi operativi:

```text
GET     safe + idempotent
PUT     non safe + idempotent
DELETE  non safe + idempotent nella semantica dell'intento
POST    non e garantito idempotent
```

Questa distinzione diventa importante con retry, cache e sistemi distribuiti.

---

# 4. Status code: il risultato appartiene al protocollo

Lo status code non e decorazione.

Le classi principali:

```text
1xx  informational
2xx  successo
3xx  redirezione
4xx  problema attribuito alla richiesta/client
5xx  errore del server nell'elaborare una richiesta apparentemente valida
```

Per Feisbuc useremo soprattutto:

| Status | Uso didattico |
| --- | --- |
| `200 OK` | lettura o modifica con representation in risposta |
| `201 Created` | nuova risorsa creata |
| `204 No Content` | successo senza content |
| `400 Bad Request` | request non interpretabile/valida |
| `404 Not Found` | risorsa non trovata |
| `405 Method Not Allowed` | metodo noto ma non ammesso sulla risorsa |
| `415 Unsupported Media Type` | representation inviata con media type non supportato |
| `500 Internal Server Error` | errore non gestito lato server |

Regola didattica:

> Prima interpretiamo lo status, poi il payload.

---

# 5. Representation e Content-Type

HTTP trasferisce representation.

JSON e una possibile representation, non il protocollo.

```http
Content-Type: application/json
```

significa che il content della message e JSON.

Se inviamo JSON con `fetch`:

```js
await fetch("/api/posts", {
  method: "POST",
  headers: {
    "Content-Type": "application/json"
  },
  body: JSON.stringify({ text: "Ciao" })
});
```

Le due parti hanno ruoli diversi:

```text
Content-Type       descrive i byte inviati
JSON.stringify()   produce una stringa JSON
```

Dimenticarne una delle due e un bug diverso.

---

# 6. Statelessness

HTTP e stateless a livello di semantica del protocollo: ogni request deve poter essere interpretata nel proprio contesto senza assumere una conversazione nascosta nel protocollo stesso.

Questo non significa che una applicazione non possa mantenere stato.

Lo stato puo vivere, per esempio:

```text
database
sessione server
cookie/token
cache
browser state
```

Cookie e session verranno approfonditi nell'UDA backend/auth.

---

# 7. Osservare HTTP con DevTools e curl

Prima di programmare `fetch`, osserviamo richieste vere.

Esempio:

```bash
curl -i http://localhost:3000/api/posts
```

Per inviare JSON:

```bash
curl -i \
  -X POST \
  -H "Content-Type: application/json" \
  -H "Accept: application/json" \
  -d '{"text":"Post da curl"}' \
  http://localhost:3000/api/posts
```

Nel pannello **Network** del browser cerchiamo sempre:

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

Il browser diventa uno strumento di protocol analysis, non solo un visualizzatore della pagina.

---

# 8. Dal callback alla Promise

Una operazione asincrona termina in futuro.

Invece di bloccare il programma:

```text
start request
   |
   +---- il programma continua
   |
response disponibile
   |
callback/promise continuation
```

Una `Promise` rappresenta un risultato futuro.

Stati concettuali:

```text
pending
  |
  +--> fulfilled
  |
  +--> rejected
```

Esempio:

```js
fetch("/api/posts")
  .then((response) => response.json())
  .then((posts) => console.log(posts))
  .catch((error) => console.error(error));
```

Il problema non e che `.then()` sia sbagliato: il problema e leggere pipeline lunghe senza rendere evidente il flusso e la gestione errori.

---

# 9. async/await

Una funzione `async` restituisce una Promise.

```js
const loadPosts = async () => {
  const response = await fetch("/api/posts");
  return response.json();
};
```

Con `try/catch`:

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

Quale controllo manca?

`response.ok`.

---

# 10. fetch(): errore di rete != errore HTTP

Questa e una delle idee piu importanti dell'UDA.

```js
const response = await fetch("/api/posts/manca");
```

Se il server risponde `404`, abbiamo comunque ricevuto una risposta HTTP.

Per questo il codice robusto controlla:

```js
if (!response.ok) {
  throw new Error(`HTTP ${response.status}`);
}
```

Poi interpreta il content.

## 10.1 Helper minimo

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

Notare l'ordine:

```text
fetch
 -> response
 -> content type
 -> payload
 -> response.ok
 -> risultato oppure errore applicativo
```

---

# 11. Abort e timeout applicativo

Una request non dovrebbe necessariamente restare pendente per sempre.

Pattern:

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

Per il core basta capire:

- abort e timeout applicativo sono decisioni del client;
- un timeout non e uno status HTTP;
- non va confuso `500` con una mancata connessione.

---

# 12. REST: modellare risorse

REST non significa soltanto usare JSON con quattro verbi.

Nel core usiamo una regola pratica:

> URL descrive la risorsa; metodo descrive l'intento; status descrive il risultato; representation descrive i dati.

Per Feisbuc:

```text
GET   /api/posts
POST  /api/posts
GET   /api/posts/p42
PATCH /api/posts/p42
```

Esempi:

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

## 12.1 Endpoint orientati alle azioni

Un endpoint come:

```text
POST /api/likePost42
```

lega URL e azione in modo rigido.

Per il nostro modello preferiamo:

```text
PATCH /api/posts/p42
{ "liked": true }
```

Non e una legge universale: e una scelta di design coerente con una risorsa `post`.

---

# 13. Query e filtri

Per leggere subset di una collezione:

```text
GET /api/posts?author=ada
GET /api/posts?limit=10
```

Non useremo un body GET per passare filtri ordinari.

---

# 14. Error model della API

Una API didattica deve avere errori prevedibili.

Formato scelto:

```json
{
  "error": "post-not-found",
  "message": "Il post richiesto non esiste"
}
```

Il client non deve cercare stringhe casuali nell'HTML di errore.

---

# 15. Same-origin e CORS

Origin comprende schema, host e porta.

Quindi:

```text
http://localhost:3000
http://localhost:5173
```

sono origin diverse perche cambia la porta.

Il protocollo CORS appartiene al modello Fetch/browser e decide quando una risposta cross-origin puo essere esposta allo script chiamante.

Strategia didattica:

1. prima Feisbuc e API sono same-origin, cosi HTTP resta il problema principale;
2. poi facciamo un micro-esperimento cross-origin;
3. osserviamo `Origin`, eventuale preflight `OPTIONS` e header `Access-Control-Allow-*`;
4. solo dopo, in Express, vedremo middleware/librerie che configurano CORS.

Non insegniamo:

```text
CORS = problema del server che blocca Internet
```

ma:

```text
browser + origin policy + protocol CORS
```

---

# 16. Caching: concetto minimo

HTTP prevede meccanismi di caching.

In questa UDA ci basta riconoscere che header come:

```text
Cache-Control
ETag
If-None-Match
```

possono cambiare se e quando una representation viene riusata.

La progettazione avanzata della cache resta nel track advanced/senior.

---

# 17. Feisbuc milestone 4: da localStorage a API

Prima:

```text
UI
 |
app.js
 |
posts.js
 |
localStorage
```

Dopo:

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

Il server e volutamente una fixture: in questa UDA non vogliamo ancora studiare routing e middleware server-side.

## 17.1 Contratto

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

## 17.2 Responsabilita client

`api.js`:

```text
requestJson
getPosts
createPost
setLiked
```

`app.js`:

```text
DOM
loading state
submit
click delegation
render
error feedback
```

Lo stato persistente non vive piu nel browser.

---

# 18. Errori frequenti

## 18.1 `catch()` come unico controllo

```js
try {
  const response = await fetch(url);
  return await response.json();
} catch (error) {
  // pensa di avere gestito anche 404 e 500
}
```

Manca `response.ok`.

## 18.2 JSON senza stringify

```js
body: { text: "ciao" }
```

non e un body JSON valido per `fetch`.

## 18.3 Stringify senza Content-Type

Il server riceve bytes JSON ma il metadata non dichiara correttamente il media type.

## 18.4 Content-Type senza JSON

```js
headers: { "Content-Type": "application/json" },
body: new URLSearchParams(...)
```

metadata e content non concordano.

## 18.5 Parsing cieco

```js
const body = await response.json();
```

non tutte le response devono avere JSON o content.

## 18.6 Usare `200` per tutto

Status code diversi esprimono semantica diversa.

## 18.7 Confondere CORS con autenticazione

CORS non e un sistema di login e non protegge una API da client non-browser.

---

# 19. Metodo di debug HTTP/fetch

Quando una richiesta fallisce:

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

DevTools Network viene prima delle modifiche casuali al codice.

---

# 20. Esercizi A-F

## A — osserva

Avvia la fixture HTTP e confronta con `curl -i`:

- `GET /api/posts`;
- `GET /api/posts/missing`;
- `POST /api/posts` JSON;
- richiesta con `Content-Type` sbagliato.

Annota method, status, header e body.

## B — modifica controllata

Completa una funzione asincrona che interpreta metadata di una Response distinguendo:

- `ok`;
- classe status;
- presenza di content;
- JSON/non JSON.

## C — implementazione autonoma

Porta Feisbuc milestone 3 da `localStorage` a API HTTP.

## D — debug

Correggi un client che:

- non controlla `response.ok`;
- invia object senza `JSON.stringify`;
- usa `Content-Type` incoerente;
- interpreta qualunque response come JSON;
- confonde errore HTTP e network error.

## E — mini-progetto

Estendi API/client con filtro `?liked=true` o `?limit=n`, documentando contract e status.

## F — prodotto integrato

Verrà completato nelle UDA successive quando la fixture server verra sostituita dal backend Express con database e auth.

---

# 21. Verifica rapida

1. Quali sono le quattro parti che vogliamo riconoscere in una request HTTP?
2. Perche `GET /posts?id=7` e `GET /posts/7` non esprimono necessariamente lo stesso design?
3. Che cosa comunica `Content-Type`?
4. Perche `fetch()` con response 404 non deve essere trattato come una semplice eccezione di rete?
5. Quando `response.ok` e vero?
6. Differenza fra `201` e `200` nel nostro POST `/api/posts`?
7. Che cosa significa idempotent?
8. Perche CORS entra in gioco con `localhost:3000` e `localhost:5173`?
9. Perche `JSON.stringify` e `Content-Type: application/json` servono a problemi diversi?
10. Quale componente sostituisce `localStorage` nella milestone 4 di Feisbuc?

---

# 22. Sintesi inclusiva

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

# 23. Fonti e provenance

Fonti tecniche/professionali:

- RFC 9110 — HTTP Semantics;
- WHATWG Fetch Standard;
- Node.js HTTP documentation per la fixture didattica;
- MDN Web Docs come documentazione professionale per studenti;
- ECMAScript Language Specification per Promise/async functions quando serve risalire allo standard.

Teacher-reference legacy auditate:

- `kinderp/lab5` snapshot `b518922bf346ffe6402d67806acf4c5bc78916b9`;
- `kinderp/lab6` snapshot `79f4d056958b083b70f75b178ef08f00b3f902a8`;
- `kinderp/lab7` snapshot `b4ee8a661d0127d5dc92254e5b3bc0a24b6075e5`;
- `TheBitPoets/labs_summary` snapshot gia registrato nel Content Pack.

I lab legacy sono usati come provenance e confronto storico; codice, esempi e struttura del nuovo modulo sono riscritti.

---

# 24. Activity correlate

- `tpsi5-activity-a-http-microscope-001`;
- `tpsi5-activity-b-async-response-policy-001`;
- `tpsi5-activity-c-feisbuc-rest-client-001`;
- `tpsi5-activity-d-debug-fetch-http-001`.

## Prossimo passo

UDA 24 prende il server-fixture che qui trattiamo come black box e lo apre:

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
