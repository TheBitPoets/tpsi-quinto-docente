# Activity A — schema `posts`

Obiettivo: trasformare il modello del post in uno schema che **impedisca stati impossibili**.

## Da fare

Completa `main.sql` aggiungendo:

- tabella `STRICT`;
- `CHECK` su author non vuoto;
- `CHECK` su text dopo trim: 1–280 caratteri;
- `CHECK (likes >= 0)`;
- `CHECK (liked IN (0, 1))`;
- indice `idx_posts_liked_created(liked, created_at DESC)`.

Non cambiare i due seed `p1` e `p2`.

## Cosa misura il grader

Il grader TheBitLab usa un SQLite isolato in memoria. Dopo il tuo script esegue query aggiuntive per verificare:

1. dati seed;
2. rifiuto di stati invalidi con `INSERT OR IGNORE`;
3. presenza dell'indice richiesto.

## Metodo

Prima di modificare lo schema, scrivi accanto a ogni proprietà JavaScript l'invariante che vuoi proteggere nel database.

```text
text   -> ?
likes  -> ?
liked  -> ?
```

Poi traduci gli invarianti in constraint SQL.
