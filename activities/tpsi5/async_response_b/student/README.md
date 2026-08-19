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
- `isJson` deve riconoscere `application/json` anche quando il media type contiene parametri come `charset`;
- JSON e successo sono concetti indipendenti;
- la funzione deve attraversare almeno un confine asincrono con Promise/`await`;
- in questa Activity non usare `fetch`: stiamo isolando la logica di interpretazione della Response.

## Esecuzione manuale

```bash
echo '{"status":404,"contentType":"application/json"}' | node main.js
```

## Perche prima di fetch?

Perche nella prossima Activity vogliamo poter leggere:

```js
const response = await fetch(url);
```

sapendo gia che cosa fare con `status`, `ok` e `Content-Type`.
