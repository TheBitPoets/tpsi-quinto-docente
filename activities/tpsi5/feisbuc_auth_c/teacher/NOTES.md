# Note docente — Feisbuc milestone 7

## Evidenze da chiedere

- tabella `users`: `password_hash` non plaintext;
- due registrazioni con stessa password -> hash diversi;
- cookie con `HttpOnly; SameSite=Strict; Path=/`;
- config production rifiuta `COOKIE_SECURE=false`;
- tabella `sessions`: solo hash SHA-256 del token;
- `POST /api/posts` ignora/non accetta identita scelta dal client;
- due utenti: non-owner DELETE -> 403, owner -> 204;
- logout rende inutilizzabile il cookie precedente;
- cross-site unsafe request -> 403;
- sessione ancora valida dopo restart se non scaduta.

## Domande orali

1. Perche salviamo i parametri scrypt dentro l'hash?
2. Che cosa protegge il salt e che cosa non protegge?
3. Perche hashare il session token nel DB?
4. `HttpOnly` impedisce CSRF?
5. Perche il bottone Delete nascosto non e authorization?
6. Differenza fra 401 e 403?
7. Perche login email inesistente e password errata hanno lo stesso errore pubblico?
8. Perche non abbiamo usato JWT?

## Boundary

Non premiare l'aggiunta di librerie auth/ORM come scorciatoia: l'obiettivo e vedere i primitive e i confini. Non richiedere password reset/MFA/OAuth in questa milestone.
