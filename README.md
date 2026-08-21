# TPSI quinto anno — Full Stack Web Developer

Repository docente del corso **TPSI quinto anno — Full Stack Web Developer** per l'a.s. **2026/2027**.

Il curriculum è congelato nella release authoring **Content Pack 1.0.0**, conforme a `thebitlab.content-pack.v1` e pinned alla revisione Accettata `5472eef86568a4e7ce59ad34ba937220df27efd7` di TheBitLab/2cornot2c.

## Stato della release

- **33 settimane** di Course Design;
- UDA **20–26** complete;
- **19 moduli** originali, da architettura/metodo a runtime deploy/capstone;
- progetto longitudinale **Feisbuc milestone 0–12**;
- mirror Python **01–04**: FastAPI/OpenAPI → SQLAlchemy/SQLite → testing boundaries → runtime/deploy/evidence;
- Activity A–F e reference solution collegate ai content item;
- Quality cross-platform su Ubuntu Python 3.11/3.12 e Windows Python 3.11.

Il freeze editoriale è documentato in `doc/CURRICULUM_FREEZE_2026_2027.md`.

## Stack core congelato

```text
Web Platform / HTML / CSS / Bootstrap
        ↓
JavaScript / DOM / Browser APIs
        ↓
HTTP / async / fetch / REST
        ↓
Node.js / Express 5
        ↓
SQL raw / SQLite
        ↓
auth / session / authorization / security
        ↓
SSR comparison / Nunjucks
        ↓
Vue 3 / Vite / Vue Router
        ↓
TypeScript targeted boundary typing
        ↓
Socket.IO realtime + REST recovery
        ↓
React translation/comparison lab
        ↓
FastAPI mirror / SQLAlchemy / pytest / deploy capstone
```

## Documenti principali

- `content/tpsi5/content-pack.json` — manifest Content Pack **1.0.0 approved**;
- `content/tpsi5/COVERAGE.md` — matrice di copertura congelata;
- `content/tpsi5/00_COURSE_ARCHITECTURE.md` — architettura didattica;
- `doc/course_designs/tpsi_quinto_2026_2027.json` — Course Design di 33 settimane;
- `doc/OPEN_DECISIONS.md` — decisioni D1–D5 congelate;
- `doc/CURRICULUM_FREEZE_2026_2027.md` — baseline, confini e policy post-freeze;
- `doc/LEGACY_REUSE_AUDIT.md` — provenance e audit dei materiali legacy;
- `activities/tpsi5/` — Activity e reference solution;
- `.github/workflows/quality.yml` — Quality del consumer reale.

## Confini deliberati

Non fanno parte del core 2026/27: ORM Node, Pinia senza requisito concreto, TypeScript avanzato/backend TypeScript, un secondo framework frontend core, duplicazione auth/session/realtime nel mirror Python, Alembic/PostgreSQL/async ORM, Kubernetes/cloud/scaling e CI/CD avanzata.

Il futuro corso SQL separato potrà approfondire e riusare milestone condivise, ma **non è un prerequisito bloccante** per questa release: TPSI5 contiene il minimo SQL raw necessario prima delle astrazioni.

Le capability di piattaforma #729 (browser/HTML grader) e #731 (TypeScript Activity runner) restano follow-up indipendenti e non bloccano il curriculum freeze.

Umbrella di progetto: `TheBitPoets/2cornot2c#728`. Standard cross-course accettato: `TheBitPoets/2cornot2c#723`.
