# Testing strategy e integration boundaries: evidenze affidabili senza test fragili

Questo terzo slice di UDA26 non aggiunge un framework di prodotto e non amplia il dominio Feisbuc. Cambia invece una cosa fondamentale: **come dimostriamo che il sistema continua a rispettare i suoi contratti** mentre cambiano adapter, database e configurazione.

Il punto di partenza e gia forte:

```text
mirror 01 -> FastAPI + Pydantic + OpenAPI + MemoryPostStore
mirror 02 -> stesso HTTP contract + SQLAlchemy 2.0 + SQLite
```

Adesso dobbiamo smettere di pensare ai test come a una lista piatta di `assert` e iniziare a progettarli come una **architettura di evidenze**.

---

## Obiettivi

Al termine devi saper:

- distinguere unit test, repository integration test, HTTP contract test ed end-to-end test;
- scegliere il livello minimo che dimostra davvero una proprieta;
- usare `pytest` con fixture piccole e lifecycle esplicito;
- usare `tmp_path` per isolare i database dei test;
- mantenere i test indipendenti dall'ordine di esecuzione;
- capire quando usare un oggetto reale e quando un test double;
- verificare il contratto osservabile invece dei dettagli interni;
- costruire un'app nuova per ogni boundary di test quando serve;
- separare test di persistenza, test HTTP e restart test;
- leggere la CI come una pipeline di evidenze, non come un unico semaforo.

---

## Prerequisiti

Servono:

- HTTP/REST e status code di UDA23;
- Express/store/SQL/auth di UDA24;
- `TestClient`, Pydantic e OpenAPI del mirror 01;
- Engine, SessionFactory, repository e transazioni del mirror 02;
- Python di base: funzioni, context manager, import, eccezioni.

---

## 1. Un test non vale per il numero di righe

Questo test e corto:

```python
assert app.state.session_factory is not None
```

ma non dimostra che un client riesca a creare un post.

Questo test e piu vicino al contratto:

```python
response = client.post('/api/posts', json={'text': 'ciao'})
assert response.status_code == 201
assert response.headers['location'].startswith('/api/posts/')
```

La domanda corretta non e:

> quanti test abbiamo?

ma:

> quale proprieta vogliamo dimostrare e qual e il boundary piu economico che la rende osservabile?

---

## 2. Quattro livelli utili nel nostro mirror

Per questo corso useremo quattro livelli operativi.

| Livello | Cosa attraversa | Esempio Feisbuc | Costo |
| --- | --- | --- | --- |
| unit/policy | funzione o regola pura | normalizzazione/validation policy | basso |
| repository integration | repository + SQLAlchemy + SQLite reale | create/list/like + commit | medio |
| HTTP contract integration | FastAPI + Pydantic + repository + DB | GET/POST/PATCH/404/422 | medio-alto |
| end-to-end | processo/rete/browser o piu servizi | browser -> server -> DB | alto |

Il nome non e una religione. Quello che conta e dichiarare **quale boundary attraversiamo**.

---

## 3. Piramide: una guida, non un dogma

Una forma ragionevole e:

```text
                pochi E2E
             /                     HTTP integration tests
       /                      repository integration tests
/                               molti test di policy/funzioni pure
```

Se tutto e E2E, il feedback e lento e la diagnosi e difficile.

Se tutto e unit test con mock, rischiamo di provare un sistema che in produzione non esiste.

---

## 4. Il contratto osservabile resta la bussola

Il mirror continua a promettere:

```text
GET   /api/posts
POST  /api/posts        -> 201 + Location
PATCH /api/posts/{id}
missing id              -> 404
invalid payload         -> 422
/openapi.json            -> path + schema previsti
```

Questi sono fatti osservabili dal client.

Non sono parte del contratto pubblico:

```text
nome della SessionFactory
numero di helper privati
ordine delle funzioni nel file
attributi app.state non documentati
classe concreta usata dentro il repository
```

Un test che dipende troppo dagli interni diventa fragile durante i refactor.

---

## 5. Baseline pytest del corso

La reference UDA26 usa:

```text
pytest       9.1.1
FastAPI     0.141.1
Pydantic    2.13.4
HTTPX       0.28.1
SQLAlchemy  2.0.51
Python      3.11 / 3.12 CI
```

Non introduciamo ancora:

- pytest-cov;
- xdist;
- factory-boy;
- Testcontainers;
- Docker Compose nel test harness;
- PostgreSQL;
- browser automation.

Prima impariamo lifecycle, isolamento e boundary.

---

## 6. Arrange, Act, Assert

Una struttura leggibile:

```python
def test_missing_post_returns_404(client):
    # Arrange
    post_id = 'missing'

    # Act
    response = client.patch(f'/api/posts/{post_id}', json={'liked': True})

    # Assert
    assert response.status_code == 404
    assert response.json()['detail']['code'] == 'post-not-found'
```

Non serve commentare sempre le tre parole, ma la separazione mentale aiuta.

---

## 7. Fixture: setup riusabile con ownership chiara

Una fixture non e una variabile globale elegante.

```python
import pytest

@pytest.fixture
def client(tmp_path):
    db_path = tmp_path / 'test.db'
    app = create_app(f'sqlite:///{db_path.as_posix()}')
    try:
        with TestClient(app) as client:
            yield client
    finally:
        app.state.engine.dispose()
```

La fixture possiede:

- database temporaneo;
- app;
- client;
- teardown dell'Engine.

---

## 8. Function scope come default didattico

Per default pytest crea una fixture nuova per ogni test.

Questo significa:

```text
test A -> db A

test B -> db B
```

Non:

```text
test A -> shared.db <- test B <- test C
```

Il secondo schema introduce dipendenze dall'ordine.

---

## 9. `tmp_path`: isolamento concreto

`tmp_path` non e solo comodita. Rende esplicito che ogni test possiede i propri file.

```python
def test_database_exists_after_write(tmp_path):
    db_path = tmp_path / 'posts.db'
    ...
    assert db_path.is_file()
```

Non usiamo `./test.db` condiviso fra test diversi.

---

## 10. App factory = test seam

Il mirror 02 ha gia:

```python
def create_app(database_url: str) -> FastAPI:
    ...
```

Questa funzione e contemporaneamente:

- composition root;
- punto di configurazione;
- seam di test.

Il test puo creare un'app con un database dedicato senza cambiare route o globali.

---

## 11. Test repository: usiamo il database vero

Per provare il repository non mockiamo SQLAlchemy.

```python
store.create('ciao')
posts = store.list()
assert posts[0]['text'] == 'ciao'
```

Il valore del test nasce proprio dall'attraversare:

```text
repository -> Session -> SQLAlchemy -> SQLite
```

Se sostituissimo SQLite con un mock, elimineremmo il boundary che vogliamo verificare.

---

## 12. HTTP integration: niente rete TCP, ma stack reale

`TestClient` non apre una porta reale, ma attraversa:

```text
request
  -> FastAPI routing
  -> Pydantic validation
  -> adapter HTTP
  -> repository
  -> SQLAlchemy
  -> SQLite
  -> response
```

Questo e un test d'integrazione molto utile e relativamente economico.

---

## 13. Restart test: una proprieta diversa

Il restart test non e un duplicato del test repository.

Dimostra:

> i dati sopravvivono alla distruzione dell'app e dell'Engine.

Schema:

```text
app A -> write -> dispose engine
                    ↓
               stesso file
                    ↓
app B -> read -> dato ancora presente
```

Per questo merita un test separato.

---

## 14. Test isolation: prova negativa contro lo stato condiviso

Una coppia utile:

```python
def test_first_client_starts_with_seed_only(client):
    assert len(client.get('/api/posts').json()) == 1


def test_second_client_also_starts_with_seed_only(client):
    assert len(client.get('/api/posts').json()) == 1
```

Se la fixture usa un database globale, il secondo test puo ereditare lo stato del primo.

---

## 15. Parametrizzazione per una policy ripetibile

Quando cambia solo l'input:

```python
import pytest

@pytest.mark.parametrize('liked,expected_likes', [
    (True, 1),
    (False, 0),
])
def test_like_transition(store, liked, expected_likes):
    ...
```

La parametrizzazione riduce duplicazione senza nascondere il caso di test.

---

## 16. Quando usare mock

Un mock e utile quando il vero collaborator e:

- lento;
- esterno;
- costoso;
- non deterministico;
- non disponibile nel processo di test.

Esempi futuri:

```text
provider email
payment gateway
API esterna
clock controllato
```

Nel nostro slice non sono buoni candidati al mock:

```text
Pydantic
repository SQLAlchemy
SQLite
FastAPI routing
```

perche sono proprio parte dell'integrazione che vogliamo osservare.

---

## 17. Over-mocking: test verde, sistema rotto

Questo test puo passare anche se SQLAlchemy e configurato male:

```python
fake_store.create.return_value = {'id': 'p1', ...}
response = client.post('/api/posts', json={'text': 'x'})
assert response.status_code == 201
```

Ha valore come unit test dell'adapter, ma **non** dimostra la persistenza.

Dobbiamo chiamarlo con il suo nome corretto e non usarlo come unica evidence.

---

## 18. Test del comportamento, non dell'implementazione

Fragile:

```python
assert store._session_factory is app.state.session_factory
```

Robusto rispetto a refactor interni:

```python
created = client.post('/api/posts', json={'text': 'x'})
assert created.status_code == 201
assert client.get('/api/posts').status_code == 200
```

---

## 19. Negative paths

Un test suite professionale non verifica solo il percorso felice.

Per il mirror:

- testo vuoto -> `422`;
- testo troppo lungo -> `422`;
- id inesistente -> `404`;
- like ripetuto -> conteggio idempotente;
- seed ripetuto -> una sola riga seed.

---

## 20. OpenAPI smoke test

OpenAPI e un artifact del contratto.

```python
schema = client.get('/openapi.json').json()
assert '/api/posts' in schema['paths']
assert 'PostCreate' in schema['components']['schemas']
```

Non confrontiamo l'intero JSON byte-per-byte: sarebbe troppo fragile.

---

## 21. Test naming

Meglio:

```text
test_post_returns_201_and_location

test_missing_post_returns_404

test_restart_preserves_liked_state
```

Peggio:

```text
test_1

test_api

test_everything
```

Il nome deve aiutare la diagnosi quando la CI diventa rossa.

---

## 22. Un assert per test? Non e una regola assoluta

Un test di contratto puo avere piu assert se descrivono una sola proprieta coerente.

```python
assert response.status_code == 201
assert response.headers['location'] == f"/api/posts/{body['id']}"
assert body['authorId'] == 'mirror-user'
```

Sono tre osservazioni dello stesso evento HTTP.

---

## 23. Il boundary del database nei test

Per repository e HTTP integration usiamo SQLite reale.

Il database deve essere:

- creato dal test;
- isolato;
- piccolo;
- distrutto automaticamente;
- configurato dal composition root.

Non puntiamo mai al database di sviluppo.

---

## 24. Configurazione per ambiente: qui solo il seam

Il deploy verra nel prossimo slice. Qui prepariamo il principio:

```text
configurazione entra dall'esterno
codice non decide da solo dove sono i dati
```

Nei test:

```python
create_app(test_database_url)
```

In produzione potra arrivare da environment/configuration.

---

## 25. CI come pipeline di evidenze

La Quality docente esegue gate distinti:

```text
reference repository fixture tests
        ↓
mirror 03 HTTP/integration/restart tests
        ↓
content-pack/course-design/activity contracts
        ↓
regression suite completa
```

Se fallisce il primo gate sappiamo gia che il problema e piu vicino al repository/fixture layer.

---

## 26. Cosa non introduciamo

In questo slice niente:

- coverage percentage come obiettivo didattico;
- mutation testing;
- browser E2E automation;
- Docker/Testcontainers;
- PostgreSQL;
- CI matrix aggiuntive;
- async pytest;
- auth/session Python;
- Socket.IO Python;
- nuova API.

Il focus e **qualita del boundary**, non quantita di strumenti.

---

## 27. Progressione A-D

### A — Testing boundary microscope

Classifica casi reali e scegli il livello minimo che dimostra la proprieta.

### B — Pytest fixture e isolamento

Rifattorizza un repository test in fixture function-scoped con `tmp_path`, teardown e parametrizzazione.

### C — Feisbuc mirror 03

Costruisci il test harness del mirror 02 separando:

- HTTP contract;
- OpenAPI smoke;
- repository integration;
- restart persistence;
- isolation.

### D — Debug dei test fragili

Correggi shared state, test order dependency, over-mocking, assert sugli interni e teardown mancante.

---

## 28. Milestone Feisbuc mirror 03

La milestone non aggiunge una schermata o una route.

Aggiunge una nuova capacita del progetto:

> possiamo cambiare internamente il sistema e ottenere evidence localizzata su cosa si e rotto.

Artifact principale:

```text
tests/
  conftest.py
  test_http_contract.py
  test_openapi_contract.py
  test_repository_integration.py
  test_restart_persistence.py
  test_isolation.py
```

---

## 29. Checklist professionale

- [ ] ogni test dichiara implicitamente o esplicitamente il boundary attraversato;
- [ ] niente database condiviso fra test indipendenti;
- [ ] `tmp_path` per file SQLite temporanei;
- [ ] Engine disposed quando il test ne possiede il lifecycle;
- [ ] app costruita tramite factory;
- [ ] test HTTP osservano status/header/body;
- [ ] repository test usa SQLite reale;
- [ ] restart test separato;
- [ ] OpenAPI verificato per path/schema significativi;
- [ ] niente assert su dettagli privati inutili;
- [ ] mock solo quando sostituisce un boundary davvero esterno o costoso;
- [ ] nomi dei test descrittivi;
- [ ] test indipendenti dall'ordine;
- [ ] pytest pinned nella reference;
- [ ] CI mantiene gate separati.

---

## 30. Ponte al quarto slice UDA26

Ora il mirror Python ha tre incrementi coerenti:

```text
01 contratto HTTP
02 persistenza ORM
03 strategia di test e integration boundaries
```

Il quarto e ultimo slice di UDA26 puo quindi concentrarsi su:

- configurazione runtime;
- packaging/deploy minimale;
- health/readiness e osservabilita base;
- capstone Feisbuc;
- evidence bundle finale.

La regola resta la stessa:

> non aggiungere tecnologia se non rende piu verificabile un requisito reale.
