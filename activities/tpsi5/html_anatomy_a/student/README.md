# Activity A — Anatomia di un documento HTML moderno

Tempo indicativo: 30 minuti.

## Obiettivo

Partire da una pagina che il browser riesce gia a visualizzare e renderla un documento HTML moderno e consapevole, senza cambiare il contenuto mostrato.

## Procedura

1. Apri `index.html` nel browser.
2. Apri DevTools (`F12`) e osserva il pannello Elements/Inspector.
3. Apri il file nell'editor.
4. Aggiungi `<!doctype html>` come prima riga.
5. Imposta `lang="it"` sull'elemento `html`.
6. Aggiungi nel `head`:

```html
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
```

7. Ricarica la pagina.
8. Sostituisci il `div` con classe `header` con un vero elemento `header`.
9. Controlla che rimanga un solo `h1`.

## Cosa osservare

Dopo ogni modifica chiediti:

- il contenuto visibile e cambiato?
- la struttura del documento e cambiata?
- DevTools mostra gli elementi come li hai scritti?
- il browser ha aggiunto o corretto qualcosa automaticamente?

## Usa MDN come sviluppatore

Non cercare la soluzione completa. Cerca e verifica separatamente:

- `doctype`;
- elemento `html` e attributo `lang`;
- `meta charset`;
- viewport;
- elemento `header`.

Pagine di partenza:

- https://developer.mozilla.org/en-US/docs/Learn_web_development/Core/Structuring_content/Basic_HTML_syntax
- https://developer.mozilla.org/en-US/docs/Learn_web_development/Core/Structuring_content/Webpage_metadata

## Checklist consegna

- [ ] doctype presente;
- [ ] lingua impostata su italiano;
- [ ] UTF-8 dichiarato;
- [ ] viewport dichiarato;
- [ ] `title` presente;
- [ ] intestazione trasformata in `header`;
- [ ] un solo `h1`;
- [ ] nessun CSS;
- [ ] nessun JavaScript;
- [ ] so spiegare a voce la differenza tra `head` e `header`.
