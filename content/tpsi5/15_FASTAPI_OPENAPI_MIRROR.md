# FastAPI e OpenAPI: stesso dominio, un altro modo di esprimere la API

<table align="center" width="100%"><tr><td>
<details>
<summary>&#128506; <strong>Orientamento della lezione</strong></summary>

<p align="justify"><strong>Contesto:</strong> il contratto Feisbuc è già stato implementato in Express. Il mirror Python serve a distinguere ciò che appartiene a HTTP e al dominio da ciò che appartiene al framework.</p>
<p align="justify"><strong>Domande guida:</strong> come diventano i type hint validation e schema? Che rapporto c'è fra path operation e OpenAPI? Quali differenze di default possono cambiare il contratto osservabile?</p>
<p align="justify"><strong>Obiettivi osservabili:</strong> modellare input e output separati, dichiarare status ed errori, leggere <code>/openapi.json</code>, testare con <code>TestClient</code> e confrontare una route FastAPI con Express.</p>
<p align="justify"><strong>Prossimo passo:</strong> la lezione 16 sostituirà lo store in memoria del mirror con SQLAlchemy e SQLite.</p>

</details>
</td></tr></table>

<p align="justify">Stato didattico: <strong>draft</strong>.</p>

## Obiettivi

<p align="justify">Al termine del modulo lo studente sa:</p>

<ul>
  <li>distinguere il <strong>contratto HTTP</strong> dal framework che lo implementa;</li>
  <li>leggere una path operation FastAPI e metterla in corrispondenza con una route Express;</li>
  <li>usare type hint Python e modelli Pydantic per descrivere input e output;</li>
  <li>spiegare la differenza tra <strong>tipo Python</strong>, <strong>validation runtime</strong>, <strong>JSON Schema</strong> e <strong>OpenAPI</strong>;</li>
  <li>osservare <code>/openapi.json</code>, <code>/docs</code> e <code>/redoc</code> come rappresentazioni del contratto esposto dall'applicazione;</li>
  <li>usare <code>response_model</code> e <code>status_code</code> per rendere esplicite le response;</li>
  <li>riconoscere quando un default del framework cambia il contratto osservabile, per esempio la response <code>422</code> di validation;</li>
  <li>testare una API FastAPI senza aprire una porta TCP usando <code>TestClient</code>;</li>
  <li>costruire un piccolo mirror della risorsa <code>posts</code> senza riscrivere l'intero Feisbuc in Python;</li>
  <li>mantenere SQLAlchemy, auth e deployment separati finche il relativo problema non viene introdotto.</li>
</ul>

## Prerequisiti

<ul>
  <li>UDA23: HTTP, status code, header, JSON e REST;</li>
  <li>UDA24: Express Router, validation, store boundary e SQLite;</li>
  <li>UDA25: TypeScript boundary typing e runtime validation;</li>
  <li>Python di base: funzioni, classi semplici, liste/dizionari, type hint essenziali.</li>
</ul>

## Orientamento nella documentazione

<p align="center">
  <img src="../../assets/tpsi5/lesson-documentation-depth.svg" alt="La dispensa seleziona nelle fonti ufficiali i contenuti da studiare ora, riconoscere, rimandare o dichiarare fuori confine">
</p>

<table align="center"><tr><td>
<details>
<summary>&#128279; <strong>Indice incrociato — FastAPI, Pydantic e OpenAPI</strong></summary>

<table align="center">
<thead><tr><th>Dispensa</th><th>Documentazione ufficiale</th><th>Profondità</th></tr></thead>
<tbody>
<tr><td><a href="#lesson-fastapi-contract">Path operation e contratto HTTP</a></td><td><a href="https://fastapi.tiangolo.com/tutorial/first-steps/">FastAPI — First Steps</a><br><a href="https://fastapi.tiangolo.com/tutorial/response-status-code/">Response Status Code</a></td><td>&#128994; studiare ora</td></tr>
<tr><td><a href="#lesson-fastapi-models">Input, output e <code>response_model</code></a></td><td><a href="https://fastapi.tiangolo.com/tutorial/body/">Request Body</a><br><a href="https://fastapi.tiangolo.com/tutorial/response-model/">Response Model</a></td><td>&#128994; studiare ora</td></tr>
<tr><td><a href="#lesson-fastapi-openapi">OpenAPI e documentazione generata</a></td><td><a href="https://fastapi.tiangolo.com/tutorial/first-steps/#openapi">FastAPI — OpenAPI</a><br><a href="https://spec.openapis.org/oas/latest.html">OpenAPI Specification</a></td><td>&#128994; schema generato; specifica da riconoscere</td></tr>
<tr><td><a href="#lesson-fastapi-testing">TestClient</a></td><td><a href="https://fastapi.tiangolo.com/tutorial/testing/">FastAPI — Testing</a></td><td>&#128994; studiare ora</td></tr>
<tr><td>Dependency system avanzato, async DB e security framework</td><td><a href="https://fastapi.tiangolo.com/advanced/">FastAPI — Advanced User Guide</a></td><td>&#128993; più avanti o fuori dal mirror</td></tr>
</tbody>
</table>

</details>
</td></tr></table>

## Problema iniziale

<p align="justify">Abbiamo gia una API Feisbuc in Express.</p>

<p align="justify">Una parte del suo contratto e riconoscibile senza sapere in quale linguaggio sia implementata:</p>

```text
GET   /api/posts
POST  /api/posts
PATCH /api/posts/:id
```

<p align="justify">Il client osserva:</p>

```text
method + URL + request body + status + header + JSON response
```

<p align="justify">Non osserva direttamente:</p>

```text
Express Router
Pydantic
funzione Python
middleware JavaScript
classe del repository
```

<p align="justify">La domanda di UDA26 e quindi:</p>

<blockquote>
<p align="justify">se cambiamo implementazione da Express/JavaScript a FastAPI/Python, quali parti del contratto possono restare uguali e quali differenze dobbiamo governare consapevolmente?</p>
</blockquote>

<p align="justify">Questo e un <strong>mirror track</strong>, non una migrazione del prodotto principale.</p>

---

<a id="lesson-fastapi-contract"></a>
## 1. Il contratto viene prima del framework

<p align="justify">Pensiamo a questa response:</p>

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

<p align="justify">Possiamo produrla con Express, FastAPI o un server scritto a mano.</p>

<p align="justify">Il contratto osservabile e indipendente dal framework.</p>

<p align="justify">Schema mentale:</p>

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

<p align="justify">Il framework e un <strong>adapter</strong> che traduce HTTP in chiamate applicative e ritorno applicativo in HTTP.</p>

---

## 2. Una prima route Express e FastAPI

<p align="justify">Express:</p>

```js
router.get("/", async (req, res) => {
  const posts = await postStore.list();
  res.json(posts);
});
```

<p align="justify">FastAPI:</p>

```py
from fastapi import FastAPI

app = FastAPI()

@app.get("/api/posts")
def list_posts():
    return post_store.list()
```

<p align="justify">La sintassi cambia, ma il problema e lo stesso:</p>

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

<p align="justify">Il decoratore <code>@app.get(...)</code> non e "la API": e il modo con cui FastAPI registra una path operation.</p>

---

## 3. ASGI e Uvicorn: chi ascolta davvero la rete?

<p align="justify">FastAPI costruisce una applicazione <strong>ASGI</strong>.</p>

<p align="justify">Per ascoltare una porta possiamo usare un server ASGI come Uvicorn:</p>

```bash
uvicorn app:app --reload
```

<p align="justify">Separiamo i ruoli:</p>

```text
Uvicorn
  ↓ riceve HTTP sulla rete
FastAPI
  ↓ routing / validation / response
funzioni dominio/store
```

<p align="justify">E analogo al principio gia visto con Node:</p>

```text
HTTP server
  ↓
Express app
```

<p align="justify">Non confondere quindi:</p>

```text
FastAPI = server di rete completo
```

<p align="justify">con:</p>

```text
FastAPI = applicazione/framework ASGI eseguita da un server ASGI
```

### Baseline riproducibile 2026/27

<p align="justify">Il primo mirror pinna:</p>

```text
Python    3.11 / 3.12 CI
FastAPI   0.141.1
Pydantic  2.13.4
Uvicorn   0.52.1
HTTPX     0.28.1
```

<p align="justify">SQLAlchemy <strong>non entra ancora</strong> in questo blocco.</p>

---

<a id="lesson-fastapi-models"></a>
## 4. Request model: type hint non significa solo editor

<p align="justify">Con Pydantic possiamo dichiarare un command HTTP:</p>

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

<p align="justify">Poi:</p>

```py
@app.post("/api/posts")
def create_post(command: PostCreate):
    return {"text": command.text}
```

<p align="justify">Qui succedono piu cose contemporaneamente:</p>

```text
JSON remoto
   ↓
parsing
   ↓
validation runtime Pydantic
   ↓
PostCreate Python affidabile per quella regola
```

<p align="justify">Questo richiama TypeScript UDA25:</p>

```text
TypeScript:
JSON -> unknown -> runtime parser -> Post

FastAPI/Pydantic:
JSON -> Pydantic validation -> PostCreate
```

<p align="justify">In entrambi i casi il punto importante e:</p>

<blockquote>
<p align="justify">il dato di rete non diventa affidabile perche abbiamo scritto un tipo; serve una verifica runtime.</p>
</blockquote>

---

## 5. Input model e output model non sono la stessa cosa

<p align="justify">Un client che crea un post deve poter inviare:</p>

```json
{
  "text": "ciao"
}
```

<p align="justify">Non deve decidere:</p>

```text
id
authorId
likes
createdAt
```

<p align="justify">Quindi separiamo:</p>

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

<p align="justify">Questo e lo stesso principio usato nel backend Express:</p>

```text
command input != entity/output
```

<p align="justify">E soprattutto impedisce un errore gia studiato:</p>

```json
{
  "text": "post",
  "authorId": "utente-che-voglio-impersonare"
}
```

<p align="justify">Se <code>authorId</code> non appartiene al request model, non diventa automaticamente identita affidabile.</p>

<p align="justify">Nel primo mirror non replichiamo ancora la sessione Feisbuc: usiamo un autore fixture del mirror e dichiariamo questo limite invece di inventare una seconda autenticazione.</p>

---

## 6. response_model: l'output e un boundary

<p align="justify">FastAPI permette di dichiarare il modello pubblico:</p>

```py
@app.get("/api/posts", response_model=list[Post])
def list_posts():
    return post_store.list()
```

<p align="justify"><code>response_model</code> rende esplicito il boundary di output.</p>

<p align="justify">Se internamente avessimo:</p>

```py
{
  "id": "p1",
  "text": "ciao",
  "internal_secret": "NON PUBBLICARE"
}
```

<p align="justify">il modello pubblico non dovrebbe includere <code>internal_secret</code>.</p>

<p align="justify">Regola:</p>

<blockquote>
<p align="justify">la shape interna del programma e la representation HTTP pubblica non devono coincidere per accidente.</p>
</blockquote>

---

## 7. status_code e header non vanno dimenticati

<p align="justify">Una POST che crea una risorsa non dovrebbe diventare <code>200</code> solo perche il framework lo usa come default.</p>

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

<p align="justify">Il framework non sostituisce HTTP.</p>

<p align="justify">Dobbiamo ancora ragionare su:</p>

<ul>
  <li>200 vs 201;</li>
  <li>404;</li>
  <li>Location;</li>
  <li>representation;</li>
  <li>idempotenza;</li>
  <li>error semantics.</li>
</ul>

---

## 8. HTTPException e l'errore osservabile

<p align="justify">FastAPI fornisce <code>HTTPException</code>:</p>

```py
from fastapi import HTTPException

post = post_store.find(post_id)
if post is None:
    raise HTTPException(status_code=404, detail="post-not-found")
```

<p align="justify">Questo e comodo, ma attenzione:</p>

```json
{
  "detail": "post-not-found"
}
```

<p align="justify">non e necessariamente lo stesso error envelope che avevamo progettato in Express.</p>

<p align="justify">Possiamo scegliere due strategie:</p>

<ol>
  <li>accettare consapevolmente una differenza nel mirror didattico;</li>
  <li>introdurre un exception handler per mantenere esattamente lo stesso envelope.</li>
</ol>

<p align="justify">La scelta corretta dipende dal requisito.</p>

<p align="justify">Nel <strong>primo slice UDA26</strong> preserviamo con precisione:</p>

<ul>
  <li>route principali;</li>
  <li>request fields del dominio;</li>
  <li>success status;</li>
  <li><code>Location</code> sulla create;</li>
  <li>public <code>Post</code> shape;</li>
  <li>404 come categoria HTTP.</li>
</ul>

<p align="justify">Documentiamo invece la validation <code>422</code> di Pydantic/FastAPI come differenza osservabile da confrontare, non da nascondere.</p>

---

## 9. Il caso 422: un framework puo cambiare il contratto

<p align="justify">Con un body invalido:</p>

```json
{
  "text": ""
}
```

<p align="justify">FastAPI/Pydantic normalmente produce una response di validation <code>422</code>.</p>

<p align="justify">Il vecchio backend potrebbe avere usato un <code>400</code> personalizzato.</p>

<p align="justify">Questa differenza e didatticamente preziosa:</p>

```text
stesso requisito di dominio
        ↓
framework default diverso
        ↓
contratto HTTP osservabile diverso
```

<p align="justify">Domanda professionale:</p>

<blockquote>
<p align="justify">il client tollera questa differenza oppure dobbiamo adattare il framework al contratto esistente?</p>
</blockquote>

<p align="justify">Non modificare uno status code solo per "far contento il test". Prima capire quale contratto vogliamo mantenere.</p>

---

<a id="lesson-fastapi-openapi"></a>
## 10. OpenAPI: il contratto diventa una risorsa interrogabile

<p align="justify">FastAPI genera uno schema OpenAPI a partire dalle path operation e dai modelli.</p>

<p align="justify">Endpoint predefinito:</p>

```text
/openapi.json
```

<p align="justify">Interfacce predefinite:</p>

```text
/docs   -> Swagger UI
/redoc  -> ReDoc
```

<p align="justify">La catena e:</p>

```text
Python annotations + Pydantic models + path metadata
                ↓
             OpenAPI
                ↓
        documentazione / tooling
```

<p align="justify">OpenAPI non sostituisce i test.</p>

<p align="justify">Uno schema puo dire che esiste una response <code>201</code>; dobbiamo comunque verificare che il codice la produca davvero.</p>

---

## 11. Leggere `/openapi.json` come sviluppatori

<p align="justify">Non limitarsi a guardare Swagger.</p>

<p align="justify">Nel JSON cerchiamo:</p>

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

<p align="justify">Domande:</p>

<ol>
  <li>quali metodi sono dichiarati?</li>
  <li>quali status sono documentati?</li>
  <li>quale schema entra nella POST?</li>
  <li>quale schema esce?</li>
  <li>quali campi risultano required?</li>
  <li>compare una response di validation?</li>
</ol>

<p align="justify">Questo collega la documentazione professionale al codice reale.</p>

---

<a id="lesson-fastapi-testing"></a>
## 12. TestClient: testare HTTP senza una porta reale

<p align="justify">Per test deterministici possiamo usare:</p>

```py
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

response = client.get("/api/posts")
assert response.status_code == 200
```

<p align="justify"><code>TestClient</code> usa HTTPX e permette di osservare la app come client HTTP senza lanciare Uvicorn su una porta.</p>

<p align="justify">Possiamo verificare:</p>

```py
response = client.post("/api/posts", json={"text": "ciao"})
assert response.status_code == 201
assert response.headers["location"].startswith("/api/posts/")
```

<p align="justify">E anche OpenAPI:</p>

```py
schema = client.get("/openapi.json").json()
assert "/api/posts" in schema["paths"]
```

<p align="justify">Questo e un ottimo ponte verso il blocco testing di UDA26.</p>

---

## 13. Store boundary: non leghiamo FastAPI alla persistenza

<p align="justify">Anche nel mirror manteniamo una separazione:</p>

```text
FastAPI route
    ↓
PostStore
    ↓
MemoryPostStore  (questo slice)
```

<p align="justify">Successivamente:</p>

```text
FastAPI route
    ↓
PostStore / repository
    ↓
SQLAlchemy
    ↓
SQLite
```

<p align="justify">Questa sequenza e intenzionale.</p>

<p align="justify">Prima impariamo:</p>

```text
HTTP + Pydantic + OpenAPI + TestClient
```

<p align="justify">Poi aggiungiamo:</p>

```text
ORM + mapping + transaction/persistence
```

<p align="justify">Altrimenti quando qualcosa non funziona non sappiamo se il problema e routing, schema, ORM o SQL.</p>

---

## 14. Mirror non significa duplicazione totale

<p align="justify">Feisbuc principale resta:</p>

```text
Vue -> Express -> SQLite -> session/auth -> Socket.IO
```

<p align="justify">Il mirror Python iniziale e:</p>

```text
TestClient / client HTTP
        ↓
FastAPI
        ↓
Pydantic
        ↓
MemoryPostStore
```

<p align="justify">Obiettivo:</p>

<blockquote>
<p align="justify">dimostrare che un contratto HTTP e un modello di dominio possono attraversare stack differenti.</p>
</blockquote>

<p align="justify">Non stiamo ancora duplicando:</p>

<ul>
  <li>password hashing;</li>
  <li>session table;</li>
  <li>cookie HttpOnly;</li>
  <li>authorization ownership;</li>
  <li>Socket.IO;</li>
  <li>frontend Vue;</li>
  <li>SQLAlchemy.</li>
</ul>

<p align="justify">Se provassimo a replicare tutto subito, il mirror diventerebbe un secondo corso backend completo.</p>

---

## 15. Confronto Express ↔ FastAPI

<table align="center">
<thead>
<tr>
<th>Concetto</th>
<th>Express</th>
<th>FastAPI</th>
</tr>
</thead>
<tbody>
<tr>
<td>registrare GET</td>
<td><code>router.get(...)</code></td>
<td><code>@app.get(...)</code></td>
</tr>
<tr>
<td>path param</td>
<td><code>req.params.id</code></td>
<td>parametro funzione tipizzato</td>
</tr>
<tr>
<td>body</td>
<td><code>req.body</code> + validation</td>
<td>model Pydantic</td>
</tr>
<tr>
<td>status create</td>
<td><code>res.status(201)</code></td>
<td><code>status_code=201</code></td>
</tr>
<tr>
<td>output contract</td>
<td>codice/rubrica/validatori</td>
<td><code>response_model</code> + test</td>
</tr>
<tr>
<td>error HTTP</td>
<td><code>HttpError</code> + middleware</td>
<td><code>HTTPException</code> / handler</td>
</tr>
<tr>
<td>docs contratto</td>
<td>scritte a parte</td>
<td>OpenAPI generato</td>
</tr>
<tr>
<td>test HTTP</td>
<td>server live/supertest-like</td>
<td><code>TestClient</code></td>
</tr>
</tbody>
</table>

<p align="justify">Nessuna colonna significa "migliore in assoluto".</p>

<p align="justify">Il punto e vedere quali responsabilita esistono in entrambi gli stack.</p>

---

## 16. Errori frequenti

### Confondere type hint con sicurezza del dato

<p align="justify">Il type hint Python guida tooling e framework; e la validation runtime a verificare l'input.</p>

### Usare un solo model per input e output

<p align="justify">Rischia di rendere scrivibili campi che appartengono al server.</p>

### Accettare tutti i default HTTP senza guardarli

<p align="justify"><code>200</code> al posto di <code>201</code> o <code>422</code> al posto di un precedente <code>400</code> sono cambiamenti di contratto.</p>

### Restituire direttamente oggetti interni

<p align="justify">Puoi esporre campi che non appartengono alla representation pubblica.</p>

### Aggiungere SQLAlchemy subito

<p align="justify">Nasconde il confine fra framework HTTP e persistenza.</p>

### Riscrivere tutto Feisbuc in Python

<p align="justify">Distrugge il valore comparativo del mirror e consuma il tempo di testing/deploy/capstone.</p>

---

## 17. Debugging FastAPI

<p align="justify">Strumenti:</p>

<ul>
  <li><code>/docs</code>;</li>
  <li><code>/openapi.json</code>;</li>
  <li><code>TestClient</code>;</li>
  <li>traceback pytest;</li>
  <li>log Uvicorn quando si usa il server reale;</li>
  <li>confronto request/response con Express.</li>
</ul>

<p align="justify">Checklist:</p>

<ol>
  <li>la route e registrata?</li>
  <li>il path e il method sono corretti?</li>
  <li>il body entra nel modello previsto?</li>
  <li>la validation fallisce prima della funzione?</li>
  <li>lo status e esplicito?</li>
  <li><code>response_model</code> corrisponde alla representation?</li>
  <li>OpenAPI documenta quello che crediamo?</li>
  <li>il test osserva HTTP, non dettagli interni?</li>
</ol>

---

## 18. Esercizi A-F

### A — osservazione

<p align="justify">Eseguire il microscope FastAPI e confrontare route, <code>/docs</code>, <code>/openapi.json</code>, request model e validation 422.</p>

### B — modifica controllata

<p align="justify">Implementare in Python puro la stessa policy di normalizzazione del testo post (<code>trim</code>, required, max 280) con input/output deterministico.</p>

### C — scrittura autonoma

<p align="justify">Costruire il mirror FastAPI di <code>GET/POST/PATCH /api/posts</code> con <code>PostCreate</code>, <code>PostLikePatch</code>, <code>Post</code>, <code>response_model</code>, status e MemoryPostStore.</p>

### D — debugging

<p align="justify">Diagnosticare un backend che usa <code>dict</code> indiscriminati, risponde 200 alla create, si fida di <code>authorId</code>, perde il 404 e pubblica campi interni.</p>

### E — estensione

<p align="justify">Confrontare lo schema OpenAPI generato con il contratto Express e redigere una compatibility matrix.</p>

### F — integrazione futura

<p align="justify">Portare il mirror su SQLAlchemy mantenendo invariata la suite HTTP del blocco C.</p>

---

## 19. Laboratorio mirror FastAPI

<p align="justify">Definition of Done del primo slice UDA26:</p>

<ul>
  <li>FastAPI/Pydantic/Uvicorn/HTTPX pinned;</li>
  <li><code>GET /api/posts</code> restituisce una lista di Post pubblici;</li>
  <li><code>POST /api/posts</code> usa <code>PostCreate</code>, normalizza il testo e restituisce <code>201</code>;</li>
  <li>la POST espone <code>Location</code>;</li>
  <li><code>PATCH /api/posts/{id}</code> aggiorna <code>liked</code>;</li>
  <li>id inesistente produce <code>404</code>;</li>
  <li><code>authorId</code> non viene accettato come identita affidabile dal command model;</li>
  <li><code>response_model</code> definisce la shape pubblica;</li>
  <li><code>/openapi.json</code> descrive GET/POST/PATCH;</li>
  <li>TestClient verifica il contratto senza server TCP;</li>
  <li>invalid input Pydantic viene osservato come <code>422</code> e documentato come differenza rispetto ad altri adapter;</li>
  <li>nessun SQLAlchemy, auth/session o realtime nel primo mirror.</li>
</ul>

---

## 20. Verifica rapida

<ol>
  <li>Perche FastAPI non sostituisce HTTP?</li>
  <li>Che differenza c'e tra <code>PostCreate</code> e <code>Post</code>?</li>
  <li>Perche un type hint non basta per fidarsi del JSON?</li>
  <li>Che cosa genera <code>/openapi.json</code>?</li>
  <li>Perche <code>response_model</code> e un boundary?</li>
  <li>Che cosa dimostra <code>TestClient</code>?</li>
  <li>Perche <code>422</code> puo essere una compatibility decision?</li>
  <li>Perche SQLAlchemy e rinviato al blocco successivo?</li>
</ol>

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

<p align="justify">Concetto chiave:</p>

<blockquote>
<p align="justify">cambiare framework non deve obbligarci a dimenticare il contratto che il client osserva.</p>
</blockquote>

<p align="justify">FastAPI rende particolarmente visibili i contratti tramite Pydantic, JSON Schema e OpenAPI, ma proprio per questo dobbiamo imparare a distinguere cio che il framework genera automaticamente dalle decisioni applicative che restano nostre.</p>

## Fonti professionali da leggere

<ul>
  <li>FastAPI official documentation: first steps, request body, response model, testing e OpenAPI;</li>
  <li>OpenAPI/JSON Schema come standard esposto tramite <code>/openapi.json</code>;</li>
  <li>Pydantic documentation per model/field validation;</li>
  <li>HTTPX/TestClient per i test HTTP in-process;</li>
  <li>RFC 9110 per status e semantica HTTP gia studiati;</li>
  <li>Express reference del corso per il confronto adapter-to-adapter.</li>
</ul>

<p align="justify">Le fonti servono per imparare a ricostruire il comportamento del framework dalla documentazione, non per copiare ricette senza comprendere il contratto.</p>
