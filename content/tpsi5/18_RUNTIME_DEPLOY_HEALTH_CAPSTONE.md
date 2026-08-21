# Runtime configuration, health/readiness, deploy e capstone: dal codice a un servizio verificabile

Questo quarto e ultimo slice di UDA26 non aggiunge feature al dominio Feisbuc. Il contratto `posts` resta quello gia verificato nei mirror 01-03. Cambia il confine: non basta piu sapere che una app funziona dentro `TestClient`; dobbiamo saper **configurare, preparare, avviare, osservare e consegnare** il servizio in modo riproducibile.

La sequenza completa diventa:

```text
mirror 01  FastAPI + Pydantic + OpenAPI + TestClient
    ↓
mirror 02  SQLAlchemy 2.0 + SQLite + restart persistence
    ↓
mirror 03  pytest + fixture/isolation + integration boundaries
    ↓
mirror 04  runtime config + prestart + liveness/readiness + live process + evidence
```

Il mirror rimane didattico: il backend principale del prodotto e ancora Node/Express.

---

## Obiettivi

Al termine devi saper:

- distinguere configurazione applicativa da configurazione del process server;
- leggere configurazione da environment senza incorporare secret o path locali nel codice;
- fallire subito quando una configurazione production obbligatoria manca;
- separare la preparazione del database dall'avvio della web app;
- distinguere **liveness** e **readiness**;
- avviare Uvicorn come processo reale e verificarlo via TCP/HTTP;
- chiudere il processo di test in modo deterministico;
- produrre un evidence bundle riproducibile con manifest, OpenAPI e checksum;
- consegnare un capstone con runbook, comandi di verifica e limiti dichiarati.

---

## 1. Configurazione: il codice non deve conoscere la macchina

Nel mirror 04 usiamo tre variabili:

```text
FEISBUC_ENV
FEISBUC_DATABASE_URL
FEISBUC_BUILD_SHA
```

La configurazione di default e adatta allo sviluppo locale, non alla produzione.

```python
settings = load_settings(os.environ)
```

In `production`, l'assenza di `FEISBUC_DATABASE_URL` e un errore di startup. Non inventiamo un database locale silenzioso.

Non mettiamo invece in `RuntimeSettings`:

```text
host
port
workers
reload
```

Questi appartengono al **process server Uvicorn**, non al dominio/app.

---

## 2. Development default, production fail-fast

Una policy semplice:

```text
FEISBUC_ENV=development + DB assente
    -> sqlite:///./feisbuc-mirror.db

FEISBUC_ENV=production + DB assente
    -> errore esplicito
```

Il vantaggio non e estetico: un servizio production non deve partire accidentalmente con un file SQLite creato nella working directory.

---

## 3. Prestart: preparare prima di servire

Nei mirror precedenti `create_app()` poteva creare schema e seed. Era utile mentre studiavamo ORM e test. Nel runtime finale separiamo le responsabilita:

```text
python -m app.prepare
        ↓
create schema + seed idempotente

python -m uvicorn app.main:app ...
        ↓
serve request, NON prepara il database
```

Questa separazione rende significativa la readiness: un processo puo essere vivo ma non ancora pronto.

---

## 4. Liveness != readiness

### Liveness

Domanda:

> il processo applicativo risponde?

```http
GET /health
200 OK
```

La liveness **non deve interrogare il database**. Se il DB e giu ma il processo Python e vivo, `/health` resta 200.

### Readiness

Domanda:

> il servizio puo usare la dipendenza necessaria per servire il suo contratto?

```http
GET /ready
200 OK
```

Nel nostro baseline readiness esegue una query minima sulla tabella `posts`.

Se schema/database non sono pronti:

```http
GET /ready
503 Service Unavailable
```

La risposta di errore e generica: non esponiamo path locali, stack trace o connection string.

---

## 5. Il contratto di prodotto non cambia

Mirror 04 conserva:

```text
GET   /api/posts
POST  /api/posts        -> 201 + Location
PATCH /api/posts/{id}
missing                 -> 404
invalid payload         -> 422
```

Aggiungiamo solo endpoint **operativi**:

```text
GET /health
GET /ready
```

Questa distinzione e importante: operazionalizzare un servizio non significa inventare nuove feature di prodotto.

---

## 6. Lifespan: cleanup dell'Engine

FastAPI puo possedere risorse con un lifespan:

```python
@asynccontextmanager
async def lifespan(app):
    yield
    app.state.engine.dispose()
```

L'Engine nasce nel composition root e viene chiuso quando termina l'app. Non apriamo Session globali condivise.

---

## 7. Uvicorn: processo, non funzione magica

Baseline didattica production-like:

```bash
python -m app.prepare
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --workers 1
```

`--reload` e utile nello sviluppo, ma non fa parte del runbook production-like.

Per questo corso non introduciamo ancora:

- reverse proxy;
- TLS termination;
- process manager;
- multi-worker orchestration;
- Docker Compose;
- Kubernetes;
- PostgreSQL;
- Alembic;
- async ORM.

Sono argomenti validi, ma allargherebbero il perimetro invece di chiudere UDA26.

---

## 8. Live process probe

`TestClient` attraversa il boundary HTTP dell'app, ma non prova che Uvicorn parta davvero.

Il capstone aggiunge un probe che:

1. sceglie una porta locale libera;
2. prepara un database temporaneo;
3. avvia Uvicorn come subprocess;
4. attende `/health` con timeout limitato;
5. verifica `/ready` e `GET /api/posts` via HTTP reale;
6. termina il processo anche in caso di errore.

Il probe non dorme "a caso" per dieci secondi: usa retry brevi con deadline.

---

## 9. Evidence bundle deterministico

Una consegna tecnica deve poter dire **cosa e stato verificato**.

Il capstone genera:

```text
evidence/
├── manifest.json
├── openapi.json
└── SHA256SUMS.txt
```

Il manifest contiene solo dati riproducibili:

- milestone;
- versione Content Pack;
- build SHA dichiarata;
- contratti verificati;
- nomi dei file evidence.

Non contiene:

- timestamp;
- PID;
- porta casuale;
- path temporanei;
- connection string;
- secret.

`SHA256SUMS.txt` permette di verificare l'integrita dei file.

---

## 10. Runbook minimo

Un runbook utile deve permettere a un'altra persona di ripetere il flusso:

```text
1. install dependencies
2. set environment
3. prepare DB
4. start process
5. check health/readiness
6. run tests/probe
7. build evidence
8. stop process
```

Non scriviamo "avvia il server normalmente". Scriviamo i comandi reali.

---

## 11. Capstone: evidence, non nuove feature

Il capstone finale deve dimostrare insieme:

- configurazione development/production;
- fail-fast production;
- prepare esplicito e idempotente;
- liveness senza dipendenza DB;
- readiness con dipendenza DB reale;
- contratto posts invariato;
- persistenza dopo restart;
- processo Uvicorn reale;
- evidence bundle deterministico;
- runbook e limiti dichiarati.

Questa e una chiusura architetturale: **il sistema non e solo scritto; e verificabile e ripetibile**.

---

## 12. Cosa resta deliberatamente fuori

Alla fine di UDA26 non aggiungiamo:

```text
auth/session nel mirror Python
Socket.IO nel mirror Python
Alembic
PostgreSQL
async SQLAlchemy
Docker Compose
Kubernetes
reverse proxy/TLS
browser automation
coverage/xdist
```

Queste scelte possono diventare corsi, moduli o roadmap future. Non sono prerequisiti per dimostrare il boundary runtime fondamentale.

---

## Definition of Done UDA26

UDA26 e chiusa quando:

- Content Pack registra tutti e quattro i slice;
- Activity A-F del closeout sono valide;
- Activity B config passa il runner Python TheBitLab;
- health/readiness reference passa su Linux e Windows;
- il capstone mantiene i test HTTP/restart precedenti;
- un processo Uvicorn reale viene avviato e verificato in CI;
- l'evidence bundle e deterministico e checksum-verificabile;
- la regression suite completa resta verde;
- il corso rimane a 33 settimane e UDA26 a 4 settimane.
