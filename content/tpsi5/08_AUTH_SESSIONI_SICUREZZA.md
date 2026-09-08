<!--
content_id: tpsi5-content-auth-sessions-security
status: draft
curriculum_reference: TPSI quinto - autenticazione, sessioni e sicurezza web
technical_sources: NIST SP 800-63B, OWASP Password Storage/Session Management/CSRF, MDN cookies, Node crypto, Express 5
transformation: original-course-material
-->

# Autenticazione, sessioni e autorizzazione: identita affidabile nel backend

<table align="center" width="100%"><tr><td>
<details>
<summary>&#128506; <strong>Orientamento della lezione</strong></summary>

<p align="justify"><strong>Contesto:</strong> Feisbuc possiede ormai dati persistenti, ma il backend non sa ancora chi stia agendo. Questa lezione costruisce un'identità verificabile e la usa per prendere decisioni server-side.</p>
<p align="justify"><strong>Domande guida:</strong> come si verifica una password senza conservarla? Che rapporto c'è fra sessione, session ID e cookie? Perché nascondere un pulsante non equivale ad autorizzare?</p>
<p align="justify"><strong>Obiettivi osservabili:</strong> tracciare register e login, motivare hash e direttive cookie, derivare l'identità dalla sessione e applicare ownership e controlli CSRF alle mutazioni.</p>
<p align="justify"><strong>Prossimo passo:</strong> la lezione 09 riuserà identità, store e regole di authorization per produrre anche pagine HTML server-side.</p>

</details>
</td></tr></table>

## Obiettivi

<p align="justify">Al termine del modulo lo studente deve saper:</p>

<ul>
  <li>distinguere <strong>identificazione</strong>, <strong>autenticazione</strong> e <strong>autorizzazione</strong>;</li>
  <li>spiegare perche una password non si salva in chiaro e non si cifra reversibilmente;</li>
  <li>applicare una policy password moderna senza regole di composizione arbitrarie;</li>
  <li>descrivere salt, password hashing adattivo e confronto a tempo costante;</li>
  <li>usare <code>crypto.scrypt</code>, <code>randomBytes</code> e <code>timingSafeEqual</code> nel backend Node;</li>
  <li>distinguere sessione server-side, session ID e cookie;</li>
  <li>generare un session ID opaco e imprevedibile e conservare nel DB solo il suo hash;</li>
  <li>configurare cookie di sessione con <code>HttpOnly</code>, <code>Secure</code>, <code>SameSite</code> e <code>Path</code> motivati;</li>
  <li>spiegare session fixation, scadenza e invalidazione al logout;</li>
  <li>applicare controlli same-origin/CSRF alle richieste che modificano stato;</li>
  <li>implementare un middleware <code>requireAuth</code>;</li>
  <li>applicare authorization <strong>server-side</strong> alla proprieta di una risorsa;</li>
  <li>evitare user enumeration e fiducia nei dati di identita inviati dal client;</li>
  <li>evolvere Feisbuc da <code>author = "Studente"</code> a una identita autenticata persistente.</li>
</ul>

## Prerequisiti

<ul>
  <li>HTTP, cookie/header e same-origin;</li>
  <li><code>fetch</code> e REST;</li>
  <li>Node.js, Express 5, middleware e Router;</li>
  <li>SQL raw, constraint, prepared statement e repository;</li>
  <li>Feisbuc milestone 6 con <code>SqlPostStore</code>.</li>
</ul>

## Orientamento nella documentazione

<p align="center">
  <img src="../../assets/tpsi5/lesson-documentation-depth.svg" alt="La dispensa seleziona nelle fonti ufficiali i contenuti da studiare ora, riconoscere, rimandare o dichiarare fuori confine">
</p>

<table align="center"><tr><td>
<p align="justify"><strong><span style="font-size: 1.15em;">&#128279;</span> Percorso MDN — cookie e sessione:</strong> riprendi la <a href="GUIDA_USO_MDN.md#mdn-guide-http">checklist HTTP della guida trasversale</a>. MDN chiarisce il comportamento del browser e del protocollo; RFC, OWASP e NIST guidano le decisioni di sicurezza del modulo.</p>
<ul>
  <li><strong>Studia:</strong> <a href="https://developer.mozilla.org/en-US/docs/Web/HTTP/Guides/Cookies">Using HTTP cookies</a>, distinguendo cookie, sessione server-side e identificatore di sessione;</li>
  <li><strong>consulta:</strong> la reference di <a href="https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Set-Cookie"><code>Set-Cookie</code></a> per sintassi e direttive <code>HttpOnly</code>, <code>Secure</code>, <code>SameSite</code>, <code>Path</code> e scadenza;</li>
  <li><strong>riconosci:</strong> gli avvisi di sicurezza e compatibilità, senza trasformarli in una policy completa per l'applicazione.</li>
</ul>
<p align="justify"><strong>Prodotto atteso:</strong> parti da un header <code>Set-Cookie</code> del laboratorio e spiega chi lo produce, chi lo conserva, quando viene rinviato e quali attacchi riduce ogni direttiva scelta.</p>
</td></tr></table>

<table align="center"><tr><td>
<details>
<summary>&#128279; <strong>Indice incrociato — autenticazione e sessioni ↔ fonti ufficiali</strong></summary>

<table align="center">
<thead><tr><th>Dispensa</th><th>Documentazione ufficiale</th><th>Profondità</th></tr></thead>
<tbody>
<tr><td><a href="#lesson-auth-passwords">Password policy, hashing e salt</a></td><td><a href="https://pages.nist.gov/800-63-4/sp800-63b.html">NIST SP 800-63B</a><br><a href="https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html">OWASP — Password Storage</a></td><td>&#128994; studiare principi e scelte del corso</td></tr>
<tr><td><a href="#lesson-auth-sessions">Sessione server-side e cookie</a></td><td><a href="https://developer.mozilla.org/en-US/docs/Web/HTTP/Guides/Cookies">MDN — HTTP cookies</a><br><a href="https://cheatsheetseries.owasp.org/cheatsheets/Session_Management_Cheat_Sheet.html">OWASP — Session Management</a></td><td>&#128994; studiare ora</td></tr>
<tr><td><a href="#lesson-auth-authorization">Authorization e ownership</a></td><td><a href="https://cheatsheetseries.owasp.org/cheatsheets/Authorization_Cheat_Sheet.html">OWASP — Authorization</a></td><td>&#128994; studiare ora</td></tr>
<tr><td><a href="#lesson-auth-csrf">CSRF, SameSite e same-origin</a></td><td><a href="https://cheatsheetseries.owasp.org/cheatsheets/Cross-Site_Request_Forgery_Prevention_Cheat_Sheet.html">OWASP — CSRF Prevention</a></td><td>&#128994; comprendere il threat model del corso</td></tr>
<tr><td>OAuth, WebAuthn, MFA e architetture JWT</td><td>NIST, OWASP e specifiche dedicate</td><td>&#128993; riconoscere, fuori dal core</td></tr>
</tbody>
</table>

</details>
</td></tr></table>

---

## Problema iniziale

<p align="justify">Nella milestone 6 il client puo pubblicare un post, ma il backend non sa davvero <strong>chi</strong> stia operando.</p>

```text
POST /api/posts
{
  "text": "Ciao"
}
```

<p align="justify">Il server usava un autore convenzionale:</p>

```text
author = "Studente"
```

<p align="justify">Una scorciatoia ingenua sarebbe accettare:</p>

```json
{
  "authorId": "utente-123",
  "text": "Ciao"
}
```

<p align="justify">ma questo non autentica nessuno.</p>

<p align="justify">Un client malevolo potrebbe inviare:</p>

```json
{
  "authorId": "id-del-docente",
  "text": "Messaggio falso"
}
```

<p align="justify">La regola che guida tutta l'UDA e:</p>

<blockquote>
<p align="justify"><strong>l'identita usata per autorizzare una operazione deve provenire da una prova verificata dal server, non da un campo scelto dal client.</strong></p>
</blockquote>

---

## 1. Identificazione, autenticazione, autorizzazione

<p align="justify">Sono tre domande diverse.</p>

### Identificazione

<blockquote>
<p align="justify">Chi dichiari di essere?</p>
</blockquote>

<p align="justify">Esempio:</p>

```text
email = maria@example.test
```

### Autenticazione

<blockquote>
<p align="justify">Riesci a dimostrare di essere quell'utente?</p>
</blockquote>

<p align="justify">Nel nostro laboratorio:</p>

```text
email + password
       ↓
verifica password hash
       ↓
identita autenticata
```

### Autorizzazione

<blockquote>
<p align="justify">Ora che so chi sei, puoi fare <strong>questa</strong> operazione su <strong>questa</strong> risorsa?</p>
</blockquote>

```text
utente autenticato
       ↓
post.authorId === user.id ?
       ↓
DELETE consentita / negata
```

<p align="justify">Autenticazione non implica autorizzazione.</p>

<p align="justify">Un utente autenticato puo non avere il diritto di cancellare il post di un altro utente.</p>

---

## 2. Threat model minimo

<p align="justify">Prima del codice elenchiamo cosa non vogliamo permettere.</p>

<table align="center">
<thead>
<tr>
<th>Minaccia</th>
<th>Esempio</th>
<th>Contromisura didattica</th>
</tr>
</thead>
<tbody>
<tr>
<td>furto DB</td>
<td>dump della tabella <code>users</code></td>
<td>password hash adattivo + salt</td>
</tr>
<tr>
<td>password guessing offline</td>
<td>milioni di tentativi</td>
<td><code>scrypt</code> costoso</td>
</tr>
<tr>
<td>session prediction</td>
<td>token <code>user-12</code></td>
<td><code>randomBytes(32)</code></td>
</tr>
<tr>
<td>furto token via JS</td>
<td><code>document.cookie</code></td>
<td><code>HttpOnly</code></td>
</tr>
<tr>
<td>invio token in HTTP di produzione</td>
<td>rete non cifrata</td>
<td><code>Secure</code> + HTTPS</td>
</tr>
<tr>
<td>cross-site request</td>
<td>pagina terza invia POST</td>
<td><code>SameSite</code> + same-origin checks</td>
</tr>
<tr>
<td>session fixation</td>
<td>token scelto prima del login riutilizzato</td>
<td>nuova sessione dopo login</td>
</tr>
<tr>
<td>user enumeration</td>
<td>messaggi login diversi</td>
<td><code>invalid-credentials</code> generico</td>
</tr>
<tr>
<td>identity spoofing</td>
<td><code>authorId</code> nel body</td>
<td>identita da <code>req.auth.user</code></td>
</tr>
<tr>
<td>IDOR</td>
<td>DELETE di risorsa altrui</td>
<td>authorization server-side</td>
</tr>
<tr>
<td>SQL injection</td>
<td>email concatenata in query</td>
<td>prepared statements</td>
</tr>
<tr>
<td>token rubato dal DB</td>
<td>session ID salvato in chiaro</td>
<td>hash del session token nel DB</td>
</tr>
</tbody>
</table>

<p align="justify">Il modello non rende Feisbuc una banca. Serve a costruire abitudini corrette e confini verificabili.</p>

---

<a id="lesson-auth-passwords"></a>
## 3. Password policy moderna

### 3.1 Lunghezza prima della complessita artificiale

<p align="justify">Per un'autenticazione a singolo fattore adottiamo nel corso:</p>

```text
minimo 15 caratteri
massimo accettato 128 caratteri
```

<p align="justify">Non imponiamo:</p>

```text
almeno una maiuscola
almeno un numero
almeno un simbolo
cambio ogni 30 giorni
```

<p align="justify">come regole automatiche del laboratorio.</p>

<p align="justify">Esempio valido:</p>

```text
la pizza sul mare di sera
```

<p align="justify">puo essere migliore di una password corta costruita solo per soddisfare una regex.</p>

### 3.2 Unicode e lunghezza

<p align="justify">In JavaScript:</p>

```js
Array.from(password).length
```

<p align="justify">conta i code point in modo piu utile di affidarsi ciecamente ai code unit UTF-16 per la policy didattica.</p>

### 3.3 Validazione non e hashing

```text
policy
  ↓
password accettabile come input?

hashing
  ↓
come la memorizziamo in modo resistente?
```

<p align="justify">Sono responsabilita separate.</p>

---

## 4. Mai password in chiaro

<p align="justify">Schema sbagliato:</p>

```sql
CREATE TABLE users (
  email TEXT,
  password TEXT
);
```

<p align="justify">Insert sbagliato:</p>

```sql
INSERT INTO users(email, password)
VALUES(?, ?);
```

<p align="justify">se <code>?</code> e la password originale.</p>

<p align="justify">Se il DB viene letto, tutte le password sono immediatamente disponibili.</p>

---

## 5. Hashing, salt e funzione adattiva

<p align="justify">Non ci serve poter ricostruire la password.</p>

<p align="justify">Ci serve verificare:</p>

```text
password candidata
       ↓
stesso KDF + stesso salt
       ↓
derived key
       ↓
confronto con hash memorizzato
```

### 5.1 Perche non SHA-256(password)

<p align="justify">Una funzione hash generale e intenzionalmente veloce.</p>

<p align="justify">Per le password vogliamo invece una funzione il cui costo renda piu caro un attacco offline.</p>

<p align="justify">Nel laboratorio usiamo <strong>scrypt</strong>, disponibile nel modulo <code>node:crypto</code>, senza dipendenza npm.</p>

### 5.2 Parametri del corso

<p align="justify">Useremo una delle configurazioni scrypt indicate come baseline da OWASP:</p>

```text
N = 2^14
r = 8
p = 5
```

<p align="justify">con salt casuale da 16 byte e derived key da 32 byte.</p>

<p align="justify">Il formato salvato sara auto-descrittivo:</p>

```text
scrypt$16384$8$5$<salt-base64url>$<hash-base64url>
```

<p align="justify">Se domani cambiamo costo, ogni hash conserva i parametri con cui e stato creato.</p>

### 5.3 Hash asincrono

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

<p align="justify">Usiamo la variante asincrona per non bloccare volontariamente il thread JavaScript durante una operazione costosa.</p>

### 5.4 Salt casuale

```js
import { randomBytes } from "node:crypto";

const salt = randomBytes(16);
```

<p align="justify">Due utenti con la stessa password devono normalmente ottenere hash diversi.</p>

### 5.5 Confronto

<p align="justify">Per confrontare byte segreti usiamo:</p>

```js
timingSafeEqual(actual, expected)
```

<p align="justify">solo dopo avere verificato che i Buffer abbiano la stessa lunghezza.</p>

---

## 6. Register

<p align="justify">Pipeline:</p>

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

<p align="justify">La response <strong>non</strong> contiene:</p>

```text
password
passwordHash
session hash
```

---

## 7. Login senza user enumeration

<p align="justify">Errore da evitare:</p>

```text
email inesistente   -> "utente non trovato"
password sbagliata  -> "password errata"
```

<p align="justify">Queste differenze permettono di verificare quali account esistano.</p>

<p align="justify">Nel laboratorio la response pubblica e la stessa:</p>

```json
{
  "error": {
    "code": "invalid-credentials",
    "message": "Credenziali non valide."
  }
}
```

<p align="justify">Il flusso e:</p>

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

<p align="justify">La nuova sessione evita di promuovere un eventuale identificatore pre-autenticazione in una sessione autenticata.</p>

---

<a id="lesson-auth-sessions"></a>
## 8. Sessioni server-side

<p align="justify">Dopo il login non vogliamo reinviare la password a ogni request.</p>

<p align="justify">Creiamo una sessione:</p>

```text
browser                    server / DB

session token  ──────────>  hash(token)
nel cookie                  user_id
                            expires_at
```

### 8.1 Token opaco

```js
randomBytes(32).toString("base64url")
```

<p align="justify">32 byte = 256 bit casuali prima della codifica.</p>

<p align="justify">Il token non contiene:</p>

```text
user id
email
ruolo
timestamp leggibile
```

<p align="justify">E un riferimento opaco.</p>

### 8.2 Perche hashare anche il session token nel DB

<p align="justify">Se salvassimo:</p>

```text
sessions.token = token-cookie
```

<p align="justify">un dump DB fornirebbe sessioni immediatamente utilizzabili.</p>

<p align="justify">Nel corso salviamo:</p>

```js
sha256(token)
```

<p align="justify">Nel browser resta il token originale; nel DB resta soltanto l'impronta usata per la ricerca.</p>

---

## 9. Cookie di sessione

<p align="justify">Per lo stesso token:</p>

```text
Cookie: feisbuc.sid=<opaque-token>
```

<p align="justify">in produzione vogliamo attributi espliciti:</p>

```text
HttpOnly
Secure
SameSite=Strict
Path=/
```

### `HttpOnly`

<p align="justify">Il cookie non deve essere leggibile da <code>document.cookie</code>.</p>

<p align="justify">Il browser continua comunque a inviarlo nelle request HTTP appropriate.</p>

### `Secure`

<p align="justify">In produzione il cookie deve viaggiare solo su HTTPS.</p>

<p align="justify">Il laboratorio locale HTTP deve poter girare anche sui PC della scuola; quindi distinguiamo configurazione development e production invece di fingere TLS dove non esiste.</p>

### `SameSite=Strict`

<p align="justify">Per Feisbuc same-origin scegliamo <code>Strict</code>.</p>

<p align="justify">Serve come difesa contro molte request cross-site, ma <strong>non e l'unica difesa CSRF</strong>.</p>

### `Path=/`

<p align="justify">La sessione serve all'intera applicazione.</p>

### Prefisso `__Host-`

<p align="justify">In produzione il nome preferito e:</p>

```text
__Host-feisbuc.sid
```

<p align="justify">che richiede <code>Secure</code>, <code>Path=/</code> e nessun <code>Domain</code>.</p>

---

## 10. Development e production non sono la stessa cosa

<p align="justify">Configurazione development:</p>

```text
NODE_ENV=development
COOKIE_SECURE=false
cookieName=feisbuc.sid
```

<p align="justify">Configurazione production:</p>

```text
NODE_ENV=production
COOKIE_SECURE=true
cookieName=__Host-feisbuc.sid
HTTPS davanti all'app
```

<p align="justify">Regola fail-closed del corso:</p>

<blockquote>
<p align="justify">se <code>NODE_ENV=production</code> e <code>COOKIE_SECURE</code> non e <code>true</code>, il server non parte.</p>
</blockquote>

<p align="justify">Una configurazione insicura non deve diventare silenziosamente la produzione.</p>

---

## 11. Parsing del cookie

<p align="justify">Per capire il protocollo non aggiungiamo subito <code>cookie-parser</code>.</p>

<p align="justify">Header:</p>

```http
Cookie: theme=dark; feisbuc.sid=abc123
```

<p align="justify">Il middleware estrae soltanto il cookie necessario.</p>

<p align="justify">La lettura del cookie non autentica ancora l'utente:</p>

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

## 12. Middleware di autenticazione

<p align="justify">Vogliamo distinguere due responsabilita.</p>

### `loadAuth`

<p align="justify">Prova a caricare una identita.</p>

```js
req.auth = {
  user: null,
  sessionHash: null,
};
```

<p align="justify">oppure:</p>

```js
req.auth = {
  user: { id, email, displayName },
  sessionHash,
};
```

### `requireAuth`

<p align="justify">Decide se una route richiede autenticazione.</p>

```js
export function requireAuth(req, res, next) {
  if (!req.auth?.user) {
    next(new HttpError(401, "authentication-required", "Autenticazione richiesta."));
    return;
  }
  next();
}
```

<p align="justify"><code>401</code> significa che manca una autenticazione valida.</p>

---

<a id="lesson-auth-authorization"></a>
## 13. Autorizzazione: il server decide

<p align="justify">Il client puo nascondere il bottone Delete per UX.</p>

<p align="justify">Ma la sicurezza non puo essere:</p>

```js
if (!isOwner) deleteButton.hidden = true;
```

<p align="justify">Un attaccante puo inviare la request direttamente.</p>

<p align="justify">La route deve verificare:</p>

```text
req.auth.user.id
       vs
post.author_id nel DB
```

<p align="justify">Esempio:</p>

```text
DELETE /api/posts/p123
```

<p align="justify">possibili risultati:</p>

```text
204  utente proprietario
403  autenticato ma non proprietario
404  post inesistente
401  sessione assente/non valida
```

---

## 14. Mai fidarsi di `authorId` nel body

<p align="justify">Route sbagliata:</p>

```js
postStore.create({
  text: req.body.text,
  authorId: req.body.authorId,
});
```

<p align="justify">Route corretta:</p>

```js
postStore.create({
  text,
  authorId: req.auth.user.id,
});
```

<p align="justify">L'identita viene dal contesto autenticato.</p>

---

## 15. Schema relazionale della milestone 7

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

<p align="justify">Relazioni:</p>

```text
users 1 ───── N sessions
users 1 ───── N posts
```

<p align="justify">Non salviamo <code>author</code> come stringa duplicata nel post.</p>

<p align="justify">Per la response:</p>

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

## 16. Prepared statements anche nell'autenticazione

<p align="justify">Mai:</p>

```js
`SELECT * FROM users WHERE email = '${email}'`
```

<p align="justify">Sempre binding:</p>

```js
db.prepare(`
  SELECT id, email, display_name, password_hash
  FROM users
  WHERE email = ?
`).get(email)
```

<p align="justify">Email, session hash, user id e post id sono tutti input da trattare come dati.</p>

---

## 17. Scadenza server-side

<p align="justify">Una sessione ha una scadenza reale nel DB:</p>

```text
expires_at = Date.now() + SESSION_TTL_MS
```

<p align="justify">La query valida solo:</p>

```sql
WHERE sessions.expires_at > ?
```

<p align="justify">Una sessione scaduta non diventa valida solo perche il browser conserva ancora un cookie.</p>

<p align="justify">Il laboratorio usa una TTL di 8 ore come valore didattico configurabile.</p>

---

## 18. Logout

<p align="justify">Logout significa due operazioni:</p>

```text
1. DELETE session dal DB
2. Set-Cookie che cancella il cookie browser
```

<p align="justify">Fare solo:</p>

```text
clear cookie
```

<p align="justify">lascia il token eventualmente copiato valido server-side.</p>

<p align="justify">Fare solo:</p>

```text
delete DB row
```

<p align="justify">lascia un cookie inutile nel browser.</p>

<p align="justify">Servono entrambe.</p>

---

## 19. Cache delle response auth

<p align="justify">Le response che impostano o descrivono sessioni non devono essere trattate come normali contenuti cacheabili.</p>

<p align="justify">Nel modulo usiamo:</p>

```http
Cache-Control: no-store
```

<p align="justify">per <code>/api/auth/*</code> e per le response private principali.</p>

---

<a id="lesson-auth-csrf"></a>
## 20. CSRF: perche SameSite non chiude il discorso

<p align="justify">Il browser invia automaticamente i cookie nelle request che rispettano le regole del cookie.</p>

<p align="justify">Questo e comodo per le sessioni, ma introduce il problema CSRF.</p>

<p align="justify">Nel laboratorio applichiamo defense in depth:</p>

```text
SameSite=Strict
      +
controllo Sec-Fetch-Site quando presente
      +
controllo Origin quando presente
```

<p align="justify">Per metodi unsafe:</p>

```text
POST
PUT
PATCH
DELETE
```

<p align="justify">una request browser dichiaratamente <code>cross-site</code> viene rifiutata.</p>

<p align="justify">Questa non e una scusa per inventare un CORS permissivo.</p>

---

## 21. CORS non e autenticazione e non e CSRF protection completa

<p align="justify">Tre concetti distinti:</p>

```text
CORS
  -> quali response cross-origin possono essere lette dal browser

autenticazione
  -> chi e l'utente

CSRF defense
  -> impedire uso involontario delle credenziali browser su request mutate
```

<p align="justify">Non risolviamo auth aggiungendo:</p>

```js
app.use(cors({ origin: "*" }));
```

---

## 22. Il token non va in `localStorage`

<p align="justify">Nella milestone 3 abbiamo usato <code>localStorage</code> per <strong>dati applicativi non sensibili</strong>.</p>

<p align="justify">Non riutilizziamo quel pattern per la sessione.</p>

<p align="justify">No:</p>

```js
localStorage.setItem("token", token);
```

<p align="justify">La sessione viaggia in cookie <code>HttpOnly</code> e il JavaScript client non deve conoscerne il valore.</p>

<p align="justify">Il client chiede:</p>

```text
GET /api/auth/me
```

<p align="justify">e riceve l'utente pubblico.</p>

---

## 23. API auth della milestone 7

```text
POST /api/auth/register
POST /api/auth/login
GET  /api/auth/me
POST /api/auth/logout
```

<p align="justify">Contratto pubblico utente:</p>

```json
{
  "id": "...",
  "email": "maria@example.test",
  "displayName": "Maria"
}
```

<p align="justify">Mai:</p>

```json
{
  "passwordHash": "..."
}
```

---

## 24. API post della milestone 7

<p align="justify">Le route esistenti rimangono, ma richiedono auth:</p>

```text
GET    /api/posts
POST   /api/posts
PATCH  /api/posts/:id
DELETE /api/posts/:id
```

<p align="justify">Il nuovo <code>DELETE</code> serve a rendere osservabile l'autorizzazione per ownership.</p>

<p align="justify">Response post:</p>

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

## 25. Feisbuc milestone 7

<p align="justify">Prima:</p>

```text
browser
  -> API
  -> Express
  -> SqlPostStore
  -> SQLite
```

<p align="justify">Ora:</p>

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

<p align="justify">Il cambiamento fondamentale e:</p>

```text
"autore scelto dal codice/client"
              ↓
"autore derivato dalla sessione verificata"
```

---

## 26. Error model auth

<p align="justify">Esempi:</p>

```text
400 registration-invalid
401 invalid-credentials
401 authentication-required
403 forbidden
409 email-already-registered
```

<p align="justify">Login usa intenzionalmente un errore generico:</p>

```text
invalid-credentials
```

<p align="justify">sia per email inesistente sia per password errata.</p>

---

## 27. Cosa non entra ancora

<p align="justify">Questa UDA non deve diventare un corso completo di identity management.</p>

<p align="justify">Rimandiamo:</p>

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

<p align="justify">Verranno richiamati nel track advanced/security.</p>

---

## 28. Perche non JWT adesso

<p align="justify">Il nostro problema e:</p>

```text
browser same-origin
backend Express
sessione applicativa
```

<p align="justify">Una sessione server-side opaca ci permette di studiare bene:</p>

<ul>
  <li>cookie;</li>
  <li>revoca;</li>
  <li>expiry;</li>
  <li>session fixation;</li>
  <li>DB lookup;</li>
  <li>authorization.</li>
</ul>

<p align="justify">Aggiungere JWT qui aumenterebbe i concetti senza risolvere un requisito reale della milestone.</p>

---

## 29. Errori frequenti

### Password in chiaro

```sql
password TEXT
```

<p align="justify">con valore originale.</p>

### Hash veloce singolo

```js
sha256(password)
```

### Salt fisso

```js
const salt = "feisbuc";
```

### Session ID prevedibile

```js
const sid = user.id;
```

### Session token nel localStorage

```js
localStorage.setItem("sid", token);
```

### Cookie senza HttpOnly

```text
Set-Cookie: sid=...
```

### `Secure=false` in produzione

<p align="justify">configurazione che deve fallire, non essere tollerata.</p>

### Identita dal body

```js
const authorId = req.body.authorId;
```

### Autorizzazione solo nella UI

```js
button.hidden = !owned;
```

<p align="justify">senza controllo route.</p>

### DELETE senza ownership check

```js
postStore.delete(req.params.id);
```

### Messaggi di login enumerabili

```text
email non registrata
```

### Sessione mai invalidata

<p align="justify">record DB che vive per sempre.</p>

---

## 30. Esercizi A-F

### A — osserva/modifica

<p align="justify">Implementa la policy credenziali pura: normalizzazione email e password 15–128, senza regole di composizione.</p>

### B — modifica controllata

<p align="justify">Implementa una funzione pura di authorization su post: read/like per utente autenticato, delete/edit solo per owner.</p>

### C — implementazione autonoma

<p align="justify"><strong>Feisbuc milestone 7</strong>: integra <code>users</code>, password hashing, session store, cookie, auth Router, <code>requireAuth</code> e ownership.</p>

### D — debugging/diagnosi

<p align="justify">Analizza un backend deliberatamente vulnerabile: password plaintext, sid prevedibile, cookie debole, identity spoofing, authorization client-side.</p>

### E — mini-progetto

<p align="justify">Aggiungi una pagina profilo autenticata e una route di modifica display name con re-authentication progettata sulla carta prima dell'implementazione.</p>

### F — prodotto integrato

<p align="justify">Esegui una security review della milestone Feisbuc: asset, trust boundaries, attacchi, controlli, evidence e debiti residui.</p>

---

## 31. Laboratorio

<p align="justify">Sequenza consigliata:</p>

```text
A policy credenziali autograded
      ↓
B authorization pura autograded
      ↓
C Feisbuc auth/session E2E
      ↓
D security debugging + review
```

<p align="justify">Il laboratorio C deve provare realmente:</p>

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

## 32. Verifica rapida

<ol>
  <li>Identificazione e autenticazione sono la stessa cosa?</li>
  <li>Perche SHA-256 diretto non e un password KDF adeguato?</li>
  <li>A cosa serve il salt?</li>
  <li>Perche il session token deve essere casuale?</li>
  <li>Perche nel DB salviamo il suo hash?</li>
  <li><code>HttpOnly</code> impedisce al browser di inviare il cookie?</li>
  <li><code>SameSite</code> elimina ogni rischio CSRF?</li>
  <li>Chi deve determinare <code>authorId</code>: client o server?</li>
  <li>Qual e la differenza fra <code>401</code> e <code>403</code> nel nostro modello?</li>
  <li>Perche una sessione deve essere eliminata server-side al logout?</li>
</ol>

---

## 33. Sintesi inclusiva

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

<p align="justify">La frase da ricordare e:</p>

<blockquote>
<p align="justify"><strong>Il client puo dichiarare un'intenzione; soltanto il server puo stabilire l'identita e autorizzare l'effetto.</strong></p>
</blockquote>

---

## Fonti e collegamenti

<ul>
  <li>NIST SP 800-63B — password authenticator requirements;</li>
  <li>OWASP Password Storage Cheat Sheet — Argon2id/scrypt e parametri;</li>
  <li>OWASP Session Management Cheat Sheet — session ID e cookie security;</li>
  <li>OWASP CSRF Prevention Cheat Sheet — <code>SameSite</code> come defense in depth;</li>
  <li>MDN <code>Set-Cookie</code> e HTTP cookies;</li>
  <li>Node.js <code>node:crypto</code>: <code>scrypt</code>, <code>randomBytes</code>, <code>timingSafeEqual</code>;</li>
  <li>Express 5 documentation: Router, middleware e <code>res.cookie</code>;</li>
  <li><code>07_SQL_RAW_PERSISTENCE.md</code> — schema/prepared statements/repository;</li>
  <li><code>06_NODE_EXPRESS_BACKEND.md</code> — pipeline Express e middleware.</li>
</ul>

---

## Activity correlate

<ul>
  <li><code>tpsi5-activity-a-auth-credential-policy-001</code>;</li>
  <li><code>tpsi5-activity-b-auth-post-authorization-001</code>;</li>
  <li><code>tpsi5-activity-c-feisbuc-auth-session-001</code>;</li>
  <li><code>tpsi5-activity-d-debug-auth-security-001</code>.</li>
</ul>
