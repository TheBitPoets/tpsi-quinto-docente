# Feisbuc milestone 4 — REST client

## Avvio

```bash
node server.mjs
```

Apri l'URL stampato dal server, normalmente `http://127.0.0.1:3000`.

La fixture serve **sia** la pagina **sia** la API: il primo esercizio e same-origin.

## Contratto API

### Leggere il feed

```text
GET /api/posts
-> 200 application/json
```

### Creare un post

```text
POST /api/posts
Content-Type: application/json

{"text":"Nuovo post"}

-> 201 Created
Location: /api/posts/:id
```

### Aggiornare il like

```text
PATCH /api/posts/:id
Content-Type: application/json

{"liked":true}

-> 200 OK
```

## Architettura richiesta

```text
DOM / event delegation
        |
      app.js
        |
      api.js
        |
      fetch
        |
       HTTP
        |
   server fixture
```

Non deve piu esistere:

```text
app.js -> localStorage
```

## requestJson

Il tuo helper deve ragionare in questo ordine:

```text
await fetch
   ↓
Response
   ↓
Content-Type
   ↓
payload (JSON/text/nessuno)
   ↓
response.ok ?
   ├─ si -> ritorna payload
   └─ no -> Error utile
```

## DevTools obbligatorio

Verifica nel pannello Network almeno:

- GET iniziale;
- POST di un nuovo post;
- PATCH di un like.

Per ciascuno controlla method, status, request payload e response.

## Definition of done

- [ ] feed caricato via GET;
- [ ] POST crea il post e usa la representation restituita;
- [ ] PATCH aggiorna il like;
- [ ] nessun localStorage/sessionStorage;
- [ ] `api.js` non manipola il DOM;
- [ ] `app.js` non costruisce manualmente URL/status handling duplicato;
- [ ] response 4xx/5xx diventa un messaggio UI;
- [ ] testo utente scritto con `textContent`;
- [ ] loading state visibile/semanticamente rappresentato;
- [ ] Network panel usato per verificare le tre request.
