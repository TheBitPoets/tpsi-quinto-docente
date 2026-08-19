# Decisioni da congelare prima del curriculum freeze

## D1 — Framework frontend principale

Candidati iniziali: Vue 3, React. Svelte resta riferimento comparativo, non terzo framework core.

Criteri: continuità didattica con HTML/CSS/JS, carico cognitivo, tooling, ecosistema, occupabilità, qualità docs, facilità lab/TheBitLab.

Stato: `TBD`.

## D2 — ORM Node

Candidati iniziali: Drizzle, Prisma, Sequelize.

Criteri: visibilità del mapping SQL, maturità, TypeScript requirement, migrazioni, SQLite/PostgreSQL, chiarezza didattica.

Stato: `TBD`.

## D3 — TypeScript

Alternative: nessun core; introduzione breve nel secondo quadrimestre; track advanced separato.

Criterio principale: non sacrificare HTTP/SQL/testing per inseguire tooling.

Stato: `TBD`.

## D4 — Mirror Python

Direzione iniziale: FastAPI + SQLAlchemy, con un sottoinsieme significativo della stessa REST API Express per mostrare la portabilità del contratto HTTP.

Da decidere: ampiezza esatta e collocazione temporale.

## D5 — Corso SQL separato

TPSI5 deve consumare il corso SQL senza duplicarlo. Nel backend restano comunque query SQL raw prima dell'ORM, così lo studente vede la relazione tra SQL e astrazione applicativa.

Da decidere: prerequisiti e milestone condivise fra i due Course Design.
