# Security review — riferimento

| # | Asset / trust boundary | Vulnerabilita | Attacco possibile | Fix | Evidence dopo fix |
| --- | --- | --- | --- | --- | --- |
| 1 | password storage | password plaintext | dump DB rivela credenziali | scrypt + salt casuale | DB contiene solo `scrypt$...` |
| 2 | login error model | `email-not-found` vs `wrong-password` | user enumeration | `invalid-credentials` generico | stesso code per i due casi |
| 3 | session ID | `sessionId = user.id` | previsione/fissazione | `randomBytes(32)` e nuova sessione al login | token opaco diverso a ogni login |
| 4 | cookie | nessun attributo | lettura JS / invio cross-site o insecure | HttpOnly, SameSite=Strict, Secure in prod, Path=/ | header Set-Cookie verificato |
| 5 | response login | restituisce password e session ID | leak in JS/log/devtools | restituisci solo user pubblico | nessun secret nel JSON |
| 6 | create post identity | `authorId` dal body | impersonation | `req.auth.user.id` | authorId body ignorato/assente |
| 7 | delete authorization | `userId`/`authorId` dal body | IDOR/cancellazione altrui | lookup owner DB + user autenticato | non-owner -> 403 |
| 8 | session lifecycle | nessun server store/logout | token non revocabile | session table con expiry + delete logout | vecchio cookie -> 401 |

## Trust boundary corretto

```text
browser
  -> cookie opaco HttpOnly
  -> hash(token)
  -> session DB non scaduta
  -> user verificato
  -> authorization server-side
  -> prepared SQL
```

Il client puo scegliere `text` e l'azione richiesta; non puo scegliere l'identita che il server usera per autorizzarla.
