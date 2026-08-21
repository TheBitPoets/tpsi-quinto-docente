---
marp: true
paginate: true
size: 16:9
title: 00 — Architettura didattica del corso Full Stack
---

# 00 — Architettura del corso Full Stack
## Dal browser al servizio verificabile

TPSI quinto — Full Stack Web Developer 2026/27

---

# Domanda iniziale

Quando apriamo una pagina web e premiamo **Pubblica**, quante cose diverse succedono davvero?

- browser;
- rete;
- server;
- database;
- identità;
- aggiornamento della UI;
- eventualmente realtime.

> Obiettivo: smettere di vedere “il sito” come un blocco unico.

---

# Obiettivi della lezione

Alla fine dovrai saper:

- distinguere frontend, protocollo, backend e database;
- spiegare il ruolo di HTTP;
- riconoscere un **boundary**;
- descrivere la progressione del progetto Feisbuc;
- capire perché studiamo prima i concetti e poi i framework.

---

# Il modello mentale

```text
utente
  ↓
browser / UI
  ↓
HTTP
  ↓
backend
  ↓
data layer
  ↓
database
```

Più avanti aggiungeremo:

```text
sessione / auth
realtime
runtime / deploy
```

---

# Boundary: il concetto chiave

Un **boundary** è un confine tra responsabilità diverse.

Esempi:

- browser ↔ server;
- JSON ↔ oggetto di dominio;
- backend ↔ database;
- utente ↔ sessione;
- request/response ↔ evento realtime.

Quando qualcosa si rompe, il primo problema è capire **in quale boundary**.

---

# Perché non partire subito da Vue o Express?

Se partiamo dal framework rischiamo di imparare solo sintassi.

Il percorso fa invece:

```text
Web Platform
→ JavaScript/DOM
→ HTTP
→ Express
→ SQL
→ auth
→ Vue
→ realtime
```

Ogni astrazione arriva dopo il problema che risolve.

---

# Feisbuc: un solo progetto che cresce

Feisbuc non riparte da zero a ogni UDA.

```text
HTML statico
→ responsive
→ feed dinamico
→ client REST
→ API Express
→ SQLite
→ sessione/auth
→ SPA Vue
→ realtime
→ mirror Python
→ deploy/evidence
```

La domanda ricorrente sarà: **cosa abbiamo spostato o aggiunto?**

---

# Esempio: pubblicare un post

Versione iniziale:

```text
utente → form HTML → JavaScript → array in memoria → DOM
```

Versione full stack:

```text
utente
→ Vue
→ POST /posts
→ Express
→ validazione
→ repository SQL
→ SQLite
→ risposta JSON
→ UI aggiornata
```

---

# Errore tipico: “non funziona il sito”

Troppo generico.

Domande migliori:

- la request parte?
- quale status HTTP torna?
- il body è valido?
- il backend entra nella route?
- il repository scrive davvero?
- il database contiene la riga?
- il client aggiorna lo stato?

Il debugging è una ricerca del boundary rotto.

---

# Checkpoint

Per ciascun elemento, indica dove vive:

1. `button`;
2. `POST /posts`;
3. `INSERT INTO posts`;
4. cookie di sessione;
5. `socket.emit(...)`;
6. health endpoint.

Confronta la risposta con un compagno e giustificala.

---

# Come useremo il laboratorio

Ogni modulo contiene almeno una combinazione di:

- Activity di osservazione;
- modifica guidata;
- implementazione;
- debug;
- milestone Feisbuc.

Non basta ottenere l'output: dovrai saper spiegare **perché** è corretto.

---

# Recap

Tre idee da portare via:

1. full stack = responsabilità collegate, non “tante tecnologie”;
2. i confini sono più importanti della sintassi;
3. Feisbuc rende visibile come cambia l'architettura nel tempo.

Prossimo modulo: **Web Platform e HTML moderno**.