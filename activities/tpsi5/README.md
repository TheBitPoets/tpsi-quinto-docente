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

## Grading HTML nel bootstrap

Il grader generico di 2cornot2c pinned dal corso dichiara attualmente `html` come `planned`. Per questo le Activity HTML iniziali hanno:

```json
{
  "compila": false,
  "test": false,
  "sandbox": false,
  "ai_feedback": false
}
```

Sono assegnabili e valutabili tramite checklist/rubrica, ma non devono essere presentate come autograded.

La CI del repository valida schema Activity, asset, collegamenti al Content Pack e struttura delle soluzioni di riferimento. Il supporto browser/HTML automatico verra governato come capability separata della piattaforma.

## Prossimi livelli richiesti per il gate Content Pack v1

- [x] A;
- [x] B;
- [ ] C o D;
- [ ] E o F.
