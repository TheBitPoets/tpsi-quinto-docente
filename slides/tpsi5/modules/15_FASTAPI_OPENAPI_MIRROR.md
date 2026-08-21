---
marp: true
paginate: true
size: 16:9
title: 15 — FastAPI e OpenAPI mirror
---

# 15 — FastAPI e OpenAPI
## Stesso dominio, un altro modo di esprimere la API

UDA 26 — Python mirror

---

# Perché un mirror Python?

Non costruiamo un secondo Feisbuc completo.

Usiamo Python per confrontare:

- stesso contratto HTTP;
- validation diversa;
- tooling diverso;
- stessi boundary architetturali.

---

# Obiettivi

Alla fine dovrai saper:

- leggere una route FastAPI;
- usare modelli Pydantic;
- capire validation e response model;
- leggere OpenAPI generato;
- confrontare Express e FastAPI;
- verificare il contratto con TestClient.

---

# Route equivalente

Express:

```js
app.get('/posts', async (req, res) => {
  res.json(await store.list());
});
```

FastAPI:

```py
@app.get('/posts', response_model=list[PostOut])
def list_posts():
    return store.list()
```

---

# Pydantic

```py
class PostCreate(BaseModel):
    text: str
```

Il modello rende esplicito il contratto atteso in input.

---

# Validation

Se il body non rispetta il modello, FastAPI/Pydantic producono una risposta di errore strutturata.

Il punto didattico:

> la validation può essere espressa in modi diversi, ma il boundary resta lo stesso.

---

# Response model

```py
class PostOut(BaseModel):
    id: int
    text: str
```

```py
@app.get('/posts', response_model=list[PostOut])
```

La risposta dichiarata diventa parte del contratto e della documentazione.

---

# OpenAPI

FastAPI genera uno schema OpenAPI dal codice dichiarativo.

Puoi osservare:

- path;
- method;
- request schema;
- response schema;
- status.

---

# Mirror ≠ duplicazione

Non replichiamo:

- tutta auth/session;
- tutto realtime;
- ogni feature frontend.

Replichiamo abbastanza per confrontare il boundary HTTP e poi la persistenza/testing/runtime.

---

# TestClient

```py
def test_list_posts(client):
    response = client.get('/posts')
    assert response.status_code == 200
    assert response.json() == []
```

Testiamo il contratto HTTP, non solo una funzione interna.

---

# Errore tipico: confrontare solo la sintassi

Domanda debole:

> “Quale route è più corta?”

Domanda utile:

> “Dove vive validation? Come viene espresso il response contract? Come lo testiamo?”

---

# Checkpoint

Confronta Express e FastAPI per:

1. routing;
2. parsing body;
3. validation;
4. response schema;
5. documentazione API;
6. test HTTP.

---

# Feisbuc mirror 01

Obiettivo:

```text
GET /posts
POST /posts
```

con contratto equivalente alla baseline Node dove previsto.

---

# Handoff al laboratorio

1. leggi una route FastAPI;
2. modifica un modello;
3. osserva OpenAPI;
4. prova input valido/non valido;
5. verifica con TestClient.

---

# Recap

Il mirror ci mostra che:

- i framework cambiano;
- il protocollo resta;
- validation e schema possono essere più dichiarativi;
- il test del boundary resta fondamentale.

Prossimo modulo: **SQLAlchemy 2.0 e persistenza**.