---
marp: true
paginate: true
size: 16:9
title: 18 — Runtime, deploy, health/readiness e capstone
---

# 18 — Runtime e deploy
## Dal codice funzionante a un servizio verificabile

UDA 26 — Capstone

---

# Richiamo

Finora abbiamo dimostrato che il codice funziona nei test.

Ultima domanda:

> sappiamo configurarlo, avviarlo, osservarlo e consegnarlo come processo reale?

---

# Obiettivi

Alla fine dovrai saper:

- separare configurazione dal codice;
- usare environment in modo fail-fast;
- distinguere prepare/prestart da app startup;
- distinguere liveness e readiness;
- avviare e verificare Uvicorn come processo reale;
- produrre evidence bundle riproducibile.

---

# Configurazione

Da evitare:

```py
DATABASE_URL = 'sqlite:///prod.db'
```

hardcoded nel codice per ogni ambiente.

Meglio leggere configurazione esplicita dall'ambiente.

---

# Dev / test / prod

Un'app può avere policy diverse:

```text
dev  -> default locale comodo

test -> risorsa isolata

prod -> configurazione richiesta esplicitamente
```

In produzione, valori critici mancanti devono fallire presto.

---

# Fail-fast

Meglio:

```text
startup -> errore chiaro: FEISBUC_DATABASE_URL mancante
```

che:

```text
app avviata -> failure ambigua alla prima request
```

---

# Prepare separato da startup

Operazioni come:

- creare schema;
- applicare preparazione;
- seed iniziale;

non dovrebbero essere effetti collaterali nascosti dell'import/app factory.

```text
prepare command
→ app start
```

---

# Liveness

Domanda:

> il processo HTTP è vivo?

Endpoint tipico:

```text
GET /health -> 200
```

Non deve necessariamente verificare ogni dipendenza esterna.

---

# Readiness

Domanda:

> il servizio è pronto a gestire traffico utile?

Esempio:

```text
GET /ready
→ verifica DB
→ 200 se pronto
→ errore se dipendenza critica non disponibile
```

---

# Health ≠ readiness

```text
processo vivo ma DB non raggiungibile
```

può significare:

- `/health` = OK;
- `/ready` = NOT READY.

Sono segnali diversi.

---

# Processo reale

TestClient non dimostra che il servizio sappia partire come processo.

Prova reale:

```text
uvicorn subprocess
→ porta disponibile
→ GET /health
→ GET /ready
→ terminazione controllata
```

---

# Evidence bundle

Una consegna riproducibile può includere:

- manifest;
- OpenAPI;
- checksum;
- output dei probe;
- identificatore commit/release.

Non basta dire “sul mio PC funziona”.

---

# Determinismo

Due build equivalenti dovrebbero produrre evidenze confrontabili.

Esempio:

```text
SHA256SUMS.txt
```

per verificare integrità degli artifact.

---

# Errore tipico: startup che prepara tutto di nascosto

Se importare `app` crea schema, seed e file, i test e il deploy diventano meno controllabili.

Separare:

```text
configuration
prepare
startup
runtime checks
```

rende il sistema più osservabile.

---

# Checkpoint

Classifica:

1. processo risponde HTTP;
2. database disponibile;
3. env var mancante;
4. creazione schema;
5. OpenAPI salvato;
6. checksum artifact.

Liveness? readiness? config? prepare? evidence?

---

# Feisbuc mirror 04 / capstone

```text
config
→ prepare
→ Uvicorn
→ health/readiness
→ API + DB
→ live probe
→ evidence bundle
```

Il prodotto non guadagna nuove feature: guadagna **operabilità verificabile**.

---

# Handoff al laboratorio

1. prova config dev/prod;
2. verifica fail-fast;
3. esegui prepare;
4. avvia processo Uvicorn;
5. prova `/health` e `/ready`;
6. genera/controlla evidence bundle.

---

# Capstone: cosa devi saper raccontare

Alla fine del corso devi saper spiegare:

- dove vive ogni responsabilità;
- quale contratto collega i componenti;
- come persiste il dato;
- come viene protetta l'identità;
- come cambia la UI;
- come arriva il realtime;
- come testi i boundary;
- come avvii e osservi il servizio.

---

# Chiusura

Il risultato finale non è solo una web app.

È la capacità di passare da:

```text
“ho scritto del codice”
```

a:

```text
“so spiegare, verificare e consegnare un sistema full stack”
```

Fine del percorso TPSI quinto 2026/27.