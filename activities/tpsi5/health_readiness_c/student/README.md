# Health/readiness

Implementa `/health` senza dipendenza DB e `/ready` con query minima alla tabella posts. Prima di `prepare_database`, health=200 e ready=503; dopo prepare, entrambi 200.
