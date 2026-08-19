# Note docente — Feisbuc milestone 3

## Obiettivo architetturale

Il risultato visuale conta meno della separazione:

```text
posts.js    -> dominio/stato
storage.js  -> persistenza locale
app.js      -> DOM + eventi + orchestrazione
```

Non introdurre `fetch` durante questa Activity: serve a rendere osservabile la sostituzione `localStorage -> REST API` in UDA 23.

## Punti da osservare

### Event delegation

Il criterio non e solo "il nuovo pulsante funziona". Lo studente deve saper spiegare:

- bubbling;
- perche `#post-list` e stabile;
- `event.target.closest()`;
- `data-action` e `data-post-id`;
- differenza target/currentTarget.

### State/render

Chiedere dove vive il numero di like. La risposta desiderata e: nello state JavaScript; il DOM lo rappresenta.

### Sicurezza anticipata

Provare il testo:

```text
Ciao <strong>mondo</strong>
```

Deve comparire come testo. Non trasformiamo l'Activity in un modulo XSS, ma fissiamo subito l'abitudine `textContent` per input utente.

### Storage

Aprire Application/Storage di DevTools e mostrare che il valore e una stringa JSON. Corrompere manualmente il JSON e verificare il recovery.

## Alternative accettabili

- `append()` o `appendChild()`;
- rendering con `DocumentFragment`;
- naming differente dei moduli;
- nuova lista tramite spread o `unshift` su uno state locale, purche lo studente sappia motivare la scelta.

Non accettare come equivalente:

- listener registrato singolarmente su ogni like dopo ogni render senza comprenderne il costo/modello;
- id globali generati per ogni pulsante come unica identita del post;
- `innerHTML` con testo utente interpolato;
- salvataggio del DOM nello storage invece dei dati;
- backend/fetch anticipato.

## Collegamento con framework frontend

Dopo questa milestone possiamo mostrare che un framework componentizzato riduce lavoro manuale di rendering e sincronizzazione, ma non elimina i concetti di state, evento, identita e side effect.
