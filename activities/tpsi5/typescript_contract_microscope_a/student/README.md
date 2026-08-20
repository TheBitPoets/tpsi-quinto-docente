# Activity A — Microscopio TypeScript

## Procedura

1. `npm install`
2. `npm run type-check`
3. apri `src/microscope.ts`
4. individua ogni `@ts-expect-error`
5. per ciascun caso annota:
   - tipo atteso;
   - tipo ricevuto;
   - quale regola evita l'errore;
   - se lo stesso problema sarebbe visibile solo a runtime in JavaScript.

## Domande

- Quali tipi sono inferiti senza annotazione?
- Perche `"logged"` non e un `AuthStatus` valido?
- Perche `User | null` impedisce l'accesso diretto a `displayName`?
- Perche `unknown` obbliga a fare narrowing?
- Cosa cambia con `noUncheckedIndexedAccess` su `posts[0]`?
- Un `Post` TypeScript garantisce che il server abbia davvero inviato un Post?

## Definition of done

Il type-check resta verde e la spiegazione distingue chiaramente controllo statico e validazione runtime.
