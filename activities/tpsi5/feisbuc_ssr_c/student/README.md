# Feisbuc milestone 8 — overlay SSR

Questa Activity **parte dalla milestone 7**. Non riscrivere auth, sessione o repository SQL.

Applica i file starter sopra il progetto milestone 7 e completa i TODO.

Definition of Done:

- `npm install` installa Express 5.2.1 + Nunjucks 3.2.4;
- login/register della milestone 7 continuano a funzionare;
- utente anonimo su `/ssr` riceve 401;
- autenticato su `/ssr` riceve HTML;
- POST `/ssr/posts` crea con `authorId` della sessione e risponde 303;
- POST delete non-owner -> 403;
- POST delete owner -> 303 e post rimosso;
- testo come `<script>alert(1)</script>` compare escapato;
- `/api/posts` continua a restituire JSON.

Confronta in DevTools Network `/api/posts` e `/ssr`.
