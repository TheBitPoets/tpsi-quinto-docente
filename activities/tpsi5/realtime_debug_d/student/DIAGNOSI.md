# DIAGNOSI — realtime boundaries

Compila **prima** di modificare il codice.

Per almeno 5 difetti indica:

| Sintomo / codice | Categoria | Causa | Rischio | Fix proposto | Evidence |
| --- | --- | --- | --- | --- | --- |
| | security / lifecycle / delivery / architecture | | | | |
| | | | | | |
| | | | | | |
| | | | | | |
| | | | | | |

Domande obbligatorie:

1. Perche `payload.authorId` non puo essere fonte di identita?
2. Perche `socket.on("post:create")` crea un secondo command path?
3. Che cosa succede se `mountFeed()` viene chiamata due volte?
4. Perche `connect` dopo una disconnessione non dimostra che il client abbia tutti gli eventi?
5. Come rendi `post:created` idempotente?
6. Quale operazione REST usi per il recovery?
