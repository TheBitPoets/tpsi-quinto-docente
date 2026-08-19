# TPSI quinto anno — Content Pack

Questo package contiene i contenuti originali del corso **TPSI quinto anno — Full Stack Web Developer**, a.s. 2026/2027.

Contratto di authoring: `thebitlab.content-pack.v1`, pinned alla revisione Accettata `5472eef86568a4e7ce59ad34ba937220df27efd7` di `TheBitPoets/2cornot2c`.

## Principi

- Web Platform prima dei framework;
- HTTP esplicito prima di `fetch`/Express;
- SQL raw prima dell'ORM;
- trasporto, validation, persistence, auth, authorization e presentation separati;
- identita derivata server-side da sessione verificata;
- SSR e client rendering confrontati sopra lo stesso dominio, non trattati come tecnologie in competizione assoluta;
- Node.js + Express backend principale; FastAPI mirror mirato;
- Feisbuc progetto longitudinale;
- documentazioni ufficiali e security guidance come reference;
- Activity A–F con asset student/teacher separati.

## Contenuti disponibili

1. `00_COURSE_ARCHITECTURE.md` — architettura e metodo;
2. `01_WEB_PLATFORM_HTML_MODERNO.md` — HTML; milestone 0;
3. `02_CSS_MODERNO_RESPONSIVE.md` — CSS/responsive; milestone 1;
4. `03_BOOTSTRAP_DA_CSS_A_FRAMEWORK.md` — Bootstrap; milestone 2;
5. `04_JAVASCRIPT_DOM_BROWSER_APIS.md` — JS/DOM/storage; milestone 3;
6. `05_HTTP_ASYNC_FETCH_REST.md` — HTTP/fetch/REST; milestone 4;
7. `06_NODE_EXPRESS_BACKEND.md` — Node/Express; milestone 5;
8. `07_SQL_RAW_PERSISTENCE.md` — SQL raw/SQLite; milestone 6;
9. `08_AUTH_SESSIONI_SICUREZZA.md` — auth/session/authorization; milestone 7;
10. `09_SSR_NUNJUCKS_CONFRONTO.md` — SSR/Nunjucks/PRG e confronto rendering; milestone 8.

## Feisbuc oggi

```text
0 semantic HTML
1 responsive native CSS
2 Bootstrap UI
3 dynamic JS + localStorage
4 HTTP REST client + node:http fixture
5 Express 5 + MemoryPostStore
6 Express 5 + SqlPostStore + SQLite
7 users + scrypt + HttpOnly session + ownership
8 API JSON + SSR Nunjucks sopra stesso auth/store
```

Milestone 8 non sostituisce la API:

```text
                      +-> /api -> JSON -> browser JS -> DOM
session + stores -----|
                      +-> /ssr -> view model -> Nunjucks -> HTML
```

## Activity UDA24 — SSR/template

- `tpsi5-activity-a-ssr-view-model-001` — view model puro, autograded JS;
- `tpsi5-activity-b-nunjucks-autoescape-001` — Nunjucks Environment/autoescape;
- `tpsi5-activity-c-feisbuc-ssr-001` — milestone 8 overlay, API+SSR coesistono;
- `tpsi5-activity-d-debug-ssr-boundaries-001` — review di escape/authz/PRG/view context.

## UDA24 chiusa come percorso didattico

```text
node:http -> Express -> SQL raw -> auth/session -> SSR comparison
```

Restano volutamente fuori da UDA24:

- ORM Node: **TBD** dopo SQL raw;
- JWT/OAuth/OIDC/MFA: track security successivo quando motivato;
- framework frontend: UDA25;
- realtime: UDA25.

## Stato

Versione authoring **`0.10.0`**, ancora `draft` perche il curriculum completo non e congelato.

Il prossimo incremento e **UDA25 — frontend framework, SPA e realtime**. Prima di scriverlo vanno congelate almeno la scelta del framework frontend e la profondita TypeScript; la scelta ORM puo restare separata finche non serve al percorso.
