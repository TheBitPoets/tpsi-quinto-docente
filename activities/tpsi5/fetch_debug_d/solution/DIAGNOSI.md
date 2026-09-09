# Diagnosi di riferimento

### GET missing

- **Sintomo:** la UI mostra `success:true` con il payload d'errore.
- **Evidenza:** Network mostra una Response `404 application/json`.
- **Causa e categoria:** manca il controllo `response.ok`; è un **HTTP error** non trasformato in errore applicativo.
- **Fix:** leggere il payload e poi lanciare un errore con `kind: "http"` quando `!response.ok`.
- **Verifica:** la UI mostra `kind:http` e status 404; il GET della collezione continua a funzionare.

### POST broken

- **Sintomo:** il server rifiuta la creazione.
- **Evidenza:** Network mostra `415` prima della correzione.
- **Causa e categoria:** `Content-Type: text/plain` non descrive JSON e il body riceve un object convertito implicitamente; è un problema di **media type e serializzazione**.
- **Fix:** usare `Content-Type: application/json` insieme a `JSON.stringify()`.
- **Verifica:** Network mostra il JSON corretto e una Response `201`.

### 204 no content

- **Sintomo:** `response.json()` fallisce dopo una Response riuscita.
- **Evidenza:** Network mostra status `204` e nessun body.
- **Causa e categoria:** il client tenta di parsare una rappresentazione inesistente; è un problema di **response body policy**.
- **Fix:** quando `response.status === 204` o 205 restituire `null` senza parsing.
- **Verifica:** l'operazione termina come successo con risultato `null`; gli altri payload restano leggibili.

## Idee chiave

- `fetch()` non rifiuta la Promise soltanto perché lo status è `404` o `500`: il client riceve una Response e deve interpretarne lo status.
- `Content-Type` descrive la representation; non serializza l'object JavaScript.
- `JSON.stringify()` serializza; non imposta l'header.
- `try/catch` distingue gli errori solo se il nostro codice assegna categorie coerenti: `network-or-cors`, `abort`, `http`, `representation` oppure `runtime`.
- DevTools Network permette di distinguere immediatamente "request non partita", "risposta 4xx/5xx" e "parsing client fallito dopo una risposta riuscita".
