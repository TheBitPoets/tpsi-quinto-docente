# Note docente

Questo lab e volutamente **senza FastAPI**: serve a far vedere che la persistenza e un componente sostituibile.

Review minima:

- `select(PostRow)` + `session.scalars`;
- `session.get` per primary key;
- Session creata con la factory dentro ogni metodo;
- `commit()` sulle mutazioni;
- transizione like idempotente;
- mapping esplicito con `to_public_post`;
- nessun `row.__dict__`;
- nessun `HTTPException` o import FastAPI;
- nessuna legacy `session.query`.

La suite teacher/reference viene eseguita dalla CI del repository. Non presentarla come supporto di un nuovo grader browser SQLAlchemy: l'attivita resta manuale nella piattaforma.
