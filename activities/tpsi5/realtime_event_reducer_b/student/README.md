# Activity B — realtime event reducer

Input da `stdin`:

```json
{
  "posts": [{"id":"p1","text":"ciao"}],
  "event": {"type":"post:created","post":{"id":"p2","text":"nuovo"}}
}
```

Output: il nuovo array posts in JSON, senza log aggiuntivi.

Contratto:

- `post:created`: inserisce in testa **solo se l'id non esiste gia**;
- `post:updated`: sostituisce l'elemento con lo stesso id;
- `post:deleted`: elimina `postId`;
- non modificare direttamente `posts`.

Domanda da motivare nel commento finale: perche `post:created` deve essere idempotente se il client che ha fatto POST riceve anche il broadcast dello stesso post?
