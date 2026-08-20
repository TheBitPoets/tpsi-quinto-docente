# TPSI quinto 2026/27 — matrice di copertura iniziale

Stato: **draft**.

| Area | Core 2026/27 | Progetto Feisbuc | Note |
| --- | --- | --- | --- |
| Web Platform/HTML/CSS | sì | milestone 0–1 | semantica, responsive, Flexbox/Grid |
| Bootstrap | sì, dopo CSS | milestone 2 | framework come astrazione |
| JavaScript/DOM/Storage | sì | milestone 3 | state/render, delegation, localStorage temporaneo |
| HTTP/Fetch/REST | sì | milestone 4 | request/response, status, errors, REST |
| Node/Express | sì | milestone 5 | Express 5.2.1, Router/middleware/validation/error model |
| SQL raw/SQLite | sì | milestone 6 | `node:sqlite`, constraint, prepared statement, persistence |
| Auth/session/authz | sì | milestone 7 | scrypt, HttpOnly cookie, session server-side, ownership |
| SSR/template | sì, compatto | milestone 8 | Nunjucks, view model, autoescape, PRG, coexistence API/SSR |
| Vue 3 + Vite | **sì, D1 deciso** | milestone 9 | SFC, Composition API, ref/computed, props/emits, API/auth invariati |
| Vue Router / SPA routing | **sì** | milestone 10 | URL/history, named routes, guard, client 404, Express deep-link fallback |
| TypeScript | **sì, D3 deciso** | **milestone 11** | targeted boundary typing: dominio, API `unknown`, props/emits, session e route meta |
| Global state/Pinia | solo se motivato | non ancora | session composable sufficiente; store solo con requisito condiviso reale |
| ORM Node | TBD | futuro | confronto solo dopo SQL raw |
| WebSocket/realtime | sì | prossimo UDA25 | WebSocket concettuale + Socket.IO applicato |
| FastAPI mirror/OpenAPI/SQLAlchemy | sì, mirato | UDA26 | stesso contratto HTTP come mirror |
| Testing/deploy/capstone | sì | UDA26 | release finale e osservabilita base |

## Progressione Feisbuc

```text
0 semantic HTML
1 native responsive CSS
2 Bootstrap UI
3 JavaScript DOM + localStorage
4 HTTP REST API client + node:http fixture
5 Express 5 + MemoryPostStore
6 Express 5 + SqlPostStore + SQLite file
7 users + scrypt + server-side session + ownership
8 Nunjucks SSR + stessa API/auth/session/store
9 Vue 3 + Vite SPA shell + stessa API/auth/session/store
10 Vue Router + URL/history + protected navigation + deep-link fallback
11 TypeScript strict sui boundary frontend + stesso backend/API
```

### Milestone 11 — tipi sopra contratti gia esistenti

```text
JSON rete
   ↓
unknown
   ↓ runtime narrowing
User / Post
   ↓
session / router / SFC
   ↓
Vue SPA
   ↓
/api/* invariato
   ↓
Express authz + SQLite invariati
```

Invariant:

- TypeScript non sostituisce runtime validation del JSON;
- `User`, `Post` e `AuthStatus` hanno una fonte di verita unica;
- navigation policy usa una discriminated union;
- `RouteMeta.requiresAuth` e tipizzato;
- props/emits principali sono type-based;
- `strict`, `noUncheckedIndexedAccess` ed `exactOptionalPropertyTypes` restano attivi;
- nessun `any` nei boundary core della reference;
- token sessione ancora solo nel cookie `HttpOnly`;
- backend Express/auth/ownership/SQLite non cambia;
- nessun Pinia/ORM/WebSocket introdotto nella milestone 11.

La Quality reference deve verificare almeno:

- `tsc --noEmit` / `vue-tsc --noEmit` verdi su A/B/C solution;
- starter D **rosso** per errori statici intenzionali e solution D verde;
- Vite build verde sulla milestone 11;
- composizione milestone 10 + overlay TypeScript riproducibile;
- `GET /vue/feed` continua a funzionare sul backend composto;
- `/api/posts` anonimo continua a produrre 401;
- register/session/posts API restano operativi;
- nessun falso supporto TypeScript dichiarato dal grader TheBitLab finche il runner non esiste.

## Activity UDA25 — Vue foundations

- [x] `tpsi5-activity-a-vue-reactivity-microscope-001`;
- [x] `tpsi5-activity-b-vue-post-card-001`;
- [x] `tpsi5-activity-c-feisbuc-vue-spa-001` — milestone 9;
- [x] `tpsi5-activity-d-debug-vue-reactivity-001`.

## Activity UDA25 — Vue Router

- [x] `tpsi5-activity-a-vue-router-microscope-001`;
- [x] `tpsi5-activity-b-navigation-policy-001` — automatico JS;
- [x] `tpsi5-activity-c-feisbuc-vue-router-001` — milestone 10;
- [x] `tpsi5-activity-d-debug-vue-router-001`.

## Activity UDA25 — TypeScript mirato

- [x] `tpsi5-activity-a-typescript-contract-microscope-001` — compiler microscope;
- [x] `tpsi5-activity-b-typescript-navigation-policy-001` — discriminated union;
- [x] `tpsi5-activity-c-feisbuc-typescript-boundaries-001` — milestone 11 overlay;
- [x] `tpsi5-activity-d-debug-typescript-boundaries-001` — debug statico intenzionalmente rosso.

## Boundary di grading UDA25

Il browser grader TheBitLab non e ancora implementato e il runner deterministico TheBitLab non dichiara ancora TypeScript. Le Activity TS restano quindi `correzione.test=false`; `vue-tsc`/`tsc` in Quality sono evidence del **repository docente**, non autograding studente della piattaforma.

## Gate prima del freeze del curriculum TPSI5

1. definire/creare il corso SQL separato riusando il blocco SQL;
2. **framework frontend: completato — Vue 3 + Vite**;
3. **SPA routing: completato — Vue Router**;
4. **profondita TypeScript: completata — targeted boundary typing**;
5. decidere ORM Node quando serve realmente;
6. verificare ore reali e calendario definitivo;
7. completare UDA25: realtime e translation lab React;
8. completare UDA26: FastAPI mirror, testing, deploy e capstone.
