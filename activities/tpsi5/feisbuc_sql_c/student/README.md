# Feisbuc milestone 6 — SQL raw persistence

## Obiettivo

La milestone 5 aveva gia un buon confine:

```text
Router -> PostStore
```

Ora devi dimostrare che quel confine funziona davvero:

```text
MemoryPostStore
      ↓ sostituito da
SqlPostStore -> SQLite
```

Il client e il contratto HTTP restano invariati.

## File da completare

- `src/schema.sql`;
- `src/sql-post-store.js`;
- la risoluzione di `DB_PATH` in `src/server.js`.

Gli altri file sono reference della milestone precedente: non usarli per nascondere errori del repository.

## Avvio in memoria

```bash
DB_PATH=:memory: npm start
```

Su PowerShell:

```powershell
$env:DB_PATH=":memory:"
npm start
```

I dati spariscono al restart: utile nei test.

## Avvio persistente

```bash
DB_PATH=data/feisbuc.db npm start
```

Su PowerShell:

```powershell
$env:DB_PATH="data/feisbuc.db"
npm start
```

### Prova obbligatoria di persistenza

1. avvia su file;
2. `POST /api/posts`;
3. annota l'id;
4. termina il server;
5. riavvia con lo stesso `DB_PATH`;
6. `GET /api/posts`;
7. il post deve esserci ancora.

## Checklist SQL

- [ ] schema `STRICT`;
- [ ] `CHECK` sugli invarianti;
- [ ] indice motivated by `liked` filter;
- [ ] `INSERT OR IGNORE` per seed;
- [ ] prepared statement riutilizzabili;
- [ ] nessuna concatenazione di `id`, `text`, `author` dentro SQL;
- [ ] 0/1 SQLite convertito a boolean JavaScript;
- [ ] `setLiked` modifica una sola row;
- [ ] `null` se l'id non esiste;
- [ ] `close()` chiude il DB.

## Cose da non aggiungere

- `sqlite3`, `better-sqlite3` o altri package: usiamo `node:sqlite`;
- ORM;
- auth;
- CORS;
- template engine.

## Domanda di review

Se il Router deve sapere che `liked` e salvato come `INTEGER`, quale confine architetturale hai rotto?
