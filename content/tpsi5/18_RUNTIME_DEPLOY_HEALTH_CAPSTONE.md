# Runtime configuration, health/readiness, deploy e capstone: dal codice a un servizio verificabile

<table align="center" width="100%"><tr><td>
<details>
<summary>&#128506; <strong>Orientamento della lezione</strong></summary>

<p align="justify"><strong>Contesto:</strong> un'applicazione corretta nei test non è ancora un servizio operabile. L'ultimo slice collega configurazione, preparazione, processo live, segnali di salute ed evidence bundle.</p>
<p align="justify"><strong>Domande guida:</strong> che cosa deve essere configurato dall'ambiente? Quale differenza c'è fra processo vivo e servizio pronto? Come si dimostra che il sistema funziona senza una verifica manuale irripetibile?</p>
<p align="justify"><strong>Obiettivi osservabili:</strong> applicare fail-fast, eseguire un prestart idempotente, distinguere health e readiness, gestire il lifecycle delle risorse, interrogare un processo reale e produrre evidenze ripetibili.</p>
<p align="justify"><strong>Prossimo passo:</strong> il capstone conclude il percorso: la consegna finale deve collegare contratto, implementazione, test, configurazione e runbook senza introdurre nuove feature.</p>

</details>
</td></tr></table>

<p align="justify">Questo quarto e ultimo slice di UDA26 non aggiunge feature al dominio Feisbuc. Il contratto <code>posts</code> resta quello gia verificato nei mirror 01-03. Cambia il confine: non basta piu sapere che una app funziona dentro <code>TestClient</code>; dobbiamo saper <strong>configurare, preparare, avviare, osservare e consegnare</strong> il servizio in modo riproducibile.</p>

<p align="justify">La sequenza completa diventa:</p>

```text
mirror 01  FastAPI + Pydantic + OpenAPI + TestClient
    ↓
mirror 02  SQLAlchemy 2.0 + SQLite + restart persistence
    ↓
mirror 03  pytest + fixture/isolation + integration boundaries
    ↓
mirror 04  runtime config + prestart + liveness/readiness + live process + evidence
```

<p align="justify">Il mirror rimane didattico: il backend principale del prodotto e ancora Node/Express.</p>

---

## Obiettivi

<p align="justify">Al termine devi saper:</p>

<ul>
  <li>distinguere configurazione applicativa da configurazione del process server;</li>
  <li>leggere configurazione da environment senza incorporare secret o path locali nel codice;</li>
  <li>fallire subito quando una configurazione production obbligatoria manca;</li>
  <li>separare la preparazione del database dall'avvio della web app;</li>
  <li>distinguere <strong>liveness</strong> e <strong>readiness</strong>;</li>
  <li>avviare Uvicorn come processo reale e verificarlo via TCP/HTTP;</li>
  <li>chiudere il processo di test in modo deterministico;</li>
  <li>produrre un evidence bundle riproducibile con manifest, OpenAPI e checksum;</li>
  <li>consegnare un capstone con runbook, comandi di verifica e limiti dichiarati.</li>
</ul>

## Prerequisiti

<ul>
  <li>configurazione e composition root del mirror FastAPI;</li>
  <li>Engine, SessionFactory e persistenza SQLite;</li>
  <li>test repository, HTTP e restart del mirror 03;</li>
  <li>uso essenziale di processi, environment variable, porte TCP e comandi shell.</li>
</ul>

## Orientamento nella documentazione

<p align="center">
  <img src="../../assets/tpsi5/lesson-documentation-depth.svg" alt="La dispensa seleziona nelle fonti ufficiali i contenuti da studiare ora, riconoscere, rimandare o dichiarare fuori confine">
</p>

<table align="center"><tr><td>
<details>
<summary>&#128279; <strong>Indice incrociato — runtime, lifecycle e deploy</strong></summary>

<table align="center">
<thead><tr><th>Dispensa</th><th>Documentazione ufficiale</th><th>Profondità</th></tr></thead>
<tbody>
<tr><td><a href="#lesson-runtime-config">Configurazione e fail-fast</a></td><td><a href="https://www.uvicorn.org/settings/">Uvicorn — Settings</a><br><a href="https://fastapi.tiangolo.com/deployment/concepts/">FastAPI — Deployment Concepts</a></td><td>&#128994; studiare ora</td></tr>
<tr><td><a href="#lesson-runtime-health">Prestart, liveness e readiness</a></td><td><a href="https://fastapi.tiangolo.com/deployment/concepts/">Deployment concepts</a></td><td>&#128994; studiare il contratto del corso</td></tr>
<tr><td><a href="#lesson-runtime-lifecycle">Lifespan e processo Uvicorn</a></td><td><a href="https://fastapi.tiangolo.com/advanced/events/">FastAPI — Lifespan Events</a><br><a href="https://www.uvicorn.org/server-behavior/">Uvicorn — Server Behavior</a></td><td>&#128994; studiare ora</td></tr>
<tr><td><a href="#lesson-runtime-evidence">Probe, evidence bundle e runbook</a></td><td><a href="https://www.uvicorn.org/deployment/">Uvicorn — Deployment</a></td><td>&#128994; applicare al capstone</td></tr>
<tr><td>Orchestrazione, autoscaling, cloud e CI/CD avanzata</td><td>Documentazione della piattaforma scelta</td><td>&#128993; fuori dal core</td></tr>
</tbody>
</table>

</details>
</td></tr></table>

---

<a id="lesson-runtime-config"></a>
## 1. Configurazione: il codice non deve conoscere la macchina

<p align="justify">Nel mirror 04 usiamo tre variabili:</p>

```text
FEISBUC_ENV
FEISBUC_DATABASE_URL
FEISBUC_BUILD_SHA
```

<p align="justify">La configurazione di default e adatta allo sviluppo locale, non alla produzione.</p>

```python
settings = load_settings(os.environ)
```

<p align="justify">In <code>production</code>, l'assenza di <code>FEISBUC_DATABASE_URL</code> e un errore di startup. Non inventiamo un database locale silenzioso.</p>

<p align="justify">Non mettiamo invece in <code>RuntimeSettings</code>:</p>

```text
host
port
workers
reload
```

<p align="justify">Questi appartengono al <strong>process server Uvicorn</strong>, non al dominio/app.</p>

---

## 2. Development default, production fail-fast

<p align="justify">Una policy semplice:</p>

```text
FEISBUC_ENV=development + DB assente
    -> sqlite:///./feisbuc-mirror.db

FEISBUC_ENV=production + DB assente
    -> errore esplicito
```

<p align="justify">Il vantaggio non e estetico: un servizio production non deve partire accidentalmente con un file SQLite creato nella working directory.</p>

---

<a id="lesson-runtime-health"></a>
## 3. Prestart: preparare prima di servire

<p align="justify">Nei mirror precedenti <code>create_app()</code> poteva creare schema e seed. Era utile mentre studiavamo ORM e test. Nel runtime finale separiamo le responsabilita:</p>

```text
python -m app.prepare
        ↓
create schema + seed idempotente

python -m uvicorn app.main:app ...
        ↓
serve request, NON prepara il database
```

<p align="justify">Questa separazione rende significativa la readiness: un processo puo essere vivo ma non ancora pronto.</p>

---

## 4. Liveness != readiness

### Liveness

<p align="justify">Domanda:</p>

<blockquote>
<p align="justify">il processo applicativo risponde?</p>
</blockquote>

```http
GET /health
200 OK
```

<p align="justify">La liveness <strong>non deve interrogare il database</strong>. Se il DB e giu ma il processo Python e vivo, <code>/health</code> resta 200.</p>

### Readiness

<p align="justify">Domanda:</p>

<blockquote>
<p align="justify">il servizio puo usare la dipendenza necessaria per servire il suo contratto?</p>
</blockquote>

```http
GET /ready
200 OK
```

<p align="justify">Nel nostro baseline readiness esegue una query minima sulla tabella <code>posts</code>.</p>

<p align="justify">Se schema/database non sono pronti:</p>

```http
GET /ready
503 Service Unavailable
```

<p align="justify">La risposta di errore e generica: non esponiamo path locali, stack trace o connection string.</p>

---

## 5. Il contratto di prodotto non cambia

<p align="justify">Mirror 04 conserva:</p>

```text
GET   /api/posts
POST  /api/posts        -> 201 + Location
PATCH /api/posts/{id}
missing                 -> 404
invalid payload         -> 422
```

<p align="justify">Aggiungiamo solo endpoint <strong>operativi</strong>:</p>

```text
GET /health
GET /ready
```

<p align="justify">Questa distinzione e importante: operazionalizzare un servizio non significa inventare nuove feature di prodotto.</p>

---

<a id="lesson-runtime-lifecycle"></a>
## 6. Lifespan: cleanup dell'Engine

<p align="justify">FastAPI puo possedere risorse con un lifespan:</p>

```python
@asynccontextmanager
async def lifespan(app):
    yield
    app.state.engine.dispose()
```

<p align="justify">L'Engine nasce nel composition root e viene chiuso quando termina l'app. Non apriamo Session globali condivise.</p>

### Arresto controllato

<p align="justify">Un deploy o un riavvio non dovrebbe interrompere il processo come se mancasse improvvisamente corrente. Il percorso mentale e:</p>

```text
segnale di arresto
  -> il servizio smette di accettare nuovo lavoro
  -> completa o interrompe entro un limite il lavoro in corso
  -> chiude Engine e altre risorse possedute
  -> termina il processo
```

<p align="justify">Uvicorn gestisce i segnali del processo e FastAPI esegue la parte successiva a <code>yield</code> nel lifespan. Il nostro compito e mettere li un cleanup rapido, idempotente e limitato: niente nuovi job, niente attese infinite. Durante l'arresto la readiness deve smettere di promettere nuovo traffico prima che il processo scompaia.</p>

---

## 7. Uvicorn: processo, non funzione magica

<p align="justify">Baseline didattica production-like:</p>

```bash
python -m app.prepare
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --workers 1
```

<p align="justify"><code>--reload</code> e utile nello sviluppo, ma non fa parte del runbook production-like.</p>

### Log minimi e osservabilita

<p align="justify"><code>/health</code> e <code>/ready</code> rispondono a domande puntuali; i log spiegano cosa e accaduto nel tempo. Per ogni request ci servono almeno metodo, percorso, status e durata, insieme a un identificatore di correlazione quando disponibile. Gli errori devono conservare il contesto tecnico lato server senza restituire stack trace o segreti al client.</p>

<p align="justify">Preferiamo record strutturati e stabili a frasi casuali:</p>

```text
level=INFO event=http_request method=GET path=/api/posts status=200 duration_ms=8
level=ERROR event=db_unavailable path=/ready error_type=OperationalError
```

<p align="justify">Non registriamo password, cookie di sessione, token, connection string o body sensibili. Metriche distribuite, tracing e piattaforme di osservabilita restano fuori dal core; il requisito attuale e lasciare evidenze utili e sicure per diagnosticare avvio, request, readiness e shutdown.</p>

<p align="justify">Per questo corso non introduciamo ancora:</p>

<ul>
  <li>reverse proxy;</li>
  <li>TLS termination;</li>
  <li>process manager;</li>
  <li>multi-worker orchestration;</li>
  <li>Docker Compose;</li>
  <li>Kubernetes;</li>
  <li>PostgreSQL;</li>
  <li>Alembic;</li>
  <li>async ORM.</li>
</ul>

<p align="justify">Sono argomenti validi, ma allargherebbero il perimetro invece di chiudere UDA26.</p>

---

<a id="lesson-runtime-evidence"></a>
## 8. Live process probe

<p align="justify"><code>TestClient</code> attraversa il boundary HTTP dell'app, ma non prova che Uvicorn parta davvero.</p>

<p align="justify">Il capstone aggiunge un probe che:</p>

<ol>
  <li>sceglie una porta locale libera;</li>
  <li>prepara un database temporaneo;</li>
  <li>avvia Uvicorn come subprocess;</li>
  <li>attende <code>/health</code> con timeout limitato;</li>
  <li>verifica <code>/ready</code> e <code>GET /api/posts</code> via HTTP reale;</li>
  <li>termina il processo anche in caso di errore.</li>
</ol>

<p align="justify">Il probe non dorme "a caso" per dieci secondi: usa retry brevi con deadline.</p>

---

## 9. Evidence bundle deterministico

<p align="justify">Una consegna tecnica deve poter dire <strong>cosa e stato verificato</strong>.</p>

<p align="justify">Il capstone genera:</p>

```text
evidence/
├── manifest.json
├── openapi.json
└── SHA256SUMS.txt
```

<p align="justify">Il manifest contiene solo dati riproducibili:</p>

<ul>
  <li>milestone;</li>
  <li>versione Content Pack;</li>
  <li>build SHA dichiarata;</li>
  <li>contratti verificati;</li>
  <li>nomi dei file evidence.</li>
</ul>

<p align="justify">Non contiene:</p>

<ul>
  <li>timestamp;</li>
  <li>PID;</li>
  <li>porta casuale;</li>
  <li>path temporanei;</li>
  <li>connection string;</li>
  <li>secret.</li>
</ul>

<p align="justify"><code>SHA256SUMS.txt</code> permette di verificare l'integrita dei file.</p>

---

## 10. Runbook minimo

<p align="justify">Un runbook utile deve permettere a un'altra persona di ripetere il flusso:</p>

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

<p align="justify">Non scriviamo "avvia il server normalmente". Scriviamo i comandi reali.</p>

### Handoff operativo

<p align="justify">La consegna e completa quando una persona che non ha scritto il codice puo rispondere, usando il runbook, a queste domande:</p>

<ul>
  <li>quali variabili sono obbligatorie e quali valori sono solo di sviluppo?</li>
  <li>quale comando prepara lo stato persistente e puo essere ripetuto senza danni?</li>
  <li>quale comando avvia il processo e su quale indirizzo ascolta?</li>
  <li>come distinguo processo vivo, servizio pronto e API funzionante?</li>
  <li>dove trovo i log e quali dati sensibili non devono comparire?</li>
  <li>come fermo il processo e come verifico che le risorse siano state chiuse?</li>
  <li>quali test ed evidence identificano esattamente la build consegnata?</li>
</ul>

<p align="justify">Questo checklist trasforma il deploy da "funziona sul mio computer" a procedura osservabile e ripetibile.</p>

---

## 11. Capstone: evidence, non nuove feature

<p align="justify">Il capstone finale deve dimostrare insieme:</p>

<ul>
  <li>configurazione development/production;</li>
  <li>fail-fast production;</li>
  <li>prepare esplicito e idempotente;</li>
  <li>liveness senza dipendenza DB;</li>
  <li>readiness con dipendenza DB reale;</li>
  <li>contratto posts invariato;</li>
  <li>persistenza dopo restart;</li>
  <li>processo Uvicorn reale;</li>
  <li>evidence bundle deterministico;</li>
  <li>runbook e limiti dichiarati.</li>
</ul>

<p align="justify">Questa e una chiusura architetturale: <strong>il sistema non e solo scritto; e verificabile e ripetibile</strong>.</p>

---

## 12. Cosa resta deliberatamente fuori

<p align="justify">Alla fine di UDA26 non aggiungiamo:</p>

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

<p align="justify">Queste scelte possono diventare corsi, moduli o roadmap future. Non sono prerequisiti per dimostrare il boundary runtime fondamentale.</p>

---

## Definition of Done UDA26

<p align="justify">UDA26 e chiusa quando:</p>

<ul>
  <li>Content Pack registra tutti e quattro i slice;</li>
  <li>Activity A-F del closeout sono valide;</li>
  <li>Activity B config passa il runner Python TheBitLab;</li>
  <li>health/readiness reference passa su Linux e Windows;</li>
  <li>il capstone mantiene i test HTTP/restart precedenti;</li>
  <li>un processo Uvicorn reale viene avviato e verificato in CI;</li>
  <li>l'evidence bundle e deterministico e checksum-verificabile;</li>
  <li>la regression suite completa resta verde;</li>
  <li>il corso rimane a 33 settimane e UDA26 a 4 settimane.</li>
</ul>
