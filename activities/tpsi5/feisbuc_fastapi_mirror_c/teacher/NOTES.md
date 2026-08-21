# Note docente — Feisbuc mirror 01

Il criterio di successo non e "abbiamo riscritto Feisbuc in Python". E dimostrare che lo stesso problema HTTP puo essere espresso con un adapter diverso.

Review:
- command/output models separati;
- `authorId` non fa parte di PostCreate;
- MemoryPostStore non importa FastAPI;
- 201 + Location;
- 404;
- 422 riconosciuto come differenza di framework;
- OpenAPI verificato da test;
- nessun SQLAlchemy/auth/session/realtime.

Il prossimo slice sostituisce MemoryPostStore con SQLAlchemy mantenendo questa suite di contratto.
