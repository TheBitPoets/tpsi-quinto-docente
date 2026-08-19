# Activity B — DML controllato

Stato iniziale:

```text
p1            likes=2 liked=1
p2            likes=0 liked=0
draft-remove  likes=0 liked=0
```

Stato richiesto:

```text
p1  likes=2 liked=1
p2  likes=1 liked=1
p3  likes=0 liked=0
```

`draft-remove` non deve piu esistere.

## Regola di lavoro

Per ogni `UPDATE` o `DELETE`, prima scrivi in italiano:

> voglio modificare/eliminare esattamente ...

Poi traduci quell'insieme nella clausola `WHERE`.

## View

Crea anche `liked_posts` come vista dei soli post con `liked = 1`.

Il grader interroghera sia la tabella sia la view.
