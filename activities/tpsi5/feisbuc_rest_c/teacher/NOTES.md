# Note docente — Feisbuc milestone 4

## Obiettivo concettuale

Non valutare "quanto codice fetch" scrive lo studente. Valutare se mantiene questo boundary:

```text
DOM/state temporaneo -> app.js -> api.js -> HTTP -> server
```

## Osservazioni attese

- il feed iniziale arriva con GET;
- POST restituisce `201` e una representation gia completa di `id`;
- PATCH restituisce la representation aggiornata;
- il client non ricostruisce localmente `likes` dopo una modifica riuscita: usa la risposta del server come nuova fonte di verita;
- `requestJson` interpreta `Content-Type` e `response.ok`;
- `catch` gestisce anche gli errori che `requestJson` trasforma da status HTTP a `Error` JavaScript.

## Domande guida

- "Perche il server restituisce il post creato invece di solo OK?"
- "Perche app.js non deve sapere come si costruisce la request POST?"
- "Che differenza c'e fra 404 e server spento?"
- "Se il POST risponde 201, perche non aggiungiamo un id generato dal browser?"
- "Che cosa succede se Content-Type non e application/json?"

## Confine con UDA 24

Non fare code review del server come esercizio backend. Possiamo aprire brevemente `server.mjs` per mostrare che esiste un server HTTP reale, ma routing, parsing e struttura server diventano oggetto didattico nell'UDA successiva.
