# Note docente — Activity D CSS debug

## Bug intenzionali

1. body rigido a 1200px;
2. nav `nowrap` + width 700px;
3. Grid con tre track fisse e width complessiva fissa;
4. `content-box` che aumenta l'ingombro effettivo;
5. feed con `min-width: 700px`;
6. `!important` che batte la successiva regola piu specifica nella normale cascata;
7. media query wide che imposta erroneamente una colonna;
8. contenuto lungo che rende evidente il problema.

Non serve che lo studente elenchi esattamente otto punti. La consegna richiede almeno cinque cause concrete e un fix coerente.

## Cosa osservare

- apre DevTools prima di modificare?
- distingue sintomo e causa?
- cita selettore e proprieta specifici?
- controlla la regola barrata per il padding?
- comprende che `overflow-x: hidden` nasconderebbe il sintomo?
- sa spiegare perche il breakpoint e invertito?

## Valutazione

Premiare una diagnosi incompleta ma fondata piu di un CSS finale corretto ottenuto a tentativi senza spiegazione.

## Alternative accettabili

- `overflow-wrap: break-word` o altra strategia equivalente per il testo lungo;
- breakpoint leggermente diverso se il resto dell'Activity viene rispettato;
- uso di custom properties nel fix come miglioramento, non requisito.
