# Diagnosi SQLAlchemy

Per ogni difetto compila:

- sintomo osservabile;
- causa;
- boundary/lifetime violato;
- fix minimo;
- test che impedirebbe la regressione.

## 1. Engine

Perche creare Engine nella factory chiamata dall'adapter a ogni operazione e un problema?

## 2. Session globale

Quale stato conserva una Session? Perche il lifetime indefinito e pericoloso?

## 3. Query API

Perche `session.query(...)` non e la baseline scelta dal corso SQLAlchemy 2.0?

## 4. `flush()` vs `commit()`

Cosa garantisce `flush()`? Cosa aggiunge `commit()`? Come dimostreresti il bug con un restart test?

## 5. `row.__dict__`

Quale dettaglio ORM puo comparire? Perche non deve diventare representation pubblica?

## 6. Error recovery

Dopo un `IntegrityError` durante commit, perche una Session riusata richiede rollback prima di nuove operazioni?

## 7. Correzione architetturale

Disegna:

```text
composition root
      ↓
Engine + SessionFactory
      ↓
repository
      ↓
Session corta per metodo
```
