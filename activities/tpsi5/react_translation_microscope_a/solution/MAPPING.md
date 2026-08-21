# Mappa Vue -> React

| Problema | Vue | React | Spiegazione |
| --- | --- | --- | --- |
| state locale | `ref(0)` | `useState(0)` | entrambi rappresentano state che provoca un nuovo render quando cambia |
| aggiornamento state | `count++` nel template / `count.value` nello script | `setCount(...)` | si aggiorna tramite l'API di state del framework, non il DOM |
| valore derivato | `computed(() => count.value * 2)` | `const doubled = count * 2` | non e una seconda source of truth |
| event binding | `@click` | `onClick` | l'evento richiama una funzione che aggiorna state |
| rendering del valore | `{{ count }}` | `{count}` | il markup e dichiarativo rispetto allo state |

## Domande

1. `doubled` deriva interamente da `count`: salvarlo separatamente crea sincronizzazione inutile.
2. Il calcolo e banale; `useMemo` e un'ottimizzazione, non il meccanismo necessario per ottenere un valore derivato.
3. In entrambi: evento -> update dello state -> framework esegue un nuovo render -> UI coerente.
