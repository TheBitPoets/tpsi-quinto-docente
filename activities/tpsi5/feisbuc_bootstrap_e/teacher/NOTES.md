# Note docente — Activity E Feisbuc Bootstrap

## Scopo

Questa Activity verifica che lo studente sappia **rifattorizzare** una soluzione CSS nativa in un framework senza perdere semantica, accessibilita e modello mentale.

Non valutare il numero assoluto di classi Bootstrap. Valutare la qualita delle scelte e la capacita di collegarle ai concetti CSS.

## Evidenze attese

- `container`, `row` e colonne responsive;
- proporzione desktop 3/6/3 da `lg`;
- navbar con toggler, target coerente e `bootstrap.bundle`;
- `article.card` per i post;
- button Bootstrap;
- utility Flexbox/spacing usate in modo leggibile;
- nessuna perdita di heading/landmark;
- `custom.css` minimo e senza reimplementazione di layout;
- almeno sei mapping sostanziali.

## Alternative accettabili

- `container-fluid` e una strategia di max-width motivata, se il risultato resta coerente;
- breakpoint diverso da `lg` solo se lo studente motiva la scelta e aggiorna il mapping; per la consegna standard usare `lg` rende il confronto uniforme;
- componenti Bootstrap equivalenti possono variare se semantica/accessibilita restano corrette.

## Uso CDN / offline

La soluzione di riferimento usa il CDN ufficialmente documentato per Bootstrap 5.3.8.

In laboratorio offline si possono distribuire i file compilati e sostituire i link CDN con path locali. Non penalizzare questa sostituzione: il requisito e usare Bootstrap 5.3.x, non un particolare CDN.

## Errori frequenti

- aggiungere Bootstrap ma lasciare attivo tutto il Grid/Flexbox custom precedente;
- trasformare `article` in `div` copiando alla lettera un esempio di card;
- navbar che non collassa per `data-bs-target` errato o bundle mancante;
- usare `!important` per correggere conflitti introdotti dal framework;
- `MAPPING.md` scritto a posteriori con descrizioni vaghe;
- class soup senza una spiegazione del comportamento prodotto.

## Domande orali

1. Cosa fa concettualmente `d-flex`?
2. Perche `col-12 col-lg-6` e mobile-first?
3. Quale parte della navbar richiede JavaScript?
4. Perche il post resta `article` anche se diventa una card?
5. Quale regola hai mantenuto in `custom.css` e perche non e una responsabilita Bootstrap?
6. Se togliessi Bootstrap, quali parti sapresti riscrivere con CSS nativo?

## Rubrica

La rubrica in `activity.json` totalizza 10 punti. Il mapping vale 2 punti proprio per evitare una valutazione puramente estetica.
