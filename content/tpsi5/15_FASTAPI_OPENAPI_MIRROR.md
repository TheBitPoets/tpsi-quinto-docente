# FastAPI e OpenAPI: stesso dominio, un altro modo di esprimere la API

Stato didattico: **draft**.

## Obiettivi

Al termine del modulo lo studente sa:

- distinguere il **contratto HTTP** dal framework che lo implementa;
- leggere una path operation FastAPI e metterla in corrispondenza con una route Express;
- usare type hint Python e modelli Pydantic per descrivere input e output;
- spiegare la differenza tra **tipo Python**, **validation runtime**, **JSON Schema** e **OpenAPI**;
- osservare `/openapi.json`, `/docs` e `/redoc` come rappresentazioni del contratto esposto dall'applicazione;
- usare `response_model` e `status_code` per rendere esplicite le response;
- riconoscere quando un default del framework cambia il contratto osservabile, per esempio la response `422` di validation;
- testare una API FastAPI senza aprire una porta TCP usando `TestClient`;
- costruire un piccolo mirror della risorsa `posts` senza riscrivere l'intero Feisbuc in Python;
- mantenere SQLAlchemy, auth e deployment separati finche il relativo problema non viene introdotto.

## Prerequisiti

- UDA23: HTTP, status code, header, JSON e REST;
- UDA24: Express Router, validation, store boundary e SQLite;
- UDA25: TypeScript boundary typing e runtime validation;
- Python di base: funzioni, classi semplici, liste/dizionari, type hint essenziali.

## Problema iniziale

Abbiamo gia una API Feisbuc in Express.

Una parte del suo contratto e riconoscibile senza sapere in quale linguaggio sia implementata:

```text
GET   /api/posts
POST  /api/posts
PATCH /api/posts/:id
```

Il client osserva:

```text
method + URL + request body + status + header + JSON response
```

Non osserva direttamente:

```text
Express Router
Pydantic
funzione Python
middleware JavaScript
classe del repository
```

La domanda di UDA26 e quindi:

> se cambiamo implementazione da Express/JavaScript a FastAPI/Python, quali parti del contratto possono restare uguali e quali differenze dobbiamo governare consapevolmente?

Questo e un **mirror track**, non una migrazione del prodotto principale.

---

## 1. Il contratto viene prima del framework

Pensiamo a questa response:

```http
HTTP/1.1 201 Created
Location: /api/posts/p42
Content-Type: application/json

{
  "id": "p42",
  "text": "ciao",
  "liked": false,
  "likes": 0
}
```

Possiamo produrla con Express, FastAPI o un server scritto a mano.

Il contratto osservabile e indipendente dal framework.

Schema mentale:

```text
client
  |
  | HTTP contract
  v
framework adapter
  |
  | domain/store calls
  v
state
```

Il framework e un **adapter** che traduce HTTP in chiamate applicative e ritorno applicativo in HTTP.

---

## 2. Una prima route Express e FastAPI

Express:

```js
router.get("/", async (req, res) => {
  const posts = await postStore.list();
  res.json(posts);
});
```

FastAPI:

```py
from fastapi import FastAPI

app = FastAPI()

@app.get("/api/posts")
def list_posts():
    return post_store.list()
```

La sintassi cambia, ma il problema e lo stesso:

```text
GET /api/posts
     ↓
route matching
     ↓
funzione applicativa
     ↓
lista Post
     ↓
JSON 200
```

Il decoratore `@app.get(...)` non e "la API": e il modo con cui FastAPI registra una path operation.

---

## 3. ASGI e Uvicorn: chi ascolta davvero la rete?

FastAPI costruisce una applicazione **ASGI**.

Per ascoltare una porta possiamo usare un server ASGI come Uvicorn:

```bash
uvicorn app:app --reload
```

Separiamo i ruoli:

```text
Uvicorn
  ↓ riceve HTTP sulla rete
FastAPI
  ↓ routing / validation / response
funzioni dominio/store
```

E analogo al principio gia visto con Node:

```text
HTTP server
  ↓
Express app
```

Non confondere quindi:

```text
FastAPI = server di rete completo
```

con:

```text
FastAPI = applicazione/framework ASGI eseguita da un server ASGI
```

### Baseline riproducibile 2026/27

Il primo mirror pinna:

```text
Python    3.11 / 3.12 CI
FastAPI   0.141.1
Pydantic  2.13.4
Uvicorn   0.52.1
HTTPX     0.28.1
```

SQLAlchemy **non entra ancora** in questo blocco.

---

## 4. Request model: type hint non significa solo editor

Con Pydantic possiamo dichiarare un command HTTP:

```py
from pydantic import BaseModel, Field, field_validator

class PostCreate(BaseModel):
    text: str = Field(min_length=1, max_length=280)

    @field_validator("text", mode="before")
    @classmethod
    def normalize_text(cls, value):
        if isinstance(value, str):
            return value.strip()
        return value
```

Poi:

```py
@app.post("/api/posts")
def create_post(command: PostCreate):
    return {"text": command.text}
```

Qui succedono piu cose contemporaneamente:

```text
JSON remoto
   ↓
parsing
   ↓
validation runtime Pydantic
   ↓
PostCreate Python affidabile per quella regola
```

Questo richiama TypeScript UDA25:

```text
TypeScript:
JSON -> unknown -> runtime parser -> Post

FastAPI/Pydantic:
JSON -> Pydantic validation -> PostCreate
```

In entrambi i casi il punto importante e:

> il dato di rete non diventa affidabile perche abbiamo scritto un tipo; serve una verifica runtime.

---

## 5. Input model e output model non sono la stessa cosa

Un client che crea un post deve poter inviare:

```json
{
  "text": "ciao"
}
```

Non deve decidere:

```text
id
authorId
likes
createdAt
```

Quindi separiamo:

```py
class PostCreate(BaseModel):
    text: str

class Post(BaseModel):
    id: str
    text: str
    authorId: str
    author: str
    liked: bool
    likes: int
```

Questo e lo stesso principio usato nel backend Express:

```text
command input != entity/output
```

E soprattutto impedisce un errore gia studiato:

```json
{
  "text": "post",
  "authorId": "utente-che-voglio-impersonare"
}
```

Se `authorId` non appartiene al request model, non diventa automaticamente identita affidabile.

Nel primo mirror non replichiamo ancora la sessione Feisbuc: usiamo un autore fixture del mirror e dichiariamo questo limite invece di inventare una seconda autenticazione.

---

## 6. response_model: l'output e un boundary

FastAPI permette di dichiarare il modello pubblico:

```py
@app.get("/api/posts", response_model=list[Post])
def list_posts():
    return post_store.list()
```

`response_model` rende esplicito il boundary di output.

Se internamente avessimo:

```py
{
  "id": "p1",
  "text": "ciao",
  "internal_secret": "NON PUBBLICARE"
}
```

il modello pubblico non dovrebbe includere `internal_secret`.

Regola:

> la shape interna del programma e la representation HTTP pubblica non devono coincidere per accidente.

---

## 7. status_code e header non vanno dimenticati

Una POST che crea una risorsa non dovrebbe diventare `200` solo perche il framework lo usa come default.

```py
from fastapi import Response, status

@app.post(
    "/api/posts",
    response_model=Post,
    status_code=status.HTTP_201_CREATED,
)
def create_post(command: PostCreate, response: Response):
    post = post_store.create(command.text)
    response.headers["Location"] = f"/api/posts/{post['id']}"
    return post
```

Il framework non sostituisce HTTP.

Dobbiamo ancora ragionare su:

- 200 vs 201;
- 404;
- Location;
- representation;
- idempotenza;
- error semantics.

---

## 8. HTTPException e l'errore osservabile

FastAPI fornisce `HTTPException`:

```py
from fastapi import HTTPException

post = post_store.find(post_id)
if post is None:
    raise HTTPException(status_code=404, detail="post-not-found")
```

Questo e comodo, ma attenzione:

```json
{
  "detail": "post-not-found"
}
```

non e necessariamente lo stesso error envelope che avevamo progettato in Express.

Possiamo scegliere due strategie:

1. accettare consapevolmente una differenza nel mirror didattico;
2. introdurre un exception handler per mantenere esattamente lo stesso envelope.

La scelta corretta dipende dal requisito.

Nel **primo slice UDA26** preserviamo con precisione:

- route principali;
- request fields del dominio;
- success status;
- `Location` sulla create;
- public `Post` shape;
- 404 come categoria HTTP.

Documentiamo invece la validation `422` di Pydantic/FastAPI come differenza osservabile da confrontare, non da nascondere.

---

## 9. Il caso 422: un framework puo cambiare il contratto

Con un body invalido:

```json
{
  "text": ""
}
```

FastAPI/Pydantic normalmente produce una response di validation `422`.

Il vecchio backend potrebbe avere usato un `400` personalizzato.

Questa differenza e didatticamente preziosa:

```text
stesso requisito di dominio
        ↓
framework default diverso
        ↓
contratto HTTP osservabile diverso
```

Domanda professionale:

> il client tollera questa differenza oppure dobbiamo adattare il framework al contratto esistente?

Non modificare uno status code solo per "far contento il test". Prima capire quale contratto vogliamo mantenere.

---

## 10. OpenAPI: il contratto diventa una risorsa interrogabile

FastAPI genera uno schema OpenAPI a partire dalle path operation e dai modelli.

Endpoint predefinito:

```text
/openapi.json
```

Interfacce predefinite:

```text
/docs   -> Swagger UI
/redoc  -> ReDoc
```

La catena e:

```text
Python annotations + Pydantic models + path metadata
                ↓
             OpenAPI
                ↓
        documentazione / tooling
```

OpenAPI non sostituisce i test.

Uno schema puo dire che esiste una response `201`; dobbiamo comunque verificare che il codice la produca davvero.

---

## 11. Leggere `/openapi.json` come sviluppatori

Non limitarsi a guardare Swagger.

Nel JSON cerchiamo:

```text
paths
  /api/posts
    get
    post
components
  schemas
    Post
    PostCreate
```

Domande:

1. quali metodi sono dichiarati?
2. quali status sono documentati?
3. quale schema entra nella POST?
4. quale schema esce?
5. quali campi risultano required?
6. compare una response di validation?

Questo collega la documentazione professionale al codice reale.

---

## 12. TestClient: testare HTTP senza una porta reale

Per test deterministici possiamo usare:

```py
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

response = client.get("/api/posts")
assert response.status_code == 200
```

`TestClient` usa HTTPX e permette di osservare la app come client HTTP senza lanciare Uvicorn su una porta.

Possiamo verificare:

```py
response = client.post("/api/posts", json={"text": "ciao"})
assert response.status_code == 201
assert response.headers["location"].startswith("/api/posts/")
```

E anche OpenAPI:

```py
schema = client.get("/openapi.json").json()
assert "/api/posts" in schema["paths"]
```

Questo e un ottimo ponte verso il blocco testing di UDA26.

---

## 13. Store boundary: non leghiamo FastAPI alla persistenza

Anche nel mirror manteniamo una separazione:

```text
FastAPI route
    ↓
PostStore
    ↓
MemoryPostStore  (questo slice)
```

Successivamente:

```text
FastAPI route
    ↓
PostStore / repository
    ↓
SQLAlchemy
    ↓
SQLite
```

Questa sequenza e intenzionale.

Prima impariamo:

```text
HTTP + Pydantic + OpenAPI + TestClient
```

Poi aggiungiamo:

```text
ORM + mapping + transaction/persistence
```

Altrimenti quando qualcosa non funziona non sappiamo se il problema e routing, schema, ORM o SQL.

---

## 14. Mirror non significa duplicazione totale

Feisbuc principale resta:

```text
Vue -> Express -> SQLite -> session/auth -> Socket.IO
```

Il mirror Python iniziale e:

```text
TestClient / client HTTP
        ↓
FastAPI
        ↓
Pydantic
        ↓
MemoryPostStore
```

Obiettivo:

> dimostrare che un contratto HTTP e un modello di dominio possono attraversare stack differenti.

Non stiamo ancora duplicando:

- password hashing;
- session table;
- cookie HttpOnly;
- authorization ownership;
- Socket.IO;
- frontend Vue;
- SQLAlchemy.

Se provassimo a replicare tutto subito, il mirror diventerebbe un secondo corso backend completo.

---

## 15. Confronto Express ↔ FastAPI

| Concetto | Express | FastAPI |
| --- | --- | --- |
| registrare GET | `router.get(...)` | `@app.get(...)` |
| path param | `req.params.id` | parametro funzione tipizzato |
| body | `req.body` + validation | model Pydantic |
| status create | `res.status(201)` | `status_code=201` |
| output contract | codice/rubrica/validatori | `response_model` + test |
| error HTTP | `HttpError` + middleware | `HTTPException` / handler |
| docs contratto | scritte a parte | OpenAPI generato |
| test HTTP | server live/supertest-like | `TestClient` |

Nessuna colonna significa "migliore in assoluto".

Il punto e vedere quali responsabilita esistono in entrambi gli stack.

---

## 16. Errori frequenti

### Confondere type hint con sicurezza del dato

Il type hint Python guida tooling e framework; e la validation runtime a verificare l'input.

### Usare un solo model per input e output

Rischia di rendere scrivibili campi che appartengono al server.

### Accettare tutti i default HTTP senza guardarli

`200` al posto di `201` o `422` al posto di un precedente `400` sono cambiamenti di contratto.

### Restituire direttamente oggetti interni

Puoi esporre campi che non appartengono alla representation pubblica.

### Aggiungere SQLAlchemy subito

Nasconde il confine fra framework HTTP e persistenza.

### Riscrivere tutto Feisbuc in Python

Distrugge il valore comparativo del mirror e consuma il tempo di testing/deploy/capstone.

---

## 17. Debugging FastAPI

Strumenti:

- `/docs`;
- `/openapi.json`;
- `TestClient`;
- traceback pytest;
- log Uvicorn quando si usa il server reale;
- confronto request/response con Express.

Checklist:

1. la route e registrata?
2. il path e il method sono corretti?
3. il body entra nel modello previsto?
4. la validation fallisce prima della funzione?
5. lo status e esplicito?
6. `response_model` corrisponde alla representation?
7. OpenAPI documenta quello che crediamo?
8. il test osserva HTTP, non dettagli interni?

---

## 18. Esercizi A-F

### A — osservazione

Eseguire il microscope FastAPI e confrontare route, `/docs`, `/openapi.json`, request model e validation 422.

### B — modifica controllata

Implementare in Python puro la stessa policy di normalizzazione del testo post (`trim`, required, max 280) con input/output deterministico.

### C — scrittura autonoma

Costruire il mirror FastAPI di `GET/POST/PATCH /api/posts` con `PostCreate`, `PostLikePatch`, `Post`, `response_model`, status e MemoryPostStore.

### D — debugging

Diagnosticare un backend che usa `dict` indiscriminati, risponde 200 alla create, si fida di `authorId`, perde il 404 e pubblica campi interni.

### E — estensione

Confrontare lo schema OpenAPI generato con il contratto Express e redigere una compatibility matrix.

### F — integrazione futura

Portare il mirror su SQLAlchemy mantenendo invariata la suite HTTP del blocco C.

---

## 19. Laboratorio mirror FastAPI

Definition of Done del primo slice UDA26:

- FastAPI/Pydantic/Uvicorn/HTTPX pinned;
- `GET /api/posts` restituisce una lista di Post pubblici;
- `POST /api/posts` usa `PostCreate`, normalizza il testo e restituisce `201`;
- la POST espone `Location`;
- `PATCH /api/posts/{id}` aggiorna `liked`;
- id inesistente produce `404`;
- `authorId` non viene accettato come identita affidabile dal command model;
- `response_model` definisce la shape pubblica;
- `/openapi.json` descrive GET/POST/PATCH;
- TestClient verifica il contratto senza server TCP;
- invalid input Pydantic viene osservato come `422` e documentato come differenza rispetto ad altri adapter;
- nessun SQLAlchemy, auth/session o realtime nel primo mirror.

---

## 20. Verifica rapida

1. Perche FastAPI non sostituisce HTTP?
2. Che differenza c'e tra `PostCreate` e `Post`?
3. Perche un type hint non basta per fidarsi del JSON?
4. Che cosa genera `/openapi.json`?
5. Perche `response_model` e un boundary?
6. Che cosa dimostra `TestClient`?
7. Perche `422` puo essere una compatibility decision?
8. Perche SQLAlchemy e rinviato al blocco successivo?

---

## Sintesi inclusiva

```text
CONTRATTO HTTP
method + path + body + status + headers + JSON
             |
             v
FASTAPI ADAPTER
route + Pydantic + response_model
             |
             v
DOMINIO / STORE
prima memory, poi SQLAlchemy
```

Concetto chiave:

> cambiare framework non deve obbligarci a dimenticare il contratto che il client osserva.

FastAPI rende particolarmente visibili i contratti tramite Pydantic, JSON Schema e OpenAPI, ma proprio per questo dobbiamo imparare a distinguere cio che il framework genera automaticamente dalle decisioni applicative che restano nostre.

## Fonti professionali da leggere

- FastAPI official documentation: first steps, request body, response model, testing e OpenAPI;
- OpenAPI/JSON Schema come standard esposto tramite `/openapi.json`;
- Pydantic documentation per model/field validation;
- HTTPX/TestClient per i test HTTP in-process;
- RFC 9110 per status e semantica HTTP gia studiati;
- Express reference del corso per il confronto adapter-to-adapter.

Le fonti servono per imparare a ricostruire il comportamento del framework dalla documentazione, non per copiare ricette senza comprendere il contratto.