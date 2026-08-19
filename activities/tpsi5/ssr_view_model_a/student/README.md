# Activity A — View model SSR

Il database model non coincide necessariamente con il modello utile alla vista.

Implementa `buildFeedViewModel` senza produrre HTML.

Regola:

```text
post.authorId == user.id -> canDelete=true
altrimenti                -> canDelete=false
```

`canDelete` serve soltanto a decidere se mostrare un controllo. La DELETE reale deve comunque verificare ownership sul server.

Esegui localmente:

```bash
printf '%s\n' '{"user":{"id":"u1"},"posts":[]}' | node main.js
```
