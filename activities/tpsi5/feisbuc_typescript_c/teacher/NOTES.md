# Teacher notes — milestone 11

Review in questo ordine:

1. **domain.ts**: una sola definizione di User/Post/AuthStatus;
2. **api.ts**: `response.json()` entra come `unknown`, poi parser/narrowing;
3. **session.ts**: `User | null` e AuthStatus union, nessun `!` per nascondere nullability;
4. **navigation-policy.ts**: discriminated union e funzione pura;
5. **router.ts**: RouteMeta tipizzato e stessa semantica della milestone 10;
6. **SFC**: props/emits type-based e handler con id string;
7. **system smoke**: deep link e backend security invariati.

Non premiare annotazioni ridondanti. Il criterio e il valore del contratto, non la quantita di sintassi TypeScript.

`as unknown` sul risultato di `response.json()` e accettato come passaggio esplicito verso il boundary non affidabile; `as Post`/`as User` non e accettato come sostituto della validazione.

TypeScript 7 non e baseline di questo modulo finche `vue-tsc` non e verificato come compatibile nella matrice del corso.
