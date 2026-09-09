# Interpreta una Response

Input su `stdin`:

```json
{
  "status": 404,
  "contentType": "application/json; charset=utf-8"
}
```

Output atteso:

```json
{
  "ok": false,
  "statusClass": "4xx",
  "isJson": true,
  "outcome": "http-error"
}
```

## Regole

- `ok` vale `true` soltanto per status 200–299;
- `statusClass` usa la prima cifra (`2xx`, `4xx`, ...);
- `isJson` deve riconoscere `application/json`, i parametri come `charset` e i media type con suffisso `+json`;
- JSON e successo sono concetti indipendenti;
- la funzione è pura e sincrona: non aggiungere Promise o `await` dove non esiste attesa;
- in questa Activity non usare `fetch`: stiamo isolando la policy sui metadati della Response.

## Esecuzione manuale

```bash
echo '{"status":404,"contentType":"application/json"}' | node main.js
```

## Perché prima di Fetch?

Perché nella prossima Activity vogliamo poter leggere:

```js
const response = await fetch(url);
```

sapendo già che cosa fare con `status`, `ok` e `Content-Type`. L'asincronia reale entra quando attendiamo la Response e consumiamo il body; non serve per calcolare una classe di status.
