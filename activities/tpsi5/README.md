# Activity TPSI5

Le Activity del corso usano lo schema TheBitLab Activity 1.0 e la tassonomia ufficiale A–F:

- A: esegui/osserva;
- B: modifica controllata;
- C: implementazione autonoma;
- D: debug/diagnosi;
- E: mini-progetto;
- F: prodotto integrato.

Ogni Activity deve collegare i propri `content_ids` al Content Pack v1 e mantenere separati asset studente, grading e docente.

## Activity disponibili

| Livello | ID | UDA | Scopo | Grading |
| --- | --- | --- | --- | --- |
| A | `tpsi5-activity-a-html-anatomy-001` | UDA 21 | completare e osservare lo scheletro di un documento HTML moderno | manuale |
| B | `tpsi5-activity-b-feisbuc-semantic-001` | UDA 21 | Feisbuc milestone 0: trasformare contenitori generici in struttura HTML semantica | manuale |
| C | `tpsi5-activity-c-feisbuc-responsive-layout-001` | UDA 21 | Feisbuc milestone 1: costruire autonomamente una shell responsive con Grid/Flexbox | manuale |
| D | `tpsi5-activity-d-debug-responsive-css-001` | UDA 21 | diagnosticare overflow, cascade, box model e breakpoint errati | manuale |
| E | `tpsi5-activity-e-feisbuc-bootstrap-ui-001` | UDA 21 | Feisbuc milestone 2: rifattorizzare la UI con Bootstrap e mapping verso CSS nativo | manuale |
| A | `tpsi5-activity-a-js-feed-pipeline-001` | UDA 22 | trasformare dati del feed con filter/map e output JSON deterministico | **automatico JS** |
| B | `tpsi5-activity-b-js-post-refactor-001` | UDA 22 | aggiornare lo stato dei like con map/spread | **automatico JS** |
| C | `tpsi5-activity-c-feisbuc-dynamic-feed-001` | UDA 22 | Feisbuc milestone 3: DOM, form, event delegation, ES modules e localStorage | browser/manuale |
| D | `tpsi5-activity-d-debug-feisbuc-js-001` | UDA 22 | diagnosticare bug reali di eventi, stato, delegation e storage | browser/manuale |

## Boundary di grading

Nel contratto 2cornot2c pinned dal corso:

```text
javascript / nodejs  -> implemented
html                 -> planned
```

Di conseguenza distinguiamo esplicitamente due casi.

### JavaScript puro

Le Activity A/B di UDA 22 possono essere corrette deterministicamente dal runner Node.js:

```text
stdin JSON
   -> main.js
   -> stdout JSON
   -> confronto expected_stdout
```

Hanno quindi `correzione.test=true` e `sandbox=true`.

### Browser/DOM

Le Activity HTML/CSS e le Activity JavaScript che dipendono da `document`, eventi browser, `localStorage` o rendering restano valutate tramite checklist/rubrica:

```json
{
  "compila": false,
  "test": false,
  "sandbox": false,
  "ai_feedback": false
}
```

La CI del repository valida comunque schema, asset e proprietà strutturali delle soluzioni/starter. Il vero runtime/grader HTML/browser resta governato da `TheBitPoets/2cornot2c#729`; non viene simulato con falsi test verdi.

## Content Pack v1

Il gate A-E usato per accettare `thebitlab.content-pack.v1` è completato e il corso è pinned alla revisione Accettata del contratto. Le Activity successive continuano a usare lo stesso standard senza trasformare il curriculum TPSI5 in una specifica congelata.
