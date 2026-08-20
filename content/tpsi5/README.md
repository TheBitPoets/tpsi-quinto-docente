# TPSI quinto anno — Content Pack

Questo package contiene i contenuti originali del corso **TPSI quinto anno — Full Stack Web Developer**, a.s. 2026/2027.

Contratto di authoring: `thebitlab.content-pack.v1`, pinned alla revisione Accettata `5472eef86568a4e7ce59ad34ba937220df27efd7` di `TheBitPoets/2cornot2c`.

## Principi

- Web Platform prima dei framework;
- HTTP esplicito prima di `fetch`/Express;
- SQL raw prima dell'ORM;
- trasporto, validation, persistence, auth, authorization e presentation separati;
- identita derivata server-side da sessione verificata;
- SSR e client rendering confrontati sopra lo stesso dominio;
- Vue viene introdotto dopo DOM manuale/API/auth/SSR come astrazione di concetti gia osservati;
- Vue Router entra solo quando l'URL deve rappresentare piu viste;
- TypeScript entra dopo Vue/Router per rendere verificabili boundary reali, non come secondo corso di sintassi;
- JSON di rete resta non fidato: `unknown` + runtime narrowing prima dei tipi di dominio;
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
10. `09_SSR_NUNJUCKS_CONFRONTO.md` — SSR/Nunjucks/PRG; milestone 8;
11. `10_VUE3_COMPONENTI_REATTIVITA.md` — Vue 3/Vite; milestone 9;
12. `11_VUE_ROUTER_NAVIGAZIONE_SPA.md` — Vue Router; milestone 10;
13. `12_TYPESCRIPT_CONTRATTI_FRONTEND.md` — TypeScript mirato ai boundary; milestone 11.

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
9 Vue 3 + Vite SPA shell sopra stessa API/auth/store
10 Vue Router + URL/history + protected routes + deep-link fallback
11 TypeScript strict sui boundary frontend + stesso backend/API
```

Milestone 11 non introduce un nuovo backend:

```text
response.json()
    ↓
 unknown
    ↓ parser/narrowing
 User / Post
    ↓
session / router / props-emits
    ↓
Vue SPA
    ↓
/api/*
    ↓
Express auth + SQLite invariati
```

## Decisioni frontend

D1 e D3 sono congelate:

```text
framework core      = Vue 3 + Vite
router core         = Vue Router
TypeScript depth    = targeted-boundary-typing
React               = translation/comparison lab
```

Baseline reference UDA25:

```text
Vue                  3.5.40
Vue Router           5.2.0
Vite                 8.2.1
@vitejs/plugin-vue   6.0.8
TypeScript           6.0.3
vue-tsc              3.3.8
Node                 >=22.18
```

TypeScript 7 non viene adottato automaticamente: il corso privilegia una toolchain Vue/vue-tsc riproducibile e la rivalutera quando la compatibilita sara stabile.

## Activity UDA25 — TypeScript

- `tpsi5-activity-a-typescript-contract-microscope-001` — inferenza, union, `unknown`, narrowing e nullability;
- `tpsi5-activity-b-typescript-navigation-policy-001` — navigation decision come discriminated union;
- `tpsi5-activity-c-feisbuc-typescript-boundaries-001` — milestone 11, overlay TypeScript della milestone 10;
- `tpsi5-activity-d-debug-typescript-boundaries-001` — starter volutamente rosso con errori statici reali.

## Boundary UDA25

Non sono ancora introdotti:

```text
Pinia
WebSocket / Socket.IO
ORM
backend Express in TypeScript
```

Il piccolo stato condiviso della sessione resta un composable/module. Pinia entra solo se il realtime crea un problema di stato condiviso reale.

## Grading

Il browser grader TheBitLab non e ancora implementato e lo snapshot accettato del runner non dichiara TypeScript come linguaggio supportato. Le Activity TS restano quindi rubric/manuali (`correzione.test=false`). La Quality docente usa `tsc`/`vue-tsc`, build Vite e smoke E2E del sistema composto come evidence della reference solution; non viene spacciata per autograding TypeScript della piattaforma.

## Stato

Versione authoring **`0.13.0`**, ancora `draft` perche il curriculum completo non e congelato.

Decisioni ancora aperte: ORM Node, ampiezza mirror FastAPI/SQLAlchemy, corso SQL separato e calendario definitivo dopo verifica delle ore reali.
