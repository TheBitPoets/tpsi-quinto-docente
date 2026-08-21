---
marp: true
paginate: true
size: 16:9
title: 07 — SQL raw e persistenza
---

# 07 — SQL raw e persistenza
## Da MemoryPostStore a SQLite

UDA 24 — Backend

---

# Richiamo

Il backend Express funziona, ma i dati stanno in memoria.

Se il processo si riavvia:

```text
posts = []
```

Problema: **non abbiamo persistenza reale**.

---

# Obiettivi

Alla fine dovrai saper:

- distinguere memoria e persistenza;
- leggere uno schema SQL;
- usare DDL e DML;
- spiegare vincoli e chiavi;
- usare prepared statement;
- implementare un repository SQL dietro lo stesso `PostStore`.

---

# Schema

```sql
CREATE TABLE posts (
  id INTEGER PRIMARY KEY,
  author TEXT NOT NULL,
  text TEXT NOT NULL,
  created_at TEXT NOT NULL
);
```

Lo schema non è solo struttura: contiene **regole sui dati**.

---

# DDL e DML

DDL — definisce struttura:

```sql
CREATE TABLE ...
ALTER TABLE ...
```

DML — legge/modifica dati:

```sql
SELECT ...
INSERT ...
UPDATE ...
DELETE ...
```

---

# INSERT

```sql
INSERT INTO posts(author, text, created_at)
VALUES (?, ?, ?);
```

I valori arrivano separati dalla query.

Questo evita di concatenare input utente dentro SQL.

---

# Prepared statement

Da evitare:

```js
const sql = `INSERT INTO posts(text) VALUES ('${text}')`;
```

Meglio:

```js
statement.run(text);
```

Separare query e dati è una regola fondamentale di sicurezza e correttezza.

---

# SELECT

```sql
SELECT id, author, text, created_at
FROM posts
ORDER BY created_at DESC;
```

Il risultato SQL va poi trasformato nel contratto atteso dal dominio/API.

---

# Repository SQL

```js
class SqlPostStore {
  async list() {
    return this.db
      .prepare('SELECT id, author, text, created_at FROM posts')
      .all();
  }
}
```

La route Express non deve cambiare perché abbiamo cambiato store.

---

# Boundary importante

```text
Express route
→ PostStore contract
→ SqlPostStore
→ SQLite
```

Il resto dell'applicazione non deve conoscere dettagli SQL inutilmente.

---

# Vincoli

Esempi:

- `PRIMARY KEY`;
- `NOT NULL`;
- `UNIQUE`;
- foreign key.

Un vincolo è una regola che il database può difendere anche se il codice applicativo sbaglia.

---

# Errore tipico: WHERE sbagliato

```sql
DELETE FROM posts;
```

vs

```sql
DELETE FROM posts WHERE id = ?;
```

Una piccola differenza può cambiare tutto il dataset.

Prima di eseguire query distruttive: controlla predicate e parametri.

---

# Restart test

Prova minima di persistenza:

1. crea un post;
2. chiudi il processo;
3. riavvia;
4. rileggi il post.

Se sparisce, non hai persistenza reale.

---

# Checkpoint

Classifica:

1. `CREATE TABLE`;
2. `SELECT`;
3. `NOT NULL`;
4. parametro `?`;
5. `SqlPostStore`;
6. restart test.

Schema? DML? sicurezza? boundary? evidenza?

---

# Feisbuc milestone

Ora:

```text
client
→ Express
→ PostStore
→ SQLite
```

I dati sopravvivono al processo.

Il prossimo problema: **chi è davvero l'utente che sta scrivendo?**

---

# Handoff al laboratorio

Durante le Activity:

1. crea/leggi schema;
2. esegui DML;
3. usa parametri;
4. sostituisci MemoryPostStore;
5. prova restart persistence;
6. diagnostica un bug SQL.

---

# Recap

SQL raw ci rende visibili:

- schema;
- query;
- vincoli;
- parametri;
- persistenza;
- repository boundary.

Prossimo modulo: **autenticazione, sessioni e autorizzazione**.