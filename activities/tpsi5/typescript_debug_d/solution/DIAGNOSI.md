# Diagnosi reference — TypeScript boundaries

| # | Sintomo | Causa | Evidence | Fix |
|---|---|---|---|---|
| 1 | `"logged"` non assegnabile ad `AuthStatus` | la literal union ammette solo unknown/anonymous/authenticated | errore sul valore iniziale | usare uno stato realmente modellato oppure estendere consapevolmente il dominio |
| 2 | `posts[0]` puo essere undefined | `noUncheckedIndexedAccess` rende esplicito che l'indice puo non esistere | errore prima di `.text` | assegnare `first` e fare narrowing con `if (first)` |
| 3 | `payload.id` non disponibile su unknown | il dato non e ancora stato verificato | errore sull'accesso proprieta | type guard `isRecord` + verifica `typeof payload.id === "string"` |
| 4 | emit delete riceve number | il contratto eventi richiede `id: string` | vue-tsc segnala il payload dell'emit | emettere `props.id` |
| 5 | `requireAuth` non appartiene a RouteMeta | typo rispetto a `requiresAuth` | `satisfies RouteMeta` rende visibile la chiave in eccesso | usare `requiresAuth` |

## Regola emersa

Il compilatore non va convinto a tacere. Ogni errore rappresenta una discrepanza tra il modello dichiarato e il programma. Il fix corretto migliora il modello o il codice; non disabilita `strict`.
