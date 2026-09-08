# SQLAlchemy 2.0 e persistenza: stesso contratto, nuovo data layer

<table align="center" width="100%"><tr><td>
<details>
<summary>&#128506; <strong>Orientamento della lezione</strong></summary>

<p align="justify"><strong>Contesto:</strong> dopo SQL raw possiamo introdurre l'ORM senza nascondere tabella, chiave, query e transazione. Il contratto HTTP non deve accorgersi del cambio di data layer.</p>
<p align="justify"><strong>Domande guida:</strong> che differenza c'è fra modello di dominio, modello API e mapping ORM? Chi possiede la Session? Quando avvengono flush, commit e rollback?</p>
<p align="justify"><strong>Obiettivi osservabili:</strong> definire mapping tipizzati, configurare Engine e Session, eseguire CRUD con lo stile 2.0, delimitare la transazione e dimostrare la persistenza con un restart test.</p>
<p align="justify"><strong>Prossimo passo:</strong> la lezione 17 progetterà test affidabili intorno a repository, HTTP e riavvio.</p>

</details>
</td></tr></table>

<p align="justify">Stato didattico: <strong>draft</strong>.</p>

## Obiettivi

<p align="justify">Al termine del modulo lo studente sa:</p>

<ul>
  <li>spiegare perche un ORM non sostituisce ne HTTP ne il modello relazionale;</li>
  <li>riconoscere il mapping tra classe Python, tabella, attributo e colonna;</li>
  <li>usare lo stile SQLAlchemy 2.0 con <code>DeclarativeBase</code>, <code>Mapped</code> e <code>mapped_column</code>;</li>
  <li>distinguere <strong>Engine</strong>, <strong>Connection</strong>, <strong>Session</strong> e repository;</li>
  <li>usare <code>select(...)</code> e <code>Session.scalars(...)</code> senza ricadere nella legacy Query API;</li>
  <li>spiegare <code>add</code>, <code>flush</code>, <code>commit</code>, <code>rollback</code>, identity map e unit of work a livello essenziale;</li>
  <li>costruire un <code>SqlAlchemyPostStore</code> che non importi FastAPI;</li>
  <li>mantenere invariati route, status, <code>Location</code>, Pydantic model e OpenAPI del mirror precedente;</li>
  <li>usare SQLite come database del laboratorio senza confondere SQLite e SQLAlchemy;</li>
  <li>verificare con <code>TestClient</code> che i dati sopravvivano alla ricreazione dell'applicazione;</li>
  <li>riconoscere i problemi di session lifetime, transazioni non committate, engine creati nel posto sbagliato e state leakage nei test;</li>
  <li>spiegare perche <code>create_all()</code> va bene nel laboratorio ma non e una strategia completa di migrazione schema per un prodotto reale.</li>
</ul>

## Prerequisiti

<ul>
  <li>UDA24: SQL raw, schema, constraint, prepared statement, transazioni e repository;</li>
  <li>primo slice UDA26: FastAPI, Pydantic, OpenAPI, <code>response_model</code> e <code>TestClient</code>;</li>
  <li>Python: classi, context manager, type hint essenziali;</li>
  <li>contratto Feisbuc mirror gia funzionante:</li>
</ul>

```text
GET   /api/posts
POST  /api/posts
PATCH /api/posts/{post_id}
```

## Orientamento nella documentazione

<p align="center">
  <img src="../../assets/tpsi5/lesson-documentation-depth.svg" alt="La dispensa seleziona nelle fonti ufficiali i contenuti da studiare ora, riconoscere, rimandare o dichiarare fuori confine">
</p>

<table align="center"><tr><td>
<details>
<summary>&#128279; <strong>Indice incrociato — SQLAlchemy 2.0 e SQLite</strong></summary>

<table align="center">
<thead><tr><th>Dispensa</th><th>Documentazione ufficiale</th><th>Profondità</th></tr></thead>
<tbody>
<tr><td><a href="#lesson-sqla-mapping">Mapping dichiarativo e tipi</a></td><td><a href="https://docs.sqlalchemy.org/en/20/orm/quickstart.html">ORM Quick Start</a><br><a href="https://docs.sqlalchemy.org/en/20/orm/declarative_tables.html">Table Configuration</a></td><td>&#128994; studiare ora</td></tr>
<tr><td><a href="#lesson-sqla-session">Engine, Session e identity map</a></td><td><a href="https://docs.sqlalchemy.org/en/20/orm/session_basics.html">SQLAlchemy — Session Basics</a></td><td>&#128994; studiare il modello essenziale</td></tr>
<tr><td><a href="#lesson-sqla-transactions">CRUD, flush, commit e rollback</a></td><td><a href="https://docs.sqlalchemy.org/en/20/tutorial/orm_data_manipulation.html">Data Manipulation with the ORM</a><br><a href="https://docs.sqlalchemy.org/en/20/orm/session_transaction.html">Transactions and Connection Management</a></td><td>&#128994; studiare ora</td></tr>
<tr><td><a href="#lesson-sqla-testing">Repository e restart test</a></td><td><a href="https://docs.sqlalchemy.org/en/20/orm/session_basics.html#session-faq-whentocreate">Session lifecycle</a></td><td>&#128994; applicare al boundary del corso</td></tr>
<tr><td>Relazioni complesse, async ORM, migration e performance</td><td><a href="https://docs.sqlalchemy.org/en/20/">SQLAlchemy documentation</a></td><td>&#128993; riconoscere o fuori dal core</td></tr>
</tbody>
</table>

</details>
</td></tr></table>

---

## 1. Perche l'ORM arriva dopo SQL raw

<p align="justify">In UDA24 abbiamo visto il database senza astrazioni premature:</p>

```text
SQL
prepared statement
constraint
transaction
repository
```

<p align="justify">Ora possiamo introdurre un ORM sapendo quale problema sta nascondendo.</p>

<p align="justify">Se iniziassimo direttamente da:</p>

```py
session.add(post)
session.commit()
```

<p align="justify">senza avere mai studiato <code>INSERT</code>, primary key e transaction, il codice sembrerebbe magia.</p>

<p align="justify">Il nuovo schema mentale e invece:</p>

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

<p align="justify">L'ORM non elimina SQL. Produce e coordina SQL per noi.</p>

<p align="justify">Regola didattica:</p>

<blockquote>
<p align="justify">prima comprendiamo il modello relazionale; poi impariamo l'astrazione che lo mappa su oggetti.</p>
</blockquote>

---

## 2. Il contratto HTTP non deve accorgersi del cambio

<p align="justify">Mirror 01:</p>

```text
TestClient
    ↓
FastAPI
    ↓
Pydantic
    ↓
MemoryPostStore
```

<p align="justify">Mirror 02:</p>

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

<p align="justify">Il client continua a vedere:</p>

```text
GET /api/posts          -> 200 + list[Post]
POST /api/posts         -> 201 + Location + Post
PATCH /api/posts/{id}   -> 200 + Post oppure 404
```

<p align="justify">Questa e la prova che il repository e un boundary utile:</p>

<blockquote>
<p align="justify">possiamo cambiare il modo in cui salviamo i dati senza riscrivere l'adapter HTTP.</p>
</blockquote>

---

## 3. Baseline riproducibile

<p align="justify">Il secondo mirror mantiene i pin gia testati:</p>

```text
FastAPI    0.141.1
Pydantic   2.13.4
Uvicorn    0.52.1
HTTPX      0.28.1
```

<p align="justify">e aggiunge:</p>

```text
SQLAlchemy 2.0.51
```

<p align="justify">Usiamo intenzionalmente l'API moderna 2.0:</p>

<ul>
  <li><code>DeclarativeBase</code>;</li>
  <li><code>Mapped[...]</code>;</li>
  <li><code>mapped_column(...)</code>;</li>
  <li><code>select(...)</code>;</li>
  <li><code>Session</code> / <code>sessionmaker</code>.</li>
</ul>

<p align="justify">Non introduciamo la legacy <code>session.query(...)</code> come baseline del corso.</p>

---

<a id="lesson-sqla-mapping"></a>
## 4. Tre modelli diversi da non confondere

<p align="justify">Nel mirror ora convivono tre rappresentazioni.</p>

### Request model

```py
class PostCreate(BaseModel):
    text: str
```

<p align="justify">Descrive cio che il client puo inviare.</p>

### ORM entity

```py
class PostRow(Base):
    __tablename__ = "posts"
    ...
```

<p align="justify">Descrive il mapping persistente.</p>

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

<p align="justify">Descrive la representation HTTP pubblica.</p>

<p align="justify">Schema:</p>

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

<p align="justify">Errore frequente:</p>

```text
PostCreate == PostRow == Post
```

<p align="justify">Non sono la stessa responsabilita.</p>

---

## 5. DeclarativeBase: il catalogo dei mapping

<p align="justify">SQLAlchemy 2.0 permette di definire una base dichiarativa:</p>

```py
from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    pass
```

<p align="justify">Le entity che ereditano da <code>Base</code> partecipano allo stesso metadata.</p>

```py
from sqlalchemy.orm import Mapped, mapped_column

class PostRow(Base):
    __tablename__ = "posts"

    id: Mapped[str] = mapped_column(primary_key=True)
    text: Mapped[str]
```

<p align="justify">Leggiamolo lentamente:</p>

```text
PostRow         -> classe Python persistente
posts           -> tabella
id              -> attributo Python
mapped_column   -> mapping verso una colonna
primary_key     -> vincolo relazionale
```

<p align="justify">La classe non e la tabella: e un mapping della tabella nel programma.</p>

---

## 6. Tipi Python e tipi SQL

<p align="justify">Possiamo rendere il mapping piu esplicito:</p>

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

<p align="justify">Qui sono visibili due mondi:</p>

```text
Mapped[str]     -> tipo dell'attributo Python
String(280)     -> tipo/constraint del mapping SQL
```

<p align="justify">Pydantic continua a validare il boundary HTTP. Il database continua ad avere propri constraint.</p>

<p align="justify">Defense in depth:</p>

```text
request validation
      +
domain invariant
      +
database constraint
```

---

<a id="lesson-sqla-session"></a>
## 7. Engine: configurazione e accesso al database

<p align="justify">Creiamo un Engine:</p>

```py
from sqlalchemy import create_engine

engine = create_engine("sqlite:///./feisbuc-mirror.db")
```

<p align="justify">L'Engine rappresenta la configurazione di accesso al database e gestisce il pool delle connessioni.</p>

<p align="justify">Non significa:</p>

```text
una query
una Session
una tabella
```

<p align="justify">Pensiamolo come infrastruttura condivisa:</p>

```text
application
    ↓
Engine
    ↓
connection pool
    ↓
SQLite
```

<p align="justify">Errore importante:</p>

<blockquote>
<p align="justify">creare un nuovo Engine dentro ogni route.</p>
</blockquote>

<p align="justify">Se la configurazione appartiene al composition root, la route non deve reinventarla a ogni request.</p>

---

## 8. Session: unit of work, non sessione login

<p align="justify">La parola <code>Session</code> qui <strong>non</strong> significa la sessione HTTP dell'utente.</p>

<p align="justify">SQLAlchemy Session:</p>

```text
coordina oggetti ORM + query + transaction
```

<p align="justify">Sessione web Feisbuc:</p>

```text
identifica/autentica un utente tra request diverse
```

<p align="justify">Sono concetti completamente differenti.</p>

<p align="justify">Usiamo una factory:</p>

```py
from sqlalchemy.orm import sessionmaker

SessionFactory = sessionmaker(bind=engine, expire_on_commit=False)
```

<p align="justify">Poi:</p>

```py
with SessionFactory() as session:
    ...
```

<p align="justify">Il context manager rende esplicito il lifetime.</p>

---

## 9. Identity map: perche una Session tiene traccia degli oggetti

<p align="justify">Dentro la stessa Session, SQLAlchemy mantiene una identity map.</p>

<p align="justify">Concettualmente:</p>

```text
(primary key, entity type)
        ↓
istanza Python gia caricata
```

<p align="justify">Questo permette alla Session di sapere quali oggetti sono:</p>

<ul>
  <li>nuovi;</li>
  <li>modificati;</li>
  <li>gia caricati;</li>
  <li>da sincronizzare col database.</li>
</ul>

<p align="justify">Non serve conoscere tutti i dettagli interni, ma serve capire che una Session <strong>ha stato</strong>.</p>

<p align="justify">Per questo non vogliamo una Session globale condivisa indefinitamente da tutta l'applicazione.</p>

---

<a id="lesson-sqla-transactions"></a>
## 10. INSERT: add, flush e commit

<p align="justify">Creiamo una entity:</p>

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

<p align="justify">La aggiungiamo:</p>

```py
session.add(row)
```

<p align="justify">A questo punto l'oggetto e nella unit of work, ma non dobbiamo confondere <code>add</code> con una transazione definitivamente salvata.</p>

<p align="justify">Concettualmente:</p>

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

<p align="justify"><code>flush</code> e <code>commit</code> non sono sinonimi.</p>

<p align="justify">Per il corso usiamo normalmente:</p>

```py
session.add(row)
session.commit()
```

<p align="justify">ma sappiamo che il commit chiude la transaction, mentre il flush sincronizza lo stato pendente senza confermare definitivamente la transaction.</p>

---

## 11. SELECT con lo stile SQLAlchemy 2.0

<p align="justify">Importiamo <code>select</code>:</p>

```py
from sqlalchemy import select
```

<p align="justify">Costruiamo uno statement:</p>

```py
statement = select(PostRow)
```

<p align="justify">Eseguiamo tramite Session:</p>

```py
rows = session.scalars(statement).all()
```

<p align="justify">Catena mentale:</p>

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

<p align="justify">Per una primary key possiamo usare:</p>

```py
row = session.get(PostRow, post_id)
```

<p align="justify">Questo comunica bene l'intenzione: ricerca per identity/primary key.</p>

---

## 12. Repository: teniamo FastAPI fuori dalla persistenza

<p align="justify">Il repository riceve una session factory:</p>

```py
class SqlAlchemyPostStore:
    def __init__(self, session_factory):
        self._session_factory = session_factory
```

<p align="justify">Poi:</p>

```py
def list(self):
    with self._session_factory() as session:
        rows = session.scalars(select(PostRow)).all()
        return [to_public_post(row) for row in rows]
```

<p align="justify">Il file del repository non deve importare:</p>

```py
FastAPI
Request
Response
HTTPException
```

<p align="justify">Boundary:</p>

```text
FastAPI adapter
     ↓
PostStore
     ↓
SQLAlchemy
```

<p align="justify">In questo modo un test del repository non deve avviare FastAPI.</p>

---

## 13. Mapping ORM -> representation pubblica

<p align="justify">Una entity ORM non e automaticamente la nostra API.</p>

<p align="justify">Possiamo usare una funzione esplicita:</p>

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

<p align="justify">Perche farlo?</p>

<p align="justify">Perche la tabella potrebbe contenere anche:</p>

```text
internal_note
version
moderation_state
foreign key tecniche
```

<p align="justify">che non devono diventare campi HTTP per accidente.</p>

<p align="justify">La stessa lezione di <code>response_model</code> resta valida anche con un ORM.</p>

---

## 14. UPDATE del like e idempotenza applicativa

<p align="justify">La PATCH riceve:</p>

```json
{"liked": true}
```

<p align="justify">Il repository trova il post:</p>

```py
row = session.get(PostRow, post_id)
```

<p align="justify">Se manca:</p>

```py
return None
```

<p align="justify">Se esiste, applichiamo la transizione solo se cambia stato:</p>

```py
if row.liked != liked:
    row.likes += 1 if liked else -1
    row.liked = liked
```

<p align="justify">Poi:</p>

```py
session.commit()
```

<p align="justify">La route continua a decidere la semantica HTTP del <code>None</code>:</p>

```py
if post is None:
    raise HTTPException(status_code=404, ...)
```

<p align="justify">Responsabilita separate:</p>

```text
repository -> risorsa assente: None
HTTP adapter -> None significa 404
```

---

## 15. Transaction boundary

<p align="justify">Per una singola operazione repository semplice possiamo usare:</p>

```py
with SessionFactory() as session:
    ...
    session.commit()
```

<p align="justify">Se un errore avviene prima del commit, la transaction non deve essere considerata conclusa con successo.</p>

<p align="justify">Quando gestiamo esplicitamente errori all'interno di una Session riutilizzata, <code>rollback()</code> e importante per riportare la Session in uno stato utilizzabile.</p>

<p align="justify">Nel laboratorio preferiamo lifetime corti:</p>

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

<p align="justify">Questo riduce lo state leakage tra operazioni.</p>

---

## 16. SQLite: file, memoria e connessioni

<p align="justify">Questi URL non sono equivalenti:</p>

```text
sqlite:///./feisbuc.db
sqlite:///:memory:
sqlite://
```

<p align="justify">Per dimostrare la persistenza usiamo un <strong>file temporaneo</strong> nei test:</p>

```py
database_url = f"sqlite:///{db_path.as_posix()}"
```

<p align="justify">Poi:</p>

```text
app 1 -> crea post -> dispose engine
app 2 -> stesso file -> GET -> post ancora presente
```

<p align="justify">Questo testa una proprieta che MemoryPostStore non aveva:</p>

<blockquote>
<p align="justify">il processo/applicazione puo essere ricreato senza perdere i dati.</p>
</blockquote>

### Il piccolo problema di `check_same_thread`

<p align="justify">Con SQLite + test web multithread possiamo configurare:</p>

```py
connect_args={"check_same_thread": False}
```

<p align="justify">E una scelta specifica del driver SQLite, non una regola generale di SQLAlchemy.</p>

---

## 17. Composition root: dove colleghiamo i pezzi

<p align="justify">Vogliamo una factory:</p>

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

<p align="justify">Questo rende il test indipendente dalla configurazione reale:</p>

```py
app = create_app(temp_database_url)
```

<p align="justify">Produzione/lab locale possono invece usare:</p>

```py
app = create_app("sqlite:///./feisbuc-mirror.db")
```

<p align="justify">Il composition root decide <strong>quale implementazione</strong> usare.</p>

<p align="justify">La route non decide il path del database.</p>

---

## 18. Seed idempotente

<p align="justify">Il mirror ha un post iniziale <code>seed-1</code>.</p>

<p align="justify">Se eseguiamo l'app due volte non vogliamo due copie.</p>

<p align="justify">Pattern:</p>

```py
with SessionFactory() as session:
    if session.get(PostRow, "seed-1") is None:
        session.add(PostRow(...))
        session.commit()
```

<p align="justify">Questa e una piccola forma di bootstrap idempotente.</p>

<p align="justify">Non e una migration system.</p>

<p align="justify">Serve solo a rendere riproducibile la fixture didattica.</p>

---

## 19. `create_all()` non e Alembic

<p align="justify">Nel laboratorio possiamo fare:</p>

```py
Base.metadata.create_all(engine)
```

<p align="justify">Questo crea le tabelle mancanti sulla base del metadata.</p>

<p align="justify">Ma in un prodotto reale serve gestire evoluzioni come:</p>

```text
aggiungi colonna
rinomina colonna
migra dati
crea indice senza perdere dati
rollback di release
```

<p align="justify"><code>create_all()</code> non descrive una storia di migrazioni.</p>

<p align="justify">Per ora fissiamo il boundary:</p>

```text
mirror 02 -> create_all per fixture didattica
futuro professionale -> migration tool/versioned schema
```

<p align="justify">Non introduciamo Alembic nello stesso momento dell'ORM: sarebbe un'altra nuova responsabilita.</p>

---

<a id="lesson-sqla-testing"></a>
## 20. Test del repository e test HTTP non sono duplicati

### Test repository

<p align="justify">Verifica:</p>

```text
create
list
set_liked
persistenza
```

<p align="justify">senza FastAPI.</p>

### Test HTTP

<p align="justify">Verifica:</p>

```text
status
Location
JSON shape
404
422
OpenAPI
```

<p align="justify">con <code>TestClient</code>.</p>

<p align="justify">I due livelli rispondono a domande diverse.</p>

```text
repository test -> il data layer conserva correttamente lo stato?
HTTP test       -> il client osserva ancora lo stesso contratto?
```

---

## 21. Test di restart: la prova che il nuovo slice aggiunge davvero qualcosa

<p align="justify">Un test importante:</p>

```text
1. crea database temporaneo
2. crea app A
3. POST un post
4. chiudi/dispose A
5. crea app B sullo stesso database
6. GET /api/posts
7. verifica che il post esista ancora
```

<p align="justify">Se questo test passa, abbiamo evidenza della proprieta nuova:</p>

```text
MemoryPostStore -> state legato al processo
SQLAlchemy/SQLite -> state persistente su file
```

---

## 22. Errori frequenti

### Una Session globale per tutta l'app

<p align="justify">Problema:</p>

```py
session = Session(engine)
```

<p align="justify">creata una volta e riusata indefinitamente.</p>

<p align="justify">Rischi:</p>

<ul>
  <li>state leakage;</li>
  <li>transaction boundary confuso;</li>
  <li>error recovery difficile;</li>
  <li>concorrenza/lifetime non espliciti.</li>
</ul>

### Engine dentro ogni route

<p align="justify">Problema:</p>

```py
@app.get(...)
def route():
    engine = create_engine(...)
```

<p align="justify">L'infrastruttura viene ricreata nel posto sbagliato.</p>

### `add()` senza `commit()`

<p align="justify">L'oggetto entra nella unit of work ma non abbiamo confermato la transaction.</p>

### Restituire direttamente `row.__dict__`

<p align="justify">Espone dettagli ORM come <code>_sa_instance_state</code> e rompe il boundary pubblico.</p>

### Confondere Session SQLAlchemy e sessione utente

<p align="justify">Stesso nome, responsabilita diversa.</p>

### Mettere `HTTPException` nel repository

<p align="justify">Il data layer diventerebbe dipendente da FastAPI.</p>

### Test con database condiviso involontariamente

<p align="justify">Un test crea dati che fanno fallire quello successivo.</p>

<p align="justify">Usare database temporanei/fixture isolate.</p>

---

## 23. Confronto: SQL raw UDA24 e SQLAlchemy UDA26

<table align="center">
<thead>
<tr>
<th>Problema</th>
<th>SQL raw</th>
<th>SQLAlchemy ORM</th>
</tr>
</thead>
<tbody>
<tr>
<td>schema</td>
<td>DDL esplicito</td>
<td>mapping + metadata</td>
</tr>
<tr>
<td>select</td>
<td><code>SELECT ...</code></td>
<td><code>select(PostRow)</code></td>
</tr>
<tr>
<td>bind param</td>
<td>placeholder</td>
<td>expression binding</td>
</tr>
<tr>
<td>row -> object</td>
<td>manuale</td>
<td>ORM mapping</td>
</tr>
<tr>
<td>transaction</td>
<td>API DB</td>
<td>Session/unit of work</td>
</tr>
<tr>
<td>repository</td>
<td>SQL dentro metodi</td>
<td>ORM dentro metodi</td>
</tr>
<tr>
<td>constraint DB</td>
<td>visibile nel DDL</td>
<td>dichiarato nel mapping / DB</td>
</tr>
<tr>
<td>HTTP contract</td>
<td>fuori dal repository</td>
<td>fuori dal repository</td>
</tr>
</tbody>
</table>

<p align="justify">Non stiamo sostituendo una conoscenza con l'altra.</p>

<p align="justify">Stiamo aggiungendo un secondo modo di implementare lo stesso data layer.</p>

---

## 24. Cosa non entra ancora

<p align="justify">Questo slice <strong>non</strong> introduce:</p>

<ul>
  <li>auth/session Python;</li>
  <li>utenti e password nel mirror;</li>
  <li>Socket.IO Python;</li>
  <li>frontend Python;</li>
  <li>Alembic;</li>
  <li>PostgreSQL;</li>
  <li>async SQLAlchemy;</li>
  <li>relationship complesse;</li>
  <li>ORM nel backend Node principale;</li>
  <li>deploy container/cloud.</li>
</ul>

<p align="justify">Questi temi hanno valore solo quando rispondono a un requisito reale del blocco successivo.</p>

---

## 25. Progressione A-D

### A — SQLAlchemy mapping microscope

<p align="justify">Osservare:</p>

<ul>
  <li>metadata;</li>
  <li>mapping;</li>
  <li>Engine;</li>
  <li>Session;</li>
  <li>SQL prodotto;</li>
  <li>identity/commit/select.</li>
</ul>

### B — Repository controllato

<p align="justify">Completare un piccolo <code>SqlAlchemyPostStore</code> senza FastAPI.</p>

### C — Feisbuc mirror 02

<p align="justify">Sostituire il MemoryPostStore con SQLAlchemy + SQLite mantenendo il contratto FastAPI e verificando il restart.</p>

### D — Debug transaction/session boundaries

<p align="justify">Diagnosticare:</p>

<ul>
  <li>Session globale;</li>
  <li>Engine nel posto sbagliato;</li>
  <li>commit mancante;</li>
  <li>output ORM esposto;</li>
  <li>rollback/lifetime non governato.</li>
</ul>

---

## 26. Milestone Feisbuc mirror 02

<p align="justify">Nome:</p>

```text
feisbuc-mirror-02-sqlalchemy-persistence
```

<p align="justify">Architettura:</p>

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

<p align="justify">Invarianti:</p>

<ol>
  <li>stesso contratto HTTP di mirror 01;</li>
  <li><code>PostCreate</code> non accetta identita trusted dal client;</li>
  <li>entity ORM separata dai model Pydantic;</li>
  <li>repository senza import FastAPI;</li>
  <li>Session lifetime corto e visibile;</li>
  <li>commit esplicito sulle mutazioni;</li>
  <li>seed idempotente;</li>
  <li>database configurabile dal composition root;</li>
  <li>test con file temporaneo;</li>
  <li>test di restart/persistenza;</li>
  <li>nessuna auth/realtime/deploy aggiunti prematuramente.</li>
</ol>

---

## 27. Checklist professionale

<p align="justify">Prima di considerare completo il slice:</p>

<ul>
  <li>[ ] SQLAlchemy 2.0.51 pinned;</li>
  <li>[ ] <code>DeclarativeBase</code> / <code>Mapped</code> / <code>mapped_column</code>;</li>
  <li>[ ] nessuna legacy Query API come baseline;</li>
  <li>[ ] Engine creato nel composition root;</li>
  <li>[ ] SessionFactory iniettata nel repository;</li>
  <li>[ ] repository indipendente da FastAPI;</li>
  <li>[ ] Pydantic separato dalle entity ORM;</li>
  <li>[ ] create fa commit;</li>
  <li>[ ] update fa commit;</li>
  <li>[ ] missing resource resta 404 nell'adapter;</li>
  <li>[ ] <code>201 + Location</code> resta invariato;</li>
  <li>[ ] <code>422</code> resta documentato come validation boundary del mirror;</li>
  <li>[ ] OpenAPI resta presente;</li>
  <li>[ ] persistenza verificata dopo ricreazione app;</li>
  <li>[ ] engine disposed nei test che usano file temporanei;</li>
  <li>[ ] niente auth, Socket.IO o deploy nel mirror 02.</li>
</ul>

---

## 28. Ponte al prossimo slice

<p align="justify">A questo punto abbiamo due assi di test:</p>

```text
HTTP contract test
repository/persistence test
```

<p align="justify">Il passo successivo di UDA26 non deve aggiungere un altro framework per il gusto di farlo.</p>

<p align="justify">Dobbiamo consolidare:</p>

<ul>
  <li>piramide dei test e fixture;</li>
  <li>integration/e2e boundaries;</li>
  <li>configurazione per ambienti;</li>
  <li>packaging/deploy;</li>
  <li>capstone Feisbuc con evidenze verificabili.</li>
</ul>

<p align="justify">Il punto raggiunto e importante:</p>

<blockquote>
<p align="justify">abbiamo cambiato linguaggio, framework e tecnologia di persistenza, ma il contratto osservabile e rimasto sotto controllo.</p>
</blockquote>
