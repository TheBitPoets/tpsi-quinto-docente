# Note docente — HTTP al microscopio

## Sequenza consigliata

1. prima `curl -i` senza guardare il codice server;
2. far nominare agli studenti le parti osservate;
3. soltanto dopo aprire `server.mjs` e mostrare che Node espone request/response HTTP senza Express;
4. ripetere uno dei casi nell'osservatore same-origin e in DevTools Network;
5. servire l'osservatore sulla porta 5173 e confrontare GET semplice e POST JSON con preflight.

## Risultati attesi

- `GET /api/posts` -> `200`, JSON;
- `GET /api/posts/missing` -> `404`, JSON error model;
- `POST /api/posts` con JSON -> `201`, `Location`, JSON;
- POST senza media type JSON -> `415`;
- JSON malformato -> `400`;
- metodo non ammesso -> `405` + `Allow`.
- il POST JSON cross-origin mostra prima `OPTIONS`, poi `201`, con gli header `Access-Control-Allow-*`;
- CORS viene applicato dal browser e non cambia il comportamento di `curl`.

## Domande chiave

- “Se il body contiene `{error: ...}`, dove sta formalmente il risultato HTTP?”
- “Se il server restituisce 404, la connessione ha funzionato?”
- “Perché 415 non è uguale a 400?”
- “Che cosa descrive Content-Type: il file, la rotta o il contenuto del messaggio?”
- “Perché CORS non impedisce a `curl` di interrogare l'API?”

## Non anticipare

Non spiegare ancora `req.params`, `req.body`, middleware o Router Express: il server è una fixture e serve a rendere osservabile il protocollo.
