# DIAGNOSI — reference

| Difetto | Categoria | Causa / rischio | Fix |
| --- | --- | --- | --- |
| nessuna auth handshake | security | qualunque client puo aprire il canale e ricevere eventi | riusare cookie HttpOnly + session store server-side |
| `payload.authorId` trusted | security | identity spoofing / IDOR | identita derivata solo dalla sessione verificata |
| `socket.on("post:create")` | architecture | secondo command path, validation/auth/error semantics duplicate | mantenere POST/PATCH/DELETE REST e pubblicare eventi dopo successo |
| `mountFeed()` registra listener ogni volta | lifecycle | lo stesso evento viene elaborato N volte | handler nominati + start idempotente + `off` nello stop |
| `posts.unshift(post)` | delivery/state | HTTP response + broadcast o duplicate event producono duplicati | reducer idempotente per `post.id` |
| connect/reconnect senza resync | delivery/recovery | eventi accaduti offline non sono ricostruiti | al reconnect `GET /api/posts` e replace dello snapshot |
| `cors: { origin: "*" }` senza requisito | security/config | amplia inutilmente le origini ammesse e nasconde il modello same-origin | nessun CORS wildcard nel core same-origin |

## Principio finale

```text
REST = command path + authorization + validation + status
Socket.IO = event distribution
SQLite = source of truth persistente
reconnect = non prova delivery completa
REST snapshot = recovery baseline
```

`strict` e i tipi non risolvono trust, lifecycle o delivery: servono boundary runtime espliciti.
