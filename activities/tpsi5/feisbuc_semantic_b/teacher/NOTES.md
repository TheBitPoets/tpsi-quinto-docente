# Note docente — Feisbuc milestone 0

## Scopo

Questa Activity non valuta la capacita di memorizzare una lista di tag. Valuta la capacita di scegliere un elemento in base al significato del contenuto.

## Alternative accettabili

La soluzione di riferimento usa una `section` anche per il profilo, ma e accettabile una diversa struttura se lo studente sa motivarla e conserva una gerarchia coerente.

`div` non deve essere penalizzato in quanto tale: va penalizzato quando sostituisce un elemento semanticamente piu adatto senza una motivazione.

## Discussione finale consigliata

Mostrare tre versioni dello stesso markup:

1. quasi solo `div`;
2. sostituzione meccanica `div -> section`;
3. soluzione semantica ragionata.

Chiedere quale delle tre comunica meglio l'intenzione e perche.

## Collegamento col Feisbuc legacy

La milestone deriva dal progetto `TheBitPoets/feisbuc` pinned allo SHA `086995ece4260a3408740b94cfe2701ce24f8b57`. Non viene copiata la vecchia implementazione: si conserva l'idea incrementale del progetto e si ricostruisce il markup con standard moderni.

## Limite runtime attuale

Come per Activity A, `html` e ancora `planned` nel grader generico 2cornot2c. La correzione resta manuale/rubric-based; CI e Activity validator controllano il contratto e la presenza degli asset, non la correttezza semantica della consegna dello studente.
