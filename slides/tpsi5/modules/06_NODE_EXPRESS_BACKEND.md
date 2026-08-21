---
marp: true
paginate: true
size: 16:9
title: 06 — Node.js ed Express 5
---

# 06 — Node.js ed Express 5
## Dal protocollo HTTP al backend

UDA 24 — Backend

---

# Richiamo

Nel modulo 05 abbiamo scritto un client che invia request HTTP.

Ora costruiamo il componente che riceve quelle request.

```text
browser -> HTTP -> ? -> store
```

Quel `?` diventa il nostro backend.

---

# Obiettivi

Alla fine dovrai saper:

- distinguere Node.js da Express;
- leggere un server `node:http` minimale;
- spiegare Router e middleware;
- validare input;
- separare route, dominio e store;
- costruire una pipeline di errore prevedibile.

---

# Node.js

Node.js esegue JavaScript fuori dal browser.

Non porta con sé DOM o CSS.

Porta invece API per:

- rete;
- filesystem;
- processi;
- moduli;
- runtime server-side.

---

# HTTP senza framework

```js
import http from 'node:http';

const server = http.createServer((req, res) => {
  if (req.method === 'GET' && req.url === '/posts') {
    res.writeHead(200, { 'Content-Type': 'application/json' });
    res.end(JSON.stringify([]));
    return;
  }

  res.writeHead(404);
  res.end();
});
```

Questo ci fa vedere il protocollo senza astrazioni.

---

# Perché Express?

Express riduce codice ripetitivo per:

- routing;
- middleware;
- body parsing;
- error handling;
- modularizzazione.

Ma non cambia HTTP: lo rende più comodo da esprimere.

---

# Prima route Express

```js
import express from 'express';

const app = express();
app.use(express.json());

app.get('/posts', async (req, res) => {
  const posts = await postStore.list();
  res.json(posts);
});
```

Il contratto HTTP resta lo stesso del client.

---

# Router

```js
const router = express.Router();

router.get('/', listPosts);
router.post('/', createPost);

app.use('/posts', router);
```

Il Router raccoglie endpoint di uno stesso dominio senza trasformare tutto il server in un file unico.

---

# Middleware

Un middleware vive nella pipeline:

```text
request
→ middleware A
→ middleware B
→ route
→ response
```

Esempi:

- logging;
- auth;
- parsing;
- validation;
- policy cross-cutting.

---

# Validazione

```js
function parseCreatePost(body) {
  if (!body || typeof body.text !== 'string') {
    throw new ValidationError('text required');
  }

  const text = body.text.trim();
  if (!text) throw new ValidationError('text empty');

  return { text };
}
```

Il backend non deve fidarsi del client.

---

# Dependency boundary: PostStore

```js
class MemoryPostStore {
  async list() { ... }
  async create(input) { ... }
}
```

La route non deve sapere **come** salviamo i dati.

Oggi memoria. Nel prossimo modulo SQLite.

---

# Error pipeline

```js
app.use((err, req, res, next) => {
  if (err instanceof ValidationError) {
    res.status(400).json({ error: err.message });
    return;
  }

  console.error(err);
  res.status(500).json({ error: 'internal_error' });
});
```

Errore previsto ≠ crash casuale.

---

# Errore tipico: tutto nella route

```js
app.post('/posts', async (req, res) => {
  // validation
  // business rules
  // SQL
  // auth
  // rendering
  // logging
});
```

Funziona all'inizio, poi diventa ingestibile.

Separare responsabilità è parte del design.

---

# Checkpoint

Dove metteresti:

1. parsing JSON;
2. controllo `text` obbligatorio;
3. salvataggio post;
4. logging request;
5. mapping ValidationError → 400;
6. mapping `/posts` → controller.

---

# Feisbuc milestone

Feisbuc ora ha una vera API server-side:

```text
client REST
→ Express Router
→ validation
→ PostStore
→ response JSON
```

Il prossimo problema: la memoria sparisce al riavvio.

---

# Handoff al laboratorio

Durante le Activity:

1. confronta `node:http` ed Express;
2. implementa/leggi una route;
3. valida input;
4. inietta uno store;
5. diagnostica un errore nella pipeline.

---

# Recap

Express è utile perché rende espliciti e modulari:

- route;
- middleware;
- validation;
- error handling;
- dependency boundary.

Prossimo modulo: **SQL raw e persistenza**.