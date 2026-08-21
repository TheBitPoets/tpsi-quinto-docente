# Decisioni congelate — curriculum TPSI quinto 2026/27

Freeze editoriale: **21 agosto 2026**.

Tutte le decisioni D1–D5 sono chiuse per la release Content Pack 1.0.0. Una modifica futura del perimetro richiede issue esplicita, motivazione didattica e version bump.

## D1 — Framework frontend principale

Decisione: **Vue 3 + Vite**.

Stato: `DECIDED`.

Motivazione didattica:

- continuita forte con HTML, CSS e JavaScript gia studiati;
- Single File Components leggibili come evoluzione di struttura, comportamento e stile;
- Composition API rende espliciti `state -> render`, props, emits, computed e lifecycle dopo il DOM manuale;
- carico cognitivo compatibile con le 5 settimane di UDA25;
- tooling ufficiale coerente con Vite.

Boundary: React resta un **translation/comparison lab**, non un secondo framework core. Le astrazioni Vue vanno ricondotte alla Web Platform gia studiata.

## D2 — ORM Node

Decisione: **nessun ORM Node nel core 2026/27**.

Stato: `DECIDED`.

Motivazione:

- UDA24 rende visibile SQL raw con `node:sqlite`, constraint, prepared statement, repository e persistenza reale prima di qualunque astrazione;
- il budget di 33 settimane e gia completo senza comprimere auth, frontend, realtime o deploy;
- il concetto ORM viene comunque osservato nel mirror Python con SQLAlchemy 2.0.51, dove il mapping SQL/ORM e esplicito;
- introdurre Drizzle/Prisma/Sequelize ora aggiungerebbe superficie sintattica senza un nuovo obiettivo curricolare necessario.

Boundary: un ORM Node puo diventare estensione futura/senior o revisione di una release successiva, ma non va aggiunto silenziosamente al core 2026/27.

## D3 — TypeScript

Decisione: **targeted boundary typing nel core UDA25**.

Stato: `DECIDED`.

Il core copre inferenza e annotazioni utili, union/discriminated union, `unknown`, narrowing, nullability, tipi di dominio, boundary HTTP `JSON -> unknown -> runtime validation`, props/emits Vue, session/navigation policy e modalita strict.

Restano fuori type gymnastics, decorators/metaprogrammazione, migrazione completa del backend Express a TypeScript e duplicazione sistematica degli esercizi JavaScript.

Baseline 2026/27: TypeScript 6.0.3 + `vue-tsc` 3.3.8. Regola didattica: TypeScript descrive un contratto statico ma non rende affidabile un JSON di rete senza runtime validation.

## D4 — Mirror Python

Decisione: **FastAPI mirror track mirato in UDA26**, con SQLAlchemy in un secondo slice e testing/runtime in slice separati.

Stato: `DECIDED`.

Sequenza congelata:

1. FastAPI + Pydantic + OpenAPI + TestClient + MemoryPostStore;
2. SQLAlchemy 2.0.51 + SQLite sotto lo stesso contratto;
3. pytest fixture/isolation/integration boundaries;
4. environment config, prestart, health/readiness, live Uvicorn ed evidence capstone.

Boundary: il prodotto principale resta `Vue -> Express -> SQLite -> session/auth -> Socket.IO`; il mirror Python non duplica SPA, auth/session o realtime.

## D5 — Corso SQL separato

Decisione: **integrazione futura non bloccante**.

Stato: `DECIDED`.

TPSI5 2026/27 e autosufficiente per il sottoinsieme SQL necessario a UDA24: schema/constraint, DDL/DML, `WHERE`, prepared statement, transazioni concettuali e repository SQLite. Il futuro Content Pack SQL separato potra fornire prerequisiti piu profondi, esercitazioni aggiuntive e milestone condivise, ma non e requisito per pubblicare o svolgere questa release.

Boundary: il corso SQL non deve essere duplicato dentro TPSI5; una futura integrazione dovra mantenere visibile il mapping fra query SQL e astrazioni applicative.
