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
11. `10_VUE3_COMPONENTI_REATTIVITA.md` — Vue 3/Vite, reattivita, componenti e prima SPA; milestone 9.

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
```

Milestone 9 cambia ancora una volta **solo il presentation layer**:

```text
browser
  -> Vue App
     -> props/emits + reactive state
     -> api.js
     -> /api/* JSON
     -> session + Express + SQLite
```

Il session token resta nel cookie `HttpOnly`; Vue non legge `document.cookie` e non usa storage per l'autenticazione.

## Decisione frontend

D1 e congelata:

```text
framework core = Vue 3 + Vite
React          = translation/comparison lab
```

La prima verticale pinna nelle reference:

```text
Vue                  3.5.40
Vite                 8.2.1
@vitejs/plugin-vue   6.0.8
Node                 >=22.18
```

TypeScript resta `TBD`: direzione preferita, introduzione mirata sui tipi del dominio e sui confini applicativi dopo i fondamenti Vue.

## Activity UDA25 — Vue foundations

- `tpsi5-activity-a-vue-reactivity-microscope-001` — `ref`/`computed` come osservazione guidata;
- `tpsi5-activity-b-vue-post-card-001` — props down / emits up;
- `tpsi5-activity-c-feisbuc-vue-spa-001` — milestone 9, SPA a singola vista sopra API/auth esistenti;
- `tpsi5-activity-d-debug-vue-reactivity-001` — debug reattivita, state derivato, prop mutation, event contract e key.

## Boundary della prima verticale Vue

Non sono ancora introdotti:

```text
Vue Router
Pinia
TypeScript
WebSocket / Socket.IO
ORM
```

Il secondo blocco UDA25 introdurra il routing perche emergera un requisito reale: **URL e navigazione fra viste**. Realtime entrera dopo il routing.

## Grading

Il browser grader TheBitLab non e ancora implementato. Le Activity Vue restano quindi rubric/manuali; la Quality del repository docente installa le dipendenze pinned, compila le reference con Vite e verifica la composizione della SPA con il backend auth esistente. Questa evidence non viene spacciata per autograding della consegna studente.

## Stato

Versione authoring **`0.11.0`**, ancora `draft` perche il curriculum completo non e congelato.

Decisioni ancora aperte: profondita TypeScript, ORM Node, ampiezza mirror FastAPI/SQLAlchemy, corso SQL separato e calendario definitivo dopo verifica delle ore reali.
