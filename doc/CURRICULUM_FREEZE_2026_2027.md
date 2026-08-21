# Curriculum freeze — TPSI quinto 2026/27

Data freeze: **21 agosto 2026**
Release: **Content Pack 1.0.0**
Contratto: `thebitlab.content-pack.v1` @ `5472eef86568a4e7ce59ad34ba937220df27efd7`

## Esito

Il percorso TPSI quinto 2026/27 e congelato come curriculum **junior full-stack solido** di 33 settimane. UDA20–UDA26, Feisbuc milestone 0–12 e mirror Python 01–04 hanno contenuti, Activity, reference solution e gate CI coerenti.

Il freeze non dichiara che ogni possibile estensione sia stata implementata: dichiara quale perimetro costituisce la release didattica 2026/27 e quali idee restano deliberate estensioni future.

## Sequenza congelata

| Blocco | Core | Evidenza principale |
| --- | --- | --- |
| Web Platform | HTML moderno, CSS responsive, Bootstrap | Feisbuc 0–2 |
| JavaScript browser | JS moderno, DOM, Browser APIs, storage | Feisbuc 3 |
| Protocollo/API | HTTP, async/await, fetch, REST | Feisbuc 4 |
| Backend | Node.js, Express 5, Router/middleware/validation | Feisbuc 5 |
| Persistenza | SQL raw, SQLite, repository | Feisbuc 6 |
| Sicurezza | authn/authz, scrypt, session server-side, ownership | Feisbuc 7 |
| Rendering | Nunjucks SSR comparison, autoescape, PRG | Feisbuc 8 |
| SPA | Vue 3 + Vite | Feisbuc 9 |
| Routing | Vue Router, history/deep link/guard | Feisbuc 10 |
| Tipi | TypeScript targeted boundary typing | Feisbuc 11 |
| Realtime | WebSocket concettuale + Socket.IO + recovery REST | Feisbuc 12 |
| Transfer | React translation/comparison | nessuna milestone nuova |
| Mirror Python | FastAPI/OpenAPI -> SQLAlchemy -> pytest -> runtime/deploy | mirror 01–04 |

## Decisioni D1–D5

- D1: Vue 3 + Vite core; React solo translation lab.
- D2: nessun ORM Node nel core 2026/27.
- D3: TypeScript targeted boundary typing.
- D4: FastAPI mirror mirato, non duplicazione del prodotto Express.
- D5: futuro corso SQL integrabile ma non prerequisito bloccante.

Dettaglio e motivazioni: `doc/OPEN_DECISIONS.md`.

## Invarianti di architettura didattica

1. Web Platform prima dei framework.
2. HTTP esplicito prima delle astrazioni client/server.
3. SQL raw prima dell'ORM.
4. Identita e authorization derivano dal server, mai da campi trusted del client.
5. REST resta command path; Socket.IO e event path; reconnect richiede resync autorevole.
6. TypeScript non sostituisce runtime validation dei dati esterni.
7. Il mirror Python preserva il contratto e rende confrontabili i boundary, senza duplicare tutto il prodotto.
8. I test osservano proprieta ai boundary reali e non sostituiscono integrazione con mock interni.

## Non-scope della release

- ORM Node nel core;
- Pinia senza una reale necessita di ownership condivisa;
- TypeScript avanzato e backend Express riscritto in TypeScript;
- React Router/Redux/Next.js o un secondo framework frontend core;
- JWT/OAuth/MFA come percorso core;
- auth/session/realtime duplicati nel mirror Python;
- Alembic, PostgreSQL, async SQLAlchemy;
- Docker Compose/Kubernetes, reverse proxy/TLS termination, cloud/scaling;
- CI/CD avanzata, performance engineering, caching/queue e architetture distribuite.

Questi elementi possono alimentare un futuro track senior senza alterare retroattivamente la release 1.0.0.

## Platform follow-up non bloccanti

- `TheBitPoets/2cornot2c#729`: browser/HTML grader;
- `TheBitPoets/2cornot2c#731`: TypeScript Activity runner.

Le Activity che richiedono capability non ancora presenti restano manual/rubric nel runtime TheBitLab; la repository Quality continua a validare le reference solution con browser/build/typecheck/server live dove previsto.

## Evidence di freeze

Baseline immediatamente precedente al freeze:

- UDA26 closeout: `TheBitPoets/tpsi-quinto-docente#22`;
- merge UDA26: `32ccb4cd69b0e23cd0cc56d16c5e7a091235a4f9`;
- Quality PR #159 / run `32471024453`;
- matrice: Ubuntu Python 3.11, Ubuntu Python 3.12, Windows Python 3.11;
- regression suite: **97 passed**;
- runtime config, health/readiness, SQLAlchemy restart, live Uvicorn ed evidence bundle: PASS.

La PR di freeze deve nuovamente passare l'intera matrice prima del merge.

## Policy post-freeze

Una modifica che cambia obiettivi, UDA, milestone, stack core o carico didattico richiede issue esplicita, analisi di impatto, aggiornamento coordinato dei contratti, version bump e Quality verde.

Fix di sicurezza, compatibilita o dipendenze che non cambiano gli obiettivi possono entrare come patch release, mantenendo tracciata la baseline.
