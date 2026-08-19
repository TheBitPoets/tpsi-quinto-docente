# TPSI quinto anno — Content Pack

Questo package contiene i contenuti originali del corso **TPSI quinto anno — Full Stack Web Developer**, a.s. 2026/2027.

Contratto di authoring: `thebitlab.content-pack.v1`.

Il consumer e pinned alla revisione **Accettata** del contratto in `TheBitPoets/2cornot2c`: `5472eef86568a4e7ce59ad34ba937220df27efd7`.

## Principi

- partire dalla Web Platform prima dei framework;
- rendere HTTP esplicito prima di `fetch`/Express;
- usare SQL raw prima dell'ORM;
- separare trasporto HTTP, validation e persistenza;
- usare Node.js + Express come backend principale dopo avere studiato il protocollo;
- mantenere Python/FastAPI come mirror track mirato;
- usare Feisbuc come progetto longitudinale;
- usare documentazioni ufficiali come reference professionali;
- mantenere Activity A–F e separazione studente/docente/grading.

## Contenuti disponibili

1. `00_COURSE_ARCHITECTURE.md` — architettura del percorso e metodo;
2. `01_WEB_PLATFORM_HTML_MODERNO.md` — HTML moderno; milestone 0;
3. `02_CSS_MODERNO_RESPONSIVE.md` — CSS/Flexbox/Grid/responsive; milestone 1;
4. `03_BOOTSTRAP_DA_CSS_A_FRAMEWORK.md` — Bootstrap sopra CSS; milestone 2;
5. `04_JAVASCRIPT_DOM_BROWSER_APIS.md` — JavaScript/DOM/storage; milestone 3;
6. `05_HTTP_ASYNC_FETCH_REST.md` — HTTP/async/fetch/REST; milestone 4;
7. `06_NODE_EXPRESS_BACKEND.md` — Node + Express 5 + backend modulare; milestone 5;
8. `07_SQL_RAW_PERSISTENCE.md` — modello relazionale, DDL/DML, constraint, prepared statement, `node:sqlite` e repository persistente; milestone 6.

## Feisbuc oggi

```text
0  semantic HTML
1  responsive native CSS
2  Bootstrap UI
3  dynamic local JS + localStorage
4  HTTP REST client + node:http fixture
5  Express 5 + MemoryPostStore
6  Express 5 + SqlPostStore + SQLite file
```

Il contratto client rimane:

```text
GET   /api/posts
POST  /api/posts
PATCH /api/posts/:id
```

La milestone 6 dimostra invece questa sostituzione:

```text
Router -> MemoryPostStore
             ↓
         SqlPostStore
             ↓
          SQLite
```

Il Router non conosce `DatabaseSync`; il client non conosce SQLite.

## Activity UDA 24 — Node/Express

- `tpsi5-activity-a-node-http-express-map-001` — confronto native/Express;
- `tpsi5-activity-b-post-validation-001` — validation pura, autograded JS;
- `tpsi5-activity-c-feisbuc-express-api-001` — milestone 5;
- `tpsi5-activity-d-debug-express-pipeline-001` — debug pipeline.

## Activity UDA 24 — SQL raw/persistence

- `tpsi5-activity-a-sql-posts-schema-001` — schema e constraint, **autograded SQL**;
- `tpsi5-activity-b-sql-posts-dml-001` — INSERT/UPDATE/DELETE/view, **autograded SQL**;
- `tpsi5-activity-c-feisbuc-sql-repository-001` — milestone 6 con `node:sqlite` e restart persistence;
- `tpsi5-activity-d-debug-sql-state-001` — debugging constraint/WHERE, **autograded SQL + diagnosi**.

## Boundary SQL / ORM

L'ORM resta **TBD e fuori da questo incremento**.

Prima lo studente deve saper spiegare:

```text
schema
constraint
SELECT
INSERT
UPDATE/DELETE + WHERE
prepared statement
transaction
repository
```

Solo dopo confrontiamo che cosa un ORM astrae e a quale costo.

## Boundary col futuro corso SQL

Nell'organizzazione non esiste ancora un repository SQL dedicato. Per ora questo blocco vive in TPSI5 come consumer reale del Content Pack; la struttura e stata resa autonoma per poter essere estratta in seguito senza rompere il percorso Full Stack.

## Stato

Versione authoring **`0.8.0`**, ancora `draft`.

Il prossimo incremento di UDA24 e **auth sicura**: modello utenti/credential, password hashing, session/authn/authz. SSR/template resta successivo e compatto.
