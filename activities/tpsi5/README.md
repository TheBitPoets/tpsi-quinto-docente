# Activity TPSI5

Le Activity usano TheBitLab Activity 1.0 e la tassonomia A–F:

- A: esegui/osserva;
- B: modifica controllata;
- C: implementazione autonoma;
- D: debug/diagnosi;
- E: mini-progetto;
- F: prodotto integrato.

## Activity disponibili

| Livello | ID | UDA | Scopo | Grading |
| --- | --- | --- | --- | --- |
| A | `tpsi5-activity-a-html-anatomy-001` | 21 | anatomia HTML | manuale |
| B | `tpsi5-activity-b-feisbuc-semantic-001` | 21 | milestone 0 semantica | manuale |
| C | `tpsi5-activity-c-feisbuc-responsive-layout-001` | 21 | milestone 1 responsive | manuale |
| D | `tpsi5-activity-d-debug-responsive-css-001` | 21 | debug CSS | manuale |
| E | `tpsi5-activity-e-feisbuc-bootstrap-ui-001` | 21 | milestone 2 Bootstrap | manuale |
| A | `tpsi5-activity-a-js-feed-pipeline-001` | 22 | pipeline dati feed | **automatico JS** |
| B | `tpsi5-activity-b-js-post-refactor-001` | 22 | state update map/spread | **automatico JS** |
| C | `tpsi5-activity-c-feisbuc-dynamic-feed-001` | 22 | milestone 3 DOM/storage | browser/manuale |
| D | `tpsi5-activity-d-debug-feisbuc-js-001` | 22 | debug eventi/stato/storage | browser/manuale |
| A | `tpsi5-activity-a-http-microscope-001` | 23 | osservare HTTP con curl/Network | manuale |
| B | `tpsi5-activity-b-async-response-policy-001` | 23 | Promise/await + Response policy | **automatico JS** |
| C | `tpsi5-activity-c-feisbuc-rest-client-001` | 23 | milestone 4 REST client | browser/manuale + smoke CI reference |
| D | `tpsi5-activity-d-debug-fetch-http-001` | 23 | debug fetch/HTTP | browser/manuale |

## Boundary di grading

Nel contratto piattaforma pinned:

```text
javascript / nodejs  -> implemented
html/browser          -> non ancora implementato come runtime completo
```

### JavaScript puro

A/B UDA 22 e B UDA 23 possono usare il runner deterministico Node.js:

```text
stdin -> JavaScript -> stdout -> expected_stdout
```

Queste Activity dichiarano `test=true` e `sandbox=true`.

### Protocollo osservato

Activity A UDA 23 e manuale perche il risultato e una lettura ragionata di request/response con `curl` e DevTools. La CI verifica comunque che la fixture HTTP restituisca realmente gli status/headers dichiarati.

### Browser/DOM/fetch

Le Activity che devono osservare DOM, event loop del browser, rendering, Web Storage o Fetch dentro una pagina restano a rubrica finche `2cornot2c#729` non fornisce il browser grader.

Questo non impedisce alla CI del **corso** di smoke-testare le soluzioni di riferimento a livello HTTP: server fixture e adapter `api.js` vengono eseguiti davvero con Node 22 per verificare GET/POST/PATCH e gestione errori.

## Regola

Non trasformiamo uno smoke test della soluzione docente in un finto autograding studente. Il tipo di evidenza deve corrispondere al comportamento che vogliamo misurare.
