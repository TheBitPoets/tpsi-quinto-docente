# SSR e template server-side: stesso dominio, altra responsabilita

## Obiettivi

Al termine del modulo lo studente sa:

- distinguere **server-side rendering (SSR)** da client-side rendering;
- spiegare che SSR e SPA sono due strategie di rendering, non una scala `vecchio -> nuovo`;
- descrivere il flusso `request -> controller/router -> view model -> template -> HTML response`;
- usare Nunjucks 3.2.4 con Express 5 e `autoescape: true`;
- separare query/storage, authorization, view model e template;
- riconoscere quando l'HTML deve essere prodotto dal server e quando dal browser;
- usare Post/Redirect/Get per le mutazioni provenienti da form HTML;
- mantenere la stessa autenticazione/sessione e lo stesso database tra API JSON e pagine SSR;
- riconoscere che nascondere un bottone nel template **non e authorization**;
- riconoscere il rischio di `|safe` su contenuto non fidato.

## Prerequisiti

- UDA 23: HTTP, status, redirect e representation;
- UDA 24: Express Router/middleware/error model;
- SQL raw e repository;
- autenticazione, session cookie e ownership;
- HTML semantico e form.

---

## Problema iniziale

Feisbuc milestone 7 funziona cosi:

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

Il server produce **dati**; il browser produce la parte dinamica dell'HTML.

Ma non e l'unica possibilita. Possiamo usare gli stessi dati, lo stesso utente e la stessa sessione e cambiare soltanto il responsabile del rendering:

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

La domanda didattica non e:

> Quale delle due tecniche e moderna?

La domanda utile e:

> Dove conviene produrre l'HTML per questa interazione e quali responsabilita cambiano?

---

## 1. Rendering: trasformare stato in interfaccia

Abbiamo gia usato il modello:

```text
state -> render -> DOM
```

Con SSR il concetto non sparisce. Cambia il luogo in cui avviene il rendering:

```text
server state -> template -> HTML string -> HTTP response
```

In entrambi i casi esistono:

- dati;
- una trasformazione;
- markup risultante;
- interazioni successive.

Quindi SSR non elimina JavaScript per definizione e SPA non elimina il server.

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

Database e regole di accesso possono rimanere gli stessi.

---

## 3. Il template non e il database layer

Un errore frequente e trasformare un template engine in un punto in cui fare tutto:

```text
route
  -> query SQL
  -> logica auth
  -> formattazione
  -> HTML
```

Noi manteniamo invece:

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

Il template deve ricevere dati **gia pronti per la presentazione**.

---

## 4. Template engine

Un template contiene HTML con punti di sostituzione e controllo presentazionale:

```html
<h2>{{ post.author }}</h2>
<p>{{ post.text }}</p>
```

Iterazione:

```html
{% for post in posts %}
  <article>
    <h2>{{ post.author }}</h2>
    <p>{{ post.text }}</p>
  </article>
{% endfor %}
```

Condizione:

```html
{% if post.canDelete %}
  <button>Elimina</button>
{% endif %}
```

La condizione `canDelete` e una decisione di **presentazione**: mostrare o meno un controllo.

La decisione di sicurezza deve comunque essere ripetuta/autorevolmente applicata sul server quando arriva la request di eliminazione.

---

## 5. Nunjucks nel corso

Per questo confronto usiamo:

```text
nunjucks 3.2.4
```

La configurazione di riferimento crea un Environment esplicito:

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

`autoescape: true` e una protezione importante quando il template stampa contenuto utente.

---

## 6. View model: preparare dati per la vista

Il post persistente puo essere:

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

Il template ha bisogno anche di informazioni puramente visuali:

```js
{
  ...post,
  canDelete: post.authorId === currentUser.id,
  likedLabel: post.liked ? "Non mi piace piu" : "Mi piace"
}
```

Queste proprieta sono un **view model**.

Vantaggi:

- template piu semplice;
- logica JavaScript testabile senza HTML;
- meno accesso a strutture applicative dal template;
- decisioni di presentazione visibili.

Attenzione:

```text
canDelete == true nel view model
```

non sostituisce:

```text
postStore.deleteOwned(postId, req.auth.user.id)
```

---

## 7. Template inheritance

Una pagina reale ripete shell, metadata e navigazione.

Nunjucks permette:

```html
{% extends "base.njk" %}

{% block content %}
  ...
{% endblock %}
```

`base.njk` puo contenere:

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

L'obiettivo non e usare il massimo numero di feature del template engine, ma rendere esplicita la composizione delle viste.

---

## 8. Autoescape e contenuto utente

Supponiamo che un post contenga:

```text
<script>alert('x')</script>
```

Con autoescape attivo:

```html
{{ post.text }}
```

viene trattato come **testo**, non come markup da eseguire.

Un pattern pericoloso e:

```html
{{ post.text | safe }}
```

`safe` dice deliberatamente al template engine:

> Questo valore e HTML fidato.

Non va applicato a contenuto arbitrario degli utenti.

La regola didattica resta coerente con il DOM:

```text
client rendering -> textContent
server rendering -> autoescape
```

Entrambe partono dallo stesso principio: i dati utente non diventano automaticamente codice/markup.

---

## 9. GET deve restare safe

La pagina SSR viene letta con:

```http
GET /ssr
```

Il GET non deve creare o eliminare post.

Per creare un post da un form HTML:

```http
POST /ssr/posts
```

Per eliminare tramite normale form HTML, che supporta GET e POST:

```http
POST /ssr/posts/:id/delete
```

Questa route non sostituisce la REST API:

```http
DELETE /api/posts/:id
```

Sono due interfacce HTTP per due interaction model differenti.

---

## 10. Post/Redirect/Get

Se dopo una POST restituiamo direttamente la pagina HTML:

```text
POST form
  -> mutate
  -> 200 HTML
```

un refresh puo proporre la ripetizione della POST.

Usiamo invece:

```text
POST /ssr/posts
  -> mutate
  -> 303 See Other
  -> Location: /ssr
  -> GET /ssr
```

Questo pattern e chiamato **Post/Redirect/Get (PRG)**.

Il `303` rende esplicito che la navigazione successiva deve essere una GET.

---

## 11. Form HTML e Content-Type

Un form standard invia tipicamente:

```http
Content-Type: application/x-www-form-urlencoded
```

Quindi il server SSR aggiunge:

```js
express.urlencoded({ extended: false, limit: "16kb" })
```

La API JSON continua invece a usare:

```js
express.json(...)
```

Il protocollo HTTP e lo stesso; cambia la representation del body.

---

## 12. Sessione condivisa

Non creiamo una seconda autenticazione per SSR.

Il browser possiede gia il cookie HttpOnly della milestone 7:

```text
feisbuc.sid=<opaque token>
```

`loadAuth` continua a produrre:

```js
req.auth.user
```

Sia le route API sia le route SSR usano lo stesso contesto autenticato.

```text
cookie
  -> loadAuth
  -> req.auth.user
       |              |
       v              v
   /api/posts       /ssr
```

Questo e un esempio concreto di **riuso del dominio e della security boundary tra due presentation layer**.

---

## 13. Status e redirect

Nel ramo SSR useremo principalmente:

- `200` per pagina resa correttamente;
- `303` dopo una POST riuscita;
- `401` se manca autenticazione;
- `403` se l'utente tenta una mutazione non autorizzata;
- `404` se la risorsa non esiste.

Il fatto che una response contenga HTML non cambia la semantica HTTP.

---

## 14. Feisbuc milestone 8: SSR senza buttare via la API

Milestone 8 **non elimina** `/api/*`.

Aggiunge un secondo presentation adapter:

```text
                    +-> JSON API -> JS -> DOM
Domain / stores ----|
                    +-> SSR Router -> view model -> Nunjucks -> HTML
```

Route SSR:

```text
GET  /ssr
POST /ssr/posts
POST /ssr/posts/:id/delete
```

La pagina SSR usa:

- stessa sessione;
- stesso `SqlPostStore`;
- stessa validation del testo;
- stessa ownership;
- stessi post persistenti.

---

## 15. Confronto tra implementazioni

### API + client rendering

Pro:

- UI altamente interattiva senza full navigation;
- API riutilizzabile da piu client;
- frontend e backend possono evolvere separatamente.

Costo:

- piu stato e orchestration nel browser;
- loading/error/render da gestire nel client;
- hydration/build framework possibili nei sistemi piu complessi.

### SSR classico

Pro:

- prima response contiene gia HTML utile;
- form e navigation funzionano bene con meccanismi browser standard;
- meno JavaScript necessario per molte interazioni CRUD.

Costo:

- molte interazioni provocano navigation completa;
- il server ha responsabilita di rendering;
- componentizzazione/stato UI ricco richiedono altre tecniche.

### Conclusione

Non esiste:

```text
SSR < SPA
```

Esiste:

```text
requirements -> trade-off -> scelta
```

---

## 16. SSR non significa zero JavaScript

Una pagina SSR puo comunque usare JavaScript per:

- progressive enhancement;
- menu;
- validazione UX;
- realtime;
- aggiornamenti parziali.

La distinzione e dove viene generato il markup iniziale e come evolve l'interazione.

---

## 17. SSR e accessibilita/progressive enhancement

Form e link standard hanno un valore architetturale:

```html
<form method="post" action="/ssr/posts">
  ...
</form>
```

Funzionano secondo il modello di navigazione HTTP senza richiedere un event handler JavaScript.

Questo non garantisce automaticamente accessibilita, ma rende visibile un baseline funzionale che puo essere migliorato progressivamente.

---

## 18. Errori frequenti e security review

### Errore 1 — SQL nel template

```text
template -> database
```

Da evitare. Il template riceve il view model.

### Errore 2 — authorization soltanto nella vista

```html
{% if post.canDelete %}
  <button>Elimina</button>
{% endif %}
```

Serve per UX, non per sicurezza.

La route deve verificare ownership.

### Errore 3 — `|safe` su dati utente

```html
{{ post.text | safe }}
```

Se il testo non e trusted HTML, stiamo bypassando l'escape.

### Errore 4 — mutazione con GET

```http
GET /delete/123
```

GET deve restare safe.

### Errore 5 — niente PRG

POST seguito da HTML 200 puo generare resubmit su refresh.

### Errore 6 — passare al template tutto l'oggetto DB

Non passiamo:

- `password_hash`;
- session hash;
- secret interni;
- oggetti database.

Il view model deve essere minimo.

### Errore 7 — usare SSR per evitare di capire HTTP

SSR usa comunque HTTP, status, header, cookie e redirect.

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

Il template non riceve `postStore`.

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

Qui sono visibili tre confini:

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

Il template puo nascondere il form ai non-owner, ma questa route resta l'autorita.

---

## 22. Cosa NON introduciamo in questo blocco

Non introduciamo ancora:

- React/Vue;
- hydration;
- server components;
- HTMX;
- Turbo;
- ORM;
- rendering distribuito/edge;
- caching HTML avanzato.

Prima vogliamo confrontare chiaramente **due modelli semplici**.

---

## Esercizi A–F

### A — osserva

Trasforma `user + posts` in un view model deterministicamente testabile.

### B — modifica controllata

Completa un template Nunjucks e verifica autoescape e rendering condizionale.

### C — implementazione autonoma

Aggiungi il presentation adapter SSR a Feisbuc milestone 7 senza cambiare DB/session/domain boundary.

### D — debug/diagnosi

Trova `|safe`, authorization soltanto visiva, mutating GET/assenza PRG e dati eccessivi nel template context.

### E — mini-project

Aggiungi una pagina profilo SSR riusando layout e sessione.

### F — prodotto integrato

Confronta la stessa feature implementata via API/client render e via SSR, documentando trade-off e evidence HTTP.

---

## Laboratorio

Aprire due finestre DevTools Network:

1. usare Feisbuc API/client;
2. usare Feisbuc `/ssr`.

Per ciascuna azione annotare:

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

1. SSR e un protocollo diverso da HTTP? **No**.
2. Un template deve interrogare SQLite? **No**.
3. `canDelete` nel template autorizza la DELETE? **No**.
4. Perche `303` dopo una POST? Per separare mutazione e successiva GET.
5. `autoescape` permette di fidarsi di ogni input? **No**, riduce il rischio di interpretare testo come HTML; non sostituisce validation e security design.
6. Possiamo avere API e SSR nella stessa applicazione? **Si**.

---

## Sintesi inclusiva

```text
API rendering:
server -> JSON -> browser JS -> HTML

SSR:
server -> view model -> template -> HTML
```

Le regole di dominio e sicurezza devono rimanere fuori dalla vista.

```text
view model = dati preparati per mostrare

template = HTML + presentazione

authorization = decisione server-side
```

Feisbuc milestone 8 dimostra che possiamo cambiare presentation layer senza buttare via autenticazione, sessione e persistenza.

---

## Fonti e collegamenti

- Nunjucks documentation: Environment, FileSystemLoader, Express integration, autoescape;
- Express 5 documentation;
- MDN HTTP, forms, redirects e cookies;
- RFC 9110 per semantica HTTP;
- `kinderp/lab10` snapshot `7319c0696c8a6f76237e1ef21b4c3c2b535c4958` come provenance storica del passaggio SQL -> template.

Nessun testo esterno viene copiato nel materiale: le fonti sono reference tecniche/provenance.

## Activity correlate

- `tpsi5-activity-a-ssr-view-model-001`;
- `tpsi5-activity-b-nunjucks-autoescape-001`;
- `tpsi5-activity-c-feisbuc-ssr-001`;
- `tpsi5-activity-d-debug-ssr-boundaries-001`.
