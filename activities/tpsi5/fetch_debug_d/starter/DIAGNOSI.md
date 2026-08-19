# Diagnosi fetch/HTTP

Compila **prima di modificare `client.js`**.

| Caso | Sintomo osservato | Network panel: status/method | Causa nel client | Categoria problema | Fix proposto | Come verifico |
| --- | --- | --- | --- | --- | --- | --- |
| GET missing | | | | | | |
| POST broken | | | | | | |
| 204 no content | | | | | | |

## Domande

1. In quale caso `fetch()` ha ricevuto una Response HTTP valida anche se il risultato era negativo?
2. Quale bug riguarda il metadata `Content-Type`?
3. Quale bug riguarda i bytes/body inviati?
4. Perche `response.json()` non e una operazione sempre valida?
5. Quale errore e veramente di rete e quale e HTTP?
