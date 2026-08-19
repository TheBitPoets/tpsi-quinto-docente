# Activity TPSI5

Le Activity usano TheBitLab Activity 1.0 e la tassonomia A–F.

## Estratto UDA24–25

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
| A | `tpsi5-activity-a-ssr-view-model-001` | view model | automatico JS |
| B | `tpsi5-activity-b-nunjucks-autoescape-001` | Nunjucks/escape | manuale + reference render CI |
| C | `tpsi5-activity-c-feisbuc-ssr-001` | milestone 8 | manuale + composed E2E CI |
| D | `tpsi5-activity-d-debug-ssr-boundaries-001` | SSR trust-boundary debug | manuale |
| A | `tpsi5-activity-a-vue-reactivity-microscope-001` | `ref`/`computed` observation | manuale + reference Vite build |
| B | `tpsi5-activity-b-vue-post-card-001` | props down / emits up | manuale + reference Vite build |
| C | `tpsi5-activity-c-feisbuc-vue-spa-001` | milestone 9 Vue SPA | manuale + build + composed backend smoke |
| D | `tpsi5-activity-d-debug-vue-reactivity-001` | reactivity/component debugging | manuale + starter/solution build |

## Boundary di grading

```text
linguaggio puro                 -> runner deterministico JS/SQL
single template/render          -> reference CI con dependency pinned
Vue/SFC/browser multi-file      -> reference build + smoke/E2E docente
backend/persistence/security    -> reference E2E
security/architecture reasoning -> rubrica + evidence
```

Il browser grader TheBitLab non e ancora implementato. Per le Activity Vue `correzione.test=false` rimane quindi intenzionale.

La Quality del repository docente puo e deve:

- installare versioni pinned;
- eseguire `vite build` su starter/reference appropriati;
- controllare staticamente boundary come props/emits e assenza di token handling;
- comporre `dist/` con il backend auth gia verificato;
- fare smoke HTTP sul sistema reference.

Queste verifiche dimostrano la qualita della **reference solution**, non trasformano automaticamente l'Activity browser in autograding studente.

## Regola

Il tipo di evidence deve corrispondere al comportamento osservato. In particolare, il successo di `vite build` non dimostra da solo che una UI reattiva funzioni nel browser: reattivita, eventi e DOM richiederanno il browser runner futuro (#729).
