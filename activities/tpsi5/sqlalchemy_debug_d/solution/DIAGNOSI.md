# Diagnosi reference

## 1. Engine nel lifetime sbagliato

`make_store()` crea l'Engine. Se l'adapter richiama questa factory a ogni request/operazione, ricrea configurazione e pool e rende il lifecycle del database dipendente dal web adapter. L'Engine appartiene al composition root e va condiviso con lifetime applicativo; il repository riceve una SessionFactory derivata da quell'Engine.

Test: costruire piu operazioni sullo stesso database e verificare che usino la stessa infrastruttura/configurazione; nel mirror, creare l'Engine una volta in `create_app`.

## 2. Session globale

La Session mantiene identity map, unit of work e stato della transaction. Una Session globale riusata indefinitamente mescola lifetime diversi, rende la recovery dopo errori fragile e crea problemi di concorrenza/state leakage.

Fix: `sessionmaker(...)` nel composition root/repository e `with session_factory() as session:` per ogni metodo/transaction boundary.

## 3. Query legacy

`session.query(PostRow)` appartiene alla Query API legacy. La baseline del corso SQLAlchemy 2.0 usa:

```py
rows = session.scalars(select(PostRow)).all()
```

Il problema non e che Query non possa funzionare, ma che insegnerebbe due stili contemporaneamente senza beneficio didattico.

## 4. `flush()` non e `commit()`

`flush()` sincronizza le modifiche pendenti con il database **dentro la transaction corrente**. Non conferma definitivamente la transaction. Se il processo termina o la transaction viene rollbackata, non abbiamo la durability attesa.

Fix:

```py
session.add(row)
session.commit()
```

Test: create con app/processo A, chiusura/dispose, nuova app/processo B sullo stesso file SQLite, GET del record.

## 5. `row.__dict__` non e una representation

L'istanza ORM contiene dettagli interni, incluso `_sa_instance_state`. Pubblicare `row.__dict__` accoppia l'API alla struttura interna dell'ORM e puo far trapelare campi non destinati al client.

Fix: mapping esplicito `to_public_post(row)` e, nell'adapter HTTP, `response_model` Pydantic.

## 6. Failure senza rollback

Se `session.commit()` fallisce con `IntegrityError`, la transaction e fallita. Se si intende riusare quella Session servirebbe `session.rollback()` prima di nuove operazioni.

Nel pattern del corso la Session e corta e viene chiusa a fine metodo; quando intercettiamo una failure dentro il metodo facciamo comunque rollback prima di propagare/gestire l'errore:

```py
try:
    session.commit()
except Exception:
    session.rollback()
    raise
```

`rollback()` non sostituisce il commit: serve a chiudere/annullare correttamente una transaction fallita.

## 7. Architettura corretta

```text
composition root
      ↓
Engine
      ↓
SessionFactory
      ↓
SqlAlchemyPostStore
      ↓
Session corta per metodo
      ↓
select / add / commit / rollback
```

FastAPI non deve entrare nel repository e il repository non deve decidere status code HTTP.
