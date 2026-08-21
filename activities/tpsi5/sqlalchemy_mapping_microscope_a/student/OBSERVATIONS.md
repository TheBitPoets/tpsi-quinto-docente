# Osservazioni SQLAlchemy microscope

Compila dopo aver eseguito:

```bash
python -m pip install -r requirements.txt
python app.py
```

## 1. Mapping

- Quale classe Python rappresenta la tabella `posts`?
- Quale attributo e primary key?
- Dove riconosci i tipi/constraint SQL?

## 2. Engine

- Qual e il database URL?
- Perche `echo=True` e utile in questo laboratorio?
- L'Engine e una singola query, una Session o infrastruttura condivisa?

## 3. Session

- Cosa significa `row in session.new` prima del commit?
- Cosa cambia dopo `commit()`?
- Perche la seconda query apre una nuova Session?
- Perche questa Session non e la sessione login studiata in auth?

## 4. SQL osservato

Copia o descrivi le operazioni equivalenti a:

- DDL / `CREATE TABLE`;
- `INSERT`;
- `COMMIT`;
- `SELECT`.

## 5. Confronto con SQL raw

Scrivi una tabella mentale:

```text
SQL raw UDA24          SQLAlchemy 2.0
-------------          --------------
CREATE TABLE           ?
INSERT                  ?
SELECT                  ?
transaction commit      ?
row result              ?
```

## 6. Una frase conclusiva

Completa:

> SQLAlchemy non elimina SQL; ...
