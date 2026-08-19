# Activity E — Feisbuc milestone 2

Obiettivo: rifattorizzare la shell Feisbuc dalla soluzione CSS nativa a Bootstrap 5.3 mantenendo semantica, responsive design e accessibilita.

## Definition of done

La consegna e completa quando:

- Bootstrap 5.3.x e caricato e la versione usata e documentata;
- la pagina usa `container`, `row` e colonne responsive;
- il layout e a una colonna sui viewport stretti e 3/6/3 da `lg`;
- la navigazione usa una navbar responsive con collapse;
- il bundle JavaScript Bootstrap e incluso per il collapse;
- ogni post resta un `article` ed usa il componente card;
- le azioni usano button Bootstrap;
- almeno una utility Flexbox e almeno una utility di spacing sono usate con uno scopo chiaro;
- `custom.css` non contiene `display: grid`, `display: flex`, `@media`, `!important` o layout rigido;
- non ci sono `style="..."` inline;
- `MAPPING.md` contiene almeno sei mapping completi;
- la gerarchia heading e gli elementi semantici restano corretti.

## Procedura suggerita

1. Apri lo starter e osservalo a viewport stretto e largo.
2. Leggi `custom.css`: individua quali regole descrivono il prodotto e quali il layout generico.
3. Inserisci Bootstrap seguendo la documentazione ufficiale.
4. Sostituisci prima il macro-layout con container/grid.
5. Trasforma la navigazione in navbar responsive.
6. Trasforma i post in card mantenendo `article`.
7. Sostituisci i pattern locali semplici con utility.
8. Elimina dal CSS custom le regole ora delegate al framework.
9. Compila `MAPPING.md` mentre lavori, non alla fine a memoria.
10. Verifica da tastiera e con DevTools.

## CDN e laboratorio offline

Lo starter non include Bootstrap. Puoi usare i link CDN indicati nella lezione e nella documentazione ufficiale.

Se il laboratorio non ha accesso Internet, il docente puo fornire i file compilati di Bootstrap e indicare i path locali. Gli obiettivi e le classi usate non cambiano.

## Cose da non fare

- copiare una navbar dalla documentazione senza capire target/collapse;
- sostituire `article` con `div` solo perche l'esempio Bootstrap usa `div`;
- lasciare tutto il vecchio CSS e aggiungere Bootstrap sopra;
- usare `!important` per vincere la cascade;
- aggiungere decine di utility senza saperle spiegare;
- modificare il layout solo per farlo sembrare corretto a una singola larghezza.

## Domande per la discussione

1. Quale parte del framework corrisponde piu direttamente a CSS Grid/Flexbox studiati prima?
2. Quale codice e diventato piu corto?
3. Quale codice e diventato meno esplicito?
4. Se domani Bootstrap venisse rimosso, sapresti ricostruire il layout con CSS nativo?
