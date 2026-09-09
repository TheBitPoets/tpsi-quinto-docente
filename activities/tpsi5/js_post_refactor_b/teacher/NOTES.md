# Note docente — Activity B

## Scopo

Preparare il passaggio da JavaScript come linguaggio a JavaScript come UI logic.

Il pattern è intenzionalmente vicino a quello che verrà usato nel Feisbuc dinamico:

```text
event -> id -> toggleLike(state, id) -> new state -> save -> render
```

## Misconception

- `const` viene confuso con immutabilità;
- lo studente usa `find()` e poi modifica l'object trovato;
- copia l'array ma modifica comunque l'object condiviso;
- usa JSON stringify/parse come falsa strategia di copia profonda;
- decrementa sotto zero;
- cambia tutti i post perché non controlla `id`.

## Nota didattica

La scelta immutabile non viene presentata come dogma del linguaggio. È una convenzione architetturale utile per rendere il cambio di stato più prevedibile e per preparare i futuri framework frontend.
