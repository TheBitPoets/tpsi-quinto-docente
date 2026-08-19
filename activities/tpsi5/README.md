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
| A | `tpsi5-activity-a-js-feed-pipeline-001` | 22 | pipeline dati feed | automatico JS |
| B | `tpsi5-activity-b-js-post-refactor-001` | 22 | state update map/spread | automatico JS |
| C | `tpsi5-activity-c-feisbuc-dynamic-feed-001` | 22 | milestone 3 DOM/storage | browser/manuale |
| D | `tpsi5-activity-d-debug-feisbuc-js-001` | 22 | debug eventi/stato/storage | browser/manuale |
| A | `tpsi5-activity-a-http-microscope-001` | 23 | osservare HTTP con curl/Network | manuale |
| B | `tpsi5-activity-b-async-response-policy-001` | 23 | Promise/await + Response policy | automatico JS |
| C | `tpsi5-activity-c-feisbuc-rest-client-001` | 23 | milestone 4 REST client | browser/manuale + reference E2E CI |
| D | `tpsi5-activity-d-debug-fetch-http-001` | 23 | debug fetch/HTTP | browser/manuale |
| A | `tpsi5-activity-a-node-http-express-map-001` | 24 | stessa API con `node:http` e Express | manuale + reference E2E CI |
| B | `tpsi5-activity-b-post-validation-001` | 24 | validation pura del body | automatico JS |
| C | `tpsi5-activity-c-feisbuc-express-api-001` | 24 | milestone 5 Express API modulare | manuale + reference E2E CI |
| D | `tpsi5-activity-d-debug-express-pipeline-001` | 24 | debug middleware/order/params/errors | manuale + reference E2E CI |

## Boundary di grading

Nel contratto piattaforma pinned:

```text
javascript / nodejs  -> runner deterministico disponibile
html/browser          -> runtime completo non ancora disponibile
```

### JavaScript puro

A/B UDA 22, B UDA 23 e B UDA 24 possono usare il runner deterministico Node.js:

```text
stdin -> JavaScript -> stdout -> expected_stdout
```

Queste Activity dichiarano `test=true` e `sandbox=true`.

### Protocollo, browser e backend multi-file

Una Activity puo richiedere evidence che il runner singolo-file non misura:

```text
curl/Network reasoning
DOM + browser APIs
server process
routing/middleware
static files
piu file e dipendenze npm
```

In questi casi l'Activity resta a rubrica/manuale finche il runtime TheBitLab appropriato non e disponibile.

La CI del **repository docente** puo comunque eseguire le soluzioni di riferimento: per UDA 23 avvia le fixture HTTP; per UDA 24 installa Express pinned e smoke-testa i server A/C/D. Questo verifica che noi non pubblichiamo una soluzione rotta, ma non viene presentato come autograding della consegna studente.

## Regola

Il tipo di evidenza deve corrispondere al comportamento che vogliamo misurare. Non trasformiamo uno smoke test docente in un finto test studente e non usiamo il runner Node per fingere di avere un browser.
