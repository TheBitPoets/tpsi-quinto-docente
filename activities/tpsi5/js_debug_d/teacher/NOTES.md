# Note docente — Activity D JavaScript debug

## Origine dei problemi

L'Activity deriva da pattern realmente presenti nel Feisbuc legacy:

- `event.preventDefault()` mentre il listener usa un parametro differente;
- counter globale per gli id dei like button;
- prima versione con listener registrati sui pulsanti esistenti;
- successivo passaggio a event delegation.

Lo starter aggiunge deliberatamente anche due debiti didattici utili da diagnosticare: storage senza JSON e input utente passato a `innerHTML`.

## Obiettivo

Valutare **diagnosi**, non solo correzione.

Chiedere allo studente di mostrare almeno:

- una eccezione e relativo stack;
- valore di `localStorage.getItem()`;
- NodeList dei like button prima/dopo la creazione di un post;
- `event.target` durante il bubbling;
- differenza fra valore nello state e testo del DOM nella soluzione finale.

## Errori di valutazione da evitare

Non assegnare il massimo solo perche l'app finale sembra funzionare. Un fix che registra listener dopo ogni render, nasconde errori con `try/catch` generico o usa `innerHTML` puo mascherare i sintomi senza risolvere il modello.

## Debrief consigliato

Confrontare tre fasi:

```text
legacy: button-id + DOM state
     ->
debug: causa/evidenza/fix
     ->
nuovo modello: post-id + app state + render + delegation
```

Questo prepara il passaggio a framework reattivi senza presentarli come magia.
