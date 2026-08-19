# Feisbuc milestone 9 — Vue SPA

Prerequisito: milestone 7 auth/session funzionante.

## Dev

1. avvia il backend milestone 7 su `PORT=3333`;
2. in `frontend/`: `npm install`;
3. `npm run dev`;
4. Vite inoltra `/api` al backend; il browser continua a usare URL relativi.

## Build

`npm run build` produce `dist/` con base `/vue/`. In integrazione gli asset vengono copiati nel `public/vue` del backend e serviti dallo stesso origin.

## Definition of done

- bootstrap `/api/auth/me`: 401 anonimo non diventa errore rosso;
- register/login valorizzano `user` e caricano il feed;
- logout azzera `user/posts`;
- create usa la representation 201 restituita dal server;
- like sostituisce il post con la representation PATCH;
- delete rimuove dal client solo dopo 204;
- PostCard resta presentazionale e usa props/emits;
- nessun token in storage o `document.cookie`;
- nessun Router/Pinia/TypeScript in questa milestone;
- `npm run build` passa.
