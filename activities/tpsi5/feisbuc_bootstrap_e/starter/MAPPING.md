# Mapping CSS nativo → Bootstrap

Compila almeno **sei righe sostanziali**.

| Problema | Soluzione CSS nativa precedente | Bootstrap scelto | Concetto CSS sottostante | Perché la scelta è adatta |
| --- | --- | --- | --- | --- |
| Esempio: gruppo azioni post | `.post-actions { display:flex; gap:... }` | `d-flex gap-2` | Flexbox + gap | pattern semplice e locale |
| 1 | | | | |
| 2 | | | | |
| 3 | | | | |
| 4 | | | | |
| 5 | | | | |
| 6 | | | | |

## Riflessione finale

1. Quale parte di `custom.css` hai potuto eliminare grazie al framework?
2. Quale regola hai scelto di mantenere custom e perché?
3. Quale classe Bootstrap hai dovuto cercare nella documentazione ufficiale?
4. Quale componente richiede il bundle JavaScript e per quale comportamento?

## Evidenze di verifica

| Viewport o prova | Risultato atteso | Risultato osservato | Correzione effettuata |
| --- | --- | --- | --- |
| 375 px | una colonna e navbar collassata | | |
| 991 px | ancora sotto `lg` | | |
| 992 px | layout 3/6/3 e navbar espansa | | |
| 1280 px | layout 3/6/3; confronto con la baseline | | |
| solo tastiera | ordine logico e toggler utilizzabile | | |
| zoom 200% | contenuti e comandi disponibili | | |
| bundle disabilitato | toggler non operativo | | |
