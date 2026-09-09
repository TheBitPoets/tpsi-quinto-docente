# Activity E — Feisbuc milestone 2

Obiettivo: rifattorizzare la shell Feisbuc dalla soluzione CSS nativa a Bootstrap 5.3 mantenendo semantica, responsive design e accessibilità.

## Definition of done

La consegna è completa quando:

- Bootstrap 5.3.x è caricato e la versione usata è documentata;
- la pagina usa `container`, `row` e colonne responsive;
- il layout e a una colonna sui viewport stretti e 3/6/3 da `lg`;
- la navigazione usa una navbar responsive con collapse;
- il bundle JavaScript Bootstrap e incluso per il collapse;
- ogni post resta un `article` ed usa il componente card;
- le azioni usano button Bootstrap;
- almeno una utility Flexbox e almeno una utility di spacing sono usate con uno scopo chiaro;
- per il vincolo didattico di questa Activity, `custom.css` non contiene `display: grid`, `display: flex`, `@media`, `!important` o layout rigido;
- non ci sono `style="..."` inline;
- `MAPPING.md` contiene almeno sei mapping completi;
- la gerarchia heading e gli elementi semantici restano corretti;
- navbar, ordine di focus e contenuti sono verificati con la matrice di prova sottostante.

## Procedura suggerita

1. Apri lo starter a 375 px e 1280 px; salva una cattura della baseline per entrambe le viewport.
2. Leggi `custom.css`: individua quali regole descrivono il prodotto e quali il layout generico.
3. Inserisci Bootstrap seguendo la documentazione ufficiale.
4. Sostituisci prima il macro-layout con container/grid.
5. Trasforma la navigazione in navbar responsive.
6. Trasforma i post in card mantenendo `article`.
7. Sostituisci i pattern locali semplici con utility.
8. Elimina dal CSS custom le regole ora delegate al framework.
9. Compila `MAPPING.md` mentre lavori, non alla fine a memoria.
10. Ripeti le catture a 375 px e 1280 px, verifica da tastiera e con DevTools, quindi registra le evidenze nella matrice di prova.

## Matrice di prova obbligatoria

| Caso | Cosa verificare | Evidenza da annotare |
| --- | --- | --- |
| viewport 375 px | una colonna, nessun overflow, toggler visibile | esito e problema eventualmente corretto |
| viewport 1280 px | layout 3/6/3 e navbar espansa | confronto visivo con la baseline |
| viewport 991 px | stato immediatamente precedente a `lg` | numero di colonne e stato navbar |
| viewport 992 px | layout 3/6/3 e navbar espansa | classi attive osservate nei DevTools |
| tastiera | `Tab`, `Shift+Tab`, `Invio`, `Spazio` | ordine del focus e apertura/chiusura navbar |
| zoom 200% | contenuti e comandi ancora disponibili | esito, overflow o sovrapposizioni |
| bundle disabilitato | comportamento del toggler | sintomo e dipendenza identificata |

## Classi presenti nella soluzione di riferimento

Non devi memorizzarle tutte né sei obbligato a riprodurre ogni scelta. Usa l'inventario per evitare di incontrare classi mai spiegate:

- layout: `container`, `row`, `col-12`, `col-lg-3`, `col-lg-6`, `g-4`;
- navbar: `navbar`, `navbar-expand-lg`, `navbar-brand`, `navbar-toggler`, `navbar-toggler-icon`, `collapse`, `navbar-collapse`, `navbar-nav`, `nav-item`, `nav-link`, `ms-auto`;
- componenti: `card`, `card-body`, `card-title`, `card-text`, `list-group`, `list-group-flush`, `list-group-item`, `btn`, `btn-outline-primary`, `btn-outline-secondary`;
- utility e helper: `bg-body`, `bg-body-tertiary`, `border-top`, `border-bottom`, `h-100`, `h4`, `h5`, `mb-0`, `mb-3`, `py-3`, `py-4`, `d-flex`, `flex-wrap`, `gap-2`, `visually-hidden`.

## CDN e laboratorio offline

Lo starter non include Bootstrap. Puoi usare i link CDN indicati nella lezione e nella documentazione ufficiale.

Se il laboratorio non ha accesso Internet, il docente può fornire i file compilati di Bootstrap e indicare i path locali. Gli obiettivi e le classi usate non cambiano.

## Cose da non fare

- copiare una navbar dalla documentazione senza capire target/collapse;
- sostituire `article` con `div` solo perché l'esempio Bootstrap usa `div`;
- lasciare tutto il vecchio CSS e aggiungere Bootstrap sopra;
- usare `!important` per vincere la cascade senza aver identificato la dichiarazione vincente;
- aggiungere decine di utility senza saperle spiegare;
- modificare il layout solo per farlo sembrare corretto a una singola larghezza.

## Domande per la discussione

1. La grid predefinita di Bootstrap è implementata con Flexbox: in che cosa differisce da CSS Grid studiato prima?
2. Quale codice è diventato più corto?
3. Quale codice è diventato meno esplicito?
4. Se domani Bootstrap venisse rimosso, sapresti ricostruire il layout con CSS nativo?
