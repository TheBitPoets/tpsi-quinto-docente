# Activity A — Pipeline del feed

## Obiettivo

Completare `prepareFeed(posts)` senza DOM e senza browser API.

Il grader eseguira `main.js` con Node.js, inviera un array JSON su stdin e confrontera lo stdout con l'output atteso.

## Input

Esempio:

```json
[
  {"id": 1, "author": "Ada", "text": "  DOM  ", "likes": 7, "published": true},
  {"id": 2, "author": "Linus", "text": "Bozza", "likes": 20, "published": false}
]
```

## Output

```json
[
  {"id": 1, "label": "Ada: DOM", "popular": true}
]
```

## Contratto

1. seleziona `published === true` con `filter`;
2. trasforma con `map`;
3. `label` combina autore e testo `trim()`;
4. `popular` vale `likes >= 5`;
5. conserva l'ordine;
6. non aggiungere `console.log` di debug: stdout e parte del contratto del test.

## Prima di consegnare

- [ ] so spiegare la differenza tra `filter` e `map`;
- [ ] non ho modificato il codice che legge stdin;
- [ ] non modifico l'array di input;
- [ ] uso `const` come default;
- [ ] l'output e JSON valido.

## Collegamento al progetto

La stessa idea ritornera nel browser:

```text
posts state
   -> filter/map
   -> createPostElement
   -> DOM
```

Prima impariamo la trasformazione dei dati, poi aggiungiamo la rappresentazione visuale.
