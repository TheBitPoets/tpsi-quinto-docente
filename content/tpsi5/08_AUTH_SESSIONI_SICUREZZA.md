<!--
content_id: tpsi5-content-auth-sessions-security
status: draft
curriculum_reference: TPSI quinto - autenticazione, sessioni e sicurezza web
technical_sources: NIST SP 800-63B, OWASP Password Storage/Session Management/CSRF, MDN cookies, Node crypto, Express 5
transformation: original-course-material
-->

# Autenticazione, sessioni e autorizzazione: identita affidabile nel backend

## Obiettivi

Al termine del modulo lo studente deve saper:

- distinguere **identificazione**, **autenticazione** e **autorizzazione**;
- spiegare perche una password non si salva in chiaro e non si cifra reversibilmente;
- applicare una policy password moderna senza regole di composizione arbitrarie;
- descrivere salt, password hashing adattivo e confronto a tempo costante;
- usare `crypto.scrypt`, `randomBytes` e `timingSafeEqual` nel backend Node;
- distinguere sessione server-side, session ID e cookie;
- generare un session ID opaco e imprevedibile e conservare nel DB solo il suo hash;
- configurare cookie di sessione con `HttpOnly`, `Secure`, `SameSite` e `Path` motivati;
- spiegare session fixation, scadenza e invalidazione al logout;
- applicare controlli same-origin/CSRF alle richieste che modificano stato;
- implementare un middleware `requireAuth`;
- applicare authorization **server-side** alla proprieta di una risorsa;
- evitare user enumeration e fiducia nei dati di identita inviati dal client;
- evolvere Feisbuc da `author = "Studente"` a una identita autenticata persistente.

## Prerequisiti

- HTTP, cookie/header e same-origin;
- `fetch` e REST;
- Node.js, Express 5, middleware e Router;
- SQL raw, constraint, prepared statement e repository;
- Feisbuc milestone 6 con `SqlPostStore`.

---

# Problema iniziale

Nella milestone 6 il client puo pubblicare un post, ma il backend non sa davvero **chi** stia operando.

```text
POST /api/posts
{
  "text": "Ciao"
}
```

Il server usava un autore convenzionale:

```text
author = "Studente"
```

Una scorciatoia ingenua sarebbe accettare:

```json
{
  "authorId": "utente-123",
  "text": "Ciao"
}
```

ma questo non autentica nessuno.

Un client malevolo potrebbe inviare:

```json
{
  "authorId": "id-del-docente",
  "text": "Messaggio falso"
}
```

La regola che guida tutta l'UDA e:

> **l'identita usata per autorizzare una operazione deve provenire da una prova verificata dal server, non da un campo scelto dal client.**

---

# 1. Identificazione, autenticazione, autorizzazione

Sono tre domande diverse.

## Identificazione

> Chi dichiari di essere?

Esempio:

```text
email = maria@example.test
```

## Autenticazione

> Riesci a dimostrare di essere quell'utente?

Nel nostro laboratorio:

```text
email + password
       ↓
verifica password hash
       ↓
identita autenticata
```

## Autorizzazione

> Ora che so chi sei, puoi fare **questa** operazione su **questa** risorsa?

```text
utente autenticato
       ↓
post.authorId === user.id ?
       ↓
DELETE consentita / negata
```

Autenticazione non implica autorizzazione.

Un utente autenticato puo non avere il diritto di cancellare il post di un altro utente.

---

# 2. Threat model minimo

Prima del codice elenchiamo cosa non vogliamo permettere.

| Minaccia | Esempio | Contromisura didattica |
| --- | --- | --- |
| furto DB | dump della tabella `users` | password hash adattivo + salt |
| password guessing offline | milioni di tentativi | `scrypt` costoso |
| session prediction | token `user-12` | `randomBytes(32)` |
| furto token via JS | `document.cookie` | `HttpOnly` |
| invio token in HTTP di produzione | rete non cifrata | `Secure` + HTTPS |
| cross-site request | pagina terza invia POST | `SameSite` + same-origin checks |
| session fixation | token scelto prima del login riutilizzato | nuova sessione dopo login |
| user enumeration | messaggi login diversi | `invalid-credentials` generico |
| identity spoofing | `authorId` nel body | identita da `req.auth.user` |
| IDOR | DELETE di risorsa altrui | authorization server-side |
| SQL injection | email concatenata in query | prepared statements |
| token rubato dal DB | session ID salvato in chiaro | hash del session token nel DB |

Il modello non rende Feisbuc una banca. Serve a costruire abitudini corrette e confini verificabili.

---

# 3. Password policy moderna

## 3.1 Lunghezza prima della complessita artificiale

Per un'autenticazione a singolo fattore adottiamo nel corso:

```text
minimo 15 caratteri
massimo accettato 128 caratteri
```

Non imponiamo:

```text
almeno una maiuscola
almeno un numero
almeno un simbolo
cambio ogni 30 giorni
```

come regole automatiche del laboratorio.

Esempio valido:

```text
la pizza sul mare di sera
```

puo essere migliore di una password corta costruita solo per soddisfare una regex.

## 3.2 Unicode e lunghezza

In JavaScript:

```js
Array.from(password).length
```

conta i code point in modo piu utile di affidarsi ciecamente ai code unit UTF-16 per la policy didattica.

## 3.3 Validazione non e hashing

```text
policy
  ↓
password accettabile come input?

hashing
  ↓
come la memorizziamo in modo resistente?
```

Sono responsabilita separate.

---

# 4. Mai password in chiaro

Schema sbagliato:

```sql
CREATE TABLE users (
  email TEXT,
  password TEXT
);
```

Insert sbagliato:

```sql
INSERT INTO users(email, password)
VALUES(?, ?);
```

se `?` e la password originale.

Se il DB viene letto, tutte le password sono immediatamente disponibili.

---

# 5. Hashing, salt e funzione adattiva

Non ci serve poter ricostruire la password.

Ci serve verificare:

```text
password candidata
       ↓
stesso KDF + stesso salt
       ↓
derived key
       ↓
confronto con hash memorizzato
```

## 5.1 Perche non SHA-256(password)

Una funzione hash generale e intenzionalmente veloce.

Per le password vogliamo invece una funzione il cui costo renda piu caro un attacco offline.

Nel laboratorio usiamo **scrypt**, disponibile nel modulo `node:crypto`, senza dipendenza npm.

## 5.2 Parametri del corso

Useremo una delle configurazioni scrypt indicate come baseline da OWASP:

```text
N = 2^14
r = 8
p = 5
```

con salt casuale da 16 byte e derived key da 32 byte.

Il formato salvato sara auto-descrittivo:

```text
scrypt$16384$8$5$<salt-base64url>$<hash-base64url>
```

Se domani cambiamo costo, ogni hash conserva i parametri con cui e stato creato.

## 5.3 Hash asincrono

```js
import { promisify } from "node:util";
import { scrypt } from "node:crypto";

const derive = promisify(scrypt);

const key = await derive(password, salt, 32, {
  cost: 2 ** 14,
  blockSize: 8,
  parallelization: 5,
  maxmem: 64 * 1024 * 1024,
});
```

Usiamo la variante asincrona per non bloccare volontariamente il thread JavaScript durante una operazione costosa.

## 5.4 Salt casuale

```js
import { randomBytes } from "node:crypto";

const salt = randomBytes(16);
```

Due utenti con la stessa password devono normalmente ottenere hash diversi.

## 5.5 Confronto

Per confrontare byte segreti usiamo:

```js
timingSafeEqual(actual, expected)
```

solo dopo avere verificato che i Buffer abbiano la stessa lunghezza.

---

# 6. Register

Pipeline:

```text
POST /api/auth/register
       ↓
Content-Type JSON
       ↓
validation email/password/displayName
       ↓
normalize email
       ↓
email gia esistente?
       ↓ no
hashPassword(password)
       ↓
INSERT users
       ↓
crea nuova sessione
       ↓
Set-Cookie
       ↓
201 user pubblico
```

La response **non** contiene:

```text
password
passwordHash
session hash
```

---

# 7. Login senza user enumeration

Errore da evitare:

```text
email inesistente   -> "utente non trovato"
password sbagliata  -> "password errata"
```

Queste differenze permettono di verificare quali account esistano.

Nel laboratorio la response pubblica e la stessa:

```json
{
  "error": {
    "code": "invalid-credentials",
    "message": "Credenziali non valide."
  }
}
```

Il flusso e:

```text
POST /api/auth/login
       ↓
lookup email
       ↓
verifyPassword
       ↓
crea SEMPRE una nuova sessione dopo login riuscito
       ↓
Set-Cookie
```

La nuova sessione evita di promuovere un eventuale identificatore pre-autenticazione in una sessione autenticata.

---

# 8. Sessioni server-side

Dopo il login non vogliamo reinviare la password a ogni request.

Creiamo una sessione:

```text
browser                    server / DB

session token  ──────────>  hash(token)
nel cookie                  user_id
                            expires_at
```

## 8.1 Token opaco

```js
randomBytes(32).toString("base64url")
```

32 byte = 256 bit casuali prima della codifica.

Il token non contiene:

```text
user id
email
ruolo
timestamp leggibile
```

E un riferimento opaco.

## 8.2 Perche hashare anche il session token nel DB

Se salvassimo:

```text
sessions.token = token-cookie
```

un dump DB fornirebbe sessioni immediatamente utilizzabili.

Nel corso salviamo:

```js
sha256(token)
```

Nel browser resta il token originale; nel DB resta soltanto l'impronta usata per la ricerca.

---

# 9. Cookie di sessione

Per lo stesso token:

```text
Cookie: feisbuc.sid=<opaque-token>
```

in produzione vogliamo attributi espliciti:

```text
HttpOnly
Secure
SameSite=Strict
Path=/
```

## `HttpOnly`

Il cookie non deve essere leggibile da `document.cookie`.

Il browser continua comunque a inviarlo nelle request HTTP appropriate.

## `Secure`

In produzione il cookie deve viaggiare solo su HTTPS.

Il laboratorio locale HTTP deve poter girare anche sui PC della scuola; quindi distinguiamo configurazione development e production invece di fingere TLS dove non esiste.

## `SameSite=Strict`

Per Feisbuc same-origin scegliamo `Strict`.

Serve come difesa contro molte request cross-site, ma **non e l'unica difesa CSRF**.

## `Path=/`

La sessione serve all'intera applicazione.

## Prefisso `__Host-`

In produzione il nome preferito e:

```text
__Host-feisbuc.sid
```

che richiede `Secure`, `Path=/` e nessun `Domain`.

---

# 10. Development e production non sono la stessa cosa

Configurazione development:

```text
NODE_ENV=development
COOKIE_SECURE=false
cookieName=feisbuc.sid
```

Configurazione production:

```text
NODE_ENV=production
COOKIE_SECURE=true
cookieName=__Host-feisbuc.sid
HTTPS davanti all'app
```

Regola fail-closed del corso:

> se `NODE_ENV=production` e `COOKIE_SECURE` non e `true`, il server non parte.

Una configurazione insicura non deve diventare silenziosamente la produzione.

---

# 11. Parsing del cookie

Per capire il protocollo non aggiungiamo subito `cookie-parser`.

Header:

```http
Cookie: theme=dark; feisbuc.sid=abc123
```

Il middleware estrae soltanto il cookie necessario.

La lettura del cookie non autentica ancora l'utente:

```text
cookie token
   ↓
sha256(token)
   ↓
SELECT session non scaduta
   JOIN user
   ↓
req.auth.user
```

---

# 12. Middleware di autenticazione

Vogliamo distinguere due responsabilita.

## `loadAuth`

Prova a caricare una identita.

```js
req.auth = {
  user: null,
  sessionHash: null,
};
```

oppure:

```js
req.auth = {
  user: { id, email, displayName },
  sessionHash,
};
```

## `requireAuth`

Decide se una route richiede autenticazione.

```js
export function requireAuth(req, res, next) {
  if (!req.auth?.user) {
    next(new HttpError(401, "authentication-required", "Autenticazione richiesta."));
    return;
  }
  next();
}
```

`401` significa che manca una autenticazione valida.

---

# 13. Autorizzazione: il server decide

Il client puo nascondere il bottone Delete per UX.

Ma la sicurezza non puo essere:

```js
if (!isOwner) deleteButton.hidden = true;
```

Un attaccante puo inviare la request direttamente.

La route deve verificare:

```text
req.auth.user.id
       vs
post.author_id nel DB
```

Esempio:

```text
DELETE /api/posts/p123
```

possibili risultati:

```text
204  utente proprietario
403  autenticato ma non proprietario
404  post inesistente
401  sessione assente/non valida
```

---

# 14. Mai fidarsi di `authorId` nel body

Route sbagliata:

```js
postStore.create({
  text: req.body.text,
  authorId: req.body.authorId,
});
```

Route corretta:

```js
postStore.create({
  text,
  authorId: req.auth.user.id,
});
```

L'identita viene dal contesto autenticato.

---

# 15. Schema relazionale della milestone 7

```text
users
├── id PK
├── email UNIQUE
├── display_name
├── password_hash
└── created_at

sessions
├── id_hash PK
├── user_id FK -> users.id
├── created_at
└── expires_at

posts
├── id PK
├── author_id FK -> users.id
├── text
├── likes
├── liked
└── created_at
```

Relazioni:

```text
users 1 ───── N sessions
users 1 ───── N posts
```

Non salviamo `author` come stringa duplicata nel post.

Per la response:

```sql
SELECT
  posts.id,
  posts.author_id,
  users.display_name AS author,
  posts.text,
  posts.likes,
  posts.liked
FROM posts
JOIN users ON users.id = posts.author_id;
```

---

# 16. Prepared statements anche nell'autenticazione

Mai:

```js
`SELECT * FROM users WHERE email = '${email}'`
```

Sempre binding:

```js
db.prepare(`
  SELECT id, email, display_name, password_hash
  FROM users
  WHERE email = ?
`).get(email)
```

Email, session hash, user id e post id sono tutti input da trattare come dati.

---

# 17. Scadenza server-side

Una sessione ha una scadenza reale nel DB:

```text
expires_at = Date.now() + SESSION_TTL_MS
```

La query valida solo:

```sql
WHERE sessions.expires_at > ?
```

Una sessione scaduta non diventa valida solo perche il browser conserva ancora un cookie.

Il laboratorio usa una TTL di 8 ore come valore didattico configurabile.

---

# 18. Logout

Logout significa due operazioni:

```text
1. DELETE session dal DB
2. Set-Cookie che cancella il cookie browser
```

Fare solo:

```text
clear cookie
```

lascia il token eventualmente copiato valido server-side.

Fare solo:

```text
delete DB row
```

lascia un cookie inutile nel browser.

Servono entrambe.

---

# 19. Cache delle response auth

Le response che impostano o descrivono sessioni non devono essere trattate come normali contenuti cacheabili.

Nel modulo usiamo:

```http
Cache-Control: no-store
```

per `/api/auth/*` e per le response private principali.

---

# 20. CSRF: perche SameSite non chiude il discorso

Il browser invia automaticamente i cookie nelle request che rispettano le regole del cookie.

Questo e comodo per le sessioni, ma introduce il problema CSRF.

Nel laboratorio applichiamo defense in depth:

```text
SameSite=Strict
      +
controllo Sec-Fetch-Site quando presente
      +
controllo Origin quando presente
```

Per metodi unsafe:

```text
POST
PUT
PATCH
DELETE
```

una request browser dichiaratamente `cross-site` viene rifiutata.

Questa non e una scusa per inventare un CORS permissivo.

---

# 21. CORS non e autenticazione e non e CSRF protection completa

Tre concetti distinti:

```text
CORS
  -> quali response cross-origin possono essere lette dal browser

autenticazione
  -> chi e l'utente

CSRF defense
  -> impedire uso involontario delle credenziali browser su request mutate
```

Non risolviamo auth aggiungendo:

```js
app.use(cors({ origin: "*" }));
```

---

# 22. Il token non va in `localStorage`

Nella milestone 3 abbiamo usato `localStorage` per **dati applicativi non sensibili**.

Non riutilizziamo quel pattern per la sessione.

No:

```js
localStorage.setItem("token", token);
```

La sessione viaggia in cookie `HttpOnly` e il JavaScript client non deve conoscerne il valore.

Il client chiede:

```text
GET /api/auth/me
```

e riceve l'utente pubblico.

---

# 23. API auth della milestone 7

```text
POST /api/auth/register
POST /api/auth/login
GET  /api/auth/me
POST /api/auth/logout
```

Contratto pubblico utente:

```json
{
  "id": "...",
  "email": "maria@example.test",
  "displayName": "Maria"
}
```

Mai:

```json
{
  "passwordHash": "..."
}
```

---

# 24. API post della milestone 7

Le route esistenti rimangono, ma richiedono auth:

```text
GET    /api/posts
POST   /api/posts
PATCH  /api/posts/:id
DELETE /api/posts/:id
```

Il nuovo `DELETE` serve a rendere osservabile l'autorizzazione per ownership.

Response post:

```json
{
  "id": "p1",
  "authorId": "u1",
  "author": "Maria",
  "text": "Ciao",
  "likes": 0,
  "liked": false
}
```

---

# 25. Feisbuc milestone 7

Prima:

```text
browser
  -> API
  -> Express
  -> SqlPostStore
  -> SQLite
```

Ora:

```text
browser
  -> register/login
  -> HttpOnly session cookie
  -> loadAuth
  -> requireAuth
  -> Router
  -> authorization
  -> SqlPostStore + SqlAuthStore
  -> SQLite
```

Il cambiamento fondamentale e:

```text
"autore scelto dal codice/client"
              ↓
"autore derivato dalla sessione verificata"
```

---

# 26. Error model auth

Esempi:

```text
400 registration-invalid
401 invalid-credentials
401 authentication-required
403 forbidden
409 email-already-registered
```

Login usa intenzionalmente un errore generico:

```text
invalid-credentials
```

sia per email inesistente sia per password errata.

---

# 27. Cosa non entra ancora

Questa UDA non deve diventare un corso completo di identity management.

Rimandiamo:

```text
password reset
email verification
MFA / passkey
OAuth / OIDC
social login
SSO
RBAC complesso
refresh token/JWT architecture
rate limiting distribuito
account lockout avanzato
```

Verranno richiamati nel track advanced/security.

---

# 28. Perche non JWT adesso

Il nostro problema e:

```text
browser same-origin
backend Express
sessione applicativa
```

Una sessione server-side opaca ci permette di studiare bene:

- cookie;
- revoca;
- expiry;
- session fixation;
- DB lookup;
- authorization.

Aggiungere JWT qui aumenterebbe i concetti senza risolvere un requisito reale della milestone.

---

# 29. Errori frequenti

## Password in chiaro

```sql
password TEXT
```

con valore originale.

## Hash veloce singolo

```js
sha256(password)
```

## Salt fisso

```js
const salt = "feisbuc";
```

## Session ID prevedibile

```js
const sid = user.id;
```

## Session token nel localStorage

```js
localStorage.setItem("sid", token);
```

## Cookie senza HttpOnly

```text
Set-Cookie: sid=...
```

## `Secure=false` in produzione

configurazione che deve fallire, non essere tollerata.

## Identita dal body

```js
const authorId = req.body.authorId;
```

## Autorizzazione solo nella UI

```js
button.hidden = !owned;
```

senza controllo route.

## DELETE senza ownership check

```js
postStore.delete(req.params.id);
```

## Messaggi di login enumerabili

```text
email non registrata
```

## Sessione mai invalidata

record DB che vive per sempre.

---

# 30. Esercizi A-F

## A — osserva/modifica

Implementa la policy credenziali pura: normalizzazione email e password 15–128, senza regole di composizione.

## B — modifica controllata

Implementa una funzione pura di authorization su post: read/like per utente autenticato, delete/edit solo per owner.

## C — implementazione autonoma

**Feisbuc milestone 7**: integra `users`, password hashing, session store, cookie, auth Router, `requireAuth` e ownership.

## D — debugging/diagnosi

Analizza un backend deliberatamente vulnerabile: password plaintext, sid prevedibile, cookie debole, identity spoofing, authorization client-side.

## E — mini-progetto

Aggiungi una pagina profilo autenticata e una route di modifica display name con re-authentication progettata sulla carta prima dell'implementazione.

## F — prodotto integrato

Esegui una security review della milestone Feisbuc: asset, trust boundaries, attacchi, controlli, evidence e debiti residui.

---

# 31. Laboratorio

Sequenza consigliata:

```text
A policy credenziali autograded
      ↓
B authorization pura autograded
      ↓
C Feisbuc auth/session E2E
      ↓
D security debugging + review
```

Il laboratorio C deve provare realmente:

```text
register
login
me
create authenticated post
ownership delete
403 su post altrui
logout
session invalidation
session persistence dopo restart
password non plaintext
session token non plaintext nel DB
cookie flags
```

---

# 32. Verifica rapida

1. Identificazione e autenticazione sono la stessa cosa?
2. Perche SHA-256 diretto non e un password KDF adeguato?
3. A cosa serve il salt?
4. Perche il session token deve essere casuale?
5. Perche nel DB salviamo il suo hash?
6. `HttpOnly` impedisce al browser di inviare il cookie?
7. `SameSite` elimina ogni rischio CSRF?
8. Chi deve determinare `authorId`: client o server?
9. Qual e la differenza fra `401` e `403` nel nostro modello?
10. Perche una sessione deve essere eliminata server-side al logout?

---

# 33. Sintesi inclusiva

```text
PASSWORD
  non si salva
  -> si deriva un hash lento con salt

LOGIN
  verifica password
  -> crea nuova sessione casuale

COOKIE
  contiene solo session token opaco
  -> HttpOnly
  -> SameSite
  -> Secure in produzione

SERVER
  hash(token)
  -> sessione DB
  -> user verificato

AUTHORIZATION
  user verificato + risorsa
  -> il SERVER decide
```

La frase da ricordare e:

> **Il client puo dichiarare un'intenzione; soltanto il server puo stabilire l'identita e autorizzare l'effetto.**

---

# Fonti e collegamenti

- NIST SP 800-63B — password authenticator requirements;
- OWASP Password Storage Cheat Sheet — Argon2id/scrypt e parametri;
- OWASP Session Management Cheat Sheet — session ID e cookie security;
- OWASP CSRF Prevention Cheat Sheet — `SameSite` come defense in depth;
- MDN `Set-Cookie` e HTTP cookies;
- Node.js `node:crypto`: `scrypt`, `randomBytes`, `timingSafeEqual`;
- Express 5 documentation: Router, middleware e `res.cookie`;
- `07_SQL_RAW_PERSISTENCE.md` — schema/prepared statements/repository;
- `06_NODE_EXPRESS_BACKEND.md` — pipeline Express e middleware.

---

# Activity correlate

- `tpsi5-activity-a-auth-credential-policy-001`;
- `tpsi5-activity-b-auth-post-authorization-001`;
- `tpsi5-activity-c-feisbuc-auth-session-001`;
- `tpsi5-activity-d-debug-auth-security-001`.
