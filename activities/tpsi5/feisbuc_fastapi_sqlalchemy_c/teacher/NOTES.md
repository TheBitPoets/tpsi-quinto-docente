# Note docente

Il criterio di successo di mirror 02 e **compatibilita del contratto + nuova proprieta di persistenza**.

Review:

- Pydantic model invariati rispetto a mirror 01;
- entity ORM separate;
- Engine/SessionFactory creati da `build_database` nel composition root;
- `SqlAlchemyPostStore` senza FastAPI;
- `select` / `Session.get`, nessuna Query legacy;
- Session per metodo;
- commit su create/update;
- seed `seed-1` idempotente;
- mapping `to_public_post`, nessun `row.__dict__`;
- test HTTP mantiene 201/Location/404/422/OpenAPI;
- test restart usa due app e dispose dell'Engine sullo stesso file SQLite;
- nessuna auth/session web, Socket.IO, Alembic o async ORM.

Far confrontare agli studenti il test di restart con il MemoryPostStore: il valore del nuovo slice non e la sintassi ORM, ma il cambio osservabile della durability senza cambiare l'API.
