# Feisbuc milestone 10 — Vue Router

Lo starter è già completo: include il backend funzionante e tutto il frontend della milestone 9, insieme ai TODO della milestone 10. Non devi copiare o sovrapporre file da altre Activity.

## Avvio

Esegui una sola volta dalla root dello starter:

```bash
npm install
```

Poi avvia backend e frontend in due terminali:

```bash
npm run dev:backend
npm run dev:frontend
```

## Frontend

Completa:

1. `main.js`: registra il router plugin;
2. `router.js`: route records, history base, `meta.requiresAuth`, catch-all e guard;
3. `App.vue`: layout + RouterLink + RouterView + logout;
4. `LoginView.vue`: `safeRedirect()` e redirect post-login.

Sono gia forniti:

- `navigation-policy.js` dalla Activity B;
- `session.js` con stato `unknown|anonymous|authenticated`;
- `FeedView.vue`, `AboutView.vue`, `NotFoundView.vue`.

## Backend integration

La build Vite usa già base `/vue/`. Dalla root dello starter esegui:

```bash
npm run build
npm start
```

Il comando di build copia automaticamente `frontend/dist/` in `backend/public/vue/`.

Completa:

- `vue-spa.js`: static mount + history fallback Express 5;
- `app.js`: installa il fallback dopo `/api/*` e prima di `notFound`.

## Definition of Done

- `/vue/` porta al feed o al login secondo la sessione;
- `/vue/feed` e protetta dalla navigation guard;
- refresh diretto di `/vue/feed` riceve `index.html` dal server;
- `/vue/about` e pubblica;
- una route client inesistente mostra NotFoundView;
- un anonimo che chiede `/api/posts` riceve ancora 401;
- un non-owner che forza DELETE riceve ancora 403;
- login con `?redirect=/feed` torna alla destinazione;
- un redirect `//evil.example` non viene accettato;
- nessun token viene letto o salvato dal JavaScript.

## Debug order

```text
HTTP fallback -> route match -> navigation policy -> view -> API
```
