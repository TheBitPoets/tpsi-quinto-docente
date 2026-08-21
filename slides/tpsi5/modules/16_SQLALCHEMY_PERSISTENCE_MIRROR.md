---
marp: true
paginate: true
size: 16:9
title: 16 — SQLAlchemy 2.0 e persistenza
---

# 16 — SQLAlchemy 2.0
## Stesso contratto, nuovo data layer

UDA 26 — Python mirror

---

# Richiamo

Nel backend Node abbiamo visto SQL raw.

Ora osserviamo un ORM nel mirror Python.

La domanda non è “ORM o SQL: chi vince?”

La domanda è:

> quale astrazione stiamo aggiungendo e cosa rimane sotto?

---

# Obiettivi

Alla fine dovrai saper:

- spiegare engine e Session;
- leggere un mapping ORM;
- distinguere modello ORM e schema HTTP;
- usare un repository dietro lo stesso contratto;
- capire commit/rollback;
- verificare persistenza con restart test.

---

# Engine

```py
engine = create_engine(database_url)
```

L'engine rappresenta la configurazione di accesso al database.

Non è “il database” e non è una sessione di lavoro utente.

---

# Mapping ORM

```py
class Post(Base):
    __tablename__ = 'posts'

    id: Mapped[int] = mapped_column(primary_key=True)
    text: Mapped[str]
```

Il mapping collega oggetti Python e righe/tabella.

---

# Session

```py
with Session(engine) as session:
    post = Post(text='Ciao')
    session.add(post)
    session.commit()
```

La Session rappresenta un'unità di lavoro con il database.

---

# ORM non cancella SQL

Dietro:

```py
session.add(post)
session.commit()
```

il sistema produrrà query SQL.

Il vantaggio è lavorare con un livello di astrazione più alto, non far sparire il database.

---

# Repository

```py
class SqlAlchemyPostRepository:
    def list(self) -> list[PostData]:
        ...

    def create(self, input: PostCreateData) -> PostData:
        ...
```

L'API può restare stabile mentre cambia il data layer.

---

# HTTP model ≠ ORM model

Non usare automaticamente l'oggetto ORM come contratto pubblico.

Separare:

```text
Pydantic schema
↕ mapping
repository/domain data
↕
ORM model
```

---

# Transazioni

Una modifica persistente richiede una decisione esplicita:

```text
commit -> rende permanente
rollback -> annulla unità di lavoro
```

Le transazioni proteggono coerenza e failure handling.

---

# Errore tipico: sessione globale

Una Session condivisa senza lifecycle chiaro può creare:

- stato inatteso;
- transazioni confuse;
- test fragili.

Meglio un confine di sessione ben definito per operazione/request/test.

---

# Restart test

Come nel modulo SQL raw:

1. crea dato;
2. chiudi app/sessione/processo;
3. ricrea app;
4. rileggi dato.

Il test dimostra persistenza reale, non memoria mascherata.

---

# Checkpoint

Associa:

1. `engine`;
2. `Session`;
3. mapped class;
4. Pydantic response model;
5. repository;
6. commit.

Configurazione? unità di lavoro? persistence model? API contract? boundary? transazione?

---

# Feisbuc mirror 02

```text
FastAPI
→ repository contract
→ SQLAlchemy repository
→ SQLite
```

Il contratto HTTP resta quello del mirror precedente.

---

# Handoff al laboratorio

1. leggi mapping ORM;
2. crea una Session scoped;
3. implementa repository;
4. verifica commit;
5. prova restart persistence;
6. confronta con SQL raw del backend Node.

---

# Recap

SQLAlchemy aggiunge:

- mapping;
- Session/unit of work;
- API ORM;

Ma restano centrali:

- schema DB;
- transazioni;
- repository boundary;
- test di persistenza.

Prossimo modulo: **testing strategy e integration boundaries**.