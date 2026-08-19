# JavaScript moderno, DOM e Browser APIs

Stato: **draft didattico**. Modulo di UDA 22. L'obiettivo non e imparare una lunga lista di sintassi, ma capire come JavaScript rappresenta dati e comportamento e come il browser espone la pagina attraverso API manipolabili dal programma.

## Obiettivi

Al termine del modulo lo studente deve saper:

- distinguere **ECMAScript** dal DOM e dalle altre Web APIs del browser;
- usare `const` e `let` in modo consapevole e spiegare perche `var` non e la scelta predefinita del corso;
- riconoscere primitive, array, object, `null` e `undefined` nei casi d'uso piu comuni;
- distinguere riassegnazione di una variabile da mutazione di un oggetto;
- usare template literal, destructuring, spread e optional chaining quando migliorano leggibilita;
- manipolare collezioni con `map`, `filter`, `find`, `some`, `every` e, quando utile, `reduce`;
- scrivere funzioni, callback e arrow function senza trattarle come sintassi magica;
- comprendere scope a blocchi e problemi causati da stato globale non necessario;
- separare codice in ES modules con `import` ed `export`;
- selezionare elementi DOM con `querySelector`/`querySelectorAll`;
- creare e modificare nodi con `createElement`, `textContent`, `classList`, `dataset` e `append`;
- registrare eventi con `addEventListener` e usare correttamente l'oggetto `Event`;
- distinguere `target` e `currentTarget` e spiegare il bubbling;
- usare **event delegation** quando gli elementi possono essere creati dinamicamente;
- intercettare una form con `submit`, `preventDefault()` e `FormData`;
- usare `localStorage` e `sessionStorage` per dati semplici, serializzando oggetti con JSON;
- organizzare una piccola UI secondo il flusso `state -> render -> events -> new state`;
- diagnosticare errori JavaScript con console, breakpoint, stack trace e DevTools.

## Prerequisiti

- UDA 21: HTML semantico, CSS responsive e Bootstrap;
- concetti generali di variabile, selezione, iterazione e funzione studiati negli anni precedenti;
- uso essenziale della console e di DevTools.

## Problema iniziale

HTML descrive **che cosa esiste** nella pagina. CSS descrive **come appare**. Ma come facciamo a dire:

> quando l'utente preme "Mi piace", aggiorna il post; quando pubblica, aggiungi un nuovo articolo al feed; se ricarica la pagina, conserva i post locali?

Serve comportamento. Nel browser, gran parte di questo comportamento viene scritto in JavaScript.

La prima idea da fissare e pero questa:

```text
JavaScript language != browser
```

JavaScript e il linguaggio. Il browser e un ambiente che offre oggetti e API aggiuntive.

## ECMAScript, JavaScript e Web APIs

Lo standard del linguaggio si chiama **ECMAScript**. La specifica tecnica descrive sintassi e semantica di dichiarazioni, funzioni, object, array, module e cosi via.

Il browser aggiunge API come:

```text
Window
Document
Element
Event
Storage
console
setTimeout
fetch
WebSocket
...
```

Per esempio:

```js
const posts = [];
```

usa solo il linguaggio ECMAScript.

```js
const feed = document.querySelector("#feed");
```

usa anche la DOM API fornita dal browser.

Questa distinzione diventera essenziale quando useremo JavaScript anche in Node.js: stesso linguaggio, ambiente e API differenti.

Riferimenti professionali:

- MDN JavaScript Guide: <https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide>
- ECMAScript specification: <https://tc39.es/ecma262/>
- MDN DOM scripting: <https://developer.mozilla.org/en-US/docs/Learn_web_development/Core/Scripting/DOM_scripting>

## `const`, `let` e il significato di una variabile

### Regola pratica del corso

Parti da `const`.

Usa `let` quando **la variabile deve essere riassegnata**.

Non usare `var` come scelta predefinita.

```js
const course = "TPSI";
let currentPost = 0;

currentPost += 1;
```

`const` non significa "oggetto immutabile".

```js
const post = {
  text: "Primo post",
  likes: 0,
};

post.likes += 1; // valido
```

Non stiamo assegnando un nuovo oggetto alla variabile `post`: stiamo modificando una proprieta dell'oggetto esistente.

Questo invece non e valido:

```js
const post = { text: "Ciao" };
post = { text: "Altro" };
```

### Perche non trasformiamo ogni errore in una regola da memorizzare

Nel vecchio materiale `lab3` esiste un esempio che assegna un nuovo valore a una `const`. Nel nuovo corso non lo presentiamo come normale codice da eseguire fino in fondo: diventa un esperimento controllato per osservare l'errore e capire la differenza fra **binding** e **mutazione**.

## Valori e tipi che ci servono davvero

Per il corso non partiamo da un catalogo enciclopedico. Partiamo dai dati di Feisbuc.

```js
const author = "Ada";          // string
const likes = 3;                // number
const liked = false;            // boolean
const deletedAt = null;         // null esplicito
let selectedPost;               // undefined finche non assegniamo
const tags = ["web", "tpsi"];  // array
const post = {                   // object
  author,
  likes,
  liked,
  tags,
};
```

### `null` e `undefined`

Useremo questa convenzione didattica:

- `undefined`: un valore non e stato ancora fornito/trovato;
- `null`: il programma rappresenta intenzionalmente l'assenza di un valore.

Non e una legge universale di ogni codebase, ma e una convenzione leggibile.

### Controllare il tipo

```js
console.log(typeof likes);  // "number"
console.log(typeof author); // "string"
```

Ricorda che JavaScript ha alcune particolarita storiche. Non cercheremo di impararle tutte a memoria: quando serve controlliamo MDN.

## Uguaglianza: preferire `===`

Nel core del corso usiamo normalmente:

```js
if (post.likes === 0) {
  // ...
}
```

invece di affidarsi alla conversione implicita di `==`.

L'obiettivo e ridurre comportamento sorprendente mentre costruiamo un modello mentale solido.

## Stringhe e template literal

```js
const author = "Ada";
const likes = 4;
const label = `${author} ha ${likes} like`;
```

Le template literal sono particolarmente utili quando combiniamo testo e valori, ma non devono diventare un modo per costruire grandi blocchi HTML non controllati.

## Array: una collezione ordinata

```js
const posts = [
  { id: 1, author: "Ada", likes: 4 },
  { id: 2, author: "Linus", likes: 1 },
  { id: 3, author: "Grace", likes: 7 },
];
```

### Leggere senza trasformare

```js
console.log(posts.length);
console.log(posts[0]);
```

### Cercare

```js
const post = posts.find((item) => item.id === 2);
const hasPopularPost = posts.some((item) => item.likes >= 5);
const allHaveAuthors = posts.every((item) => item.author.length > 0);
```

### Filtrare

```js
const popular = posts.filter((item) => item.likes >= 5);
```

`filter` produce un nuovo array contenente soltanto gli elementi che superano il test.

### Trasformare

```js
const labels = posts.map((item) => `${item.author}: ${item.likes}`);
```

`map` produce un nuovo array con un elemento di output per ogni elemento di input.

### `reduce`: utile, non obbligatorio ovunque

```js
const totalLikes = posts.reduce((sum, item) => sum + item.likes, 0);
```

`reduce` e potente, ma non e automaticamente migliore di codice piu semplice. Nel corso lo usiamo quando rende chiaro che stiamo **accumulando** un risultato.

### Metodi che mutano e metodi che restituiscono nuovi valori

E importante sapere se un'operazione modifica l'array originale.

```js
posts.push(newPost); // muta posts
```

```js
const visiblePosts = posts.filter((post) => !post.hidden); // nuovo array
```

Quando non ricordiamo il comportamento esatto di un metodo, la risposta professionale e aprire la documentazione.

Riferimento: <https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Array>

## Object: dati con un significato

```js
const post = {
  id: crypto.randomUUID(),
  author: "Ada",
  text: "Sto studiando il DOM",
  likes: 0,
  liked: false,
};
```

### Property access

```js
console.log(post.author);
console.log(post["author"]);
```

La forma con punto e normalmente la piu leggibile quando conosciamo il nome della proprieta.

## Destructuring

```js
const { author, text, likes } = post;
```

equivale concettualmente a estrarre le proprieta che ci interessano.

Con gli array:

```js
const [firstPost, secondPost] = posts;
```

Non usiamo destructuring per rendere il codice "piu moderno": lo usiamo quando riduce rumore.

## Spread: copiare una struttura superficiale

```js
const likedPost = {
  ...post,
  liked: true,
  likes: post.likes + 1,
};
```

Abbiamo creato un **nuovo object** copiando le proprieta di `post` e sostituendo quelle indicate dopo.

Per un array:

```js
const newPosts = [...posts, newPost];
```

Lo spread e superficiale (*shallow*): se dentro l'oggetto ci sono altri oggetti/array, quei valori richiedono attenzione. La copia profonda non viene data per scontata.

## Optional chaining e nullish coalescing

Quando un valore puo mancare:

```js
const city = user.profile?.city ?? "Citta non indicata";
```

- `?.` interrompe l'accesso se la parte precedente e `null`/`undefined`;
- `??` usa il valore a destra soltanto per `null`/`undefined`.

Non sostituiscono una buona modellazione dei dati.

## Funzioni: comportamento riutilizzabile

### Function declaration

```js
function formatPost(post) {
  return `${post.author}: ${post.text}`;
}
```

### Function expression

```js
const formatPost = function (post) {
  return `${post.author}: ${post.text}`;
};
```

### Arrow function

```js
const formatPost = (post) => `${post.author}: ${post.text}`;
```

Non scegliamo arrow function perche e "piu nuova". La scegliamo spesso per callback brevi e funzioni locali. Prima di usare `this` in una arrow function bisogna conoscere la differenza semantica: verra approfondita nel track advanced quando servira.

## Le funzioni sono valori

Possiamo passare una funzione a un'altra funzione:

```js
const published = posts.filter((post) => post.published);
```

La funzione:

```js
(post) => post.published
```

viene passata a `filter` come callback.

Questo concetto ritornera continuamente con gli eventi:

```js
button.addEventListener("click", handleClick);
```

anche `handleClick` e un valore funzione passato a un'altra API.

## Scope: dove esiste un nome

`let` e `const` hanno scope di blocco.

```js
if (posts.length > 0) {
  const first = posts[0];
  console.log(first);
}

// console.log(first); // first non esiste qui
```

Ridurre lo stato globale rende piu facile capire chi puo modificare cosa.

### Evitare il contatore globale quando possiamo modellare meglio l'identita

Il Feisbuc legacy usa un `counter` globale per produrre id dei like button. Nel nuovo progetto possiamo dare un'identita al **post**, non al pulsante:

```js
const post = {
  id: crypto.randomUUID(),
  text: "...",
};
```

Nel DOM possiamo poi usare:

```html
<article data-post-id="..."></article>
```

L'identita appartiene al dato; l'interfaccia la rappresenta.

## Errori: fallire in modo comprensibile

```js
function parsePosts(json) {
  try {
    const value = JSON.parse(json);

    if (!Array.isArray(value)) {
      throw new TypeError("Atteso un array di post");
    }

    return value;
  } catch (error) {
    console.error("Impossibile leggere i post", error);
    return [];
  }
}
```

Non usiamo `try/catch` per nascondere ogni errore. Lo usiamo quando sappiamo **che cosa possiamo recuperare** o quando vogliamo aggiungere contesto utile.

## ES modules nel browser

HTML:

```html
<script type="module" src="app.js"></script>
```

`posts.js`:

```js
export function createPost(author, text) {
  return {
    id: crypto.randomUUID(),
    author,
    text,
    likes: 0,
    liked: false,
  };
}
```

`app.js`:

```js
import { createPost } from "./posts.js";

const post = createPost("Ada", "Ciao moduli!");
console.log(post);
```

Il vecchio `lab3` mostra anche CommonJS e moduli Node.js. E materiale utile piu avanti nel backend, ma **non e il modello iniziale del browser**. In UDA 22 iniziamo dal module system standard `import`/`export`; CommonJS verra contestualizzato quando confronteremo ambienti e pacchetti Node.

Riferimenti:

- <https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide/Modules>
- <https://tc39.es/ecma262/#sec-modules>

## Il DOM: il documento come oggetti in memoria

Il browser interpreta HTML e costruisce una rappresentazione manipolabile.

```text
HTML source
    |
    v
browser parser
    |
    v
DOM tree
    |
    +--> Document
           |
           +--> Element
           +--> Element
           +--> ...
```

`document` e il punto di ingresso piu comune.

## Selezionare elementi

```js
const feed = document.querySelector("#feed");
const posts = document.querySelectorAll("#feed article");
```

`querySelector()` restituisce il primo elemento che corrisponde al selettore oppure `null`.

Questo significa che dobbiamo ragionare anche sul caso "elemento non trovato":

```js
const feed = document.querySelector("#feed");

if (!feed) {
  throw new Error("#feed non trovato");
}
```

Riferimento: <https://developer.mozilla.org/en-US/docs/Web/API/Document/querySelector>

## Leggere e modificare il DOM

```js
const title = document.querySelector("#feed-title");
title.textContent = "Feed aggiornato";
```

### `textContent` prima di `innerHTML` quando dobbiamo inserire testo

Se il contenuto proviene dall'utente:

```js
paragraph.textContent = userText;
```

lo trattiamo come testo.

Non costruiamo markup concatenando input utente dentro `innerHTML` senza una ragione precisa. La sicurezza XSS verra approfondita nel modulo security, ma l'abitudine parte subito.

## Creare elementi

```js
const article = document.createElement("article");
article.classList.add("card", "mb-3");
article.dataset.postId = post.id;

const heading = document.createElement("h3");
heading.textContent = post.author;

const body = document.createElement("p");
body.textContent = post.text;

article.append(heading, body);
feed.append(article);
```

La pagina diventa dinamica senza perdere la semantica HTML.

## `classList` e `dataset`

```js
button.classList.toggle("active", post.liked);
```

```js
article.dataset.postId = post.id;
```

HTML risultante:

```html
<article data-post-id="...">...</article>
```

`dataset` e utile per collegare un elemento visuale all'identita del dato senza inventare id globali per ogni controllo.

## Eventi: "quando succede X, esegui Y"

```js
const button = document.querySelector("#share-button");
button.addEventListener("click", handleShare);
```

```js
function handleShare(event) {
  console.log(event.type);
}
```

La callback viene eseguita **quando** l'evento avviene, non quando registriamo il listener.

Riferimento: <https://developer.mozilla.org/en-US/docs/Web/API/EventTarget/addEventListener>

## `target` e `currentTarget`

Dentro un listener:

```js
function handleClick(event) {
  console.log(event.target);
  console.log(event.currentTarget);
}
```

- `target`: l'elemento da cui l'evento ha avuto origine;
- `currentTarget`: l'elemento sul quale sta girando quel listener.

La differenza e fondamentale per l'event delegation.

## Bubbling

Molti eventi risalgono dall'elemento originario verso i suoi antenati.

```text
button
  -> article
      -> section#feed
          -> main
              -> document
```

Questo ci permette di ascoltare una sola volta un contenitore stabile.

## Event delegation

Problema:

1. all'avvio abbiamo due post;
2. registriamo listener sui loro pulsanti;
3. dopo un minuto JavaScript crea un nuovo post;
4. il nuovo pulsante non esisteva quando abbiamo registrato i listener.

Soluzione:

```js
feed.addEventListener("click", (event) => {
  const likeButton = event.target.closest("[data-action='like']");

  if (!likeButton) {
    return;
  }

  const article = likeButton.closest("[data-post-id]");
  if (!article) {
    return;
  }

  toggleLike(article.dataset.postId);
});
```

Un solo listener sul feed gestisce anche controlli creati successivamente.

Il Feisbuc legacy contiene gia l'intuizione dell'event delegation; la conserveremo, ma riscriveremo identificazione, gestione dello stato e aggiornamento DOM.

## Form: ascoltare `submit`, non soltanto il click

HTML:

```html
<form id="composer-form">
  <label for="post-text">Nuovo post</label>
  <textarea id="post-text" name="text" required></textarea>
  <button type="submit">Pubblica</button>
</form>
```

JavaScript:

```js
form.addEventListener("submit", (event) => {
  event.preventDefault();

  const data = new FormData(form);
  const text = String(data.get("text") ?? "").trim();

  if (!text) {
    return;
  }

  addPost(text);
  form.reset();
});
```

Ascoltare `submit` copre anche invii da tastiera e rispetta meglio il modello della form.

### Un bug concreto del Feisbuc legacy

Nel vecchio `add_post.js` il listener riceve il parametro `e`, ma chiama:

```js
event.preventDefault();
```

invece di:

```js
e.preventDefault();
```

Il nuovo corso trasforma questo genere di problema in un'attivita D di diagnosi, non in una correzione nascosta.

## Stato dell'applicazione

Una UI diventa molto piu comprensibile se separiamo:

```text
STATE
  |
  v
RENDER
  |
  v
DOM
  ^
  |
EVENTS
  |
  v
NEW STATE
```

Esempio:

```js
let posts = [];

function addPost(text) {
  posts = [
    ...posts,
    {
      id: crypto.randomUUID(),
      author: "Studente",
      text,
      likes: 0,
      liked: false,
    },
  ];

  renderPosts();
}
```

Non significa che ogni click debba ricostruire l'intera applicazione. Significa che **il dato e la fonte di verita**, mentre il DOM e una rappresentazione.

Questo prepara naturalmente componenti e framework frontend.

## Rendering con funzioni piccole

```js
function createPostElement(post) {
  const article = document.createElement("article");
  article.className = "card mb-3";
  article.dataset.postId = post.id;

  const body = document.createElement("div");
  body.className = "card-body";

  const title = document.createElement("h3");
  title.className = "h5";
  title.textContent = post.author;

  const text = document.createElement("p");
  text.textContent = post.text;

  body.append(title, text);
  article.append(body);
  return article;
}
```

Poi:

```js
function renderPosts() {
  feed.replaceChildren(...posts.map(createPostElement));
}
```

Qui si incontrano due mondi del modulo:

```text
array.map(...)
      +
DOM createElement(...)
      =
render della UI
```

## Web Storage

Per una prima persistenza locale non serve ancora un server.

```js
localStorage.setItem("feisbuc.posts", JSON.stringify(posts));
```

Lettura:

```js
const raw = localStorage.getItem("feisbuc.posts");
const savedPosts = raw ? JSON.parse(raw) : [];
```

### `localStorage` vs `sessionStorage`

Entrambi espongono una semplice interfaccia chiave/valore, ma con ciclo di vita differente.

Nel corso:

- `localStorage`: preferenze o dati demo che devono sopravvivere alla riapertura;
- `sessionStorage`: dati temporanei della singola sessione/tab.

Non sono database applicativi e non devono contenere segreti.

Riferimento: <https://developer.mozilla.org/en-US/docs/Web/API/Web_Storage_API>

### Storage conserva stringhe

Questo non funziona come molti principianti immaginano:

```js
localStorage.setItem("posts", posts);
```

Per object/array usiamo JSON:

```js
localStorage.setItem("posts", JSON.stringify(posts));
```

```js
const posts = JSON.parse(localStorage.getItem("posts") ?? "[]");
```

## Isolare lo storage dietro funzioni

`storage.js`:

```js
const STORAGE_KEY = "feisbuc.posts";

export function savePosts(posts) {
  localStorage.setItem(STORAGE_KEY, JSON.stringify(posts));
}

export function loadPosts() {
  try {
    const raw = localStorage.getItem(STORAGE_KEY);
    return raw ? JSON.parse(raw) : [];
  } catch (error) {
    console.error("Storage Feisbuc non leggibile", error);
    return [];
  }
}
```

Il resto dell'app non deve conoscere ogni dettaglio del formato di persistenza.

## Feisbuc milestone 3: feed dinamico locale

Partiamo dalla UI Bootstrap della milestone 2 e introduciamo:

```text
form composer
     |
     v
Event submit
     |
     v
createPost()
     |
     v
posts state
     |
     +----> savePosts()
     |
     v
renderPosts()
     |
     v
DOM feed

click sul like
     |
     v
event delegation
     |
     v
update state
     +----> savePosts()
     |
     v
renderPosts()
```

Nessun server e nessun `fetch` in questa milestone.

E una scelta intenzionale: prima rendiamo comprensibile il comportamento client, poi in UDA 23 sostituiremo gradualmente la persistenza locale con un contratto HTTP/REST.

## Cosa NON entra ancora in UDA 22

### `fetch`

E una Web API importante, ma viene affrontata in UDA 23 insieme a HTTP.

### Promise e `async`/`await`

Il vecchio `lab3` le introduce nella sezione async. Nel nuovo corso le spostiamo a UDA 23, dove possiamo spiegare **perche** l'operazione e asincrona e collegarla a request/response, errori di rete e `fetch`.

### Node.js filesystem, CommonJS e package ecosystem

Verranno affrontati nel backend. Non li confondiamo con il primo modello di JavaScript nel browser.

### Prototype internals, metaprogramming e performance avanzata

Track advanced/senior.

## Debug JavaScript: metodo prima della modifica

Quando qualcosa non funziona:

1. **riproduci** il comportamento;
2. leggi la prima eccezione utile nella console;
3. apri lo stack trace;
4. controlla il valore delle variabili;
5. metti un breakpoint nel listener/funzione sospetta;
6. osserva `event.target`, `event.currentTarget` e lo stato;
7. formula un'ipotesi;
8. modifica una causa alla volta;
9. verifica anche il caso che funzionava gia.

### Errori frequenti

#### Usare una variabile globale inesistente al posto del parametro

```js
button.addEventListener("click", (e) => {
  event.preventDefault(); // sbagliato nel nostro codice legacy
});
```

Corretto:

```js
button.addEventListener("click", (event) => {
  event.preventDefault();
});
```

#### Registrare listener solo sugli elementi iniziali

```js
const buttons = document.querySelectorAll(".like");
buttons.forEach((button) => button.addEventListener("click", like));
```

Se i post vengono aggiunti dopo, i nuovi pulsanti non hanno quel listener.

Per un feed dinamico e spesso migliore la delegation sul contenitore stabile.

#### Costruire testo utente con HTML concatenato

```js
feed.innerHTML += `<p>${userText}</p>`;
```

Nel core preferiamo creare elementi e assegnare `textContent`.

#### Stato nel DOM ma non nei dati

Se il numero di like vive solo nel testo di un button, il programma perde una fonte di verita chiara.

#### Salvare object direttamente in localStorage

Lo storage conserva stringhe: serializzare/deserializzare esplicitamente.

#### `querySelector` senza controllare `null`

Il selettore puo essere sbagliato o il markup puo cambiare.

## Come leggere MDN in questo modulo

Per ogni API usiamo sempre lo stesso rituale:

```text
1. nome dell'API
2. che oggetto la espone
3. sintassi
4. input
5. valore restituito
6. esempio minimo
7. eccezioni / edge cases
8. compatibilita
9. link alla specifica
```

Esempio per `querySelector`:

- API: `Document.querySelector()`;
- input: selettore CSS;
- output: primo `Element` corrispondente oppure `null`;
- poi modifichiamo l'esempio nel nostro Feisbuc.

Questo e il comportamento che vogliamo trasferire al lavoro reale: **la documentazione non e una pagina da imparare a memoria, e uno strumento di lavoro**.

## Esercizi A-F

### A — esegui/osserva

Completa una pipeline JavaScript che riceve un array JSON di post e produce un riepilogo deterministico con `filter` e `map`. Viene corretto dal runner JavaScript di TheBitLab.

### B — modifica controllata

Rifattorizza una pipeline imperativa in funzioni piccole usando destructuring, spread e array methods, mantenendo lo stesso output.

### C — implementazione autonoma

Costruisci Feisbuc milestone 3: form, stato dei post, rendering DOM, event delegation e localStorage con ES modules.

### D — debug e diagnosi

Correggi una versione derivata dal JavaScript legacy che contiene `event/e`, listener non validi per post dinamici, stato disperso nel DOM e gestione storage fragile. Prima documenta la diagnosi.

### E — mini-progetto

Estendi Feisbuc con filtri locali, contatore post/like, preferenze sessione e una piccola vista vuota, mantenendo state/render separati.

### F — prodotto integrato

Arrivera piu avanti: il Feisbuc completo unira client, API REST, database, autenticazione, frontend componentizzato e realtime.

## Verifica rapida

1. Che differenza c'e tra ECMAScript e DOM?
2. Perche `const` non rende immutabile un object?
3. Che differenza c'e fra `map` e `filter`?
4. Perche una callback e importante anche per gli eventi?
5. Cosa restituisce `querySelector()` se non trova nulla?
6. Perche `textContent` e una buona scelta per testo inserito dall'utente?
7. Che differenza c'e fra `target` e `currentTarget`?
8. Perche l'event delegation aiuta con elementi dinamici?
9. Perche localStorage richiede JSON per array/object?
10. Perche `fetch` e `async/await` vengono spostati in UDA 23?

## Sintesi inclusiva

```text
JAVASCRIPT
= dati + decisioni + funzioni

BROWSER
= Window + Document + Web APIs

DOM
= pagina rappresentata come oggetti

EVENT
= qualcosa e successo

LISTENER
= funzione da eseguire quando succede

STATE
= dati dell'applicazione

RENDER
= trasforma state -> DOM

LOCAL STORAGE
= persistenza locale semplice, a stringhe

MODULE
= separa responsabilita con import/export
```

Per Feisbuc:

```text
utente scrive
   -> submit
   -> nuovo post nello state
   -> save
   -> render

utente clicca like
   -> bubbling
   -> listener sul feed
   -> trova post via data-post-id
   -> aggiorna state
   -> save
   -> render
```

## Fonti e collegamenti

### Documentazione tecnica

- MDN JavaScript Guide: <https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide>
- MDN Array: <https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Array>
- MDN JavaScript modules: <https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide/Modules>
- MDN DOM scripting: <https://developer.mozilla.org/en-US/docs/Learn_web_development/Core/Scripting/DOM_scripting>
- MDN `querySelector`: <https://developer.mozilla.org/en-US/docs/Web/API/Document/querySelector>
- MDN events: <https://developer.mozilla.org/en-US/docs/Learn_web_development/Core/Scripting/Events>
- MDN `addEventListener`: <https://developer.mozilla.org/en-US/docs/Web/API/EventTarget/addEventListener>
- MDN Web Storage API: <https://developer.mozilla.org/en-US/docs/Web/API/Web_Storage_API>
- ECMAScript language specification: <https://tc39.es/ecma262/>

### Provenance legacy

- `TheBitPoets/labs_summary` pinned dal Content Pack: progressione `lab2`/`lab3`/`lab4`;
- `kinderp/lab3` snapshot auditato: `0deae0eb606bc9c2849ba271bdf03c128910f1ac`;
- `TheBitPoets/feisbuc` pinned dal Content Pack: `add_post.js` e `like_button_pressed.js` usati come input di audit, non copiati come soluzione canonica.

### Teacher references

- Pluralsight JavaScript path registrato nel Content Pack come `teacher-reference` licensed;
- eventuali testi Manning JavaScript/Web Platform vengono usati solo come riferimenti di progettazione docente, senza ingestione automatica.

## Activity correlate

- `tpsi5-activity-a-js-feed-pipeline-001`;
- `tpsi5-activity-b-js-post-refactor-001`;
- `tpsi5-activity-c-feisbuc-dynamic-feed-001`;
- `tpsi5-activity-d-debug-feisbuc-js-001`.
