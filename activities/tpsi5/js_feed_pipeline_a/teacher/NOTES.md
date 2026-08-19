# Note docente — Activity A JavaScript pipeline

## Intento

Prima Activity TPSI5 che usa davvero il runner JavaScript deterministico di TheBitLab.

Serve a separare due piani:

- ECMAScript: dati, funzioni e trasformazioni;
- browser: DOM/Web APIs, che arriveranno nelle Activity successive.

## Misconception da osservare

- `filter` cambia l'elemento invece di selezionarlo;
- `map` viene usato soltanto per effetti collaterali;
- `const` viene interpretato come immutabilita profonda;
- `text.trim()` viene applicato modificando il dato originale;
- aggiunta di log di debug su stdout che rompe il contratto deterministico;
- soluzione con loop accettabile concettualmente ma fuori dal vincolo didattico specifico dell'Activity.

## Discussione dopo il test

Chiedere allo studente di riscrivere a voce la pipeline come frase:

> prendi i post, mantieni quelli pubblicati, poi trasformali nel formato del riepilogo.

Il punto non e la sintassi compatta, ma la corrispondenza fra intenzione e codice.

## Grading

I test deterministici sono autoritativi sull'output. La rubrica completa richiede anche spiegazione e qualita del codice: un output corretto ottenuto con hard-code non soddisfa la parte manuale.
