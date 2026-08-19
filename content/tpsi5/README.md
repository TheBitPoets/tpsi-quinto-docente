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
- Vue viene introdotto **dopo** DOM manuale/API/auth/SSR come astrazione di concetti gia osservati;
- Vue Router entra solo quando l'URL deve rappresentare piu viste;
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
11. `10_VUE3_COMPONENTI_REATTIVITA.md` — Vue 3/Vite, reattivita, componenti e prima SPA; milestone 9;
12. `11_VUE_ROUTER_NAVIGAZIONE_SPA.md` — Vue Router, URL/history, route protette e deep-link fallback; milestone 10.

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
```

Milestone 10 aggiunge **navigazione**, non un nuovo backend:

```text
browser URL
   ↓
Vue Router
   ├── LoginView
   ├── FeedView
   ├── AboutView
   └── NotFoundView
        ↓
      api.js
        ↓
     /api/*
        ↓
session + Express + SQLite
```

Il session token resta nel cookie `HttpOnly`; Vue non legge `document.cookie` e non usa storage per l'autenticazione. La navigation guard migliora la UX, mentre 401/403 e ownership restano responsabilita del backend.

## Decisione frontend

D1 e congelata:

```text
framework core = Vue 3 + Vite
router core    = Vue Router
React          = translation/comparison lab
```

Le reference UDA25 pinning correnti sono:

```text
Vue                  3.5.40
Vue Router           5.2.0
Vite                 8.2.1
@vitejs/plugin-vue   6.0.8
Node                 >=22.18
```

TypeScript resta `TBD`: direzione preferita, introduzione mirata sui tipi del dominio e sui confini applicativi dopo i fondamenti Vue/routing.

## Activity UDA25 — Vue foundations

- `tpsi5-activity-a-vue-reactivity-microscope-001` — `ref`/`computed` come osservazione guidata;
- `tpsi5-activity-b-vue-post-card-001` — props down / emits up;
- `tpsi5-activity-c-feisbuc-vue-spa-001` — milestone 9, SPA a singola vista sopra API/auth esistenti;
- `tpsi5-activity-d-debug-vue-reactivity-001` — debug reattivita, state derivato, prop mutation, event contract e key.

## Activity UDA25 — routing

- `tpsi5-activity-a-vue-router-microscope-001` — URL, RouterLink/RouterView, history e deep link;
- `tpsi5-activity-b-navigation-policy-001` — policy di navigazione pura, autograded JS;
- `tpsi5-activity-c-feisbuc-vue-router-001` — milestone 10 con route protette e fallback Express;
- `tpsi5-activity-d-debug-vue-router-001` — diagnosi di base, guard loop, catch-all e wildcard server.

## Boundary UDA25

Non sono ancora introdotti:

```text
Pinia
TypeScript
WebSocket / Socket.IO
ORM
```

Il piccolo stato condiviso della sessione usa un composable/module. Pinia entra solo se emerge un problema di stato condiviso piu ampio. Realtime entrera dopo il gate TypeScript.

## Grading

Il browser grader TheBitLab non e ancora implementato. Le Activity Vue/router restano quindi rubric/manuali quando richiedono comportamento browser; la navigation policy B e invece autograded come JavaScript puro. La Quality docente installa dipendenze pinned, compila le reference, compone il frontend routed con il backend auth e verifica anche il deep-link HTTP `/vue/feed`. Questa evidence non viene spacciata per autograding browser dello studente.

## Stato

Versione authoring **`0.12.0`**, ancora `draft` perche il curriculum completo non e congelato.

Decisioni ancora aperte: profondita TypeScript, ORM Node, ampiezza mirror FastAPI/SQLAlchemy, corso SQL separato e calendario definitivo dopo verifica delle ore reali.
