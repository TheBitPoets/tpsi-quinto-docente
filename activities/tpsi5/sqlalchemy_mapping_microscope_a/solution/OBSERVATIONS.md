# Osservazioni attese

## 1. Mapping

`PostRow` mappa la tabella `posts`. `id` e la primary key. `String(64)`, `String(280)`, `Boolean`, `Integer`, `nullable=False` e `primary_key=True` rendono visibili tipi e constraint del mapping.

## 2. Engine

L'URL e `sqlite://`, quindi il microscope usa SQLite in memoria. `StaticPool` mantiene una sola connessione condivisa per la durata del piccolo processo e rende osservabile lo stesso database nelle due Session. `echo=True` stampa il SQL generato. L'Engine e infrastruttura di accesso/pooling, non una query e non una Session.

## 3. Session

Dopo `add`, `row` e pending nella unit of work (`session.new`). `commit()` sincronizza e conferma la transaction. La seconda Session mostra un lifetime nuovo: l'oggetto viene riletto dal database. SQLAlchemy Session coordina ORM/transaction; non identifica un utente HTTP.

## 4. SQL

Nell'echo compaiono operazioni equivalenti a:

- `CREATE TABLE posts ...`;
- `INSERT INTO posts ...`;
- `COMMIT`;
- `SELECT ... FROM posts WHERE posts.id = ?`.

## 5. Mapping concettuale

```text
SQL raw UDA24          SQLAlchemy 2.0
-------------          --------------
CREATE TABLE           Base.metadata.create_all
INSERT                  session.add + flush/commit
SELECT                  select + session.scalar/scalars
transaction commit      session.commit
row result              PostRow mapped object
```

## 6. Conclusione

SQLAlchemy non elimina SQL: costruisce/esegue SQL e mantiene il mapping tra righe relazionali e oggetti Python, aggiungendo Session/unit of work sopra il modello del database.
