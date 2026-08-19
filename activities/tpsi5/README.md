# Activity TPSI5

Le Activity usano TheBitLab Activity 1.0 e la tassonomia A–F.

## Activity disponibili — estratto UDA24

| Livello | ID | Scopo | Grading |
| --- | --- | --- | --- |
| A | `tpsi5-activity-a-node-http-express-map-001` | native HTTP -> Express | manuale + reference CI |
| B | `tpsi5-activity-b-post-validation-001` | validation pura | automatico JS |
| C | `tpsi5-activity-c-feisbuc-express-api-001` | milestone 5 | manuale + E2E |
| D | `tpsi5-activity-d-debug-express-pipeline-001` | Express debug | manuale + E2E |
| A | `tpsi5-activity-a-sql-posts-schema-001` | schema/constraint | automatico SQL |
| B | `tpsi5-activity-b-sql-posts-dml-001` | DML | automatico SQL |
| C | `tpsi5-activity-c-feisbuc-sql-repository-001` | milestone 6 | manuale + E2E |
| D | `tpsi5-activity-d-debug-sql-state-001` | SQL debug | automatico SQL + diagnosi |
| A | `tpsi5-activity-a-auth-credential-policy-001` | credential policy | automatico JS |
| B | `tpsi5-activity-b-auth-post-authorization-001` | ownership/default deny | automatico JS |
| C | `tpsi5-activity-c-feisbuc-auth-session-001` | milestone 7 | manuale + security E2E |
| D | `tpsi5-activity-d-debug-auth-security-001` | security review | manuale |
| A | `tpsi5-activity-a-ssr-view-model-001` | view model | **automatico JS** |
| B | `tpsi5-activity-b-nunjucks-autoescape-001` | Nunjucks/escape | manuale + reference render CI |
| C | `tpsi5-activity-c-feisbuc-ssr-001` | milestone 8 | manuale + composed E2E CI |
| D | `tpsi5-activity-d-debug-ssr-boundaries-001` | SSR trust-boundary debug | manuale |

## Boundary di grading

```text
linguaggio puro            -> runner deterministico JS/SQL
single template/render     -> reference CI con dependency pinned
browser/backend multi-file -> reference E2E
security/architecture      -> rubrica + evidence
```

Milestone 8 e volutamente un **overlay della milestone 7**. La CI docente compone la soluzione auth precedente con i file SSR, installa le dipendenze pinned e verifica il sistema risultante. Questo non viene spacciato come autograding della consegna studente.

La regola resta: il tipo di evidence deve corrispondere al comportamento che vogliamo osservare.
