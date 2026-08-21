# SQLAlchemy 2.0 e persistenza: stesso contratto, nuovo data layer

Stato didattico: **draft**.

## Obiettivi

Al termine del modulo lo studente sa:

- spiegare perche un ORM non sostituisce ne HTTP ne il modello relazionale;
- riconoscere il mapping tra classe Python, tabella, attributo e colonna;
- usare lo stile SQLAlchemy 2.0 con `DeclarativeBase`, `Mapped` e `mapped_column`;
- distinguere **Engine**, **Connection**, **Session** e repository;
- usare `select(...)` e `Session.scalars(...)` senza ricadere nella legacy Query API;
- spiegare `add`, `flush`, `commit`, `rollback`, identity map e unit of work a livello essenziale;
- costruire un `SqlAlchemyPostStore` che non importi FastAPI;
- mantenere invariati route, status, `Location`, Pydantic model e OpenAPI del mirror precedente;
- usare SQLite come database del laboratorio senza confondere SQLite e SQLAlchemy;
- verificare con `TestClient` che i dati sopravvivano alla ricreazione dell'applicazione;
- riconoscere i problemi di session lifetime, transazioni non committate, engine creati nel posto sbagliato e state leakage nei test;
- spiegare perche `create_all()` va bene nel laboratorio ma non e una strategia completa di migrazione schema per un prodotto reale.

## Prerequisiti

- UDA24: SQL raw, schema, constraint, prepared statement, transazioni e repository;
- primo slice UDA26: FastAPI, Pydantic, OpenAPI, `response_model` e `TestClient`;
- Python: classi, context manager, type hint essenziali;
- contratto Feisbuc mirror gia funzionante:

```text
GET   /api/posts
POST  /api/posts
PATCH /api/posts/{post_id}
```

---

## 1. Perche l'ORM arriva dopo SQL raw

In UDA24 abbiamo visto il database senza astrazioni premature:

```text
SQL
prepared statement
constraint
transaction
repository
```

Ora possiamo introdurre un ORM sapendo quale problema sta nascondendo.

Se iniziassimo direttamente da:

```py
session.add(post)
session.commit()
```

senza avere mai studiato `INSERT`, primary key e transaction, il codice sembrerebbe magia.

Il nuovo schema mentale e invece:

```text
oggetti Python
      ↓
SQLAlchemy ORM
      ↓
SQL generato
      ↓
DBAPI / driver
      ↓
SQLite
```

L'ORM non elimina SQL. Produce e coordina SQL per noi.

Regola didattica:

> prima comprendiamo il modello relazionale; poi impariamo l'astrazione che lo mappa su oggetti.

---

## 2. Il contratto HTTP non deve accorgersi del cambio

Mirror 01:

```text
TestClient
    ↓
FastAPI
    ↓
Pydantic
    ↓
MemoryPostStore
```

Mirror 02:

```text
TestClient
    ↓
FastAPI
    ↓
Pydantic
    ↓
SqlAlchemyPostStore
    ↓
Session
    ↓
SQLAlchemy ORM
    ↓
SQLite
```

Il client continua a vedere:

```text
GET /api/posts          -> 200 + list[Post]
POST /api/posts         -> 201 + Location + Post
PATCH /api/posts/{id}   -> 200 + Post oppure 404
```

Questa e la prova che il repository e un boundary utile:

> possiamo cambiare il modo in cui salviamo i dati senza riscrivere l'adapter HTTP.

---

## 3. Baseline riproducibile

Il secondo mirror mantiene i pin gia testati:

```text
FastAPI    0.141.1
Pydantic   2.13.4
Uvicorn    0.52.1
HTTPX      0.28.1
```

e aggiunge:

```text
SQLAlchemy 2.0.51
```

Usiamo intenzionalmente l'API moderna 2.0:

- `DeclarativeBase`;
- `Mapped[...]`;
- `mapped_column(...)`;
- `select(...)`;
- `Session` / `sessionmaker`.

Non introduciamo la legacy `session.query(...)` come baseline del corso.

---

## 4. Tre modelli diversi da non confondere

Nel mirror ora convivono tre rappresentazioni.

### Request model

```py
class PostCreate(BaseModel):
    text: str
```

Descrive cio che il client puo inviare.

### ORM entity

```py
class PostRow(Base):
    __tablename__ = "posts"
    ...
```

Descrive il mapping persistente.

### Response model

```py
class Post(BaseModel):
    id: str
    text: str
    authorId: str
    author: str
    liked: bool
    likes: int
```

Descrive la representation HTTP pubblica.

Schema:

```text
JSON input
   ↓
PostCreate
   ↓
repository
   ↓
PostRow
   ↓
repository mapping
   ↓
Post JSON output
```

Errore frequente:

```text
PostCreate == PostRow == Post
```

Non sono la stessa responsabilita.

---

## 5. DeclarativeBase: il catalogo dei mapping

SQLAlchemy 2.0 permette di definire una base dichiarativa:

```py
from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    pass
```

Le entity che ereditano da `Base` partecipano allo stesso metadata.

```py
from sqlalchemy.orm import Mapped, mapped_column

class PostRow(Base):
    __tablename__ = "posts"

    id: Mapped[str] = mapped_column(primary_key=True)
    text: Mapped[str]
```

Leggiamolo lentamente:

```text
PostRow         -> classe Python persistente
posts           -> tabella
id              -> attributo Python
mapped_column   -> mapping verso una colonna
primary_key     -> vincolo relazionale
```

La classe non e la tabella: e un mapping della tabella nel programma.

---

## 6. Tipi Python e tipi SQL

Possiamo rendere il mapping piu esplicito:

```py
from sqlalchemy import Boolean, Integer, String

class PostRow(Base):
    __tablename__ = "posts"

    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    text: Mapped[str] = mapped_column(String(280), nullable=False)
    author_id: Mapped[str] = mapped_column(String(64), nullable=False)
    author: Mapped[str] = mapped_column(String(120), nullable=False)
    liked: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    likes: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
```

Qui sono visibili due mondi:

```text
Mapped[str]     -> tipo dell'attributo Python
String(280)     -> tipo/constraint del mapping SQL
```

Pydantic continua a validare il boundary HTTP. Il database continua ad avere propri constraint.

Defense in depth:

```text
request validation
      +
domain invariant
      +
database constraint
```

---

## 7. Engine: configurazione e accesso al database

Creiamo un Engine:

```py
from sqlalchemy import create_engine

engine = create_engine("sqlite:///./feisbuc-mirror.db")
```

L'Engine rappresenta la configurazione di accesso al database e gestisce il pool delle connessioni.

Non significa:

```text
una query
una Session
una tabella
```

Pensiamolo come infrastruttura condivisa:

```text
application
    ↓
Engine
    ↓
connection pool
    ↓
SQLite
```

Errore importante:

> creare un nuovo Engine dentro ogni route.

Se la configurazione appartiene al composition root, la route non deve reinventarla a ogni request.

---

## 8. Session: unit of work, non sessione login

La parola `Session` qui **non** significa la sessione HTTP dell'utente.

SQLAlchemy Session:

```text
coordina oggetti ORM + query + transaction
```

Sessione web Feisbuc:

```text
identifica/autentica un utente tra request diverse
```

Sono concetti completamente differenti.

Usiamo una factory:

```py
from sqlalchemy.orm import sessionmaker

SessionFactory = sessionmaker(bind=engine, expire_on_commit=False)
```

Poi:

```py
with SessionFactory() as session:
    ...
```

Il context manager rende esplicito il lifetime.

---

## 9. Identity map: perche una Session tiene traccia degli oggetti

Dentro la stessa Session, SQLAlchemy mantiene una identity map.

Concettualmente:

```text
(primary key, entity type)
        ↓
istanza Python gia caricata
```

Questo permette alla Session di sapere quali oggetti sono:

- nuovi;
- modificati;
- gia caricati;
- da sincronizzare col database.

Non serve conoscere tutti i dettagli interni, ma serve capire che una Session **ha stato**.

Per questo non vogliamo una Session globale condivisa indefinitamente da tutta l'applicazione.

---

## 10. INSERT: add, flush e commit

Creiamo una entity:

```py
row = PostRow(
    id="p42",
    text="ciao",
    author_id="mirror-user",
    author="Mirror Student",
    liked=False,
    likes=0,
)
```

La aggiungiamo:

```py
session.add(row)
```

A questo punto l'oggetto e nella unit of work, ma non dobbiamo confondere `add` con una transazione definitivamente salvata.

Concettualmente:

```text
add
 ↓
Session conosce il nuovo oggetto
 ↓
flush
 ↓
SQL inviato al database nella transaction
 ↓
commit
 ↓
transaction confermata
```

`flush` e `commit` non sono sinonimi.

Per il corso usiamo normalmente:

```py
session.add(row)
session.commit()
```

ma sappiamo che il commit chiude la transaction, mentre il flush sincronizza lo stato pendente senza confermare definitivamente la transaction.

---

## 11. SELECT con lo stile SQLAlchemy 2.0

Importiamo `select`:

```py
from sqlalchemy import select
```

Costruiamo uno statement:

```py
statement = select(PostRow)
```

Eseguiamo tramite Session:

```py
rows = session.scalars(statement).all()
```

Catena mentale:

```text
select(PostRow)
      ↓
SQL expression
      ↓
Session.execute/scalars
      ↓
SQL sul database
      ↓
PostRow Python
```

Per una primary key possiamo usare:

```py
row = session.get(PostRow, post_id)
```

Questo comunica bene l'intenzione: ricerca per identity/primary key.

---

## 12. Repository: teniamo FastAPI fuori dalla persistenza

Il repository riceve una session factory:

```py
class SqlAlchemyPostStore:
    def __init__(self, session_factory):
        self._session_factory = session_factory
```

Poi:

```py
def list(self):
    with self._session_factory() as session:
        rows = session.scalars(select(PostRow)).all()
        return [to_public_post(row) for row in rows]
```

Il file del repository non deve importare:

```py
FastAPI
Request
Response
HTTPException
```

Boundary:

```text
FastAPI adapter
     ↓
PostStore
     ↓
SQLAlchemy
```

In questo modo un test del repository non deve avviare FastAPI.

---

## 13. Mapping ORM -> representation pubblica

Una entity ORM non e automaticamente la nostra API.

Possiamo usare una funzione esplicita:

```py
def to_public_post(row: PostRow) -> dict:
    return {
        "id": row.id,
        "text": row.text,
        "authorId": row.author_id,
        "author": row.author,
        "liked": row.liked,
        "likes": row.likes,
    }
```

Perche farlo?

Perche la tabella potrebbe contenere anche:

```text
internal_note
version
moderation_state
foreign key tecniche
```

che non devono diventare campi HTTP per accidente.

La stessa lezione di `response_model` resta valida anche con un ORM.

---

## 14. UPDATE del like e idempotenza applicativa

La PATCH riceve:

```json
{"liked": true}
```

Il repository trova il post:

```py
row = session.get(PostRow, post_id)
```

Se manca:

```py
return None
```

Se esiste, applichiamo la transizione solo se cambia stato:

```py
if row.liked != liked:
    row.likes += 1 if liked else -1
    row.liked = liked
```

Poi:

```py
session.commit()
```

La route continua a decidere la semantica HTTP del `None`:

```py
if post is None:
    raise HTTPException(status_code=404, ...)
```

Responsabilita separate:

```text
repository -> risorsa assente: None
HTTP adapter -> None significa 404
```

---

## 15. Transaction boundary

Per una singola operazione repository semplice possiamo usare:

```py
with SessionFactory() as session:
    ...
    session.commit()
```

Se un errore avviene prima del commit, la transaction non deve essere considerata conclusa con successo.

Quando gestiamo esplicitamente errori all'interno di una Session riutilizzata, `rollback()` e importante per riportare la Session in uno stato utilizzabile.

Nel laboratorio preferiamo lifetime corti:

```text
metodo repository
    ↓
apri Session
    ↓
query / mutate
    ↓
commit se serve
    ↓
chiudi Session
```

Questo riduce lo state leakage tra operazioni.

---

## 16. SQLite: file, memoria e connessioni

Questi URL non sono equivalenti:

```text
sqlite:///./feisbuc.db
sqlite:///:memory:
sqlite://
```

Per dimostrare la persistenza usiamo un **file temporaneo** nei test:

```py
database_url = f"sqlite:///{db_path.as_posix()}"
```

Poi:

```text
app 1 -> crea post -> dispose engine
app 2 -> stesso file -> GET -> post ancora presente
```

Questo testa una proprieta che MemoryPostStore non aveva:

> il processo/applicazione puo essere ricreato senza perdere i dati.

### Il piccolo problema di `check_same_thread`

Con SQLite + test web multithread possiamo configurare:

```py
connect_args={"check_same_thread": False}
```

E una scelta specifica del driver SQLite, non una regola generale di SQLAlchemy.

---

## 17. Composition root: dove colleghiamo i pezzi

Vogliamo una factory:

```py
def create_app(database_url: str) -> FastAPI:
    engine = create_engine(...)
    Base.metadata.create_all(engine)
    SessionFactory = sessionmaker(...)
    store = SqlAlchemyPostStore(SessionFactory)

    app = FastAPI(...)
    ...
    return app
```

Questo rende il test indipendente dalla configurazione reale:

```py
app = create_app(temp_database_url)
```

Produzione/lab locale possono invece usare:

```py
app = create_app("sqlite:///./feisbuc-mirror.db")
```

Il composition root decide **quale implementazione** usare.

La route non decide il path del database.

---

## 18. Seed idempotente

Il mirror ha un post iniziale `seed-1`.

Se eseguiamo l'app due volte non vogliamo due copie.

Pattern:

```py
with SessionFactory() as session:
    if session.get(PostRow, "seed-1") is None:
        session.add(PostRow(...))
        session.commit()
```

Questa e una piccola forma di bootstrap idempotente.

Non e una migration system.

Serve solo a rendere riproducibile la fixture didattica.

---

## 19. `create_all()` non e Alembic

Nel laboratorio possiamo fare:

```py
Base.metadata.create_all(engine)
```

Questo crea le tabelle mancanti sulla base del metadata.

Ma in un prodotto reale serve gestire evoluzioni come:

```text
aggiungi colonna
rinomina colonna
migra dati
crea indice senza perdere dati
rollback di release
```

`create_all()` non descrive una storia di migrazioni.

Per ora fissiamo il boundary:

```text
mirror 02 -> create_all per fixture didattica
futuro professionale -> migration tool/versioned schema
```

Non introduciamo Alembic nello stesso momento dell'ORM: sarebbe un'altra nuova responsabilita.

---

## 20. Test del repository e test HTTP non sono duplicati

### Test repository

Verifica:

```text
create
list
set_liked
persistenza
```

senza FastAPI.

### Test HTTP

Verifica:

```text
status
Location
JSON shape
404
422
OpenAPI
```

con `TestClient`.

I due livelli rispondono a domande diverse.

```text
repository test -> il data layer conserva correttamente lo stato?
HTTP test       -> il client osserva ancora lo stesso contratto?
```

---

## 21. Test di restart: la prova che il nuovo slice aggiunge davvero qualcosa

Un test importante:

```text
1. crea database temporaneo
2. crea app A
3. POST un post
4. chiudi/dispose A
5. crea app B sullo stesso database
6. GET /api/posts
7. verifica che il post esista ancora
```

Se questo test passa, abbiamo evidenza della proprieta nuova:

```text
MemoryPostStore -> state legato al processo
SQLAlchemy/SQLite -> state persistente su file
```

---

## 22. Errori frequenti

### Una Session globale per tutta l'app

Problema:

```py
session = Session(engine)
```

creata una volta e riusata indefinitamente.

Rischi:

- state leakage;
- transaction boundary confuso;
- error recovery difficile;
- concorrenza/lifetime non espliciti.

### Engine dentro ogni route

Problema:

```py
@app.get(...)
def route():
    engine = create_engine(...)
```

L'infrastruttura viene ricreata nel posto sbagliato.

### `add()` senza `commit()`

L'oggetto entra nella unit of work ma non abbiamo confermato la transaction.

### Restituire direttamente `row.__dict__`

Espone dettagli ORM come `_sa_instance_state` e rompe il boundary pubblico.

### Confondere Session SQLAlchemy e sessione utente

Stesso nome, responsabilita diversa.

### Mettere `HTTPException` nel repository

Il data layer diventerebbe dipendente da FastAPI.

### Test con database condiviso involontariamente

Un test crea dati che fanno fallire quello successivo.

Usare database temporanei/fixture isolate.

---

## 23. Confronto: SQL raw UDA24 e SQLAlchemy UDA26

| Problema | SQL raw | SQLAlchemy ORM |
| --- | --- | --- |
| schema | DDL esplicito | mapping + metadata |
| select | `SELECT ...` | `select(PostRow)` |
| bind param | placeholder | expression binding |
| row -> object | manuale | ORM mapping |
| transaction | API DB | Session/unit of work |
| repository | SQL dentro metodi | ORM dentro metodi |
| constraint DB | visibile nel DDL | dichiarato nel mapping / DB |
| HTTP contract | fuori dal repository | fuori dal repository |

Non stiamo sostituendo una conoscenza con l'altra.

Stiamo aggiungendo un secondo modo di implementare lo stesso data layer.

---

## 24. Cosa non entra ancora

Questo slice **non** introduce:

- auth/session Python;
- utenti e password nel mirror;
- Socket.IO Python;
- frontend Python;
- Alembic;
- PostgreSQL;
- async SQLAlchemy;
- relationship complesse;
- ORM nel backend Node principale;
- deploy container/cloud.

Questi temi hanno valore solo quando rispondono a un requisito reale del blocco successivo.

---

## 25. Progressione A-D

### A — SQLAlchemy mapping microscope

Osservare:

- metadata;
- mapping;
- Engine;
- Session;
- SQL prodotto;
- identity/commit/select.

### B — Repository controllato

Completare un piccolo `SqlAlchemyPostStore` senza FastAPI.

### C — Feisbuc mirror 02

Sostituire il MemoryPostStore con SQLAlchemy + SQLite mantenendo il contratto FastAPI e verificando il restart.

### D — Debug transaction/session boundaries

Diagnosticare:

- Session globale;
- Engine nel posto sbagliato;
- commit mancante;
- output ORM esposto;
- rollback/lifetime non governato.

---

## 26. Milestone Feisbuc mirror 02

Nome:

```text
feisbuc-mirror-02-sqlalchemy-persistence
```

Architettura:

```text
TestClient
    ↓
FastAPI
    ↓
Pydantic
    ↓
SqlAlchemyPostStore
    ↓
SessionFactory
    ↓
SQLAlchemy 2.0
    ↓
SQLite file
```

Invarianti:

1. stesso contratto HTTP di mirror 01;
2. `PostCreate` non accetta identita trusted dal client;
3. entity ORM separata dai model Pydantic;
4. repository senza import FastAPI;
5. Session lifetime corto e visibile;
6. commit esplicito sulle mutazioni;
7. seed idempotente;
8. database configurabile dal composition root;
9. test con file temporaneo;
10. test di restart/persistenza;
11. nessuna auth/realtime/deploy aggiunti prematuramente.

---

## 27. Checklist professionale

Prima di considerare completo il slice:

- [ ] SQLAlchemy 2.0.51 pinned;
- [ ] `DeclarativeBase` / `Mapped` / `mapped_column`;
- [ ] nessuna legacy Query API come baseline;
- [ ] Engine creato nel composition root;
- [ ] SessionFactory iniettata nel repository;
- [ ] repository indipendente da FastAPI;
- [ ] Pydantic separato dalle entity ORM;
- [ ] create fa commit;
- [ ] update fa commit;
- [ ] missing resource resta 404 nell'adapter;
- [ ] `201 + Location` resta invariato;
- [ ] `422` resta documentato come validation boundary del mirror;
- [ ] OpenAPI resta presente;
- [ ] persistenza verificata dopo ricreazione app;
- [ ] engine disposed nei test che usano file temporanei;
- [ ] niente auth, Socket.IO o deploy nel mirror 02.

---

## 28. Ponte al prossimo slice

A questo punto abbiamo due assi di test:

```text
HTTP contract test
repository/persistence test
```

Il passo successivo di UDA26 non deve aggiungere un altro framework per il gusto di farlo.

Dobbiamo consolidare:

- piramide dei test e fixture;
- integration/e2e boundaries;
- configurazione per ambienti;
- packaging/deploy;
- capstone Feisbuc con evidenze verificabili.

Il punto raggiunto e importante:

> abbiamo cambiato linguaggio, framework e tecnologia di persistenza, ma il contratto osservabile e rimasto sotto controllo.
