---
marp: true
paginate: true
size: 16:9
title: 05 — HTTP, asincronia, Fetch e REST
---

# 05 — HTTP, asincronia, Fetch e REST
## Dal browser a una API

UDA 23 — Web protocols and APIs

---

# Richiamo

Nel modulo 04 Feisbuc viveva tutto nel browser:

```text
stato JS -> render -> Local Storage
```

Ora vogliamo dati condivisi tra client diversi.

Serve un contratto di rete.

---

# Obiettivi

Alla fine dovrai saper:

- leggere request e response HTTP;
- distinguere method, URL, status, header e body;
- usare `fetch` e `async/await`;
- gestire errori di rete e di protocollo;
- leggere un contratto REST;
- ispezionare traffico con DevTools.

---

# HTTP: messaggi, non magia

Request:

```text
POST /posts HTTP/1.1
Content-Type: application/json

{"text":"Ciao"}
```

Response:

```text
HTTP/1.1 201 Created
Content-Type: application/json

{"id":42,"text":"Ciao"}
```

---

# Le parti della request

```text
METHOD + URL
headers
body opzionale
```

Esempi di method:

- `GET` — leggere;
- `POST` — creare/attivare;
- `PATCH` — modifica parziale;
- `DELETE` — eliminare.

---

# Gli status code sono parte del contratto

- `200 OK` — successo;
- `201 Created` — risorsa creata;
- `204 No Content` — successo senza body;
- `400 Bad Request` — input non valido;
- `401 Unauthorized` — autenticazione mancante/non valida;
- `403 Forbidden` — identità nota ma operazione vietata;
- `404 Not Found` — risorsa assente;
- `500` — errore server.

---

# fetch: prima osservare la Response

```js
const response = await fetch('/api/posts');

if (!response.ok) {
  throw new Error(`HTTP ${response.status}`);
}

const posts = await response.json();
```

`fetch` non lancia automaticamente un errore per ogni status HTTP non-2xx.

---

# POST JSON

```js
const response = await fetch('/api/posts', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({ text })
});
```

Qui stiamo costruendo esplicitamente il contratto client → server.

---

# Asincronia

```js
async function loadPosts() {
  const response = await fetch('/api/posts');
  const posts = await response.json();
  renderPosts(posts);
}
```

`await` sospende quella funzione, non l'intero browser.

Il punto importante è sapere **quando il dato è disponibile**.

---

# Due famiglie di errore

## Errore di trasporto/rete

- offline;
- DNS;
- connessione rifiutata.

## Errore HTTP

- `400`;
- `404`;
- `500`.

Sono problemi diversi e vanno diagnosticati diversamente.

---

# REST: risorse e contratto

Un possibile contratto Feisbuc:

```text
GET    /posts
POST   /posts
PATCH  /posts/:id
DELETE /posts/:id
```

REST non significa “URL belli”: significa usare in modo coerente semantica HTTP e risorse.

---

# Network panel

Con DevTools → Network controlla:

- method;
- URL;
- status;
- request headers;
- request payload;
- response headers;
- response body;
- timing.

È il microscopio principale per il boundary browser ↔ server.

---

# Errore tipico: `response.json()` senza policy

```js
const response = await fetch(url);
const data = await response.json();
```

Problemi:

- lo status potrebbe essere errore;
- la response potrebbe non essere JSON;
- il body potrebbe essere vuoto.

Prima definisci la policy, poi fai parsing.

---

# Checkpoint

Per ogni caso scegli lo status più adatto:

1. post creato;
2. JSON sintatticamente valido ma campo obbligatorio assente;
3. post inesistente;
4. utente non autenticato;
5. delete riuscita senza body.

---

# Feisbuc milestone

Il browser smette di essere la fonte definitiva dei dati.

```text
UI
→ fetch
→ API
→ response JSON
→ nuovo stato client
→ render
```

Il prossimo modulo implementerà il server che oggi stiamo solo consumando.

---

# Handoff al laboratorio

Durante le Activity:

1. osserva request/response reali;
2. scrivi una policy per `fetch`;
3. costruisci il client Feisbuc REST;
4. diagnostica status/body errati;
5. usa Network panel come evidenza.

---

# Recap

HTTP è il contratto esplicito tra componenti.

Da ricordare:

- method;
- URL;
- status;
- headers;
- body;
- policy client;
- osservabilità con Network.

Prossimo modulo: **Node.js ed Express 5**.