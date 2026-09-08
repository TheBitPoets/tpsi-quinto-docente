<!--
content_id: tpsi5-content-sql-raw-persistence
status: draft
curriculum_reference: TPSI quinto - persistenza dati nel backend web
technical_sources: SQLite documentation; Node.js node:sqlite documentation; TheBitLab SQL runner
transformation: original-course-material
-->

# SQL raw e persistenza: dal MemoryPostStore al database

<table align="center" width="100%"><tr><td>
<details>
<summary>&#128506; <strong>Orientamento della lezione</strong></summary>

<p align="justify"><strong>Contesto:</strong> il backend Express espone già il contratto corretto, ma perde i dati a ogni riavvio. Introduciamo SQL raw per rendere visibili schema, vincoli, query e transazioni prima di qualunque ORM.</p>
<p align="justify"><strong>Domande guida:</strong> come diventa una risorsa JavaScript una riga relazionale? Quali invarianti appartengono al database? Come si separano dati e istruzione SQL?</p>
<p align="justify"><strong>Obiettivi osservabili:</strong> progettare una tabella con vincoli, eseguire CRUD con parametri, motivare un indice, delimitare una transazione e verificare la persistenza dopo un riavvio.</p>
<p align="justify"><strong>Prossimo passo:</strong> la lezione 08 aggiungerà utenti, password hash, sessioni e authorization sopra lo stesso database.</p>

</details>
</td></tr></table>

## Obiettivi

<p align="justify">Al termine del modulo lo studente deve saper:</p>

<ul>
  <li>spiegare perche la memoria del processo non e persistenza;</li>
  <li>mappare un oggetto applicativo semplice su una tabella relazionale;</li>
  <li>distinguere DDL, DML e query;</li>
  <li>progettare chiave primaria, <code>NOT NULL</code>, <code>CHECK</code>, default e indice essenziale;</li>
  <li>usare <code>INSERT</code>, <code>SELECT</code>, <code>UPDATE</code> e <code>DELETE</code> senza perdere la semantica HTTP gia studiata;</li>
  <li>capire perche i dati esterni devono essere passati come parametri e non concatenati dentro SQL;</li>
  <li>usare prepared statement dal backend Node;</li>
  <li>distinguere transazione applicativa e singola istruzione SQL atomica;</li>
  <li>sostituire <code>MemoryPostStore</code> con <code>SqlPostStore</code> senza riscrivere Router, validation o client;</li>
  <li>usare <code>:memory:</code> nei test e un file SQLite per dimostrare la persistenza reale.</li>
</ul>

## Prerequisiti

<ul>
  <li>UDA 23: HTTP, <code>fetch</code>, REST e contratto <code>GET/POST/PATCH /api/posts</code>;</li>
  <li>UDA 24 parte 1: Node.js, Express 5, Router, middleware, validation, error model e <code>MemoryPostStore</code> iniettato;</li>
  <li>concetti di variabile, oggetto, array, funzione e modulo ES.</li>
</ul>

## Orientamento nella documentazione

<p align="center">
  <img src="../../assets/tpsi5/lesson-documentation-depth.svg" alt="La dispensa seleziona nelle fonti ufficiali i contenuti da studiare ora, riconoscere, rimandare o dichiarare fuori confine">
</p>

<table align="center"><tr><td>
<details>
<summary>&#128279; <strong>Indice incrociato — SQL raw e SQLite ↔ documentazione ufficiale</strong></summary>

<table align="center">
<thead><tr><th>Dispensa</th><th>Documentazione ufficiale</th><th>Profondità</th></tr></thead>
<tbody>
<tr><td><a href="#lesson-sql-schema">Relazione, tipi e vincoli</a></td><td><a href="https://www.sqlite.org/lang_createtable.html">SQLite — CREATE TABLE</a><br><a href="https://www.sqlite.org/datatype3.html">Datatypes in SQLite</a></td><td>&#128994; studiare ora</td></tr>
<tr><td><a href="#lesson-sql-queries">SELECT e mutazioni parametrizzate</a></td><td><a href="https://www.sqlite.org/lang.html">SQL as understood by SQLite</a><br><a href="https://nodejs.org/api/sqlite.html">Node.js SQLite</a></td><td>&#128994; studiare ora</td></tr>
<tr><td><a href="#lesson-sql-transactions">Transazioni</a></td><td><a href="https://www.sqlite.org/lang_transaction.html">SQLite — Transactions</a></td><td>&#128994; studiare ora</td></tr>
<tr><td><a href="#lesson-sql-indexes">Indici e query planner</a></td><td><a href="https://www.sqlite.org/queryplanner.html">SQLite — Query Planning</a></td><td>&#128994; comprendere il modello di base</td></tr>
<tr><td>Join complessi, window function e tuning avanzato</td><td><a href="https://www.sqlite.org/lang.html">SQLite language reference</a></td><td>&#128993; riconoscere, fuori dal core TPSI</td></tr>
</tbody>
</table>

</details>
</td></tr></table>

## Problema iniziale

<p align="justify">La milestone 5 funziona, ma dopo un riavvio del server i post scompaiono.</p>

```text
client
  -> HTTP
  -> Express Router
  -> MemoryPostStore
  -> RAM del processo
```

<p align="justify">La RAM e uno stato temporaneo. Serve una frontiera persistente:</p>

```text
client
  -> HTTP
  -> Express Router
  -> PostStore contract
       |-- MemoryPostStore   test / confronto
       `-- SqlPostStore      persistenza
              -> SQLite file
```

<p align="justify">Il punto didattico non e semplicemente "aggiungere SQLite". E dimostrare che una buona separazione delle responsabilita rende sostituibile il meccanismo di storage.</p>

<a id="lesson-sql-schema"></a>
## 1. Dal post JavaScript alla relazione

<p align="justify">Il dominio corrente usa un oggetto simile a questo:</p>

```js
{
  id: "...",
  author: "Studente",
  text: "Primo post persistente",
  likes: 0,
  liked: false
}
```

<p align="justify">Una prima relazione puo essere:</p>

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

<p align="justify">Ma uno schema utile deve esprimere anche invarianti.</p>

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

<p align="justify">La validation HTTP protegge il confine della API. I constraint SQL proteggono <strong>lo stato persistente</strong>, anche se in futuro i dati vengono scritti da:</p>

<ul>
  <li>un altro endpoint;</li>
  <li>uno script amministrativo;</li>
  <li>una migrazione;</li>
  <li>un job;</li>
  <li>un secondo servizio.</li>
</ul>

<p align="justify">Non sono duplicazioni inutili: sono difese su confini diversi.</p>

### `NULL` non e una stringa vuota

<p align="justify"><code>NULL</code> rappresenta un'informazione assente o sconosciuta. Non coincide con <code>''</code>, con <code>0</code> o con <code>false</code>. Per questo un confronto come <code>value = NULL</code> non produce il risultato atteso: si usano <code>IS NULL</code> e <code>IS NOT NULL</code>.</p>

```sql
SELECT id, author
FROM posts
WHERE deleted_at IS NULL;
```

<p align="justify">La logica SQL include infatti un terzo esito, <strong>unknown</strong>, oltre a vero e falso. Nel nostro primo schema molti campi sono <code>NOT NULL</code> proprio per eliminare stati ambigui che il dominio non ammette. Quando un dato puo davvero mancare, la sua assenza deve essere una scelta esplicita del modello.</p>

### Relazioni e chiavi esterne: il passo successivo

<p align="justify">Una tabella non diventa "relazionale" soltanto perche ha righe e colonne. Le risorse possono essere collegate attraverso chiavi:</p>

```sql
CREATE TABLE users (
    id       TEXT PRIMARY KEY,
    username TEXT NOT NULL UNIQUE
);

CREATE TABLE posts (
    id        TEXT PRIMARY KEY,
    author_id TEXT NOT NULL REFERENCES users(id),
    text      TEXT NOT NULL
);
```

<p align="justify"><code>posts.author_id</code> identifica la riga autore in <code>users</code>; la foreign key impedisce, se i vincoli sono attivi, di riferirsi a un utente inesistente. Una <code>JOIN</code> ricompone i dati quando la lettura ha bisogno di entrambe le relazioni:</p>

```sql
SELECT posts.id, posts.text, users.username AS author
FROM posts
JOIN users ON users.id = posts.author_id;
```

<p align="justify">In questa lezione bisogna riconoscere chiave primaria, chiave esterna e <code>JOIN</code>. La modellazione completa di utenti e post viene applicata nel modulo di autenticazione. I riferimenti ufficiali sono <a href="https://www.sqlite.org/lang_createtable.html">CREATE TABLE</a> e <a href="https://www.sqlite.org/lang_select.html">SELECT</a>.</p>

## 2. Boolean JavaScript e SQLite

<p align="justify">SQLite non ha un tipo boolean separato come JavaScript. In questo corso usiamo:</p>

```text
false -> 0
true  -> 1
```

<p align="justify">Lo schema impedisce valori diversi con:</p>

```sql
CHECK (liked IN (0, 1))
```

<p align="justify">Il repository converte al confine:</p>

```js
const toPost = (row) => ({
  ...row,
  liked: Boolean(row.liked),
});
```

<p align="justify">Il Router continua quindi a vedere il dominio applicativo, non i dettagli di rappresentazione SQLite.</p>

<a id="lesson-sql-queries"></a>
## 3. DDL, DML e query

### DDL

<p align="justify">Definisce la struttura:</p>

```sql
CREATE TABLE ...;
CREATE INDEX ...;
DROP TABLE ...;
ALTER TABLE ...;
```

### DML

<p align="justify">Modifica i dati:</p>

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

<p align="justify">Legge i dati:</p>

```sql
SELECT id, author, text, likes, liked
FROM posts
ORDER BY created_at DESC;
```

<p align="justify">Una <code>SELECT</code> non deve essere usata per nascondere modifiche di stato. Il vecchio <code>lab8</code> usava route GET per creare/distruggere schema: nel nuovo corso quel pattern e esplicitamente ritirato.</p>

## 4. La clausola WHERE e parte della sicurezza logica

<p align="justify">Confronta:</p>

```sql
UPDATE posts
SET liked = 1;
```

<p align="justify">con:</p>

```sql
UPDATE posts
SET liked = 1
WHERE id = ?;
```

<p align="justify">Nel primo caso <strong>tutte</strong> le righe vengono modificate.</p>

<p align="justify">Prima di eseguire un <code>UPDATE</code> o <code>DELETE</code>, chiediti sempre:</p>

<ol>
  <li>quale insieme di righe sto selezionando?</li>
  <li>il <code>WHERE</code> esprime davvero quell'insieme?</li>
  <li>cosa succede con zero righe?</li>
  <li>cosa succede con piu righe del previsto?</li>
</ol>

<p align="justify">Questo metodo diventa Activity D.</p>

## 5. Filtrare liked

<p align="justify">Il contratto REST gia supporta:</p>

```http
GET /api/posts
GET /api/posts?liked=true
GET /api/posts?liked=false
```

<p align="justify">In SQL possiamo mantenere due prepared statement semplici:</p>

```sql
SELECT id, author, text, likes, liked, created_at
FROM posts
ORDER BY created_at DESC, id DESC;
```

<p align="justify">oppure:</p>

```sql
SELECT id, author, text, likes, liked, created_at
FROM posts
WHERE liked = ?
ORDER BY created_at DESC, id DESC;
```

<p align="justify">Non serve generare SQL dinamico quando il dominio ha pochi casi chiari.</p>

## 6. Prepared statement: dati separati dal programma SQL

<p align="justify">Da evitare:</p>

```js
const sql = `SELECT * FROM posts WHERE id = '${id}'`;
```

<p align="justify">Qui un dato esterno diventa parte del testo SQL.</p>

<p align="justify">Da preferire:</p>

```js
const statement = db.prepare(`
  SELECT id, author, text, likes, liked, created_at
  FROM posts
  WHERE id = ?
`);

const row = statement.get(id);
```

<p align="justify">Il database riceve separatamente:</p>

```text
programma SQL
+
valori da associare ai placeholder
```

<p align="justify">Questo evita di affidare all'input il compito di produrre sintassi SQL e riduce il rischio di SQL injection.</p>

## 7. Perche SQLite in questo corso

<p align="justify">SQLite e adatto alla milestone perche:</p>

<ul>
  <li>non richiede un server DB separato;</li>
  <li>produce un file facile da ispezionare e cancellare;</li>
  <li>supporta SQL relazionale, constraint, indici, prepared statement e transazioni;</li>
  <li>consente <code>:memory:</code> nei test;</li>
  <li>rende visibile il passaggio da RAM a persistenza senza aggiungere infrastruttura prematuramente.</li>
</ul>

<p align="justify">Non significa che ogni applicazione reale debba usare SQLite. Il concetto da imparare e il <strong>repository SQL</strong> e il contratto relazionale.</p>

## 8. `node:sqlite`

<p align="justify">Nel baseline Node 22 del corso usiamo il modulo built-in:</p>

```js
import { DatabaseSync } from "node:sqlite";

const db = new DatabaseSync(":memory:");
```

<p align="justify">Il modulo e disponibile da Node 22.5.0; nella linea Node 22 da 22.13 non richiede piu il flag <code>--experimental-sqlite</code>, pur restando una API da trattare con attenzione rispetto alla stabilita della versione.</p>

<p align="justify">Per il laboratorio richiediamo quindi Node <code>&gt;=22.13</code> e pinniamo la CI alla linea Node 22 corrente.</p>

### Database in memoria

```js
new DatabaseSync(":memory:");
```

<p align="justify">Utile per test isolati.</p>

### Database su file

```js
new DatabaseSync("data/feisbuc.db");
```

<p align="justify">Utile per dimostrare che lo stato sopravvive al riavvio del processo.</p>

## 9. Schema inizializzato dal backend

<p align="justify">Separiamo schema e codice:</p>

```text
src/
  schema.sql
  sql-post-store.js
```

<p align="justify"><code>schema.sql</code> contiene DDL idempotente:</p>

```sql
CREATE TABLE IF NOT EXISTS posts (...);
CREATE INDEX IF NOT EXISTS idx_posts_liked_created
ON posts(liked, created_at DESC);
```

<p align="justify">Il backend legge il file e lo esegue all'avvio.</p>

<p align="justify">Per progetti piu grandi useremo migrazioni versionate. Qui il primo obiettivo e distinguere chiaramente:</p>

```text
schema
!=
seed
!=
query applicative
```

## 10. Seed idempotente

<p align="justify">Un seed didattico non deve duplicarsi a ogni riavvio.</p>

```sql
INSERT OR IGNORE INTO posts (...)
VALUES (...);
```

<p align="justify">Oppure il codice verifica se la tabella e vuota prima del seed.</p>

<p align="justify">L'importante e poter avviare il lab piu volte senza moltiplicare i dati iniziali.</p>

## 11. Il contratto PostStore non cambia

<p align="justify">Milestone 5:</p>

```js
postStore.list({ liked })
postStore.create({ text, author })
postStore.setLiked(id, liked)
```

<p align="justify">Milestone 6 usa <strong>gli stessi metodi</strong>.</p>

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

<p align="justify">Il Router non deve importare <code>DatabaseSync</code>.</p>

<p align="justify">Questa e la prova pratica del principio di inversione della dipendenza: il trasporto HTTP dipende da un contratto applicativo, non dal database concreto.</p>

## 12. Creazione di un post

<p align="justify">Il server continua a generare l'identita:</p>

```js
const id = randomUUID();
```

<p align="justify">Poi usa un prepared statement:</p>

```sql
INSERT INTO posts (id, author, text, likes, liked)
VALUES (?, ?, ?, 0, 0);
```

<p align="justify">Dopo l'insert il repository legge e restituisce la representation canonica.</p>

<p align="justify">Il Router continua a rispondere:</p>

```http
201 Created
Location: /api/posts/<id>
Content-Type: application/json
```

<p align="justify">Il database non decide lo status HTTP.</p>

## 13. Aggiornare il like in una sola istruzione

<p align="justify">Il valore di <code>likes</code> dipende dalla transizione di <code>liked</code>.</p>

<p align="justify">Una versione atomica usa <code>CASE</code>:</p>

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

<p align="justify">Poi il repository esegue una <code>SELECT</code> per restituire lo stato aggiornato.</p>

<p align="justify">Il vantaggio e evitare il ciclo fragile:</p>

```text
SELECT stato
-> modifica in JavaScript
-> UPDATE separato
```

<p align="justify">quando una singola istruzione SQL puo esprimere la transizione.</p>

<a id="lesson-sql-transactions"></a>
## 14. Transazioni

<p align="justify">Una singola istruzione SQL e atomica. Ma alcune operazioni future richiederanno piu statement che devono riuscire o fallire insieme.</p>

<p align="justify">Schema mentale:</p>

```sql
BEGIN;
-- operazione 1
-- operazione 2
COMMIT;
```

<p align="justify">In caso di errore:</p>

```sql
ROLLBACK;
```

<p align="justify">Esempio futuro: creare un post e registrare contemporaneamente un evento di audit.</p>

<p align="justify">Non useremo una transazione solo perche "suona professionale": la usiamo quando esiste un <strong>invariante multi-statement</strong>.</p>

<a id="lesson-sql-indexes"></a>
## 15. Indici

<p align="justify">Un indice non e una decorazione obbligatoria.</p>

<p align="justify">Aggiungiamo:</p>

```sql
CREATE INDEX IF NOT EXISTS idx_posts_liked_created
ON posts(liked, created_at DESC);
```

<p align="justify">perche abbiamo una query reale:</p>

```text
filtra per liked
+
ordina cronologicamente
```

<p align="justify">La regola e:</p>

```text
query reale -> misura/analizza -> indice motivato
```

<p align="justify">non:</p>

```text
aggiungi indici a ogni colonna
```

<p align="justify">Prima e dopo aver aggiunto un indice possiamo chiedere a SQLite come intende eseguire la query:</p>

```sql
EXPLAIN QUERY PLAN
SELECT id, author, text
FROM posts
WHERE liked = 1
ORDER BY created_at DESC;
```

<p align="justify">Nel risultato impariamo a distinguere almeno una scansione completa (<code>SCAN</code>) da una ricerca che sfrutta un indice (<code>SEARCH ... USING INDEX</code>). Il piano e una spiegazione del percorso scelto dal database, non una misura del tempo: per ottimizzare davvero servono anche dati realistici e misure. La <a href="https://www.sqlite.org/eqp.html">guida ufficiale a EXPLAIN QUERY PLAN</a> e materiale di consultazione guidata.</p>

## 16. Errori database e errori HTTP

<p align="justify">Non tutti gli errori SQLite devono diventare <code>500</code> con il testo grezzo del DB.</p>

<p align="justify">Il repository puo:</p>

<ul>
  <li>restituire <code>null</code> se l'id non esiste;</li>
  <li>propagare un errore tecnico inatteso;</li>
  <li>non esporre path locali o dettagli interni nel JSON pubblico.</li>
</ul>

<p align="justify">Il Router conserva la semantica applicativa:</p>

```text
post non trovato -> 404 post-not-found
input invalido   -> 400 ...
DB inatteso       -> 500 internal-error
```

<p align="justify">Il logger docente/server puo avere piu dettaglio della response pubblica.</p>

## 17. Percorsi portabili

<p align="justify">Da evitare, come nel materiale legacy:</p>

```js
new Database("C:\\Users\\...\\test.db")
```

<p align="justify">Il percorso va derivato da config e progetto:</p>

```text
DB_PATH=data/feisbuc.db
```

<p align="justify">Per test:</p>

```text
DB_PATH=:memory:
```

<p align="justify">Per CI di persistenza useremo un file temporaneo creato dal test.</p>

## 18. Confronto implementazioni

### MemoryPostStore

<p align="justify"><strong>Pro</strong></p>

<ul>
  <li>semplicissimo;</li>
  <li>velocissimo nei test;</li>
  <li>nessun I/O persistente.</li>
</ul>

<p align="justify"><strong>Contro</strong></p>

<ul>
  <li>perde tutto al restart;</li>
  <li>non esercita SQL/constraint.</li>
</ul>

### SqlPostStore

<p align="justify"><strong>Pro</strong></p>

<ul>
  <li>persistenza reale;</li>
  <li>constraint e query espressivi;</li>
  <li>stesso contratto del Router;</li>
  <li>database ispezionabile.</li>
</ul>

<p align="justify"><strong>Contro</strong></p>

<ul>
  <li>introduce schema e lifecycle DB;</li>
  <li>I/O sincrono con <code>DatabaseSync</code> nel processo Node;</li>
  <li>richiede ragionare su query, errori e migrazioni.</li>
</ul>

<p align="justify">Per questa scala didattica il trade-off e intenzionale. In sistemi ad alta concorrenza valuteremmo driver/architetture differenti.</p>

## 19. Feisbuc milestone 6

<p align="justify">La UI e la API restano uguali.</p>

```text
Feisbuc milestone 5
client -> api.js -> Express -> Router -> MemoryPostStore

Feisbuc milestone 6
client -> api.js -> Express -> Router -> SqlPostStore -> SQLite file
```

<p align="justify">Definition of done:</p>

<ol>
  <li>il client non cambia contratto;</li>
  <li><code>GET</code>, <code>POST</code>, <code>PATCH</code> mantengono status e representation;</li>
  <li>i post sopravvivono al restart del server;</li>
  <li>input esterno entra in SQL solo tramite binding;</li>
  <li>constraint proteggono gli invarianti persistenti;</li>
  <li><code>DB_PATH=:memory:</code> funziona nei test;</li>
  <li>nessun path assoluto macchina-specifico;</li>
  <li>nessun ORM.</li>
</ol>

## 20. Errori frequenti

<ul>
  <li>creare tabelle dentro una route GET;</li>
  <li>concatenare input in una query;</li>
  <li>dimenticare <code>WHERE</code> in <code>UPDATE</code>/<code>DELETE</code>;</li>
  <li>usare un path assoluto del proprio PC;</li>
  <li>mettere SQL direttamente nel Router;</li>
  <li>affidarsi solo alla validation HTTP e non avere constraint;</li>
  <li>trasformare ogni errore DB in <code>400</code>;</li>
  <li>salvare <code>true</code>/<code>false</code> senza definire la rappresentazione SQL;</li>
  <li>cambiare il client quando cambia soltanto il repository;</li>
  <li>introdurre ORM prima di capire le query che dovrebbe astrarre.</li>
</ul>

## 21. Esercizi A-F

### A — osserva e verifica lo schema

<p align="justify">Crea la tabella <code>posts</code>, inserisci seed e usa query di verifica. Activity autograded SQL.</p>

### B — modifica controllata

<p align="justify">Applica DML e filtri mantenendo invarianti e risultati deterministici. Activity autograded SQL.</p>

### C — implementazione autonoma

<p align="justify">Sostituisci <code>MemoryPostStore</code> con <code>SqlPostStore</code> senza cambiare Router/client. Feisbuc milestone 6.</p>

### D — debugging

<p align="justify">Ripara uno script che aggiorna righe sbagliate e viola invarianti perche il <code>WHERE</code> e il modello di stato sono errati. Activity autograded SQL + diagnosi.</p>

### E — mini-progetto

<p align="justify">Aggiungi una seconda risorsa persistente, ad esempio <code>profiles</code>, con schema, repository e almeno una relazione motivata.</p>

### F — prodotto integrato

<p align="justify">Nel capstone finale collega persistenza, auth e realtime mantenendo migrazioni/schema versionati e test E2E.</p>

## 22. Laboratorio

<p align="justify">Flusso consigliato:</p>

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

<ol>
  <li>Perche <code>MemoryPostStore</code> non e persistenza?</li>
  <li>Quale responsabilita appartiene al Router e quale al repository?</li>
  <li>Perche <code>CHECK (liked IN (0,1))</code> e utile anche se il Router valida il body?</li>
  <li>Che differenza c'e tra SQL con placeholder e concatenazione di stringhe?</li>
  <li>Perche un <code>UPDATE</code> senza <code>WHERE</code> e pericoloso?</li>
  <li>Quando serve una transazione?</li>
  <li>Perche usiamo <code>:memory:</code> nei test?</li>
  <li>Quale parte del client deve cambiare passando da memoria a SQLite? Idealmente nessuna.</li>
</ol>

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

<p align="justify">Fonti tecniche da consultare, non da copiare:</p>

<ul>
  <li>documentazione SQLite: SQL language, constraints e transactions;</li>
  <li>documentazione Node.js <code>node:sqlite</code> / <code>DatabaseSync</code> / prepared statements;</li>
  <li>TheBitLab SQL runner: SQLite isolato in memoria per grading deterministico;</li>
  <li><code>kinderp/lab8</code> come provenance storica di Express + SQLite, con pattern mutating-GET ritirato;</li>
  <li><code>labs_summary</code> come progressione storica.</li>
</ul>

## 26. Activity correlate

<ul>
  <li><code>tpsi5-activity-a-sql-posts-schema-001</code>;</li>
  <li><code>tpsi5-activity-b-sql-posts-dml-001</code>;</li>
  <li><code>tpsi5-activity-c-feisbuc-sql-repository-001</code>;</li>
  <li><code>tpsi5-activity-d-debug-sql-state-001</code>.</li>
</ul>

## Confine del prossimo incremento

<p align="justify">Dopo questa parte, il database contiene ancora <strong>post senza utenti autenticati</strong>.</p>

<p align="justify">Il passo successivo sara:</p>

```text
SQL raw persistence
  -> utenti/credential model
  -> password hashing
  -> session/authn/authz
```

<p align="justify">Non introduciamo ancora ORM: prima vogliamo poter leggere e spiegare il SQL reale che l'ORM andra eventualmente ad astrarre.</p>
