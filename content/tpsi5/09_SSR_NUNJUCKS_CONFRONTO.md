# SSR e template server-side: stesso dominio, altra responsabilita

<table align="center" width="100%"><tr><td>
<details>
<summary>&#128506; <strong>Orientamento della lezione</strong></summary>

<p align="justify"><strong>Contesto:</strong> la stessa applicazione può restituire dati JSON oppure HTML già renderizzato. Cambia il responsabile della presentazione, non il dominio, il database o le regole di sicurezza.</p>
<p align="justify"><strong>Domande guida:</strong> dove viene trasformato lo stato in markup? Che cos'è un view model? Perché una POST da form dovrebbe normalmente terminare con un redirect?</p>
<p align="justify"><strong>Obiettivi osservabili:</strong> seguire il flusso router → view model → template → response, applicare autoescape e Post/Redirect/Get e confrontare SSR e client rendering sullo stesso caso.</p>
<p align="justify"><strong>Prossimo passo:</strong> la lezione 10 costruirà la prima SPA Vue sopra la API e la sessione già esistenti.</p>

</details>
</td></tr></table>

## Obiettivi

<p align="justify">Al termine del modulo lo studente sa:</p>

<ul>
  <li>distinguere <strong>server-side rendering (SSR)</strong> da client-side rendering;</li>
  <li>spiegare che SSR e SPA sono due strategie di rendering, non una scala <code>vecchio -&gt; nuovo</code>;</li>
  <li>descrivere il flusso <code>request -&gt; controller/router -&gt; view model -&gt; template -&gt; HTML response</code>;</li>
  <li>usare Nunjucks 3.2.4 con Express 5 e <code>autoescape: true</code>;</li>
  <li>separare query/storage, authorization, view model e template;</li>
  <li>riconoscere quando l'HTML deve essere prodotto dal server e quando dal browser;</li>
  <li>usare Post/Redirect/Get per le mutazioni provenienti da form HTML;</li>
  <li>mantenere la stessa autenticazione/sessione e lo stesso database tra API JSON e pagine SSR;</li>
  <li>riconoscere che nascondere un bottone nel template <strong>non e authorization</strong>;</li>
  <li>riconoscere il rischio di <code>|safe</code> su contenuto non fidato.</li>
</ul>

## Prerequisiti

<ul>
  <li>UDA 23: HTTP, status, redirect e representation;</li>
  <li>UDA 24: Express Router/middleware/error model;</li>
  <li>SQL raw e repository;</li>
  <li>autenticazione, session cookie e ownership;</li>
  <li>HTML semantico e form.</li>
</ul>

## Orientamento nella documentazione

<p align="center">
  <img src="../../assets/tpsi5/lesson-documentation-depth.svg" alt="La dispensa seleziona nelle fonti ufficiali i contenuti da studiare ora, riconoscere, rimandare o dichiarare fuori confine">
</p>

<table align="center"><tr><td>
<p align="justify"><strong><span style="font-size: 1.15em;">&#128279;</span> Percorso MDN — form, rappresentazioni e redirect:</strong> usa la <a href="GUIDA_USO_MDN.md">guida trasversale a MDN</a> per separare le responsabilità della Web Platform da quelle di Express e Nunjucks.</p>
<ul>
  <li><strong>Studia:</strong> la reference di <a href="https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Elements/form"><code>&lt;form&gt;</code></a>, concentrandoti su <code>action</code>, <code>method</code>, controlli associati e invio;</li>
  <li><strong>studia:</strong> la guida alle <a href="https://developer.mozilla.org/en-US/docs/Web/HTTP/Guides/Redirections">redirezioni HTTP</a> e la scheda dello status <a href="https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Status/303"><code>303 See Other</code></a> per il pattern Post/Redirect/Get;</li>
  <li><strong>consulta:</strong> la reference di <a href="https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Content-Type"><code>Content-Type</code></a> per distinguere una risposta HTML da una rappresentazione JSON.</li>
</ul>
<p align="justify"><strong>Prodotto atteso:</strong> traccia un invio form completo e indica richiesta POST, risposta 303, nuova richiesta GET e risposta HTML, motivando ogni passaggio con il riferimento pertinente.</p>
</td></tr></table>

<table align="center"><tr><td>
<details>
<summary>&#128279; <strong>Indice incrociato — SSR, Nunjucks e Web Platform</strong></summary>

<table align="center">
<thead><tr><th>Dispensa</th><th>Documentazione ufficiale</th><th>Profondità</th></tr></thead>
<tbody>
<tr><td><a href="#lesson-ssr-rendering">SSR e responsabilità del rendering</a></td><td><a href="https://developer.mozilla.org/en-US/docs/Glossary/SSR">MDN — Server-side rendering</a><br><a href="https://expressjs.com/en/guide/using-template-engines.html">Express — Template engines</a></td><td>&#128994; studiare ora</td></tr>
<tr><td><a href="#lesson-ssr-nunjucks">Template, inheritance e view model</a></td><td><a href="https://mozilla.github.io/nunjucks/templating.html">Nunjucks — Templating</a></td><td>&#128994; studiare le parti usate</td></tr>
<tr><td><a href="#lesson-ssr-security">Autoescape e contenuto non fidato</a></td><td><a href="https://mozilla.github.io/nunjucks/api.html#configure">Nunjucks — Configuration</a><br><a href="https://cheatsheetseries.owasp.org/cheatsheets/Cross_Site_Scripting_Prevention_Cheat_Sheet.html">OWASP — XSS Prevention</a></td><td>&#128994; studiare ora</td></tr>
<tr><td><a href="#lesson-ssr-prg">Form e Post/Redirect/Get</a></td><td><a href="https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Elements/form">MDN — <code>&lt;form&gt;</code></a><br><a href="https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Status/303">MDN — 303 See Other</a></td><td>&#128994; studiare ora</td></tr>
<tr><td>Hydration e framework SSR universali</td><td>Documentazione dei framework dedicati</td><td>&#128993; fuori dal core</td></tr>
</tbody>
</table>

</details>
</td></tr></table>

---

## Problema iniziale

<p align="justify">Feisbuc milestone 7 funziona cosi:</p>

```text
GET /api/posts
      |
      v
JSON response
      |
      v
fetch()
      |
      v
app.js
      |
      v
DOM
```

<p align="justify">Il server produce <strong>dati</strong>; il browser produce la parte dinamica dell'HTML.</p>

<p align="justify">Ma non e l'unica possibilita. Possiamo usare gli stessi dati, lo stesso utente e la stessa sessione e cambiare soltanto il responsabile del rendering:</p>

```text
GET /ssr
   |
   v
Express Router
   |
   v
PostStore
   |
   v
view model
   |
   v
Nunjucks template
   |
   v
HTML response
```

<p align="justify">La domanda didattica non e:</p>

<blockquote>
<p align="justify">Quale delle due tecniche e moderna?</p>
</blockquote>

<p align="justify">La domanda utile e:</p>

<blockquote>
<p align="justify">Dove conviene produrre l'HTML per questa interazione e quali responsabilita cambiano?</p>
</blockquote>

---

<a id="lesson-ssr-rendering"></a>
## 1. Rendering: trasformare stato in interfaccia

<p align="justify">Abbiamo gia usato il modello:</p>

```text
state -> render -> DOM
```

<p align="justify">Con SSR il concetto non sparisce. Cambia il luogo in cui avviene il rendering:</p>

```text
server state -> template -> HTML string -> HTTP response
```

<p align="justify">In entrambi i casi esistono:</p>

<ul>
  <li>dati;</li>
  <li>una trasformazione;</li>
  <li>markup risultante;</li>
  <li>interazioni successive.</li>
</ul>

<p align="justify">Quindi SSR non elimina JavaScript per definizione e SPA non elimina il server.</p>

---

## 2. Due flussi dello stesso Feisbuc

### API + client rendering

```text
browser
  |
  | GET /api/posts
  v
Express
  |
  v
SqlPostStore
  |
  v
JSON
  |
  v
browser JavaScript
  |
  v
DOM
```

### SSR

```text
browser
  |
  | GET /ssr
  v
Express
  |
  v
SqlPostStore
  |
  v
view model
  |
  v
Nunjucks
  |
  v
HTML
```

<p align="justify">Database e regole di accesso possono rimanere gli stessi.</p>

---

## 3. Il template non e il database layer

<p align="justify">Un errore frequente e trasformare un template engine in un punto in cui fare tutto:</p>

```text
route
  -> query SQL
  -> logica auth
  -> formattazione
  -> HTML
```

<p align="justify">Noi manteniamo invece:</p>

```text
Router
  |
  +-> auth / authorization
  |
  +-> PostStore
  |
  +-> buildViewModel(...)
  |
  `-> template
```

<p align="justify">Il template deve ricevere dati <strong>gia pronti per la presentazione</strong>.</p>

---

## 4. Template engine

<p align="justify">Un template contiene HTML con punti di sostituzione e controllo presentazionale:</p>

```html
<h2>{{ post.author }}</h2>
<p>{{ post.text }}</p>
```

<p align="justify">Iterazione:</p>

```html
{% for post in posts %}
  <article>
    <h2>{{ post.author }}</h2>
    <p>{{ post.text }}</p>
  </article>
{% endfor %}
```

<p align="justify">Condizione:</p>

```html
{% if post.canDelete %}
  <button>Elimina</button>
{% endif %}
```

<p align="justify">La condizione <code>canDelete</code> e una decisione di <strong>presentazione</strong>: mostrare o meno un controllo.</p>

<p align="justify">La decisione di sicurezza deve comunque essere ripetuta/autorevolmente applicata sul server quando arriva la request di eliminazione.</p>

---

<a id="lesson-ssr-nunjucks"></a>
## 5. Nunjucks nel corso

<p align="justify">Per questo confronto usiamo:</p>

```text
nunjucks 3.2.4
```

<p align="justify">La configurazione di riferimento crea un Environment esplicito:</p>

```js
const loader = new nunjucks.FileSystemLoader(viewsDir, {
  noCache: true,
});

const env = new nunjucks.Environment(loader, {
  autoescape: true,
  throwOnUndefined: true,
});

env.express(app);
```

<p align="justify"><code>autoescape: true</code> e una protezione importante quando il template stampa contenuto utente.</p>

---

## 6. View model: preparare dati per la vista

<p align="justify">Il post persistente puo essere:</p>

```js
{
  id,
  authorId,
  author,
  text,
  likes,
  liked,
  createdAt
}
```

<p align="justify">Il template ha bisogno anche di informazioni puramente visuali:</p>

```js
{
  ...post,
  canDelete: post.authorId === currentUser.id,
  likedLabel: post.liked ? "Non mi piace piu" : "Mi piace"
}
```

<p align="justify">Queste proprieta sono un <strong>view model</strong>.</p>

<p align="justify">Vantaggi:</p>

<ul>
  <li>template piu semplice;</li>
  <li>logica JavaScript testabile senza HTML;</li>
  <li>meno accesso a strutture applicative dal template;</li>
  <li>decisioni di presentazione visibili.</li>
</ul>

<p align="justify">Attenzione:</p>

```text
canDelete == true nel view model
```

<p align="justify">non sostituisce:</p>

```text
postStore.deleteOwned(postId, req.auth.user.id)
```

---

## 7. Template inheritance

<p align="justify">Una pagina reale ripete shell, metadata e navigazione.</p>

<p align="justify">Nunjucks permette:</p>

```html
{% extends "base.njk" %}

{% block content %}
  ...
{% endblock %}
```

<p align="justify"><code>base.njk</code> puo contenere:</p>

```html
<!doctype html>
<html lang="it">
<head>...</head>
<body>
  <header>...</header>
  <main>{% block content %}{% endblock %}</main>
</body>
</html>
```

<p align="justify">L'obiettivo non e usare il massimo numero di feature del template engine, ma rendere esplicita la composizione delle viste.</p>

---

<a id="lesson-ssr-security"></a>
## 8. Autoescape e contenuto utente

<p align="justify">Supponiamo che un post contenga:</p>

```text
<script>alert('x')</script>
```

<p align="justify">Con autoescape attivo:</p>

```html
{{ post.text }}
```

<p align="justify">viene trattato come <strong>testo</strong>, non come markup da eseguire.</p>

<p align="justify">Un pattern pericoloso e:</p>

```html
{{ post.text | safe }}
```

<p align="justify"><code>safe</code> dice deliberatamente al template engine:</p>

<blockquote>
<p align="justify">Questo valore e HTML fidato.</p>
</blockquote>

<p align="justify">Non va applicato a contenuto arbitrario degli utenti.</p>

<p align="justify">La regola didattica resta coerente con il DOM:</p>

```text
client rendering -> textContent
server rendering -> autoescape
```

<p align="justify">Entrambe partono dallo stesso principio: i dati utente non diventano automaticamente codice/markup.</p>

---

## 9. GET deve restare safe

<p align="justify">La pagina SSR viene letta con:</p>

```http
GET /ssr
```

<p align="justify">Il GET non deve creare o eliminare post.</p>

<p align="justify">Per creare un post da un form HTML:</p>

```http
POST /ssr/posts
```

<p align="justify">Per eliminare tramite normale form HTML, che supporta GET e POST:</p>

```http
POST /ssr/posts/:id/delete
```

<p align="justify">Questa route non sostituisce la REST API:</p>

```http
DELETE /api/posts/:id
```

<p align="justify">Sono due interfacce HTTP per due interaction model differenti.</p>

---

<a id="lesson-ssr-prg"></a>
## 10. Post/Redirect/Get

<p align="justify">Se dopo una POST restituiamo direttamente la pagina HTML:</p>

```text
POST form
  -> mutate
  -> 200 HTML
```

<p align="justify">un refresh puo proporre la ripetizione della POST.</p>

<p align="justify">Usiamo invece:</p>

```text
POST /ssr/posts
  -> mutate
  -> 303 See Other
  -> Location: /ssr
  -> GET /ssr
```

<p align="justify">Questo pattern e chiamato <strong>Post/Redirect/Get (PRG)</strong>.</p>

<p align="justify">Il <code>303</code> rende esplicito che la navigazione successiva deve essere una GET.</p>

---

## 11. Form HTML e Content-Type

<p align="justify">Un form standard invia tipicamente:</p>

```http
Content-Type: application/x-www-form-urlencoded
```

<p align="justify">Quindi il server SSR aggiunge:</p>

```js
express.urlencoded({ extended: false, limit: "16kb" })
```

<p align="justify">La API JSON continua invece a usare:</p>

```js
express.json(...)
```

<p align="justify">Il protocollo HTTP e lo stesso; cambia la representation del body.</p>

---

## 12. Sessione condivisa

<p align="justify">Non creiamo una seconda autenticazione per SSR.</p>

<p align="justify">Il browser possiede gia il cookie HttpOnly della milestone 7:</p>

```text
feisbuc.sid=<opaque token>
```

<p align="justify"><code>loadAuth</code> continua a produrre:</p>

```js
req.auth.user
```

<p align="justify">Sia le route API sia le route SSR usano lo stesso contesto autenticato.</p>

```text
cookie
  -> loadAuth
  -> req.auth.user
       |              |
       v              v
   /api/posts       /ssr
```

<p align="justify">Questo e un esempio concreto di <strong>riuso del dominio e della security boundary tra due presentation layer</strong>.</p>

---

## 13. Status e redirect

<p align="justify">Nel ramo SSR useremo principalmente:</p>

<ul>
  <li><code>200</code> per pagina resa correttamente;</li>
  <li><code>303</code> dopo una POST riuscita;</li>
  <li><code>401</code> se manca autenticazione;</li>
  <li><code>403</code> se l'utente tenta una mutazione non autorizzata;</li>
  <li><code>404</code> se la risorsa non esiste.</li>
</ul>

<p align="justify">Il fatto che una response contenga HTML non cambia la semantica HTTP.</p>

---

## 14. Feisbuc milestone 8: SSR senza buttare via la API

<p align="justify">Milestone 8 <strong>non elimina</strong> <code>/api/*</code>.</p>

<p align="justify">Aggiunge un secondo presentation adapter:</p>

```text
                    +-> JSON API -> JS -> DOM
Domain / stores ----|
                    +-> SSR Router -> view model -> Nunjucks -> HTML
```

<p align="justify">Route SSR:</p>

```text
GET  /ssr
POST /ssr/posts
POST /ssr/posts/:id/delete
```

<p align="justify">La pagina SSR usa:</p>

<ul>
  <li>stessa sessione;</li>
  <li>stesso <code>SqlPostStore</code>;</li>
  <li>stessa validation del testo;</li>
  <li>stessa ownership;</li>
  <li>stessi post persistenti.</li>
</ul>

---

## 15. Confronto tra implementazioni

### API + client rendering

<p align="justify">Pro:</p>

<ul>
  <li>UI altamente interattiva senza full navigation;</li>
  <li>API riutilizzabile da piu client;</li>
  <li>frontend e backend possono evolvere separatamente.</li>
</ul>

<p align="justify">Costo:</p>

<ul>
  <li>piu stato e orchestration nel browser;</li>
  <li>loading/error/render da gestire nel client;</li>
  <li>hydration/build framework possibili nei sistemi piu complessi.</li>
</ul>

### SSR classico

<p align="justify">Pro:</p>

<ul>
  <li>prima response contiene gia HTML utile;</li>
  <li>form e navigation funzionano bene con meccanismi browser standard;</li>
  <li>meno JavaScript necessario per molte interazioni CRUD.</li>
</ul>

<p align="justify">Costo:</p>

<ul>
  <li>molte interazioni provocano navigation completa;</li>
  <li>il server ha responsabilita di rendering;</li>
  <li>componentizzazione/stato UI ricco richiedono altre tecniche.</li>
</ul>

### Conclusione

<p align="justify">Non esiste:</p>

```text
SSR < SPA
```

<p align="justify">Esiste:</p>

```text
requirements -> trade-off -> scelta
```

---

## 16. SSR non significa zero JavaScript

<p align="justify">Una pagina SSR puo comunque usare JavaScript per:</p>

<ul>
  <li>progressive enhancement;</li>
  <li>menu;</li>
  <li>validazione UX;</li>
  <li>realtime;</li>
  <li>aggiornamenti parziali.</li>
</ul>

<p align="justify">La distinzione e dove viene generato il markup iniziale e come evolve l'interazione.</p>

---

## 17. SSR e accessibilita/progressive enhancement

<p align="justify">Form e link standard hanno un valore architetturale:</p>

```html
<form method="post" action="/ssr/posts">
  ...
</form>
```

<p align="justify">Funzionano secondo il modello di navigazione HTTP senza richiedere un event handler JavaScript.</p>

<p align="justify">Questo non garantisce automaticamente accessibilita, ma rende visibile un baseline funzionale che puo essere migliorato progressivamente.</p>

---

## 18. Errori frequenti e security review

### Errore 1 — SQL nel template

```text
template -> database
```

<p align="justify">Da evitare. Il template riceve il view model.</p>

### Errore 2 — authorization soltanto nella vista

```html
{% if post.canDelete %}
  <button>Elimina</button>
{% endif %}
```

<p align="justify">Serve per UX, non per sicurezza.</p>

<p align="justify">La route deve verificare ownership.</p>

### Errore 3 — `|safe` su dati utente

```html
{{ post.text | safe }}
```

<p align="justify">Se il testo non e trusted HTML, stiamo bypassando l'escape.</p>

### Errore 4 — mutazione con GET

```http
GET /delete/123
```

<p align="justify">GET deve restare safe.</p>

### Errore 5 — niente PRG

<p align="justify">POST seguito da HTML 200 puo generare resubmit su refresh.</p>

### Errore 6 — passare al template tutto l'oggetto DB

<p align="justify">Non passiamo:</p>

<ul>
  <li><code>password_hash</code>;</li>
  <li>session hash;</li>
  <li>secret interni;</li>
  <li>oggetti database.</li>
</ul>

<p align="justify">Il view model deve essere minimo.</p>

### Errore 7 — usare SSR per evitare di capire HTTP

<p align="justify">SSR usa comunque HTTP, status, header, cookie e redirect.</p>

---

## 19. Esempio minimo

```js
router.get("/", requireAuth, (req, res) => {
  const posts = postStore.list();
  res.render("feed.njk", {
    currentUser: req.auth.user,
    posts: buildFeedViewModel(req.auth.user, posts),
  });
});
```

<p align="justify">Il template non riceve <code>postStore</code>.</p>

---

## 20. Esempio realistico: create con PRG

```js
router.post("/posts", requireAuth, (req, res) => {
  const input = requireValid(validateNewPost({ text: req.body.text }));
  postStore.create({
    text: input.text,
    authorId: req.auth.user.id,
  });
  res.redirect(303, "/ssr");
});
```

<p align="justify">Qui sono visibili tre confini:</p>

```text
body form -> validation
session   -> author identity
mutation  -> 303 -> GET
```

---

## 21. Esempio realistico: delete owner-only

```js
router.post("/posts/:id/delete", requireAuth, (req, res) => {
  const result = postStore.deleteOwned(req.params.id, req.auth.user.id);

  if (result.status === "not-found") {
    throw new HttpError(404, "post-not-found", "Post non trovato.");
  }
  if (result.status === "forbidden") {
    throw new HttpError(403, "forbidden", "Operazione non consentita.");
  }

  res.redirect(303, "/ssr");
});
```

<p align="justify">Il template puo nascondere il form ai non-owner, ma questa route resta l'autorita.</p>

---

## 22. Cosa NON introduciamo in questo blocco

<p align="justify">Non introduciamo ancora:</p>

<ul>
  <li>React/Vue;</li>
  <li>hydration;</li>
  <li>server components;</li>
  <li>HTMX;</li>
  <li>Turbo;</li>
  <li>ORM;</li>
  <li>rendering distribuito/edge;</li>
  <li>caching HTML avanzato.</li>
</ul>

<p align="justify">Prima vogliamo confrontare chiaramente <strong>due modelli semplici</strong>.</p>

---

## Esercizi A–F

### A — osserva

<p align="justify">Trasforma <code>user + posts</code> in un view model deterministicamente testabile.</p>

### B — modifica controllata

<p align="justify">Completa un template Nunjucks e verifica autoescape e rendering condizionale.</p>

### C — implementazione autonoma

<p align="justify">Aggiungi il presentation adapter SSR a Feisbuc milestone 7 senza cambiare DB/session/domain boundary.</p>

### D — debug/diagnosi

<p align="justify">Trova <code>|safe</code>, authorization soltanto visiva, mutating GET/assenza PRG e dati eccessivi nel template context.</p>

### E — mini-project

<p align="justify">Aggiungi una pagina profilo SSR riusando layout e sessione.</p>

### F — prodotto integrato

<p align="justify">Confronta la stessa feature implementata via API/client render e via SSR, documentando trade-off e evidence HTTP.</p>

---

## Laboratorio

<p align="justify">Aprire due finestre DevTools Network:</p>

<ol>
  <li>usare Feisbuc API/client;</li>
  <li>usare Feisbuc <code>/ssr</code>.</li>
</ol>

<p align="justify">Per ciascuna azione annotare:</p>

```text
request
status
Content-Type
redirect eventuale
numero di request
chi produce HTML
stato mantenuto dal browser
```

---

## Verifica rapida

<ol>
  <li>SSR e un protocollo diverso da HTTP? <strong>No</strong>.</li>
  <li>Un template deve interrogare SQLite? <strong>No</strong>.</li>
  <li><code>canDelete</code> nel template autorizza la DELETE? <strong>No</strong>.</li>
  <li>Perche <code>303</code> dopo una POST? Per separare mutazione e successiva GET.</li>
  <li><code>autoescape</code> permette di fidarsi di ogni input? <strong>No</strong>, riduce il rischio di interpretare testo come HTML; non sostituisce validation e security design.</li>
  <li>Possiamo avere API e SSR nella stessa applicazione? <strong>Si</strong>.</li>
</ol>

---

## Sintesi inclusiva

```text
API rendering:
server -> JSON -> browser JS -> HTML

SSR:
server -> view model -> template -> HTML
```

<p align="justify">Le regole di dominio e sicurezza devono rimanere fuori dalla vista.</p>

```text
view model = dati preparati per mostrare

template = HTML + presentazione

authorization = decisione server-side
```

<p align="justify">Feisbuc milestone 8 dimostra che possiamo cambiare presentation layer senza buttare via autenticazione, sessione e persistenza.</p>

---

## Fonti e collegamenti

<ul>
  <li>Nunjucks documentation: Environment, FileSystemLoader, Express integration, autoescape;</li>
  <li>Express 5 documentation;</li>
  <li>MDN HTTP, forms, redirects e cookies;</li>
  <li>RFC 9110 per semantica HTTP;</li>
  <li><code>kinderp/lab10</code> snapshot <code>7319c0696c8a6f76237e1ef21b4c3c2b535c4958</code> come provenance storica del passaggio SQL -> template.</li>
</ul>

<p align="justify">Nessun testo esterno viene copiato nel materiale: le fonti sono reference tecniche/provenance.</p>

## Activity correlate

<ul>
  <li><code>tpsi5-activity-a-ssr-view-model-001</code>;</li>
  <li><code>tpsi5-activity-b-nunjucks-autoescape-001</code>;</li>
  <li><code>tpsi5-activity-c-feisbuc-ssr-001</code>;</li>
  <li><code>tpsi5-activity-d-debug-ssr-boundaries-001</code>.</li>
</ul>
