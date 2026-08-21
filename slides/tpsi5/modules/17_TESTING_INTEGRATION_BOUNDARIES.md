---
marp: true
paginate: true
size: 16:9
title: 17 — Testing strategy e integration boundaries
---

# 17 — Testing strategy
## Evidenze affidabili senza test fragili

UDA 26 — Python mirror

---

# Richiamo

Abbiamo cambiato:

- framework;
- repository;
- database abstraction.

Come dimostriamo che il contratto resta corretto?

> Non basta che “sembri funzionare”.

---

# Obiettivi

Alla fine dovrai saper:

- distinguere unit, integration, contract e process smoke;
- scegliere il boundary da testare;
- usare fixture isolate;
- usare `tmp_path` per database temporanei;
- evitare mock che nascondono l'integrazione reale;
- leggere un failure come evidenza di un confine rotto.

---

# Piramide? Meglio partire dal rischio

Non chiedere solo:

> “Quanti unit test devo avere?”

Chiedi:

> “Quale comportamento importante potrebbe rompersi e quale test lo dimostra davvero?”

---

# Unit test

Testa una funzione/classe in isolamento quando il comportamento è locale.

Esempio:

```py
def test_parse_environment_rejects_unknown_value():
    ...
```

Veloce e preciso.

---

# Integration test

Testa componenti reali insieme.

Esempio:

```text
FastAPI
→ repository SQLAlchemy
→ SQLite temporaneo
```

Serve quando il rischio vive proprio nell'integrazione.

---

# Contract test

Verifica ciò che un consumer osserva.

```py
response = client.post('/posts', json={'text': 'Ciao'})
assert response.status_code == 201
assert response.json()['text'] == 'Ciao'
```

Il test non dipende da come la route è implementata internamente.

---

# Fixture isolate

```py
@pytest.fixture
def db_path(tmp_path):
    return tmp_path / 'test.db'
```

Ogni test deve partire da uno stato prevedibile.

Condividere database tra test crea dipendenze invisibili.

---

# Function-scoped fixture

Quando una fixture contiene stato mutabile, un lifecycle per test riduce interferenze.

```text
test A -> ambiente A

test B -> ambiente B
```

---

# Restart persistence test

Questo test attraversa un boundary importante:

1. app A crea dato;
2. app A si chiude;
3. app B usa lo stesso DB;
4. dato ancora presente.

Mockare il repository renderebbe il test inutile per questa domanda.

---

# Mock: quando aiuta

Un mock può essere utile per:

- dipendenza remota costosa;
- failure difficile da produrre;
- unit test locale.

Ma se stai testando l'integrazione DB, sostituire il DB con un mock elimina proprio il rischio da verificare.

---

# Errore tipico: test dell'implementazione

Fragile:

```text
“la funzione X deve essere chiamata esattamente due volte”
```

se ciò non è parte del contratto osservabile.

Più robusto:

```text
“la request produce status/body/stato persistente corretti”
```

---

# Checkpoint

Quale test useresti per:

1. parser di config;
2. response `POST /posts`;
3. persistenza dopo restart;
4. comportamento con database reale;
5. processo Uvicorn che parte davvero.

---

# Feisbuc mirror 03

Obiettivo: raccogliere evidenza a più livelli:

```text
function
repository + DB
HTTP contract
restart persistence
process boundary
```

---

# Handoff al laboratorio

1. costruisci una fixture isolata;
2. usa `tmp_path`;
3. scrivi un integration test reale;
4. rimuovi un mock che nasconde il boundary;
5. spiega quale rischio copre ogni test.

---

# Recap

Un buon test:

- osserva il comportamento giusto;
- controlla il boundary giusto;
- parte da stato riproducibile;
- fallisce per una ragione utile.

Prossimo modulo: **runtime, health/readiness, deploy e capstone**.