# Testing boundary matrix — soluzione

| Scenario | Livello | Reali | Mock | Evidence |
| --- | --- | --- | --- | --- |
| trim e lunghezza testo | unit | funzione/policy | nessuno | output/error code della funzione |
| repository fa commit | repository-integration | repository + SQLAlchemy + SQLite | nessuno | nuova riga leggibile da una Session successiva |
| POST restituisce 201 + Location | http-integration | FastAPI + Pydantic + repository + SQLite | nessuno | status, header Location e body |
| dato sopravvive a restart | http-integration/restart | due app + due Engine + stesso file SQLite | nessuno | app B rilegge il dato scritto da app A |
| provider email esterno fallisce | unit/integration sull'adapter | codice locale | provider remoto sostituito da fake controllato | errore applicativo previsto |
| deep-link browser dopo deploy | e2e | server deployato + browser/router | normalmente nessuno | URL diretto rende la SPA corretta |

`tutto E2E` rallenta diagnosi e feedback. `tutto mock` elimina i boundary reali e puo dare test verdi anche con integrazione rotta. La strategia usa il livello minimo che osserva davvero la proprieta.
