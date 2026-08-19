# Note docente — Express debug

## Sequenza suggerita

1. far provare solo `GET /api/posts` per avere un controllo funzionante;
2. mostrare che `/` 404 non significa che Express "non serve HTML";
3. POST e `/:id` evidenziano due errori di mapping distinti;
4. discutere il GET mutante come errore semantico HTTP, non come bug di sintassi;
5. chiudere con `/explode` e firma a quattro argomenti dell'error handler.

## Valutazione

Premiare la diagnosi con evidence (`status`, `Content-Type`, route, ordine middleware) prima della correzione.

Penalizzare il fix casuale del tipo "sposto righe finche funziona" senza modello della pipeline.

## Collegamento a Express 5

L'handler `/explode` e `async`: Express 5 inoltra la Promise rejected alla pipeline. Se lo studente aggiunge `try/catch` solo per farlo funzionare, chiedere perche sta duplicando una responsabilita gia prevista dal framework.
