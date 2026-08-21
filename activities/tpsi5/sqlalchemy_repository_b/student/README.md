# SQLAlchemy PostStore — attività B

Obiettivo: completare il repository senza coinvolgere FastAPI.

## Setup

```bash
python -m pip install -r requirements.txt
```

Il docente/CI usa una SessionFactory collegata a SQLite in-memory isolato.

## Contratto

### `list()`

Deve:

- aprire una Session con `with self._session_factory() as session:`;
- usare `select(PostRow)`;
- ottenere entity ORM con `session.scalars(...)`;
- restituire `list[dict]` tramite `to_public_post`.

### `create(text)`

Deve:

- generare id server-side;
- fissare `author_id="mirror-user"` e `author="Mirror Student"`;
- impostare `liked=False`, `likes=0`;
- `session.add(row)`;
- `session.commit()`;
- restituire la representation pubblica.

### `set_liked(post_id, liked)`

Deve:

- usare `session.get(PostRow, post_id)`;
- restituire `None` se manca;
- modificare `likes` solo se `liked` cambia;
- fare commit;
- non permettere likes negativi nella sequenza normale true/false.

## Non fare

- `session.query(...)`;
- import FastAPI;
- Session globale;
- `row.__dict__` come output;
- commit dentro una funzione HTTP esterna: il transaction boundary di questa attività appartiene al repository.

Domanda finale: quale parte di questo file cambierebbe se domani sostituissimo FastAPI con un altro adapter HTTP? Risposta attesa: **nessuna**.
