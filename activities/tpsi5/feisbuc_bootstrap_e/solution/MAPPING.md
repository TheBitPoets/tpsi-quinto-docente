# Mapping di riferimento CSS nativo → Bootstrap

| Problema | Soluzione CSS nativa precedente | Bootstrap scelto | Concetto CSS sottostante | Perché la scelta è adatta |
| --- | --- | --- | --- | --- |
| contenitore centrato | `width: min(...); margin-inline:auto` | `container` | max-width + margin/padding responsive | pattern globale standard |
| macro-layout | `display:grid` + media query | `row` + `col-12 col-lg-*` | layout responsive a colonne | esprime direttamente 1 colonna -> 3/6/3 |
| distanza fra colonne | `gap: 1rem` | `g-4` | gap/gutter | spacing coerente con la scala Bootstrap |
| azioni dei post | `display:flex; flex-wrap:wrap; gap` | `d-flex flex-wrap gap-2` | Flexbox + wrapping + gap | pattern locale semplice |
| post | border/background/padding custom | `article.card` + `card-body` | box model + componente visuale | mantiene article ma delega la presentazione |
| pulsanti | regole button custom | `btn btn-outline-*` | padding, border, states del componente | comportamento visuale standard |
| navigazione responsive | nav Flexbox + eventuale JS custom | `navbar navbar-expand-lg` + Collapse | Flexbox + breakpoint + toggle JS | evita di reimplementare il pattern |
| spaziatura feed | margin custom | `mb-3`, `py-4` | margin/padding | utility leggibile e locale |

## Inventario delle classi aggiuntive

La soluzione usa anche `bg-body`, `bg-body-tertiary`, `border-top`, `border-bottom`, `h-100`, `h4`, `h5`, `list-group*`, `ms-auto`, `mb-0`, `py-*`, `g-4` e `visually-hidden`. Sono classi Bootstrap intenzionali, non dettagli da lasciare senza spiegazione: vanno ricondotte rispettivamente a colori di sfondo, bordi, sizing, tipografia visuale, componente List group, margine logico automatico, spacing, gutter e contenuto accessibile nascosto visivamente.

## Evidenze di verifica di riferimento

| Viewport o prova | Risultato osservabile |
| --- | --- |
| 375 px | tre regioni in colonna; toggler visibile e menu apribile |
| 991 px | classi `col-12` attive; navbar ancora collassabile |
| 992 px | proporzione 3/6/3; navbar espansa |
| 1280 px | proporzione 3/6/3; confronto visivo con la baseline |
| solo tastiera | focus visibile e ordine coerente col DOM |
| zoom 200% | contenuti e comandi restano raggiungibili |
| bundle disabilitato | il pannello collassato non viene aperto dal toggler |

## Riflessione

1. Il vecchio Grid e la media query del macro-layout sono stati rimossi da `custom.css`.
2. Rimangono custom solo branding (`--feisbuc-brand`) e un vincolo di leggibilità specifico del profilo.
3. La navbar richiede il bundle JavaScript per il comportamento Collapse.
4. Se Bootstrap venisse rimosso, il mapping permette di ricostruire il comportamento usando i concetti CSS studiati nel modulo precedente.
