# JavaScript moderno, DOM e Browser APIs

<table align="center" width="100%"><tr><td>
<details>
<summary>&#128506; <strong>Orientamento della lezione</strong></summary>

<p align="justify"><strong>Contesto:</strong> HTML e CSS descrivono struttura e presentazione. JavaScript introduce stato e comportamento, mentre le Web API permettono al programma di interagire con documento, eventi e storage del browser.</p>
<p align="justify"><strong>Domande guida:</strong> che cosa appartiene al linguaggio e che cosa al browser? Come si mantiene una sola fonte di verità? Come si aggiorna il DOM senza perdere sicurezza e possibilità di debug?</p>
<p align="justify"><strong>Obiettivi osservabili:</strong> trasformare dati con funzioni e array methods, selezionare e creare nodi, gestire eventi e bubbling, separare stato e rendering e persistere uno snapshot locale.</p>
<p align="justify"><strong>Prossimo passo:</strong> la lezione 05 sostituirà lo storage locale come fonte condivisa con un contratto HTTP e una REST API.</p>

</details>
</td></tr></table>

<p align="justify">Stato: <strong>draft didattico</strong>. Modulo di UDA 22. L'obiettivo non e imparare una lunga lista di sintassi, ma capire come JavaScript rappresenta dati e comportamento e come il browser espone la pagina attraverso API manipolabili dal programma.</p>

## Obiettivi

<p align="justify">Al termine del modulo lo studente deve saper:</p>

<ul>
  <li>distinguere <strong>ECMAScript</strong> dal DOM e dalle altre Web APIs del browser;</li>
  <li>usare <code>const</code> e <code>let</code> in modo consapevole e spiegare perche <code>var</code> non e la scelta predefinita del corso;</li>
  <li>riconoscere primitive, array, object, <code>null</code> e <code>undefined</code> nei casi d'uso piu comuni;</li>
  <li>distinguere riassegnazione di una variabile da mutazione di un oggetto;</li>
  <li>usare template literal, destructuring, spread e optional chaining quando migliorano leggibilita;</li>
  <li>manipolare collezioni con <code>map</code>, <code>filter</code>, <code>find</code>, <code>some</code>, <code>every</code> e, quando utile, <code>reduce</code>;</li>
  <li>scrivere funzioni, callback e arrow function senza trattarle come sintassi magica;</li>
  <li>comprendere scope a blocchi e problemi causati da stato globale non necessario;</li>
  <li>separare codice in ES modules con <code>import</code> ed <code>export</code>;</li>
  <li>selezionare elementi DOM con <code>querySelector</code>/<code>querySelectorAll</code>;</li>
  <li>creare e modificare nodi con <code>createElement</code>, <code>textContent</code>, <code>classList</code>, <code>dataset</code> e <code>append</code>;</li>
  <li>registrare eventi con <code>addEventListener</code> e usare correttamente l'oggetto <code>Event</code>;</li>
  <li>distinguere <code>target</code> e <code>currentTarget</code> e spiegare il bubbling;</li>
  <li>usare <strong>event delegation</strong> quando gli elementi possono essere creati dinamicamente;</li>
  <li>intercettare una form con <code>submit</code>, <code>preventDefault()</code> e <code>FormData</code>;</li>
  <li>usare <code>localStorage</code> e <code>sessionStorage</code> per dati semplici, serializzando oggetti con JSON;</li>
  <li>organizzare una piccola UI secondo il flusso <code>state -&gt; render -&gt; events -&gt; new state</code>;</li>
  <li>diagnosticare errori JavaScript con console, breakpoint, stack trace e DevTools.</li>
</ul>

## Prerequisiti

<ul>
  <li>UDA 21: HTML semantico, CSS responsive e Bootstrap;</li>
  <li>concetti generali di variabile, selezione, iterazione e funzione studiati negli anni precedenti;</li>
  <li>uso essenziale della console e di DevTools.</li>
</ul>

## Orientamento nella documentazione

<p align="center">
  <img src="../../assets/tpsi5/lesson-documentation-depth.svg" alt="La dispensa seleziona nelle fonti ufficiali i contenuti da studiare ora, riconoscere, rimandare o dichiarare fuori confine">
</p>

<table align="center"><tr><td>
<details>
<summary>&#128279; <strong>Indice incrociato — JavaScript, DOM e Web API ↔ MDN</strong></summary>

<table align="center">
<thead><tr><th>Dispensa</th><th>Documentazione ufficiale</th><th>Profondità</th></tr></thead>
<tbody>
<tr><td><a href="#lesson-js-language">Linguaggio, valori e funzioni</a></td><td><a href="https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide">JavaScript Guide</a></td><td>&#128994; studiare ora</td></tr>
<tr><td><a href="#lesson-js-control-flow">Controllo di flusso e collezioni</a></td><td><a href="https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide/Control_flow_and_error_handling">Control flow and error handling</a><br><a href="https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Array">Array reference</a></td><td>&#128994; studiare ora</td></tr>
<tr><td><a href="#lesson-js-dom">DOM e creazione dei nodi</a></td><td><a href="https://developer.mozilla.org/en-US/docs/Learn_web_development/Core/Scripting/DOM_scripting">DOM scripting introduction</a></td><td>&#128994; studiare ora</td></tr>
<tr><td><a href="#lesson-js-events">Eventi e propagazione</a></td><td><a href="https://developer.mozilla.org/en-US/docs/Learn_web_development/Core/Scripting/Events">Event handling</a></td><td>&#128994; studiare ora</td></tr>
<tr><td><a href="#lesson-js-storage">Web Storage</a></td><td><a href="https://developer.mozilla.org/en-US/docs/Web/API/Web_Storage_API">Web Storage API</a></td><td>&#128994; studiare ora</td></tr>
<tr><td>Promise, Fetch, classi e prototype internals</td><td><a href="https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide">JavaScript Guide</a></td><td>&#128993; più avanti o fuori confine</td></tr>
</tbody>
</table>

</details>
</td></tr></table>

## Problema iniziale

<p align="justify">HTML descrive <strong>che cosa esiste</strong> nella pagina. CSS descrive <strong>come appare</strong>. Ma come facciamo a dire:</p>

<blockquote>
<p align="justify">quando l'utente preme "Mi piace", aggiorna il post; quando pubblica, aggiungi un nuovo articolo al feed; se ricarica la pagina, conserva i post locali?</p>
</blockquote>

<p align="justify">Serve comportamento. Nel browser, gran parte di questo comportamento viene scritto in JavaScript.</p>

<p align="justify">La prima idea da fissare e pero questa:</p>

```text
JavaScript language != browser
```

<p align="justify">JavaScript e il linguaggio. Il browser e un ambiente che offre oggetti e API aggiuntive.</p>

<a id="lesson-js-language"></a>
## ECMAScript, JavaScript e Web APIs

<p align="justify">Lo standard del linguaggio si chiama <strong>ECMAScript</strong>. La specifica tecnica descrive sintassi e semantica di dichiarazioni, funzioni, object, array, module e cosi via.</p>

<p align="justify">Il browser aggiunge API come:</p>

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

<p align="justify">Per esempio:</p>

```js
const posts = [];
```

<p align="justify">usa solo il linguaggio ECMAScript.</p>

```js
const feed = document.querySelector("#feed");
```

<p align="justify">usa anche la DOM API fornita dal browser.</p>

<p align="justify">Questa distinzione diventera essenziale quando useremo JavaScript anche in Node.js: stesso linguaggio, ambiente e API differenti.</p>

<p align="justify">Riferimenti professionali:</p>

<ul>
  <li>MDN JavaScript Guide: <a href="https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide">https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide</a></li>
  <li>ECMAScript specification: <a href="https://tc39.es/ecma262/">https://tc39.es/ecma262/</a></li>
  <li>MDN DOM scripting: <a href="https://developer.mozilla.org/en-US/docs/Learn_web_development/Core/Scripting/DOM_scripting">https://developer.mozilla.org/en-US/docs/Learn_web_development/Core/Scripting/DOM_scripting</a></li>
</ul>

## `const`, `let` e il significato di una variabile

### Regola pratica del corso

<p align="justify">Parti da <code>const</code>.</p>

<p align="justify">Usa <code>let</code> quando <strong>la variabile deve essere riassegnata</strong>.</p>

<p align="justify">Non usare <code>var</code> come scelta predefinita.</p>

```js
const course = "TPSI";
let currentPost = 0;

currentPost += 1;
```

<p align="justify"><code>const</code> non significa "oggetto immutabile".</p>

```js
const post = {
  text: "Primo post",
  likes: 0,
};

post.likes += 1; // valido
```

<p align="justify">Non stiamo assegnando un nuovo oggetto alla variabile <code>post</code>: stiamo modificando una proprieta dell'oggetto esistente.</p>

<p align="justify">Questo invece non e valido:</p>

```js
const post = { text: "Ciao" };
post = { text: "Altro" };
```

### Perche non trasformiamo ogni errore in una regola da memorizzare

<p align="justify">Nel vecchio materiale <code>lab3</code> esiste un esempio che assegna un nuovo valore a una <code>const</code>. Nel nuovo corso non lo presentiamo come normale codice da eseguire fino in fondo: diventa un esperimento controllato per osservare l'errore e capire la differenza fra <strong>binding</strong> e <strong>mutazione</strong>.</p>

## Valori e tipi che ci servono davvero

<p align="justify">Per il corso non partiamo da un catalogo enciclopedico. Partiamo dai dati di Feisbuc.</p>

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

<p align="justify">Useremo questa convenzione didattica:</p>

<ul>
  <li><code>undefined</code>: un valore non e stato ancora fornito/trovato;</li>
  <li><code>null</code>: il programma rappresenta intenzionalmente l'assenza di un valore.</li>
</ul>

<p align="justify">Non e una legge universale di ogni codebase, ma e una convenzione leggibile.</p>

### Controllare il tipo

```js
console.log(typeof likes);  // "number"
console.log(typeof author); // "string"
```

<p align="justify">Ricorda che JavaScript ha alcune particolarita storiche. Non cercheremo di impararle tutte a memoria: quando serve controlliamo MDN.</p>

## Uguaglianza: preferire `===`

<p align="justify">Nel core del corso usiamo normalmente:</p>

```js
if (post.likes === 0) {
  // ...
}
```

<p align="justify">invece di affidarsi alla conversione implicita di <code>==</code>.</p>

<p align="justify">L'obiettivo e ridurre comportamento sorprendente mentre costruiamo un modello mentale solido.</p>

## Stringhe e template literal

```js
const author = "Ada";
const likes = 4;
const label = `${author} ha ${likes} like`;
```

<p align="justify">Le template literal sono particolarmente utili quando combiniamo testo e valori, ma non devono diventare un modo per costruire grandi blocchi HTML non controllati.</p>

<a id="lesson-js-control-flow"></a>
## Controllo di flusso: scegliere e ripetere

<p align="justify">Un programma non esegue sempre tutte le istruzioni nello stesso modo. Le condizioni scelgono un ramo; i cicli ripetono un'operazione.</p>

```js
function canDelete(post, currentUser) {
  if (!currentUser) return false;
  if (currentUser.role === "admin") return true;
  return post.authorId === currentUser.id;
}
```

<p align="justify">Gli <strong>early return</strong> rendono espliciti i casi che interrompono una funzione ed evitano annidamenti profondi. <code>switch</code> e utile quando uno stesso valore deve essere confrontato con molti casi discreti, ma non sostituisce automaticamente <code>if</code>.</p>

<p align="justify">Per attraversare una collezione scegliamo in base all'intenzione:</p>

```js
for (const post of posts) {
  console.log(post.author); // effetto: scrive nella console
}

const authors = posts.map((post) => post.author); // trasformazione
```

<ul>
  <li><code>for...of</code> comunica bene una sequenza di operazioni o effetti;</li>
  <li><code>map</code>, <code>filter</code> e <code>find</code> comunicano una trasformazione o una ricerca;</li>
  <li>non usiamo <code>map</code> soltanto per produrre effetti ignorando l'array restituito;</li>
  <li><code>break</code> interrompe il ciclo, <code>continue</code> salta all'iterazione successiva.</li>
</ul>

<p align="justify">Studia su MDN <a href="https://developer.mozilla.org/en-US/docs/Learn_web_development/Core/Scripting/Conditionals">Making decisions in your code</a> e <a href="https://developer.mozilla.org/en-US/docs/Learn_web_development/Core/Scripting/Loops">Looping code</a>. In questa lezione servono <code>if/else</code>, early return e <code>for...of</code>; le forme piu specialistiche si consultano quando nasce un caso reale.</p>

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

<p align="justify"><code>filter</code> produce un nuovo array contenente soltanto gli elementi che superano il test.</p>

### Trasformare

```js
const labels = posts.map((item) => `${item.author}: ${item.likes}`);
```

<p align="justify"><code>map</code> produce un nuovo array con un elemento di output per ogni elemento di input.</p>

### `reduce`: utile, non obbligatorio ovunque

```js
const totalLikes = posts.reduce((sum, item) => sum + item.likes, 0);
```

<p align="justify"><code>reduce</code> e potente, ma non e automaticamente migliore di codice piu semplice. Nel corso lo usiamo quando rende chiaro che stiamo <strong>accumulando</strong> un risultato.</p>

### Metodi che mutano e metodi che restituiscono nuovi valori

<p align="justify">E importante sapere se un'operazione modifica l'array originale.</p>

```js
posts.push(newPost); // muta posts
```

```js
const visiblePosts = posts.filter((post) => !post.hidden); // nuovo array
```

<p align="justify">Quando non ricordiamo il comportamento esatto di un metodo, la risposta professionale e aprire la documentazione.</p>

<p align="justify">Riferimento: <a href="https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Array">https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Array</a></p>

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

<p align="justify">La forma con punto e normalmente la piu leggibile quando conosciamo il nome della proprieta.</p>

## Destructuring

```js
const { author, text, likes } = post;
```

<p align="justify">equivale concettualmente a estrarre le proprieta che ci interessano.</p>

<p align="justify">Con gli array:</p>

```js
const [firstPost, secondPost] = posts;
```

<p align="justify">Non usiamo destructuring per rendere il codice "piu moderno": lo usiamo quando riduce rumore.</p>

## Spread: copiare una struttura superficiale

```js
const likedPost = {
  ...post,
  liked: true,
  likes: post.likes + 1,
};
```

<p align="justify">Abbiamo creato un <strong>nuovo object</strong> copiando le proprieta di <code>post</code> e sostituendo quelle indicate dopo.</p>

<p align="justify">Per un array:</p>

```js
const newPosts = [...posts, newPost];
```

<p align="justify">Lo spread e superficiale (<em>shallow</em>): se dentro l'oggetto ci sono altri oggetti/array, quei valori richiedono attenzione. La copia profonda non viene data per scontata.</p>

## Optional chaining e nullish coalescing

<p align="justify">Quando un valore puo mancare:</p>

```js
const city = user.profile?.city ?? "Citta non indicata";
```

<ul>
  <li><code>?.</code> interrompe l'accesso se la parte precedente e <code>null</code>/<code>undefined</code>;</li>
  <li><code>??</code> usa il valore a destra soltanto per <code>null</code>/<code>undefined</code>.</li>
</ul>

<p align="justify">Non sostituiscono una buona modellazione dei dati.</p>

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

<p align="justify">Non scegliamo arrow function perche e "piu nuova". La scegliamo spesso per callback brevi e funzioni locali. Prima di usare <code>this</code> in una arrow function bisogna conoscere la differenza semantica: verra approfondita nel track advanced quando servira.</p>

## Le funzioni sono valori

<p align="justify">Possiamo passare una funzione a un'altra funzione:</p>

```js
const published = posts.filter((post) => post.published);
```

<p align="justify">La funzione:</p>

```js
(post) => post.published
```

<p align="justify">viene passata a <code>filter</code> come callback.</p>

<p align="justify">Questo concetto ritornera continuamente con gli eventi:</p>

```js
button.addEventListener("click", handleClick);
```

<p align="justify">anche <code>handleClick</code> e un valore funzione passato a un'altra API.</p>

## Scope: dove esiste un nome

<p align="justify"><code>let</code> e <code>const</code> hanno scope di blocco.</p>

```js
if (posts.length > 0) {
  const first = posts[0];
  console.log(first);
}

// console.log(first); // first non esiste qui
```

<p align="justify">Ridurre lo stato globale rende piu facile capire chi puo modificare cosa.</p>

### Evitare il contatore globale quando possiamo modellare meglio l'identita

<p align="justify">Il Feisbuc legacy usa un <code>counter</code> globale per produrre id dei like button. Nel nuovo progetto possiamo dare un'identita al <strong>post</strong>, non al pulsante:</p>

```js
const post = {
  id: crypto.randomUUID(),
  text: "...",
};
```

<p align="justify">Nel DOM possiamo poi usare:</p>

```html
<article data-post-id="..."></article>
```

<p align="justify">L'identita appartiene al dato; l'interfaccia la rappresenta.</p>

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

<p align="justify">Non usiamo <code>try/catch</code> per nascondere ogni errore. Lo usiamo quando sappiamo <strong>che cosa possiamo recuperare</strong> o quando vogliamo aggiungere contesto utile.</p>

## ES modules nel browser

<p align="justify">HTML:</p>

```html
<script type="module" src="app.js"></script>
```

<p align="justify"><code>posts.js</code>:</p>

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

<p align="justify"><code>app.js</code>:</p>

```js
import { createPost } from "./posts.js";

const post = createPost("Ada", "Ciao moduli!");
console.log(post);
```

<p align="justify">Il vecchio <code>lab3</code> mostra anche CommonJS e moduli Node.js. E materiale utile piu avanti nel backend, ma <strong>non e il modello iniziale del browser</strong>. In UDA 22 iniziamo dal module system standard <code>import</code>/<code>export</code>; CommonJS verra contestualizzato quando confronteremo ambienti e pacchetti Node.</p>

<p align="justify">Riferimenti:</p>

<ul>
  <li><a href="https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide/Modules">https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide/Modules</a></li>
  <li><a href="https://tc39.es/ecma262/#sec-modules">https://tc39.es/ecma262/#sec-modules</a></li>
</ul>

<a id="lesson-js-dom"></a>
## Il DOM: il documento come oggetti in memoria

<p align="justify">Il browser interpreta HTML e costruisce una rappresentazione manipolabile.</p>

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

<p align="justify"><code>document</code> e il punto di ingresso piu comune.</p>

## Selezionare elementi

```js
const feed = document.querySelector("#feed");
const posts = document.querySelectorAll("#feed article");
```

<p align="justify"><code>querySelector()</code> restituisce il primo elemento che corrisponde al selettore oppure <code>null</code>.</p>

<p align="justify">Questo significa che dobbiamo ragionare anche sul caso "elemento non trovato":</p>

```js
const feed = document.querySelector("#feed");

if (!feed) {
  throw new Error("#feed non trovato");
}
```

<p align="justify">Riferimento: <a href="https://developer.mozilla.org/en-US/docs/Web/API/Document/querySelector">https://developer.mozilla.org/en-US/docs/Web/API/Document/querySelector</a></p>

## Leggere e modificare il DOM

```js
const title = document.querySelector("#feed-title");
title.textContent = "Feed aggiornato";
```

### `textContent` prima di `innerHTML` quando dobbiamo inserire testo

<p align="justify">Se il contenuto proviene dall'utente:</p>

```js
paragraph.textContent = userText;
```

<p align="justify">lo trattiamo come testo.</p>

<p align="justify">Non costruiamo markup concatenando input utente dentro <code>innerHTML</code> senza una ragione precisa. La sicurezza XSS verra approfondita nel modulo security, ma l'abitudine parte subito.</p>

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

<p align="justify">La pagina diventa dinamica senza perdere la semantica HTML.</p>

## `classList` e `dataset`

```js
button.classList.toggle("active", post.liked);
```

```js
article.dataset.postId = post.id;
```

<p align="justify">HTML risultante:</p>

```html
<article data-post-id="...">...</article>
```

<p align="justify"><code>dataset</code> e utile per collegare un elemento visuale all'identita del dato senza inventare id globali per ogni controllo.</p>

<a id="lesson-js-events"></a>
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

<p align="justify">La callback viene eseguita <strong>quando</strong> l'evento avviene, non quando registriamo il listener.</p>

<p align="justify">Riferimento: <a href="https://developer.mozilla.org/en-US/docs/Web/API/EventTarget/addEventListener">https://developer.mozilla.org/en-US/docs/Web/API/EventTarget/addEventListener</a></p>

## `target` e `currentTarget`

<p align="justify">Dentro un listener:</p>

```js
function handleClick(event) {
  console.log(event.target);
  console.log(event.currentTarget);
}
```

<ul>
  <li><code>target</code>: l'elemento da cui l'evento ha avuto origine;</li>
  <li><code>currentTarget</code>: l'elemento sul quale sta girando quel listener.</li>
</ul>

<p align="justify">La differenza e fondamentale per l'event delegation.</p>

## Bubbling

<p align="justify">Molti eventi risalgono dall'elemento originario verso i suoi antenati.</p>

```text
button
  -> article
      -> section#feed
          -> main
              -> document
```

<p align="justify">Questo ci permette di ascoltare una sola volta un contenitore stabile.</p>

## Event delegation

<p align="justify">Problema:</p>

<ol>
  <li>all'avvio abbiamo due post;</li>
  <li>registriamo listener sui loro pulsanti;</li>
  <li>dopo un minuto JavaScript crea un nuovo post;</li>
  <li>il nuovo pulsante non esisteva quando abbiamo registrato i listener.</li>
</ol>

<p align="justify">Soluzione:</p>

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

<p align="justify">Un solo listener sul feed gestisce anche controlli creati successivamente.</p>

<p align="justify">Il Feisbuc legacy contiene gia l'intuizione dell'event delegation; la conserveremo, ma riscriveremo identificazione, gestione dello stato e aggiornamento DOM.</p>

## Form: ascoltare `submit`, non soltanto il click

<p align="justify">HTML:</p>

```html
<form id="composer-form">
  <label for="post-text">Nuovo post</label>
  <textarea id="post-text" name="text" required></textarea>
  <button type="submit">Pubblica</button>
</form>
```

<p align="justify">JavaScript:</p>

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

<p align="justify">Ascoltare <code>submit</code> copre anche invii da tastiera e rispetta meglio il modello della form.</p>

### Un bug concreto del Feisbuc legacy

<p align="justify">Nel vecchio <code>add_post.js</code> il listener riceve il parametro <code>e</code>, ma chiama:</p>

```js
event.preventDefault();
```

<p align="justify">invece di:</p>

```js
e.preventDefault();
```

<p align="justify">Il nuovo corso trasforma questo genere di problema in un'attivita D di diagnosi, non in una correzione nascosta.</p>

## Stato dell'applicazione

<p align="justify">Una UI diventa molto piu comprensibile se separiamo:</p>

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

<p align="justify">Esempio:</p>

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

<p align="justify">Non significa che ogni click debba ricostruire l'intera applicazione. Significa che <strong>il dato e la fonte di verita</strong>, mentre il DOM e una rappresentazione.</p>

<p align="justify">Questo prepara naturalmente componenti e framework frontend.</p>

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

<p align="justify">Poi:</p>

```js
function renderPosts() {
  feed.replaceChildren(...posts.map(createPostElement));
}
```

<p align="justify">Qui si incontrano due mondi del modulo:</p>

```text
array.map(...)
      +
DOM createElement(...)
      =
render della UI
```

<a id="lesson-js-storage"></a>
## Web Storage

<p align="justify">Per una prima persistenza locale non serve ancora un server.</p>

```js
localStorage.setItem("feisbuc.posts", JSON.stringify(posts));
```

<p align="justify">Lettura:</p>

```js
const raw = localStorage.getItem("feisbuc.posts");
const savedPosts = raw ? JSON.parse(raw) : [];
```

### `localStorage` vs `sessionStorage`

<p align="justify">Entrambi espongono una semplice interfaccia chiave/valore, ma con ciclo di vita differente.</p>

<p align="justify">Nel corso:</p>

<ul>
  <li><code>localStorage</code>: preferenze o dati demo che devono sopravvivere alla riapertura;</li>
  <li><code>sessionStorage</code>: dati temporanei della singola sessione/tab.</li>
</ul>

<p align="justify">Non sono database applicativi e non devono contenere segreti.</p>

<p align="justify">Riferimento: <a href="https://developer.mozilla.org/en-US/docs/Web/API/Web_Storage_API">https://developer.mozilla.org/en-US/docs/Web/API/Web_Storage_API</a></p>

### Storage conserva stringhe

<p align="justify">Questo non funziona come molti principianti immaginano:</p>

```js
localStorage.setItem("posts", posts);
```

<p align="justify">Per object/array usiamo JSON:</p>

```js
localStorage.setItem("posts", JSON.stringify(posts));
```

```js
const posts = JSON.parse(localStorage.getItem("posts") ?? "[]");
```

## Isolare lo storage dietro funzioni

<p align="justify"><code>storage.js</code>:</p>

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

<p align="justify">Il resto dell'app non deve conoscere ogni dettaglio del formato di persistenza.</p>

## Feisbuc milestone 3: feed dinamico locale

<p align="justify">Partiamo dalla UI Bootstrap della milestone 2 e introduciamo:</p>

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

<p align="justify">Nessun server e nessun <code>fetch</code> in questa milestone.</p>

<p align="justify">E una scelta intenzionale: prima rendiamo comprensibile il comportamento client, poi in UDA 23 sostituiremo gradualmente la persistenza locale con un contratto HTTP/REST.</p>

## Cosa NON entra ancora in UDA 22

### `fetch`

<p align="justify">E una Web API importante, ma viene affrontata in UDA 23 insieme a HTTP.</p>

### Promise e `async`/`await`

<p align="justify">Il vecchio <code>lab3</code> le introduce nella sezione async. Nel nuovo corso le spostiamo a UDA 23, dove possiamo spiegare <strong>perche</strong> l'operazione e asincrona e collegarla a request/response, errori di rete e <code>fetch</code>.</p>

### Node.js filesystem, CommonJS e package ecosystem

<p align="justify">Verranno affrontati nel backend. Non li confondiamo con il primo modello di JavaScript nel browser.</p>

### Prototype internals, metaprogramming e performance avanzata

<p align="justify">Track advanced/senior.</p>

## Debug JavaScript: metodo prima della modifica

<p align="justify">Quando qualcosa non funziona:</p>

<ol>
  <li><strong>riproduci</strong> il comportamento;</li>
  <li>leggi la prima eccezione utile nella console;</li>
  <li>apri lo stack trace;</li>
  <li>controlla il valore delle variabili;</li>
  <li>metti un breakpoint nel listener/funzione sospetta;</li>
  <li>osserva <code>event.target</code>, <code>event.currentTarget</code> e lo stato;</li>
  <li>formula un'ipotesi;</li>
  <li>modifica una causa alla volta;</li>
  <li>verifica anche il caso che funzionava gia.</li>
</ol>

### Errori frequenti

#### Usare una variabile globale inesistente al posto del parametro

```js
button.addEventListener("click", (e) => {
  event.preventDefault(); // sbagliato nel nostro codice legacy
});
```

<p align="justify">Corretto:</p>

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

<p align="justify">Se i post vengono aggiunti dopo, i nuovi pulsanti non hanno quel listener.</p>

<p align="justify">Per un feed dinamico e spesso migliore la delegation sul contenitore stabile.</p>

#### Costruire testo utente con HTML concatenato

```js
feed.innerHTML += `<p>${userText}</p>`;
```

<p align="justify">Nel core preferiamo creare elementi e assegnare <code>textContent</code>.</p>

#### Stato nel DOM ma non nei dati

<p align="justify">Se il numero di like vive solo nel testo di un button, il programma perde una fonte di verita chiara.</p>

#### Salvare object direttamente in localStorage

<p align="justify">Lo storage conserva stringhe: serializzare/deserializzare esplicitamente.</p>

#### `querySelector` senza controllare `null`

<p align="justify">Il selettore puo essere sbagliato o il markup puo cambiare.</p>

## Approfondimento guidato su MDN

<table align="center"><tr><td>
<p align="justify"><strong><span style="font-size: 1.15em;">&#128279;</span> Percorso MDN — JavaScript e Web API:</strong> applica il processo della <a href="GUIDA_USO_MDN.md#mdn-guide-workflow">guida trasversale a MDN</a> e usa la checklist per <a href="GUIDA_USO_MDN.md#mdn-guide-js-api">JavaScript e Web API</a>.</p>
<ul>
  <li><strong>JavaScript:</strong> individua oggetto proprietario, parametri, valore restituito, mutazione e casi limite;</li>
  <li><strong>DOM:</strong> individua interfaccia, metodo, input, possibile assenza ed eccezioni;</li>
  <li><strong>eventi:</strong> individua target, tipo di evento, fase di propagazione e possibilità di annullamento;</li>
  <li><strong>storage:</strong> individua durata, formato dei dati, origine e limiti dell'API.</li>
</ul>
<p align="justify"><strong>Prodotto atteso:</strong> compila una <a href="GUIDA_USO_MDN.md#mdn-guide-study-card">scheda di lettura</a> per <a href="https://developer.mozilla.org/en-US/docs/Web/API/Document/querySelector"><code>Document.querySelector()</code></a>, poi modifica l'esempio minimo nel Feisbuc e gestisci esplicitamente il caso <code>null</code>.</p>
</td></tr></table>

## Esercizi A-F

### A — esegui/osserva

<p align="justify">Completa una pipeline JavaScript che riceve un array JSON di post e produce un riepilogo deterministico con <code>filter</code> e <code>map</code>. Viene corretto dal runner JavaScript di TheBitLab.</p>

### B — modifica controllata

<p align="justify">Rifattorizza una pipeline imperativa in funzioni piccole usando destructuring, spread e array methods, mantenendo lo stesso output.</p>

### C — implementazione autonoma

<p align="justify">Costruisci Feisbuc milestone 3: form, stato dei post, rendering DOM, event delegation e localStorage con ES modules.</p>

### D — debug e diagnosi

<p align="justify">Correggi una versione derivata dal JavaScript legacy che contiene <code>event/e</code>, listener non validi per post dinamici, stato disperso nel DOM e gestione storage fragile. Prima documenta la diagnosi.</p>

### E — mini-progetto

<p align="justify">Estendi Feisbuc con filtri locali, contatore post/like, preferenze sessione e una piccola vista vuota, mantenendo state/render separati.</p>

### F — prodotto integrato

<p align="justify">Arrivera piu avanti: il Feisbuc completo unira client, API REST, database, autenticazione, frontend componentizzato e realtime.</p>

## Verifica rapida

<ol>
  <li>Che differenza c'e tra ECMAScript e DOM?</li>
  <li>Perche <code>const</code> non rende immutabile un object?</li>
  <li>Che differenza c'e fra <code>map</code> e <code>filter</code>?</li>
  <li>Perche una callback e importante anche per gli eventi?</li>
  <li>Cosa restituisce <code>querySelector()</code> se non trova nulla?</li>
  <li>Perche <code>textContent</code> e una buona scelta per testo inserito dall'utente?</li>
  <li>Che differenza c'e fra <code>target</code> e <code>currentTarget</code>?</li>
  <li>Perche l'event delegation aiuta con elementi dinamici?</li>
  <li>Perche localStorage richiede JSON per array/object?</li>
  <li>Perche <code>fetch</code> e <code>async/await</code> vengono spostati in UDA 23?</li>
</ol>

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

<p align="justify">Per Feisbuc:</p>

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

<ul>
  <li>MDN JavaScript Guide: <a href="https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide">https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide</a></li>
  <li>MDN Array: <a href="https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Array">https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Array</a></li>
  <li>MDN JavaScript modules: <a href="https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide/Modules">https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide/Modules</a></li>
  <li>MDN DOM scripting: <a href="https://developer.mozilla.org/en-US/docs/Learn_web_development/Core/Scripting/DOM_scripting">https://developer.mozilla.org/en-US/docs/Learn_web_development/Core/Scripting/DOM_scripting</a></li>
  <li>MDN <code>querySelector</code>: <a href="https://developer.mozilla.org/en-US/docs/Web/API/Document/querySelector">https://developer.mozilla.org/en-US/docs/Web/API/Document/querySelector</a></li>
  <li>MDN events: <a href="https://developer.mozilla.org/en-US/docs/Learn_web_development/Core/Scripting/Events">https://developer.mozilla.org/en-US/docs/Learn_web_development/Core/Scripting/Events</a></li>
  <li>MDN <code>addEventListener</code>: <a href="https://developer.mozilla.org/en-US/docs/Web/API/EventTarget/addEventListener">https://developer.mozilla.org/en-US/docs/Web/API/EventTarget/addEventListener</a></li>
  <li>MDN Web Storage API: <a href="https://developer.mozilla.org/en-US/docs/Web/API/Web_Storage_API">https://developer.mozilla.org/en-US/docs/Web/API/Web_Storage_API</a></li>
  <li>ECMAScript language specification: <a href="https://tc39.es/ecma262/">https://tc39.es/ecma262/</a></li>
</ul>

### Provenance legacy

<ul>
  <li><code>TheBitPoets/labs_summary</code> pinned dal Content Pack: progressione <code>lab2</code>/<code>lab3</code>/<code>lab4</code>;</li>
  <li><code>kinderp/lab3</code> snapshot auditato: <code>0deae0eb606bc9c2849ba271bdf03c128910f1ac</code>;</li>
  <li><code>TheBitPoets/feisbuc</code> pinned dal Content Pack: <code>add_post.js</code> e <code>like_button_pressed.js</code> usati come input di audit, non copiati come soluzione canonica.</li>
</ul>

### Teacher references

<ul>
  <li>Pluralsight JavaScript path registrato nel Content Pack come <code>teacher-reference</code> licensed;</li>
  <li>eventuali testi Manning JavaScript/Web Platform vengono usati solo come riferimenti di progettazione docente, senza ingestione automatica.</li>
</ul>

## Activity correlate

<ul>
  <li><code>tpsi5-activity-a-js-feed-pipeline-001</code>;</li>
  <li><code>tpsi5-activity-b-js-post-refactor-001</code>;</li>
  <li><code>tpsi5-activity-c-feisbuc-dynamic-feed-001</code>;</li>
  <li><code>tpsi5-activity-d-debug-feisbuc-js-001</code>.</li>
</ul>
