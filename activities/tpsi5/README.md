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
| A | `tpsi5-activity-a-sql-posts-schema-001` | 24 | schema e constraint `posts` | automatico SQL |
| B | `tpsi5-activity-b-sql-posts-dml-001` | 24 | INSERT/UPDATE/DELETE/view | automatico SQL |
| C | `tpsi5-activity-c-feisbuc-sql-repository-001` | 24 | milestone 6 `SqlPostStore` persistente | manuale + reference E2E CI |
| D | `tpsi5-activity-d-debug-sql-state-001` | 24 | debug constraint/WHERE | automatico SQL + diagnosi |
| A | `tpsi5-activity-a-auth-credential-policy-001` | 24 | policy email/password | **automatico JS** |
| B | `tpsi5-activity-b-auth-post-authorization-001` | 24 | authorization/ownership/default deny | **automatico JS** |
| C | `tpsi5-activity-c-feisbuc-auth-session-001` | 24 | milestone 7 auth/session/ownership | manuale + **reference security E2E CI** |
| D | `tpsi5-activity-d-debug-auth-security-001` | 24 | security review trust boundary | manuale |

## Boundary di grading

Nel contratto piattaforma pinned:

```text
javascript / nodejs  -> runner deterministico disponibile
sql                  -> runner SQLite deterministico disponibile
html/browser          -> runtime completo non ancora disponibile
```

### Linguaggio puro

Le Activity JavaScript pure (incluse auth A/B) usano:

```text
stdin -> JavaScript -> stdout -> expected_stdout
```

Le Activity SQL A/B/D usano:

```text
main.sql
  + SQL di test
  -> SQLite :memory:
  -> righe serializzate
  -> expected_stdout
```

### Browser, processi, persistenza e security state

Una Activity puo richiedere evidence che il runner singolo-file non misura:

```text
DOM/browser
server process
routing/middleware
file DB persistente
cookie jar
restart del processo
piu utenti/sessioni
ownership
piu file/dipendenze
```

In questi casi l'Activity resta a rubrica/manuale. La CI del repository docente esegue le **soluzioni di riferimento**, non finge che siano test automatici della consegna studente.

Per milestone 7 la Quality deve dimostrare almeno:

```text
register -> Set-Cookie
me -> identita server-side
create -> authorId dalla sessione
secondo utente -> DELETE altrui = 403
owner -> DELETE = 204
logout -> vecchio cookie = 401
restart DB -> user/session persistono entro TTL
DB -> password e session token non plaintext
cross-site unsafe -> 403
```

Activity D auth rimane manuale perche il prodotto valutato e una **security review causa/attacco/fix/evidence**, non soltanto un output di codice.

## Regola

Il tipo di evidenza deve corrispondere al comportamento osservato: linguaggio puro → runner deterministico; browser/processi/persistenza/security state → runtime/E2E appropriato; security reasoning → rubrica e review.
