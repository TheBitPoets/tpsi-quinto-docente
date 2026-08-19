# Diagnosi Vue Router

Compila **prima** di modificare gli snippet.

| # | Sintomo | Livello (`HTTP server`, `route match`, `guard`, `navigation`) | File/riga | Causa | Evidence | Fix ipotizzato |
|---|---|---|---|---|---|---|
| 1 | | | | | | |
| 2 | | | | | | |
| 3 | | | | | | |
| 4 | | | | | | |
| 5 | | | | | | |

Domande:

1. Perche un anonimo puo entrare in un redirect loop sulla login route?
2. Quale typo rende inefficace la metadata della route feed?
3. Cosa cambia fra `createWebHistory()` e `createWebHistory(import.meta.env.BASE_URL)` quando Vite usa base `/vue/`?
4. Perche `window.location.assign('/feed')` e una cattiva navigazione interna in questa SPA?
5. Perche `app.get('/vue/*', ...)` non e una route valida nel modello Express 5 usato dal corso?
6. Quale problema risolve il fallback server e quale problema risolve il catch-all Vue Router?
