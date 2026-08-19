# Diagnosi di riferimento

| Bug | Sintomo | Causa | Insieme corretto | Fix minimo | Verifica |
| --- | --- | --- | --- | --- | --- |
| 1 | lo script si interrompe sull'INSERT di `remove-me` | `liked=2` viola `CHECK (liked IN (0,1))` | la riga temporanea deve comunque essere uno stato valido | usare `liked=0` | l'INSERT riesce senza rimuovere il constraint |
| 2 | p1, p2 e p3 ricevono tutti un like | `UPDATE` senza `WHERE` seleziona tutte le righe | solo `id='p2'` | aggiungere `WHERE id='p2'` | p1 resta 2/1, p2 diventa 1/1, p3 resta 0/0 |
| 3 | il `DELETE` elimina piu righe del previsto | `WHERE id <> 'p1'` descrive p2, p3 e remove-me | solo `id='remove-me'` | `DELETE ... WHERE id='remove-me'` | rimangono esattamente p1, p2, p3 |

Rimuovere il `CHECK` non corregge il dato: indebolisce l'invariante persistente e permetterebbe altri valori impossibili in futuro.
