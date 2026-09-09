# Diagnosi fetch/HTTP

Compila **prima di modificare `client.js`**.

Ripeti questa scheda per **GET missing**, **POST broken** e **204 no content**:

### Caso: …

- Sintomo osservato:
- Evidenze in Network e Console:
- Metodo e status, oppure assenza di Response:
- Causa nel client:
- Categoria del problema:
- Fix minimo proposto:
- Verifica e prova di regressione:

## Domande

1. In quale caso `fetch()` ha ricevuto una Response HTTP valida anche se il risultato era negativo?
2. Quale bug riguarda il metadata `Content-Type`?
3. Quale bug riguarda i bytes/body inviati?
4. Perché `response.json()` non è un'operazione sempre valida?
5. Quale errore è veramente di rete e quale è HTTP?
