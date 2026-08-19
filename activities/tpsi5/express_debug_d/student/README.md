# Activity D — Debug della pipeline Express

## Setup

```bash
npm install
npm start
```

## Riproduci i sintomi prima del fix

### 1. Static file

```bash
curl -i http://127.0.0.1:3000/
```

Atteso dal prodotto: HTML `200`.

Starter: non succede.

### 2. GET lista

```bash
curl -i http://127.0.0.1:3000/api/posts
```

Questo endpoint funziona: usalo come controllo.

### 3. POST JSON

```bash
curl -i \
  -H "Content-Type: application/json" \
  -d '{"text":"Nuovo post"}' \
  http://127.0.0.1:3000/api/posts
```

Osserva status e `Content-Type` della risposta.

### 4. Path parameter

```bash
curl -i http://127.0.0.1:3000/api/posts/p1
```

Il post esiste, ma il server non lo trova.

### 5. GET che modifica stato

```bash
curl -i "http://127.0.0.1:3000/api/posts/create?text=Non+dovrebbe+essere+GET"
```

Poi ripeti la lista. Questo comportamento va eliminato, non "aggiustato".

### 6. Async error

```bash
curl -i http://127.0.0.1:3000/api/posts/explode
```

Express 5 inoltra l'errore async, ma il nostro handler custom non viene riconosciuto correttamente.

## Metodo

Per ogni sintomo:

```text
request
 -> status/header/body osservati
 -> punto della pipeline
 -> causa
 -> fix minimo
 -> stessa request dopo il fix
```

Non riscrivere l'app da zero.
