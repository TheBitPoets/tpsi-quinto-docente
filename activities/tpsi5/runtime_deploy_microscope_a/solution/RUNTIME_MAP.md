# Runtime map — reference

| Elemento | Boundary | Motivazione |
| --- | --- | --- |
| FEISBUC_DATABASE_URL | app config | dipendenza richiesta dall'app |
| --port | process config | appartiene a Uvicorn |
| create schema | prestart | prepara la dipendenza prima del serve |
| GET /health | liveness | verifica il processo, senza DB |
| GET /ready | readiness | verifica la tabella posts reale |

`/health` resta 200 anche se SQLite non e preparato: il processo e vivo. `/ready` restituisce 503 finche il servizio non puo usare la dipendenza necessaria.
