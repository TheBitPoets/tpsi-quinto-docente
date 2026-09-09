# Feisbuc milestone 9 — Vue SPA

Lo starter contiene già due progetti coordinati:

- `backend/`: baseline Express, SQLite, autenticazione e sessioni già funzionante;
- `frontend/`: applicazione Vue della milestone 9 con i TODO da completare.

Non devi recuperare né copiare file da milestone precedenti.

## Dev

Esegui una sola volta dalla root dello starter:

```bash
npm install
```

Poi usa due terminali, sempre dalla root:

```bash
npm run dev:backend
npm run dev:frontend
```

Il primo comando avvia automaticamente il backend sulla porta `3333`; il secondo avvia Vite. Vite inoltra `/api` al backend e il browser continua a usare URL relativi.

## Build

```bash
npm run build
npm start
```

`npm run build` produce `frontend/dist/` con base `/vue/` e lo integra automaticamente in `backend/public/vue/`. Non devi copiare manualmente la build.

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
