# Note docente — Activity A

## Obiettivo osservabile

Lo studente deve riconoscere che una pagina può apparire quasi identica prima e dopo la correzione, ma diventare strutturalmente e semanticamente migliore.

## Domande utili

- Perche la pagina iniziale viene comunque visualizzata senza doctype?
- `head` e `header` sono la stessa cosa?
- `title` e `h1` servono allo stesso scopo?
- Perché impostiamo `lang="it"` anche se il testo è già in italiano?
- Perché una modifica che non cambia l'aspetto può essere importante?

## Errori da non correggere subito al posto dello studente

Se lo studente mette metadata nel `body`, duplica `h1` o lascia il `div.header`, chiedere prima di confrontare sorgente e pannello Elements e poi di ricontrollare MDN.

## Valutazione

Attività formativa, adatta anche a non essere valutata numericamente. Se viene assegnato un punteggio, usare la rubrica in `activity.json` privilegiando comprensione e spiegazione rispetto alla semplice somiglianza con la soluzione.

## Limite runtime attuale

Il grader generico 2cornot2c dichiara attualmente `html` come `planned`. Questa Activity usa quindi `correzione.test=false`: non va presentata allo studente come automaticamente corretta. La CI del course pack verifica invece struttura, asset e contratto dell'Activity.
