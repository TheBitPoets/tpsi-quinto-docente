# Testing strategy e integration boundaries: evidenze affidabili senza test fragili

<table align="center" width="100%"><tr><td>
<details>
<summary>&#128506; <strong>Orientamento della lezione</strong></summary>

<p align="justify"><strong>Contesto:</strong> il mirror possiede API e persistenza. Ora dobbiamo produrre evidenze che localizzino i guasti senza dipendere da stato globale o dettagli interni fragili.</p>
<p align="justify"><strong>Domande guida:</strong> quale boundary attraversa ogni test? Chi possiede setup e teardown? Quando usare il database reale e quando un test double?</p>
<p align="justify"><strong>Obiettivi osservabili:</strong> scegliere il livello di test, usare fixture function-scoped e <code>tmp_path</code>, costruire un app factory, testare negative path e dimostrare isolamento e persistenza.</p>
<p align="justify"><strong>Prossimo passo:</strong> la lezione 18 porterà le stesse evidenze su un processo live configurato come servizio.</p>

</details>
</td></tr></table>

<p align="justify">Questo terzo slice di UDA26 non aggiunge un framework di prodotto e non amplia il dominio Feisbuc. Cambia invece una cosa fondamentale: <strong>come dimostriamo che il sistema continua a rispettare i suoi contratti</strong> mentre cambiano adapter, database e configurazione.</p>

<p align="justify">Il punto di partenza e gia forte:</p>

```text
mirror 01 -> FastAPI + Pydantic + OpenAPI + MemoryPostStore
mirror 02 -> stesso HTTP contract + SQLAlchemy 2.0 + SQLite
```

<p align="justify">Adesso dobbiamo smettere di pensare ai test come a una lista piatta di <code>assert</code> e iniziare a progettarli come una <strong>architettura di evidenze</strong>.</p>

---

## Obiettivi

<p align="justify">Al termine devi saper:</p>

<ul>
  <li>distinguere unit test, repository integration test, HTTP contract test ed end-to-end test;</li>
  <li>scegliere il livello minimo che dimostra davvero una proprieta;</li>
  <li>usare <code>pytest</code> con fixture piccole e lifecycle esplicito;</li>
  <li>usare <code>tmp_path</code> per isolare i database dei test;</li>
  <li>mantenere i test indipendenti dall'ordine di esecuzione;</li>
  <li>capire quando usare un oggetto reale e quando un test double;</li>
  <li>verificare il contratto osservabile invece dei dettagli interni;</li>
  <li>costruire un'app nuova per ogni boundary di test quando serve;</li>
  <li>separare test di persistenza, test HTTP e restart test;</li>
  <li>leggere la CI come una pipeline di evidenze, non come un unico semaforo.</li>
</ul>

---

## Prerequisiti

<p align="justify">Servono:</p>

<ul>
  <li>HTTP/REST e status code di UDA23;</li>
  <li>Express/store/SQL/auth di UDA24;</li>
  <li><code>TestClient</code>, Pydantic e OpenAPI del mirror 01;</li>
  <li>Engine, SessionFactory, repository e transazioni del mirror 02;</li>
  <li>Python di base: funzioni, context manager, import, eccezioni.</li>
</ul>

## Orientamento nella documentazione

<p align="center">
  <img src="../../assets/tpsi5/lesson-documentation-depth.svg" alt="La dispensa seleziona nelle fonti ufficiali i contenuti da studiare ora, riconoscere, rimandare o dichiarare fuori confine">
</p>

<table align="center"><tr><td>
<details>
<summary>&#128279; <strong>Indice incrociato — pytest e integration boundary</strong></summary>

<table align="center">
<thead><tr><th>Dispensa</th><th>Documentazione ufficiale</th><th>Profondità</th></tr></thead>
<tbody>
<tr><td><a href="#lesson-testing-levels">Livelli e contratto osservabile</a></td><td><a href="https://docs.pytest.org/en/stable/explanation/goodpractices.html">pytest — Good Integration Practices</a></td><td>&#128994; studiare il modello del corso</td></tr>
<tr><td><a href="#lesson-testing-fixtures">Fixture, scope e <code>tmp_path</code></a></td><td><a href="https://docs.pytest.org/en/stable/how-to/fixtures.html">pytest fixtures</a><br><a href="https://docs.pytest.org/en/stable/how-to/tmp_path.html">Temporary directories and files</a></td><td>&#128994; studiare ora</td></tr>
<tr><td><a href="#lesson-testing-integration">Repository, HTTP e restart test</a></td><td><a href="https://fastapi.tiangolo.com/tutorial/testing/">FastAPI — Testing</a><br><a href="https://docs.sqlalchemy.org/en/20/orm/session_basics.html">SQLAlchemy — Session Basics</a></td><td>&#128994; applicare ai boundary reali</td></tr>
<tr><td><a href="#lesson-testing-ci">CI come pipeline di evidenze</a></td><td><a href="https://docs.pytest.org/en/stable/how-to/usage.html">pytest usage</a></td><td>&#128994; comprendere i gate</td></tr>
<tr><td>Browser E2E distribuito, load test e chaos testing</td><td>Documentazione degli strumenti dedicati</td><td>&#128993; fuori dal core</td></tr>
</tbody>
</table>

</details>
</td></tr></table>

---

<a id="lesson-testing-levels"></a>
## 1. Un test non vale per il numero di righe

<p align="justify">Questo test e corto:</p>

```python
assert app.state.session_factory is not None
```

<p align="justify">ma non dimostra che un client riesca a creare un post.</p>

<p align="justify">Questo test e piu vicino al contratto:</p>

```python
response = client.post('/api/posts', json={'text': 'ciao'})
assert response.status_code == 201
assert response.headers['location'].startswith('/api/posts/')
```

<p align="justify">La domanda corretta non e:</p>

<blockquote>
<p align="justify">quanti test abbiamo?</p>
</blockquote>

<p align="justify">ma:</p>

<blockquote>
<p align="justify">quale proprieta vogliamo dimostrare e qual e il boundary piu economico che la rende osservabile?</p>
</blockquote>

---

## 2. Quattro livelli utili nel nostro mirror

<p align="justify">Per questo corso useremo quattro livelli operativi.</p>

<table align="center">
<thead>
<tr>
<th>Livello</th>
<th>Cosa attraversa</th>
<th>Esempio Feisbuc</th>
<th>Costo</th>
</tr>
</thead>
<tbody>
<tr>
<td>unit/policy</td>
<td>funzione o regola pura</td>
<td>normalizzazione/validation policy</td>
<td>basso</td>
</tr>
<tr>
<td>repository integration</td>
<td>repository + SQLAlchemy + SQLite reale</td>
<td>create/list/like + commit</td>
<td>medio</td>
</tr>
<tr>
<td>HTTP contract integration</td>
<td>FastAPI + Pydantic + repository + DB</td>
<td>GET/POST/PATCH/404/422</td>
<td>medio-alto</td>
</tr>
<tr>
<td>end-to-end</td>
<td>processo/rete/browser o piu servizi</td>
<td>browser -> server -> DB</td>
<td>alto</td>
</tr>
</tbody>
</table>

<p align="justify">Il nome non e una religione. Quello che conta e dichiarare <strong>quale boundary attraversiamo</strong>.</p>

---

## 3. Piramide: una guida, non un dogma

<p align="justify">Una forma ragionevole e:</p>

```text
                pochi E2E
             /                     HTTP integration tests
       /                      repository integration tests
/                               molti test di policy/funzioni pure
```

<p align="justify">Se tutto e E2E, il feedback e lento e la diagnosi e difficile.</p>

<p align="justify">Se tutto e unit test con mock, rischiamo di provare un sistema che in produzione non esiste.</p>

---

## 4. Il contratto osservabile resta la bussola

<p align="justify">Il mirror continua a promettere:</p>

```text
GET   /api/posts
POST  /api/posts        -> 201 + Location
PATCH /api/posts/{id}
missing id              -> 404
invalid payload         -> 422
/openapi.json            -> path + schema previsti
```

<p align="justify">Questi sono fatti osservabili dal client.</p>

<p align="justify">Non sono parte del contratto pubblico:</p>

```text
nome della SessionFactory
numero di helper privati
ordine delle funzioni nel file
attributi app.state non documentati
classe concreta usata dentro il repository
```

<p align="justify">Un test che dipende troppo dagli interni diventa fragile durante i refactor.</p>

---

## 5. Baseline pytest del corso

<p align="justify">La reference UDA26 usa:</p>

```text
pytest       9.1.1
FastAPI     0.141.1
Pydantic    2.13.4
HTTPX       0.28.1
SQLAlchemy  2.0.51
Python      3.11 / 3.12 CI
```

<p align="justify">Non introduciamo ancora:</p>

<ul>
  <li>pytest-cov;</li>
  <li>xdist;</li>
  <li>factory-boy;</li>
  <li>Testcontainers;</li>
  <li>Docker Compose nel test harness;</li>
  <li>PostgreSQL;</li>
  <li>browser automation.</li>
</ul>

<p align="justify">Prima impariamo lifecycle, isolamento e boundary.</p>

---

## 6. Arrange, Act, Assert

<p align="justify">Una struttura leggibile:</p>

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

<p align="justify">Non serve commentare sempre le tre parole, ma la separazione mentale aiuta.</p>

---

<a id="lesson-testing-fixtures"></a>
## 7. Fixture: setup riusabile con ownership chiara

<p align="justify">Una fixture non e una variabile globale elegante.</p>

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

<p align="justify">La fixture possiede:</p>

<ul>
  <li>database temporaneo;</li>
  <li>app;</li>
  <li>client;</li>
  <li>teardown dell'Engine.</li>
</ul>

---

## 8. Function scope come default didattico

<p align="justify">Per default pytest crea una fixture nuova per ogni test.</p>

<p align="justify">Questo significa:</p>

```text
test A -> db A

test B -> db B
```

<p align="justify">Non:</p>

```text
test A -> shared.db <- test B <- test C
```

<p align="justify">Il secondo schema introduce dipendenze dall'ordine.</p>

---

## 9. `tmp_path`: isolamento concreto

<p align="justify"><code>tmp_path</code> non e solo comodita. Rende esplicito che ogni test possiede i propri file.</p>

```python
def test_database_exists_after_write(tmp_path):
    db_path = tmp_path / 'posts.db'
    ...
    assert db_path.is_file()
```

<p align="justify">Non usiamo <code>./test.db</code> condiviso fra test diversi.</p>

---

## 10. App factory = test seam

<p align="justify">Il mirror 02 ha gia:</p>

```python
def create_app(database_url: str) -> FastAPI:
    ...
```

<p align="justify">Questa funzione e contemporaneamente:</p>

<ul>
  <li>composition root;</li>
  <li>punto di configurazione;</li>
  <li>seam di test.</li>
</ul>

<p align="justify">Il test puo creare un'app con un database dedicato senza cambiare route o globali.</p>

---

<a id="lesson-testing-integration"></a>
## 11. Test repository: usiamo il database vero

<p align="justify">Per provare il repository non mockiamo SQLAlchemy.</p>

```python
store.create('ciao')
posts = store.list()
assert posts[0]['text'] == 'ciao'
```

<p align="justify">Il valore del test nasce proprio dall'attraversare:</p>

```text
repository -> Session -> SQLAlchemy -> SQLite
```

<p align="justify">Se sostituissimo SQLite con un mock, elimineremmo il boundary che vogliamo verificare.</p>

---

## 12. HTTP integration: niente rete TCP, ma stack reale

<p align="justify"><code>TestClient</code> non apre una porta reale, ma attraversa:</p>

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

<p align="justify">Questo e un test d'integrazione molto utile e relativamente economico.</p>

---

## 13. Restart test: una proprieta diversa

<p align="justify">Il restart test non e un duplicato del test repository.</p>

<p align="justify">Dimostra:</p>

<blockquote>
<p align="justify">i dati sopravvivono alla distruzione dell'app e dell'Engine.</p>
</blockquote>

<p align="justify">Schema:</p>

```text
app A -> write -> dispose engine
                    ↓
               stesso file
                    ↓
app B -> read -> dato ancora presente
```

<p align="justify">Per questo merita un test separato.</p>

---

## 14. Test isolation: prova negativa contro lo stato condiviso

<p align="justify">Una coppia utile:</p>

```python
def test_first_client_starts_with_seed_only(client):
    assert len(client.get('/api/posts').json()) == 1


def test_second_client_also_starts_with_seed_only(client):
    assert len(client.get('/api/posts').json()) == 1
```

<p align="justify">Se la fixture usa un database globale, il secondo test puo ereditare lo stato del primo.</p>

---

## 15. Parametrizzazione per una policy ripetibile

<p align="justify">Quando cambia solo l'input:</p>

```python
import pytest

@pytest.mark.parametrize('liked,expected_likes', [
    (True, 1),
    (False, 0),
])
def test_like_transition(store, liked, expected_likes):
    ...
```

<p align="justify">La parametrizzazione riduce duplicazione senza nascondere il caso di test.</p>

---

## 16. Quando usare mock

<p align="justify">Un mock e utile quando il vero collaborator e:</p>

<ul>
  <li>lento;</li>
  <li>esterno;</li>
  <li>costoso;</li>
  <li>non deterministico;</li>
  <li>non disponibile nel processo di test.</li>
</ul>

<p align="justify">Esempi futuri:</p>

```text
provider email
payment gateway
API esterna
clock controllato
```

<p align="justify">Nel nostro slice non sono buoni candidati al mock:</p>

```text
Pydantic
repository SQLAlchemy
SQLite
FastAPI routing
```

<p align="justify">perche sono proprio parte dell'integrazione che vogliamo osservare.</p>

---

## 17. Over-mocking: test verde, sistema rotto

<p align="justify">Questo test puo passare anche se SQLAlchemy e configurato male:</p>

```python
fake_store.create.return_value = {'id': 'p1', ...}
response = client.post('/api/posts', json={'text': 'x'})
assert response.status_code == 201
```

<p align="justify">Ha valore come unit test dell'adapter, ma <strong>non</strong> dimostra la persistenza.</p>

<p align="justify">Dobbiamo chiamarlo con il suo nome corretto e non usarlo come unica evidence.</p>

---

## 18. Test del comportamento, non dell'implementazione

<p align="justify">Fragile:</p>

```python
assert store._session_factory is app.state.session_factory
```

<p align="justify">Robusto rispetto a refactor interni:</p>

```python
created = client.post('/api/posts', json={'text': 'x'})
assert created.status_code == 201
assert client.get('/api/posts').status_code == 200
```

---

## 19. Negative paths

<p align="justify">Un test suite professionale non verifica solo il percorso felice.</p>

<p align="justify">Per il mirror:</p>

<ul>
  <li>testo vuoto -> <code>422</code>;</li>
  <li>testo troppo lungo -> <code>422</code>;</li>
  <li>id inesistente -> <code>404</code>;</li>
  <li>like ripetuto -> conteggio idempotente;</li>
  <li>seed ripetuto -> una sola riga seed.</li>
</ul>

---

## 20. OpenAPI smoke test

<p align="justify">OpenAPI e un artifact del contratto.</p>

```python
schema = client.get('/openapi.json').json()
assert '/api/posts' in schema['paths']
assert 'PostCreate' in schema['components']['schemas']
```

<p align="justify">Non confrontiamo l'intero JSON byte-per-byte: sarebbe troppo fragile.</p>

---

## 21. Test naming

<p align="justify">Meglio:</p>

```text
test_post_returns_201_and_location

test_missing_post_returns_404

test_restart_preserves_liked_state
```

<p align="justify">Peggio:</p>

```text
test_1

test_api

test_everything
```

<p align="justify">Il nome deve aiutare la diagnosi quando la CI diventa rossa.</p>

---

## 22. Un assert per test? Non e una regola assoluta

<p align="justify">Un test di contratto puo avere piu assert se descrivono una sola proprieta coerente.</p>

```python
assert response.status_code == 201
assert response.headers['location'] == f"/api/posts/{body['id']}"
assert body['authorId'] == 'mirror-user'
```

<p align="justify">Sono tre osservazioni dello stesso evento HTTP.</p>

---

## 23. Il boundary del database nei test

<p align="justify">Per repository e HTTP integration usiamo SQLite reale.</p>

<p align="justify">Il database deve essere:</p>

<ul>
  <li>creato dal test;</li>
  <li>isolato;</li>
  <li>piccolo;</li>
  <li>distrutto automaticamente;</li>
  <li>configurato dal composition root.</li>
</ul>

<p align="justify">Non puntiamo mai al database di sviluppo.</p>

---

## 24. Configurazione per ambiente: qui solo il seam

<p align="justify">Il deploy verra nel prossimo slice. Qui prepariamo il principio:</p>

```text
configurazione entra dall'esterno
codice non decide da solo dove sono i dati
```

<p align="justify">Nei test:</p>

```python
create_app(test_database_url)
```

<p align="justify">In produzione potra arrivare da environment/configuration.</p>

---

<a id="lesson-testing-ci"></a>
## 25. CI come pipeline di evidenze

<p align="justify">La Quality docente esegue gate distinti:</p>

```text
reference repository fixture tests
        ↓
mirror 03 HTTP/integration/restart tests
        ↓
content-pack/course-design/activity contracts
        ↓
regression suite completa
```

<p align="justify">Se fallisce il primo gate sappiamo gia che il problema e piu vicino al repository/fixture layer.</p>

---

## 26. Cosa non introduciamo

<p align="justify">In questo slice niente:</p>

<ul>
  <li>coverage percentage come obiettivo didattico;</li>
  <li>mutation testing;</li>
  <li>browser E2E automation;</li>
  <li>Docker/Testcontainers;</li>
  <li>PostgreSQL;</li>
  <li>CI matrix aggiuntive;</li>
  <li>async pytest;</li>
  <li>auth/session Python;</li>
  <li>Socket.IO Python;</li>
  <li>nuova API.</li>
</ul>

<p align="justify">Il focus e <strong>qualita del boundary</strong>, non quantita di strumenti.</p>

---

## 27. Progressione A-D

### A — Testing boundary microscope

<p align="justify">Classifica casi reali e scegli il livello minimo che dimostra la proprieta.</p>

### B — Pytest fixture e isolamento

<p align="justify">Rifattorizza un repository test in fixture function-scoped con <code>tmp_path</code>, teardown e parametrizzazione.</p>

### C — Feisbuc mirror 03

<p align="justify">Costruisci il test harness del mirror 02 separando:</p>

<ul>
  <li>HTTP contract;</li>
  <li>OpenAPI smoke;</li>
  <li>repository integration;</li>
  <li>restart persistence;</li>
  <li>isolation.</li>
</ul>

### D — Debug dei test fragili

<p align="justify">Correggi shared state, test order dependency, over-mocking, assert sugli interni e teardown mancante.</p>

---

## 28. Milestone Feisbuc mirror 03

<p align="justify">La milestone non aggiunge una schermata o una route.</p>

<p align="justify">Aggiunge una nuova capacita del progetto:</p>

<blockquote>
<p align="justify">possiamo cambiare internamente il sistema e ottenere evidence localizzata su cosa si e rotto.</p>
</blockquote>

<p align="justify">Artifact principale:</p>

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

<ul>
  <li>[ ] ogni test dichiara implicitamente o esplicitamente il boundary attraversato;</li>
  <li>[ ] niente database condiviso fra test indipendenti;</li>
  <li>[ ] <code>tmp_path</code> per file SQLite temporanei;</li>
  <li>[ ] Engine disposed quando il test ne possiede il lifecycle;</li>
  <li>[ ] app costruita tramite factory;</li>
  <li>[ ] test HTTP osservano status/header/body;</li>
  <li>[ ] repository test usa SQLite reale;</li>
  <li>[ ] restart test separato;</li>
  <li>[ ] OpenAPI verificato per path/schema significativi;</li>
  <li>[ ] niente assert su dettagli privati inutili;</li>
  <li>[ ] mock solo quando sostituisce un boundary davvero esterno o costoso;</li>
  <li>[ ] nomi dei test descrittivi;</li>
  <li>[ ] test indipendenti dall'ordine;</li>
  <li>[ ] pytest pinned nella reference;</li>
  <li>[ ] CI mantiene gate separati.</li>
</ul>

---

## 30. Ponte al quarto slice UDA26

<p align="justify">Ora il mirror Python ha tre incrementi coerenti:</p>

```text
01 contratto HTTP
02 persistenza ORM
03 strategia di test e integration boundaries
```

<p align="justify">Il quarto e ultimo slice di UDA26 puo quindi concentrarsi su:</p>

<ul>
  <li>configurazione runtime;</li>
  <li>packaging/deploy minimale;</li>
  <li>health/readiness e osservabilita base;</li>
  <li>capstone Feisbuc;</li>
  <li>evidence bundle finale.</li>
</ul>

<p align="justify">La regola resta la stessa:</p>

<blockquote>
<p align="justify">non aggiungere tecnologia se non rende piu verificabile un requisito reale.</p>
</blockquote>
