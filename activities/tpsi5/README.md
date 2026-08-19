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

| Livello | ID | UDA | Scopo |
| --- | --- | --- | --- |
| A | `tpsi5-activity-a-html-anatomy-001` | UDA 21 | completare e osservare lo scheletro di un documento HTML moderno |
| B | `tpsi5-activity-b-feisbuc-semantic-001` | UDA 21 | Feisbuc milestone 0: trasformare contenitori generici in struttura HTML semantica |
| C | `tpsi5-activity-c-feisbuc-responsive-layout-001` | UDA 21 | Feisbuc milestone 1: costruire autonomamente una shell responsive con Grid/Flexbox |
| D | `tpsi5-activity-d-debug-responsive-css-001` | UDA 21 | diagnosticare e correggere overflow, cascade, box model e breakpoint errati |
| E | `tpsi5-activity-e-feisbuc-bootstrap-ui-001` | UDA 21 | Feisbuc milestone 2: rifattorizzare la UI con Bootstrap mantenendo il mapping verso CSS nativo |

## Grading HTML/CSS nel bootstrap

Il grader generico di 2cornot2c pinned dal corso dichiara attualmente `html` come `planned`. Per questo le Activity web iniziali hanno:

```json
{
  "compila": false,
  "test": false,
  "sandbox": false,
  "ai_feedback": false
}
```

Sono assegnabili e valutabili tramite checklist/rubrica, ma non devono essere presentate come autograded.

La CI del repository valida schema Activity, asset, collegamenti al Content Pack e struttura delle soluzioni di riferimento. Per C/D controlla inoltre proprietà strutturali delle soluzioni CSS e che gli starter di debug contengano davvero i difetti dichiarati. Per E verifica uso coerente di Bootstrap, semantica HTML, mapping CSS -> framework e CSS custom minimo. Il supporto HTML/browser automatico resta governato da `TheBitPoets/2cornot2c#729`.

## Gate Content Pack v1

- [x] A;
- [x] B;
- [x] C;
- [x] D;
- [x] E.

La tassonomia rappresentativa necessaria al gate di adozione del Content Pack v1 e ora coperta da un corso reale. Il livello F resta parte dell'evoluzione del corso e del capstone finale, non e necessario per accettare il contratto v1.
