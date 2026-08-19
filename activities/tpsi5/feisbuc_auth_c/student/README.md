# Feisbuc milestone 7 — auth/session

## Obiettivo

Parti dalla milestone SQL e aggiungi identita affidabile senza spostare il trust nel client.

```text
browser
  -> HttpOnly cookie
  -> loadAuth
  -> req.auth.user
  -> protected Router
  -> authorization
  -> SQL
```

## TODO principali

1. `schema.sql`: constraint/indici per users/sessions/posts;
2. `passwords.js`: `scrypt` + salt random + `timingSafeEqual`;
3. `auth-store.js`: user + session prepared statements;
4. `session.js`: random token, hash DB, cookie flags, `loadAuth`;
5. `auth.router.js`: register/login/me/logout;
6. `sql-post-store.js`: `author_id` + JOIN user + ownership delete;
7. `posts.router.js`: `requireAuth`, autore dalla sessione, 403 non-owner;
8. `app.js`: `loadAuth` prima dei Router;
9. `server.js`: composition root e shutdown DB.

## Definition of done

- password minima 15, massima 128; nessuna regola simbolo/maiuscola;
- password DB comincia con `scrypt$` e non coincide con l'input;
- stesso password input produce hash diversi grazie al salt;
- session cookie `HttpOnly`, `SameSite=Strict`, `Path=/`;
- in production `Secure` e obbligatorio e il nome diventa `__Host-feisbuc.sid`;
- nel DB `sessions.id_hash` e un SHA-256 hex, non il token cookie;
- login sbagliato usa sempre `invalid-credentials`;
- `/api/posts` richiede login;
- il client non invia `authorId` in create;
- post creato riceve `authorId` dalla sessione;
- DELETE proprio -> 204; DELETE altrui -> 403;
- logout elimina la sessione server-side;
- richiesta unsafe con `Sec-Fetch-Site: cross-site` -> 403;
- nessun JWT/localStorage token/ORM.

## Smoke manuale

Avvia:

```bash
npm install
DB_PATH=data/lab.db npm start
```

Prova con browser DevTools o curl cookie jar:

```bash
curl -i -c cookies.txt -H 'Content-Type: application/json' \
  -d '{"displayName":"Maria","email":"maria@example.test","password":"una passphrase lunga 2026"}' \
  http://127.0.0.1:3000/api/auth/register

curl -i -b cookies.txt http://127.0.0.1:3000/api/auth/me

curl -i -b cookies.txt -H 'Content-Type: application/json' \
  -d '{"text":"post autenticato"}' \
  http://127.0.0.1:3000/api/posts
```

Non copiare il session token in JavaScript: il browser deve gestire il cookie senza renderlo disponibile all'app client.
