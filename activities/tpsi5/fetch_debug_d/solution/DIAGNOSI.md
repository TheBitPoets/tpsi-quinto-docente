# Diagnosi di riferimento

| Caso | Sintomo | Network/status | Causa | Categoria | Fix | Verifica |
| --- | --- | --- | --- | --- | --- | --- |
| GET missing | UI mostra `success:true` con payload errore | `404` | manca controllo `response.ok` | **HTTP error non trasformato in errore applicativo** | leggere payload e poi lanciare errore se `!response.ok` | UI mostra `kind:http`, status 404 |
| POST broken | server risponde errore | `415` prima della correzione | `Content-Type: text/plain` non descrive JSON e `body` riceve un object convertito implicitamente | **media type + serialization** | `Content-Type: application/json` + `JSON.stringify` | Network mostra JSON corretto e `201` |
| 204 no content | `response.json()` fallisce | `204` | il client tenta di parsare un body che non esiste | **response body policy** | per 204/205 restituisci `null` senza parsing | operazione termina come successo con result null |

## Idee chiave

- `fetch()` non rifiuta la Promise soltanto perche lo status e `404` o `500`: il client riceve una Response e deve interpretarne lo status.
- `Content-Type` descrive la representation; non serializza l'object JavaScript.
- `JSON.stringify()` serializza; non imposta l'header.
- `try/catch` distingue gli errori solo se il nostro codice trasforma un esito HTTP negativo in un errore JavaScript coerente.
- DevTools Network permette di distinguere immediatamente "request non partita", "risposta 4xx/5xx" e "parsing client fallito dopo una risposta riuscita".
