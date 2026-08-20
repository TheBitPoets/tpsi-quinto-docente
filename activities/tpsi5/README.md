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
| A | `tpsi5-activity-a-vue-router-microscope-001` | URL/history/RouterView/deep link | manuale + Vite build |
| B | `tpsi5-activity-b-navigation-policy-001` | navigation state machine | **automatico JS** |
| C | `tpsi5-activity-c-feisbuc-vue-router-001` | milestone 10 Vue Router | manuale + composed build/deep-link E2E |
| D | `tpsi5-activity-d-debug-vue-router-001` | history/guard/fallback debug | manuale + structural checks |
| A | `tpsi5-activity-a-typescript-contract-microscope-001` | inference/union/unknown/nullability | manuale + `tsc --noEmit` reference |
| B | `tpsi5-activity-b-typescript-navigation-policy-001` | discriminated navigation union | manuale + `tsc --noEmit` reference |
| C | `tpsi5-activity-c-feisbuc-typescript-boundaries-001` | milestone 11 TS boundary overlay | manuale + `vue-tsc` + build + composed E2E |
| D | `tpsi5-activity-d-debug-typescript-boundaries-001` | static type debugging | starter type-check **deve fallire**, solution verde |

## Boundary di grading

```text
linguaggio puro JS/SQL           -> runner deterministico TheBitLab
TypeScript puro/SFC              -> reference tsc/vue-tsc in repository CI
single template/render           -> reference CI con dependency pinned
Vue/SFC/browser multi-file       -> reference build + smoke/E2E docente
HTTP deep-link fallback          -> reference server E2E
backend/persistence/security     -> reference E2E
security/architecture reasoning  -> rubrica + evidence
```

Il browser grader TheBitLab non e ancora implementato e il runner accettato non dichiara TypeScript. Per le Activity TS `correzione.test=false` e intenzionale: `tsc`/`vue-tsc` in Quality sono evidence della reference, non una capacita di grading della piattaforma.

La Quality del repository docente puo e deve:

- installare versioni pinned;
- eseguire `tsc --noEmit` / `vue-tsc --noEmit` sulle reference TypeScript;
- verificare che lo starter D fallisca realmente per gli errori dichiarati;
- eseguire `vite build` sulla milestone 11;
- comporre milestone 10 + TypeScript overlay;
- comporre `dist/` con il backend auth gia verificato;
- fare smoke HTTP su `/vue/` e `/vue/feed`;
- verificare che `/api/*` mantenga 401/403 e il contratto precedente.

## Regola

Il tipo di evidence deve corrispondere al comportamento osservato. Un type-check verde dimostra coerenza statica, non correttezza del JSON remoto, sicurezza del backend o comportamento browser. Runtime validation, 401/403 e browser runner restano livelli distinti.
