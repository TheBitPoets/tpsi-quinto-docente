# Note docente — Activity C Feisbuc responsive

## Focus

Valutare la capacita di costruire autonomamente un layout, non la somiglianza pixel-perfect con la soluzione.

## Evidenze importanti

- mobile-first reale: base a una colonna;
- Grid nel macro-layout;
- Flexbox nei gruppi monodimensionali;
- assenza di larghezza rigida principale;
- feed restringibile (`min-width: 0` o tecnica equivalente);
- breakpoint motivato dal contenuto;
- custom properties con nomi comprensibili;
- nessun `float`, `!important` o overflow nascosto per mascherare problemi.

## Alternative accettabili

- breakpoint diverso da 56rem se motivato e il comportamento e equivalente;
- `grid-template-areas` e accettabile se lo studente sa spiegare righe/colonne;
- nomi di variabili diversi;
- due colonne intermedie sono accettabili come estensione, non requisito.

## Domande orali utili

1. Mostrami il main axis della navigazione.
2. Perche qui hai scelto Grid?
3. Che cosa accade senza `min-width: 0` nel tuo feed?
4. Quale regola vince se cambio il padding della card nei DevTools?
5. Riduci il viewport: in quale momento il layout cambia e perche?

## Anti-pattern da non premiare

- layout che “funziona” solo perche tutto ha larghezze fisse;
- uso di `overflow-x: hidden` per nascondere un overflow;
- sostituzione del layout con Bootstrap o altro framework;
- uso casuale di Grid/Flex senza saper individuare container e items.
