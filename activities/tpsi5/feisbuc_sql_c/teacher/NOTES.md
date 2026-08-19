# Note docente — milestone 6

## Evidenze forti

- il Router e sostanzialmente identico alla milestone 5;
- `SqlPostStore` non importa Express;
- tutti i valori esterni passano come parametri dei prepared statement;
- la conversione 0/1 ↔ boolean avviene nel repository;
- un test restart utilizza lo stesso file DB e ritrova il post creato;
- `DB_PATH=:memory:` rende i test isolati;
- il seed non si duplica al restart.

## Domande orali

1. Perche abbiamo mantenuto `PostStore` invece di mettere SQL nelle route?
2. Quale invariante e protetto sia da validation HTTP sia da `CHECK` SQL?
3. Perche `INSERT OR IGNORE` e usato soltanto per il seed e non per nascondere errori applicativi?
4. Perche una singola `UPDATE ... CASE` e preferibile al ciclo SELECT → JS → UPDATE per il like?
5. Cosa cambia se `DB_PATH` vale `:memory:`?

## Estensioni

- `EXPLAIN QUERY PLAN` sull'indice liked/created_at;
- transaction con tabella audit;
- migrazione schema versionata.

Non anticipare ORM: prima chiedere allo studente di spiegare le query raw che l'ORM dovrebbe astrarre.
