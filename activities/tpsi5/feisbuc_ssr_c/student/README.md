# Feisbuc milestone 8 — SSR

Lo starter è già un progetto completo: contiene la baseline funzionante della milestone 7 e i file con i TODO della milestone 8. Non devi copiare o sovrapporre file provenienti da altre Activity.

Lavora direttamente nella cartella ricevuta. Non riscrivere auth, sessione o repository SQL: completa soltanto i TODO relativi al presentation adapter SSR.

## Avvio

```bash
npm install
npm start
```

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
