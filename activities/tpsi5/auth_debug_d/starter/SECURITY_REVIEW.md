# Security review

Compila **prima** di proporre fix.

| # | Asset / trust boundary | Vulnerabilita | Attacco possibile | Fix | Evidence dopo fix |
| --- | --- | --- | --- | --- | --- |
| 1 | password storage | TODO | TODO | TODO | TODO |
| 2 | login error model | TODO | TODO | TODO | TODO |
| 3 | session ID | TODO | TODO | TODO | TODO |
| 4 | cookie | TODO | TODO | TODO | TODO |
| 5 | response login | TODO | TODO | TODO | TODO |
| 6 | create post identity | TODO | TODO | TODO | TODO |
| 7 | delete authorization | TODO | TODO | TODO | TODO |
| 8 | session lifecycle | TODO | TODO | TODO | TODO |

## Trust boundary

Disegna:

```text
browser -> cookie -> backend -> session store -> user -> authorization -> DB
```

e indica quali valori sono controllati dal client e quali devono essere derivati dal server.
