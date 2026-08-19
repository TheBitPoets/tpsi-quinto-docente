# TPSI quinto anno — Full Stack Web Developer

Repository docente del corso TPSI quinto anno per l'a.s. 2026/2027.

Il corso adotta `thebitlab.content-pack.v1` come contratto di authoring e provenienza e usa Activity TheBitLab schema 1.0 per laboratori e valutazioni.

## Bootstrap corrente

- `content/tpsi5/content-pack.json` — manifest authoring v1;
- `content/tpsi5/COVERAGE.md` — perimetro iniziale del curriculum;
- `content/tpsi5/00_COURSE_ARCHITECTURE.md` — filo logico full stack;
- `doc/course_designs/tpsi_quinto_2026_2027.json` — calendario/UDA draft di 33 settimane;
- `doc/LEGACY_REUSE_AUDIT.md` — audit di `html_css_summary`, `labs_summary`, `feisbuc`;
- `doc/OPEN_DECISIONS.md` — framework frontend, ORM Node, TypeScript e altri gate;
- `activities/tpsi5/` — root delle future Activity A–F;
- `.github/workflows/quality.yml` — validazione pinned contro i contratti Content Pack v1 di 2cornot2c.

## Boundary

```text
Content Pack v1
      ↓
Course Design + Activity 1.0
      ↓
review / freeze
      ↓
Course Bundle 1.0.0
      ↓
TheBitLab runtime
```

## Stato

Bootstrap. Non sono ancora congelate le scelte su framework frontend, ORM Node e profondità TypeScript; non ci sono ancora Activity assegnabili nel nuovo formato.

Umbrella di progetto: `TheBitPoets/2cornot2c#728`. Standard cross-course: `TheBitPoets/2cornot2c#723`.
