<!--
content_id: tpsi5-content-sql-raw-persistence
status: draft
curriculum_reference: TPSI quinto - persistenza dati nel backend web
technical_sources: SQLite documentation; Node.js node:sqlite documentation; TheBitLab SQL runner
transformation: original-course-material
-->

# SQL raw e persistenza: dal MemoryPostStore al database

## Obiettivi

Al termine del modulo lo studente deve saper:

- spiegare perche la memoria del processo non e persistenza;
- mappare un oggetto applicativo semplice su una tabella relazionale;
- distinguere DDL, DML e query;
- progettare chiave primaria, `NOT NULL`, `CHECK`, default e indice essenziale;
- usare `INSERT`, `SELECT`, `UPDATE` e `DELETE` senza perdere la semantica HTTP gia studiata;
- capire perche i dati esterni devono essere passati come parametri e non concatenati dentro SQL;
- usare prepared statement dal backend Node;
- distinguere transazione applicativa e singola istruzione SQL atomica;
- sostituire `MemoryPostStore` con `SqlPostStore` senza riscrivere Router, validation o client;
- usare `:memory:` nei test e un file SQLite per dimostrare la persistenza reale.

## Prerequisiti

- UDA 23: HTTP, `fetch`, REST e contratto `GET/POST/PATCH /api/posts`;
- UDA 24 parte 1: Node.js, Express 5, Router, middleware, validation, error model e `MemoryPostStore` iniettato;
- concetti di variabile, oggetto, array, funzione e modulo ES.

## Problema iniziale

La milestone 5 funziona, ma dopo un riavvio del server i post scompaiono.

```text
client
  -> HTTP
  -> Express Router
  -> MemoryPostStore
  -> RAM del processo
```

La RAM e uno stato temporaneo. Serve una frontiera persistente:

```text
client
  -> HTTP
  -> Express Router
  -> PostStore contract
       |-- MemoryPostStore   test / confronto
       `-- SqlPostStore      persistenza
              -> SQLite file
```

Il punto didattico non e semplicemente "aggiungere SQLite". E dimostrare che una buona separazione delle responsabilita rende sostituibile il meccanismo di storage.

## 1. Dal post JavaScript alla relazione

Il dominio corrente usa un oggetto simile a questo:

```js
{
  id: "...",
  author: "Studente",
  text: "Primo post persistente",
  likes: 0,
  liked: false
}
```

Una prima relazione puo essere:

```sql
CREATE TABLE posts (
    id         TEXT PRIMARY KEY,
    author     TEXT NOT NULL,
    text       TEXT NOT NULL,
    likes      INTEGER NOT NULL DEFAULT 0,
    liked      INTEGER NOT NULL DEFAULT 0,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);
```

Ma uno schema utile deve esprimere anche invarianti.

```sql
CREATE TABLE posts (
    id         TEXT PRIMARY KEY,
    author     TEXT NOT NULL CHECK (length(trim(author)) > 0),
    text       TEXT NOT NULL CHECK (length(trim(text)) BETWEEN 1 AND 280),
    likes      INTEGER NOT NULL DEFAULT 0 CHECK (likes >= 0),
    liked      INTEGER NOT NULL DEFAULT 0 CHECK (liked IN (0, 1)),
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
) STRICT;
```

### Perche i vincoli stanno anche nel database?

La validation HTTP protegge il confine della API. I constraint SQL proteggono **lo stato persistente**, anche se in futuro i dati vengono scritti da:

- un altro endpoint;
- uno script amministrativo;
- una migrazione;
- un job;
- un secondo servizio.

Non sono duplicazioni inutili: sono difese su confini diversi.

## 2. Boolean JavaScript e SQLite

SQLite non ha un tipo boolean separato come JavaScript. In questo corso usiamo:

```text
false -> 0
true  -> 1
```

Lo schema impedisce valori diversi con:

```sql
CHECK (liked IN (0, 1))
```

Il repository converte al confine:

```js
const toPost = (row) => ({
  ...row,
  liked: Boolean(row.liked),
});
```

Il Router continua quindi a vedere il dominio applicativo, non i dettagli di rappresentazione SQLite.

## 3. DDL, DML e query

### DDL

Definisce la struttura:

```sql
CREATE TABLE ...;
CREATE INDEX ...;
DROP TABLE ...;
ALTER TABLE ...;
```

### DML

Modifica i dati:

```sql
INSERT INTO posts (...)
VALUES (...);

UPDATE posts
SET liked = 1
WHERE id = 'p1';

DELETE FROM posts
WHERE id = 'p1';
```

### Query

Legge i dati:

```sql
SELECT id, author, text, likes, liked
FROM posts
ORDER BY created_at DESC;
```

Una `SELECT` non deve essere usata per nascondere modifiche di stato. Il vecchio `lab8` usava route GET per creare/distruggere schema: nel nuovo corso quel pattern e esplicitamente ritirato.

## 4. La clausola WHERE e parte della sicurezza logica

Confronta:

```sql
UPDATE posts
SET liked = 1;
```

con:

```sql
UPDATE posts
SET liked = 1
WHERE id = ?;
```

Nel primo caso **tutte** le righe vengono modificate.

Prima di eseguire un `UPDATE` o `DELETE`, chiediti sempre:

1. quale insieme di righe sto selezionando?
2. il `WHERE` esprime davvero quell'insieme?
3. cosa succede con zero righe?
4. cosa succede con piu righe del previsto?

Questo metodo diventa Activity D.

## 5. Filtrare liked

Il contratto REST gia supporta:

```http
GET /api/posts
GET /api/posts?liked=true
GET /api/posts?liked=false
```

In SQL possiamo mantenere due prepared statement semplici:

```sql
SELECT id, author, text, likes, liked, created_at
FROM posts
ORDER BY created_at DESC, id DESC;
```

oppure:

```sql
SELECT id, author, text, likes, liked, created_at
FROM posts
WHERE liked = ?
ORDER BY created_at DESC, id DESC;
```

Non serve generare SQL dinamico quando il dominio ha pochi casi chiari.

## 6. Prepared statement: dati separati dal programma SQL

Da evitare:

```js
const sql = `SELECT * FROM posts WHERE id = '${id}'`;
```

Qui un dato esterno diventa parte del testo SQL.

Da preferire:

```js
const statement = db.prepare(`
  SELECT id, author, text, likes, liked, created_at
  FROM posts
  WHERE id = ?
`);

const row = statement.get(id);
```

Il database riceve separatamente:

```text
programma SQL
+
valori da associare ai placeholder
```

Questo evita di affidare all'input il compito di produrre sintassi SQL e riduce il rischio di SQL injection.

## 7. Perche SQLite in questo corso

SQLite e adatto alla milestone perche:

- non richiede un server DB separato;
- produce un file facile da ispezionare e cancellare;
- supporta SQL relazionale, constraint, indici, prepared statement e transazioni;
- consente `:memory:` nei test;
- rende visibile il passaggio da RAM a persistenza senza aggiungere infrastruttura prematuramente.

Non significa che ogni applicazione reale debba usare SQLite. Il concetto da imparare e il **repository SQL** e il contratto relazionale.

## 8. `node:sqlite`

Nel baseline Node 22 del corso usiamo il modulo built-in:

```js
import { DatabaseSync } from "node:sqlite";

const db = new DatabaseSync(":memory:");
```

Il modulo e disponibile da Node 22.5.0; nella linea Node 22 da 22.13 non richiede piu il flag `--experimental-sqlite`, pur restando una API da trattare con attenzione rispetto alla stabilita della versione.

Per il laboratorio richiediamo quindi Node `>=22.13` e pinniamo la CI alla linea Node 22 corrente.

### Database in memoria

```js
new DatabaseSync(":memory:");
```

Utile per test isolati.

### Database su file

```js
new DatabaseSync("data/feisbuc.db");
```

Utile per dimostrare che lo stato sopravvive al riavvio del processo.

## 9. Schema inizializzato dal backend

Separiamo schema e codice:

```text
src/
  schema.sql
  sql-post-store.js
```

`schema.sql` contiene DDL idempotente:

```sql
CREATE TABLE IF NOT EXISTS posts (...);
CREATE INDEX IF NOT EXISTS idx_posts_liked_created
ON posts(liked, created_at DESC);
```

Il backend legge il file e lo esegue all'avvio.

Per progetti piu grandi useremo migrazioni versionate. Qui il primo obiettivo e distinguere chiaramente:

```text
schema
!=
seed
!=
query applicative
```

## 10. Seed idempotente

Un seed didattico non deve duplicarsi a ogni riavvio.

```sql
INSERT OR IGNORE INTO posts (...)
VALUES (...);
```

Oppure il codice verifica se la tabella e vuota prima del seed.

L'importante e poter avviare il lab piu volte senza moltiplicare i dati iniziali.

## 11. Il contratto PostStore non cambia

Milestone 5:

```js
postStore.list({ liked })
postStore.create({ text, author })
postStore.setLiked(id, liked)
```

Milestone 6 usa **gli stessi metodi**.

```text
Posts Router
    |
    | chiama lo stesso contratto
    v
SqlPostStore
    |
    v
prepared statements
    |
    v
SQLite
```

Il Router non deve importare `DatabaseSync`.

Questa e la prova pratica del principio di inversione della dipendenza: il trasporto HTTP dipende da un contratto applicativo, non dal database concreto.

## 12. Creazione di un post

Il server continua a generare l'identita:

```js
const id = randomUUID();
```

Poi usa un prepared statement:

```sql
INSERT INTO posts (id, author, text, likes, liked)
VALUES (?, ?, ?, 0, 0);
```

Dopo l'insert il repository legge e restituisce la representation canonica.

Il Router continua a rispondere:

```http
201 Created
Location: /api/posts/<id>
Content-Type: application/json
```

Il database non decide lo status HTTP.

## 13. Aggiornare il like in una sola istruzione

Il valore di `likes` dipende dalla transizione di `liked`.

Una versione atomica usa `CASE`:

```sql
UPDATE posts
SET
  likes = CASE
    WHEN liked = ? THEN likes
    WHEN ? = 1 THEN likes + 1
    WHEN likes > 0 THEN likes - 1
    ELSE 0
  END,
  liked = ?
WHERE id = ?;
```

Poi il repository esegue una `SELECT` per restituire lo stato aggiornato.

Il vantaggio e evitare il ciclo fragile:

```text
SELECT stato
-> modifica in JavaScript
-> UPDATE separato
```

quando una singola istruzione SQL puo esprimere la transizione.

## 14. Transazioni

Una singola istruzione SQL e atomica. Ma alcune operazioni future richiederanno piu statement che devono riuscire o fallire insieme.

Schema mentale:

```sql
BEGIN;
-- operazione 1
-- operazione 2
COMMIT;
```

In caso di errore:

```sql
ROLLBACK;
```

Esempio futuro: creare un post e registrare contemporaneamente un evento di audit.

Non useremo una transazione solo perche "suona professionale": la usiamo quando esiste un **invariante multi-statement**.

## 15. Indici

Un indice non e una decorazione obbligatoria.

Aggiungiamo:

```sql
CREATE INDEX IF NOT EXISTS idx_posts_liked_created
ON posts(liked, created_at DESC);
```

perche abbiamo una query reale:

```text
filtra per liked
+
ordina cronologicamente
```

La regola e:

```text
query reale -> misura/analizza -> indice motivato
```

non:

```text
aggiungi indici a ogni colonna
```

L'analisi con `EXPLAIN QUERY PLAN` puo diventare estensione avanzata.

## 16. Errori database e errori HTTP

Non tutti gli errori SQLite devono diventare `500` con il testo grezzo del DB.

Il repository puo:

- restituire `null` se l'id non esiste;
- propagare un errore tecnico inatteso;
- non esporre path locali o dettagli interni nel JSON pubblico.

Il Router conserva la semantica applicativa:

```text
post non trovato -> 404 post-not-found
input invalido   -> 400 ...
DB inatteso       -> 500 internal-error
```

Il logger docente/server puo avere piu dettaglio della response pubblica.

## 17. Percorsi portabili

Da evitare, come nel materiale legacy:

```js
new Database("C:\\Users\\...\\test.db")
```

Il percorso va derivato da config e progetto:

```text
DB_PATH=data/feisbuc.db
```

Per test:

```text
DB_PATH=:memory:
```

Per CI di persistenza useremo un file temporaneo creato dal test.

## 18. Confronto implementazioni

### MemoryPostStore

**Pro**

- semplicissimo;
- velocissimo nei test;
- nessun I/O persistente.

**Contro**

- perde tutto al restart;
- non esercita SQL/constraint.

### SqlPostStore

**Pro**

- persistenza reale;
- constraint e query espressivi;
- stesso contratto del Router;
- database ispezionabile.

**Contro**

- introduce schema e lifecycle DB;
- I/O sincrono con `DatabaseSync` nel processo Node;
- richiede ragionare su query, errori e migrazioni.

Per questa scala didattica il trade-off e intenzionale. In sistemi ad alta concorrenza valuteremmo driver/architetture differenti.

## 19. Feisbuc milestone 6

La UI e la API restano uguali.

```text
Feisbuc milestone 5
client -> api.js -> Express -> Router -> MemoryPostStore

Feisbuc milestone 6
client -> api.js -> Express -> Router -> SqlPostStore -> SQLite file
```

Definition of done:

1. il client non cambia contratto;
2. `GET`, `POST`, `PATCH` mantengono status e representation;
3. i post sopravvivono al restart del server;
4. input esterno entra in SQL solo tramite binding;
5. constraint proteggono gli invarianti persistenti;
6. `DB_PATH=:memory:` funziona nei test;
7. nessun path assoluto macchina-specifico;
8. nessun ORM.

## 20. Errori frequenti

- creare tabelle dentro una route GET;
- concatenare input in una query;
- dimenticare `WHERE` in `UPDATE`/`DELETE`;
- usare un path assoluto del proprio PC;
- mettere SQL direttamente nel Router;
- affidarsi solo alla validation HTTP e non avere constraint;
- trasformare ogni errore DB in `400`;
- salvare `true`/`false` senza definire la rappresentazione SQL;
- cambiare il client quando cambia soltanto il repository;
- introdurre ORM prima di capire le query che dovrebbe astrarre.

## 21. Esercizi A-F

### A — osserva e verifica lo schema

Crea la tabella `posts`, inserisci seed e usa query di verifica. Activity autograded SQL.

### B — modifica controllata

Applica DML e filtri mantenendo invarianti e risultati deterministici. Activity autograded SQL.

### C — implementazione autonoma

Sostituisci `MemoryPostStore` con `SqlPostStore` senza cambiare Router/client. Feisbuc milestone 6.

### D — debugging

Ripara uno script che aggiorna righe sbagliate e viola invarianti perche il `WHERE` e il modello di stato sono errati. Activity autograded SQL + diagnosi.

### E — mini-progetto

Aggiungi una seconda risorsa persistente, ad esempio `profiles`, con schema, repository e almeno una relazione motivata.

### F — prodotto integrato

Nel capstone finale collega persistenza, auth e realtime mantenendo migrazioni/schema versionati e test E2E.

## 22. Laboratorio

Flusso consigliato:

```text
Activity A SQL
  -> Activity B SQL
  -> confronta MemoryPostStore / SqlPostStore
  -> Activity C Feisbuc milestone 6
  -> kill/restart server
  -> verifica persistenza
  -> Activity D debug SQL
```

## 23. Verifica rapida

1. Perche `MemoryPostStore` non e persistenza?
2. Quale responsabilita appartiene al Router e quale al repository?
3. Perche `CHECK (liked IN (0,1))` e utile anche se il Router valida il body?
4. Che differenza c'e tra SQL con placeholder e concatenazione di stringhe?
5. Perche un `UPDATE` senza `WHERE` e pericoloso?
6. Quando serve una transazione?
7. Perche usiamo `:memory:` nei test?
8. Quale parte del client deve cambiare passando da memoria a SQLite? Idealmente nessuna.

## 24. Sintesi inclusiva

```text
RAM
  = stato temporaneo

SQLite
  = stato persistente

schema
  = regole sui dati

prepared statement
  = SQL + parametri separati

repository
  = confine tra dominio e database

buona architettura
  = cambiare storage senza cambiare HTTP/client
```

## 25. Fonti e collegamenti

Fonti tecniche da consultare, non da copiare:

- documentazione SQLite: SQL language, constraints e transactions;
- documentazione Node.js `node:sqlite` / `DatabaseSync` / prepared statements;
- TheBitLab SQL runner: SQLite isolato in memoria per grading deterministico;
- `kinderp/lab8` come provenance storica di Express + SQLite, con pattern mutating-GET ritirato;
- `labs_summary` come progressione storica.

## 26. Activity correlate

- `tpsi5-activity-a-sql-posts-schema-001`;
- `tpsi5-activity-b-sql-posts-dml-001`;
- `tpsi5-activity-c-feisbuc-sql-repository-001`;
- `tpsi5-activity-d-debug-sql-state-001`.

## Confine del prossimo incremento

Dopo questa parte, il database contiene ancora **post senza utenti autenticati**.

Il passo successivo sara:

```text
SQL raw persistence
  -> utenti/credential model
  -> password hashing
  -> session/authn/authz
```

Non introduciamo ancora ORM: prima vogliamo poter leggere e spiegare il SQL reale che l'ORM andra eventualmente ad astrarre.
