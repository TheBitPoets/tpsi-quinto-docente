# React PostCard — consegna

Conosci gia il contratto Vue:

```text
props in:
  post
  canDelete

events out:
  toggle-like(post.id)
  delete(post.id)
```

Traducilo in React mantenendo lo stesso data flow:

```text
props in:
  post
  canDelete
  onToggleLike
  onDelete

callbacks out:
  onToggleLike(post.id)
  onDelete(post.id)
```

Non modificare `post`, non usare `fetch` nel child e non spostare lo state dentro `PostCard`.

Controlla anche nel parent:
- update immutabile con `map`;
- delete immutabile con `filter`;
- `key={post.id}`.
