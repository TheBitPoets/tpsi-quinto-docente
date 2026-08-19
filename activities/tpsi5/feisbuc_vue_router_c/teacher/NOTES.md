# Note docente — milestone 10

Review principale:

- `vue-router` 5.2.0 pinned;
- `createWebHistory(import.meta.env.BASE_URL)`;
- feed usa `meta.requiresAuth:true`;
- guard riusa `decideNavigation`, non duplica la policy;
- `unknown` viene risolto con `/api/auth/me` prima della decisione quando necessario;
- LoginView usa redirect interno safe e `router.replace`;
- FeedView gestisce un 401 tardivo invalidando la sessione client;
- App e layout, non contiene lo state del feed;
- server fallback `/vue/{*splat}` e montato prima del notFound Express;
- fallback non intercetta `/api/*`;
- catch-all Vue mostra la 404 client;
- nessuna modifica a KDF, session token, ownership o schema SQLite.

Il fatto che una route guard impedisca di vedere il feed da anonimo vale solo come UX. Chiedere sempre allo studente di dimostrare che `/api/posts` continua a rispondere 401 senza sessione.
