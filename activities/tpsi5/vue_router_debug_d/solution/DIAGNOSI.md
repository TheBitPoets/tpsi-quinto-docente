# Diagnosi reference — Vue Router

| # | Sintomo | Livello | Causa | Evidence | Fix |
|---|---|---|---|---|---|
| 1 | URL della SPA perde il prefisso `/vue/` | route/history | `createWebHistory()` non riceve la base Vite | build e browser URL non condividono la stessa base | `createWebHistory(import.meta.env.BASE_URL)` |
| 2 | anonimo su `/login` entra in un **redirect loop** verso `/login` | guard | guard tratta ogni route anonima come protetta | target login rientra nella stessa condizione e viene rediretto di nuovo | usare metadata/policy e consentire login anonima |
| 3 | feed non viene riconosciuto come protetto dalla policy | route meta | typo `requireAuth` vs `requiresAuth` | guard legge un campo differente | uniformare `meta.requiresAuth` |
| 4 | click Feed provoca document reload e apre `/feed` fuori dalla base SPA | navigation | `window.location.assign('/feed')` bypassa Vue Router | Network mostra nuova document request | usare `RouterLink` o `router.push` |
| 5 | refresh `/vue/feed` fallisce nel server Express 5 | HTTP server | wildcard `*` non nominato | Express 5 path syntax richiede wildcard nominato | `/vue/{*splat}` + `sendFile(index.html)` |
| 6 | URL inesistente non mostra una pagina 404 applicativa | route match | manca catch-all client | nessun route record dedicato | aggiungere `/:pathMatch(.*)` -> NotFoundView |

## Boundary

Il fallback server risolve la **consegna dell'entry HTML su deep link**. Il catch-all Vue Router risolve la **presentazione della route non trovata dentro la SPA**.

La navigation guard non autorizza `/api/*`: il backend deve continuare a produrre 401/403 tramite sessione e ownership.
