# Activity B — authorization per ownership

L'autenticazione risponde a **chi sei?**; l'autorizzazione risponde a **puoi fare questa operazione?**.

Input:

```json
{
  "user": {"id":"u1"},
  "post": {"id":"p1","authorId":"u1"},
  "action": "delete"
}
```

Output:

```json
{"allowed":true,"reason":"allowed"}
```

Matrice:

| Stato | read | like | create | edit | delete |
| --- | --- | --- | --- | --- | --- |
| anonimo | no | no | no | no | no |
| autenticato non owner | si | si | si | no | no |
| owner | si | si | si | si | si |

Azioni sconosciute: **default deny**.

La funzione non usa DOM, cookie o Express: serve a rendere verificabile la regola che poi verra applicata nel Router della milestone 7.
