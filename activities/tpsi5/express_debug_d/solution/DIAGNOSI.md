# Diagnosi di riferimento

| # | Sintomo | Evidence | Causa | Fix | Verifica |
| --- | --- | --- | --- | --- | --- |
| 1 | `/` restituisce 404 JSON invece di HTML | `curl -i /` | middleware 404 montato prima di `express.static` | static prima del 404 | `/` -> 200 HTML |
| 2 | POST JSON genera 500/default error | POST con `Content-Type: application/json` | `express.json()` montato dopo il Router, quindi `req.body` non e pronto | parser prima del Router | POST -> 201 JSON |
| 3 | `/api/posts/p1` non trova `p1` | GET -> 404 | route `/:id` usa `req.query.id` invece di `req.params.id` | leggere `req.params.id` | GET p1 -> 200 |
| 4 | una GET crea un nuovo post | GET `/api/posts/create?...` cambia la lista | metodo safe usato per modificare stato | rimuovere route mutante GET; usare POST | GET non modifica piu stato |
| 5 | `/explode` produce default 500 invece del nostro JSON | response `text/html` / stack dev | handler custom ha tre argomenti e non viene riconosciuto come error middleware | usare i **quattro argomenti** `(error, req, res, next)` e posizione finale | 500 `application/json` |

## Pipeline corretta

```text
request
  -> express.json
  -> express.static
  -> /api/posts Router
  -> 404
  -> error handler (solo error path)
```

Nota: `express.json` puo anche essere limitato alle sole route che ne hanno bisogno; qui la scelta globale serve a rendere evidente l'ordine.
