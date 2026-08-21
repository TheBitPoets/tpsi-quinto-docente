# Note docente

Obiettivo: impedire che l'ORM venga percepito come una tecnologia che sostituisce SQL.

Sequenza consigliata:

1. far prevedere agli studenti il SQL prima dell'esecuzione;
2. eseguire con `echo=True`;
3. evidenziare `CREATE TABLE`, `INSERT`, `COMMIT`, `SELECT`;
4. far distinguere Engine da Session;
5. mostrare `session.new` prima/dopo commit;
6. aprire una seconda Session per rendere visibile il nuovo unit-of-work lifetime;
7. richiamare la sessione HTTP di UDA24 e chiedere perche il nome uguale non indica la stessa responsabilita.

`StaticPool` e presente solo per rendere stabile il database SQLite in-memory tra le due Session del microscope. Non generalizzare questa configurazione a ogni database.

Non introdurre ancora relationship, eager loading, Alembic o async ORM.
