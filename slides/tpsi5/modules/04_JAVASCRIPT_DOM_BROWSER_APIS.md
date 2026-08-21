---
marp: true
paginate: true
size: 16:9
title: 04 — JavaScript moderno, DOM e Browser APIs
---

# 04 — JavaScript, DOM e Browser APIs
## Dati, eventi e rendering nel browser

UDA 22 — Frontend foundations

---

# Richiamo

Finora abbiamo una pagina strutturata e responsive.

Ma il contenuto è ancora statico.

Oggi introduciamo il ciclo:

```text
stato -> render -> DOM -> evento -> nuovo stato
```

---

# Obiettivi

Alla fine dovrai saper:

- gestire dati con array/oggetti;
- leggere e modificare il DOM;
- usare eventi e delegation;
- separare stato e rendering;
- usare moduli;
- usare Web Storage con criterio;
- diagnosticare errori nel browser.

---

# Stato prima del DOM

```js
const posts = [
  { id: 1, author: 'Mario', text: 'Ciao!' }
];
```

Questo è **stato applicativo**.

Il DOM è una rappresentazione visuale di quello stato.

Tenere distinti i due concetti evita molti bug.

---

# Render

```js
function renderPosts(posts) {
  const feed = document.querySelector('#feed');
  feed.replaceChildren();

  for (const post of posts) {
    const article = document.createElement('article');
    article.textContent = `${post.author}: ${post.text}`;
    feed.append(article);
  }
}
```

Input: dati.
Output: DOM.

---

# Selettori

```js
const form = document.querySelector('#post-form');
const textarea = document.querySelector('#post-text');
```

Domanda importante:

> cosa succede se il selettore non trova nulla?

`querySelector` può restituire `null`.

---

# Eventi

```js
form.addEventListener('submit', (event) => {
  event.preventDefault();
  // aggiorna lo stato
  // poi renderizza
});
```

L'evento non dovrebbe contenere tutta l'applicazione: dovrebbe orchestrare passi leggibili.

---

# State → update → render

```js
function addPost(text) {
  posts.push({
    id: crypto.randomUUID(),
    author: 'Studente',
    text
  });

  renderPosts(posts);
}
```

Pattern semplice ma potente:

```text
input -> cambia stato -> render
```

---

# Event delegation

Se il feed contiene molti pulsanti:

```js
feed.addEventListener('click', (event) => {
  const button = event.target.closest('[data-action="delete"]');
  if (!button) return;

  deletePost(button.dataset.postId);
});
```

Un listener può gestire elementi creati dinamicamente.

---

# Moduli

```js
// posts.js
export function createPost(text) { ... }

// main.js
import { createPost } from './posts.js';
```

Separare file non basta: bisogna separare **responsabilità**.

---

# Web Storage

```js
localStorage.setItem('posts', JSON.stringify(posts));
```

e:

```js
const raw = localStorage.getItem('posts');
const posts = raw ? JSON.parse(raw) : [];
```

È persistenza **nel browser**, non un database server-side.

---

# Errore tipico: DOM come database

Se leggi continuamente il DOM per ricostruire lo stato:

```js
const text = document.querySelector('.post').textContent;
```

stai invertendo il flusso.

Meglio:

```text
stato JS -> DOM
```

Il DOM è la vista, non la fonte principale dei dati.

---

# Debug browser

Usa:

- Console;
- breakpoint;
- Sources;
- Event Listener Breakpoints;
- DOM inspector;
- Application → Local Storage.

Domanda: il bug è nei dati, nell'evento o nel render?

---

# Checkpoint

Classifica:

1. array `posts`;
2. `<article>` nel feed;
3. evento `submit`;
4. `localStorage`;
5. `renderPosts()`.

Qual è stato? Qual è vista? Qual è input? Qual è persistenza browser?

---

# Feisbuc milestone

Feisbuc diventa dinamico:

- aggiunta post;
- rendering del feed;
- eventi;
- eventuale delete/edit;
- persistenza locale;
- nessun backend ancora.

Il prossimo problema sarà: **come condividiamo i dati con un server?**

---

# Handoff al laboratorio

Durante le Activity:

1. osserva il pipeline dei dati;
2. separa stato/render;
3. aggiungi un'interazione;
4. diagnostica un bug intenzionale;
5. verifica Local Storage quando previsto.

---

# Recap

JavaScript nel browser introduce:

- stato;
- trasformazioni;
- eventi;
- rendering;
- API browser.

Prossimo modulo: **HTTP, async/await, fetch e REST**.