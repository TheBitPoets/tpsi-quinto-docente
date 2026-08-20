# Decisioni da congelare prima del curriculum freeze

## D1 — Framework frontend principale

Decisione: **Vue 3 + Vite**.

Stato: `DECIDED`.

Motivazione didattica:

- continuita forte con HTML, CSS e JavaScript gia studiati;
- Single File Components leggibili come evoluzione di struttura, comportamento e stile;
- Composition API adatta a rendere espliciti `state -> render`, props, emits, computed e lifecycle dopo il DOM manuale;
- carico cognitivo compatibile con le 5 settimane di UDA25;
- tooling ufficiale coerente con Vite;
- permette di introdurre TypeScript in modo progressivo senza renderlo prerequisito del primo componente.

Motivazione professionale:

- ecosistema e documentazione maturi;
- competenze trasferibili a React: componenti, props, stato, rendering dichiarativo, routing, form e data fetching;
- React resta un **translation/comparison lab** finale, non un secondo framework core.

Boundary: il corso insegna i concetti SPA attraverso Vue; non deve trasformarsi in un corso di sintassi Vue. Ogni astrazione importante va ricondotta al modello Web Platform gia studiato.

## D2 — ORM Node

Candidati iniziali: Drizzle, Prisma, Sequelize.

Criteri: visibilita del mapping SQL, maturita, TypeScript requirement, migrazioni, SQLite/PostgreSQL, chiarezza didattica.

Stato: `TBD`.

## D3 — TypeScript

Decisione: **targeted boundary typing nel core UDA25**.

Stato: `DECIDED`.

TypeScript viene introdotto dopo Vue e Vue Router, quando esistono gia contratti reali da rendere staticamente verificabili. Il core copre:

- inferenza e annotazioni solo quando aggiungono informazione;
- union e discriminated union;
- `unknown`, narrowing e nullability;
- tipi di dominio (`User`, `Post`, credenziali e stato auth);
- boundary HTTP: JSON esterno come `unknown` prima della runtime validation;
- props/emits Vue type-based;
- session state, navigation policy e `RouteMeta`;
- `strict`, `noUncheckedIndexedAccess` ed `exactOptionalPropertyTypes`.

Restano fuori dal core:

- conditional/mapped types avanzati e type gymnastics;
- decorators/metaprogrammazione;
- migrazione completa del backend Express a TypeScript;
- duplicazione sistematica di ogni esercizio JavaScript in TypeScript.

Baseline reference 2026/27: TypeScript 6.0.3 + `vue-tsc` 3.3.8. TypeScript 7 viene rivalutato solo quando l'integrazione Vue/vue-tsc usata dal corso e stabile e riproducibile.

Regola didattica: TypeScript descrive un contratto statico, ma **non rende affidabile un JSON di rete senza runtime validation**.

## D4 — Mirror Python

Direzione iniziale: FastAPI + SQLAlchemy, con un sottoinsieme significativo della stessa REST API Express per mostrare la portabilita del contratto HTTP.

Da decidere: ampiezza esatta e collocazione temporale.

## D5 — Corso SQL separato

TPSI5 deve consumare il corso SQL senza duplicarlo. Nel backend restano comunque query SQL raw prima dell'ORM, cosi lo studente vede la relazione tra SQL e astrazione applicativa.

Da decidere: prerequisiti e milestone condivise fra i due Course Design.
