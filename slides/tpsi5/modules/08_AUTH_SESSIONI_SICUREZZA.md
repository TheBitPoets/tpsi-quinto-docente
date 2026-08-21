---
marp: true
paginate: true
size: 16:9
title: 08 — Autenticazione, sessioni e autorizzazione
---

# 08 — Autenticazione, sessioni e autorizzazione
## Identità affidabile nel backend

UDA 24 — Backend

---

# Richiamo

Abbiamo dati persistenti.

Ma se il client invia:

```json
{ "authorId": 7, "text": "Ciao" }
```

possiamo fidarci di `authorId`?

No: il client può mentire.

---

# Obiettivi

Alla fine dovrai saper:

- distinguere autenticazione e autorizzazione;
- spiegare perché le password non si salvano in chiaro;
- descrivere una sessione server-side;
- capire cookie e session ID;
- applicare ownership lato server;
- riconoscere trust boundary e rischi CSRF/sessione.

---

# Authn vs Authz

**Autenticazione (authn)**

> Chi sei?

**Autorizzazione (authz)**

> Puoi fare questa operazione?

Essere autenticati non significa poter modificare qualsiasi risorsa.

---

# Password

Mai salvare:

```text
password = "ciao123"
```

Si salva un derivato resistente:

```text
salt + password hash
```

Il server verifica la password calcolando e confrontando il risultato atteso.

---

# Salt

Due utenti con la stessa password non dovrebbero avere lo stesso valore memorizzato.

```text
password + salt casuale -> hash
```

Il salt non è segreto: serve a rendere uniche le derivazioni.

---

# Sessione server-side

Dopo il login:

```text
browser                     server
   |                          |
   | -- credentials --------> |
   | <--- session cookie ---- |
   |                          |
   | -- session id ---------> |
   |                          | -> user identity
```

Il cookie trasporta un identificatore opaco, non tutta l'identità affidabile.

---

# Cookie

Proprietà importanti:

- `HttpOnly`;
- `Secure` quando HTTPS;
- `SameSite`;
- scadenza/path adeguati.

Il cookie è un meccanismo di trasporto della sessione, non la sessione stessa.

---

# Identità server-side

Dopo il middleware auth:

```js
req.auth.user
```

La route dovrebbe derivare l'autore da lì, non da un campo libero del body.

```js
const authorId = req.auth.user.id;
```

---

# Ownership

Per modificare un post:

```text
utente autenticato
+ post esistente
+ post.owner_id == user.id
→ consentito
```

Altrimenti `403 Forbidden`.

---

# CSRF: perché esiste

Se il browser invia automaticamente cookie di sessione, un sito esterno può tentare di indurre una request indesiderata.

Difese possibili includono:

- SameSite policy;
- origin checks;
- token CSRF nei flussi che lo richiedono.

Il punto didattico: **fidarsi dell'identità non basta, bisogna fidarsi anche del contesto della request**.

---

# Logout e invalidazione

Logout non significa solo cancellare un elemento UI.

Il server deve invalidare la sessione.

```text
session id vecchio -> non più valido
```

---

# Errore tipico: sicurezza solo frontend

Una route protetta solo perché il bottone è nascosto non è protetta.

Il client può essere modificato.

La regola autorizzativa deve vivere nel server.

---

# Checkpoint

Quale status useresti?

1. login con password errata;
2. request senza sessione valida;
3. utente autenticato che prova a cancellare il post altrui;
4. post inesistente;
5. logout riuscito.

---

# Feisbuc milestone

Ora Feisbuc ha:

- utenti;
- password derivate;
- login;
- sessioni;
- cookie;
- ownership dei post;
- authn/authz lato server.

Il prossimo modulo confronterà rendering client e server senza cambiare questo modello.

---

# Handoff al laboratorio

Durante le Activity:

1. analizza una credential policy;
2. implementa/verifica ownership;
3. collega sessione a identità;
4. diagnostica una vulnerabilità di trust;
5. prova casi 401/403.

---

# Recap

Da ricordare:

- password ≠ password in chiaro;
- session ID ≠ identità dichiarata dal client;
- authn ≠ authz;
- ownership vive sul server;
- sicurezza è una proprietà dei boundary.

Prossimo modulo: **SSR e template server-side**.