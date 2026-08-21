# Diagnosi

1. **Silent production fallback**: un default SQLite locale nasconde la configurazione mancante; production deve fallire subito.
2. **Liveness coupled to DB**: `/health` non deve diventare rosso solo per una dipendenza esterna.
3. **Secret/config leakage**: la response non deve esporre `DATABASE_URL`.
4. **Fake readiness**: `/ready` verde senza query non prova che il servizio possa usare `posts`.
5. **Implicit schema preparation**: creare schema nello startup rende impossibile osservare il confine prestart/readiness.
6. **Reload + workers**: il comando mescola development reload e multi-process production senza introdurre i relativi lifecycle/orchestration problem.
7. **Cleanup**: l'Engine deve avere ownership e dispose espliciti nel lifespan.
