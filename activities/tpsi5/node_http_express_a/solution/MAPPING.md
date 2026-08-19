# Mapping di riferimento

| Responsabilita | `node:http` | Express | E concetto HTTP o framework? |
| --- | --- | --- | --- |
| Match del metodo GET | `req.method === "GET"` | `app.get(...)` | HTTP method; Express offre il dispatcher |
| Match del path `/api/health` | confronto `req.url` | path passato a `app.get` | request target HTTP; Express offre routing |
| Lettura/parsing JSON | stream `for await`, limite, `JSON.parse` | `express.json()` + `req.body` | representation HTTP + middleware framework |
| Status 200 | `writeHead(200)` | `res.status(200)` | HTTP |
| Content-Type JSON | header esplicito | `res.json()` | HTTP header; Express offre helper |
| 404 | ramo finale manuale | middleware finale | HTTP status + organizzazione Express |
| JSON invalido | `try/catch` + 400 | parser + error middleware | errore della representation + pipeline Express |
| Avvio/listen | `server.listen()` | `app.listen()` | socket/server runtime; Express delega a Node |

## Conclusione modello

Express riduce il plumbing di routing, parsing e response helpers, ma non sceglie per noi la semantica dell'API. Metodi, status, representation, validation e coerenza del contratto restano decisioni progettuali. Il framework rende piu gestibile implementare HTTP; non lo sostituisce.
