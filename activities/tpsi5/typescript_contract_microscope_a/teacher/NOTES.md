# Teacher notes — Activity A

Obiettivo: osservare il sistema di tipi, non insegnare sintassi avanzata.

Punti chiave:

- l'inferenza evita annotazioni ridondanti;
- la union restringe gli stati possibili;
- `unknown` conserva sicurezza mentre `any` la disattiva;
- `strictNullChecks` rende esplicita l'assenza di sessione;
- `noUncheckedIndexedAccess` rende visibile il caso elemento mancante;
- `@ts-expect-error` e usato solo come lente didattica per errori intenzionali;
- nessun esempio deve suggerire che TypeScript validi automaticamente una risposta HTTP.

Il gate CI corretto e `tsc --noEmit`. Non dichiarare questa Activity autograded TheBitLab finche il runner TypeScript non esiste nel contratto piattaforma.
