# Vue 3: reattivita, componenti e prima SPA Feisbuc

## Obiettivi

Al termine del modulo lo studente sa:

- spiegare perche un framework frontend diventa utile dopo avere implementato manualmente `state -> render`;
- creare una applicazione Vue 3 con Vite;
- leggere e scrivere un Single File Component (`.vue`);
- usare Composition API con `<script setup>`;
- usare `ref()` per stato locale e `computed()` per stato derivato;
- usare template dichiarativi con interpolazione, `v-if`, `v-for`, binding ed eventi;
- separare componenti tramite `props` ed `emits`;
- usare `v-model` mantenendo il collegamento concettuale con `value` + evento;
- riusare l'API Feisbuc esistente senza modificare autenticazione, sessione, autorizzazione o persistenza;
- distinguere stato locale, derivato e remoto;
- fare debug di reattivita, component contract e rete.

## Prerequisiti

- UDA21: HTML/CSS/Bootstrap;
- UDA22: JavaScript, DOM, eventi, moduli, `state -> render`;
- UDA23: HTTP, `fetch`, REST;
- UDA24: Express, SQL, auth/session/authorization e confronto SSR.

## Problema iniziale

Nelle milestone precedenti Feisbuc funziona, ma il client dinamico coordina manualmente molte responsabilita:

```text
state
  -> render()
  -> DOM
  -> event listener
  -> fetch
  -> aggiorna state
  -> render() di nuovo
```

Questa architettura e fondamentale per capire il browser. Quando pero l'interfaccia cresce, vogliamo rendere dichiarativi e componibili concetti che conosciamo gia.

## 1. Vue non sostituisce la Web Platform

Mapping didattico:

```text
prima                              Vue
-----                              ---
let state                          ref()/reactive()
state -> render()                  reattivita
createElement/template HTML        template dichiarativo
addEventListener                   @click / @submit
input.value                        v-model
if + DOM                           v-if
array + render loop                v-for
moduli UI                          componenti SFC
funzione di stato derivato         computed
argomenti funzione                 props
callback                           emits
```

Il framework non rende inutili i fondamenti: li organizza.

## 2. Tooling del corso

Per il primo blocco pinniamo:

```text
Vue 3.5.40
Vite 8.2.1
@vitejs/plugin-vue 6.0.8
Node >= 22.18
```

La documentazione Vue corrente usa Vite come build setup per le SPA con Single File Components.

Progetto minimo:

```text
index.html
package.json
vite.config.js
src/
  main.js
  App.vue
```

Comandi essenziali:

```bash
npm install
npm run dev
npm run build
npm run preview
```

La CI deve eseguire davvero `npm run build` sulle reference del corso.

## 3. Single File Components

```vue
<script setup>
// stato e comportamento
</script>

<template>
  <!-- struttura dichiarativa -->
</template>

<style scoped>
/* presentazione locale */
</style>
```

Nel core usiamo Composition API + `<script setup>`. Options API resta leggibile come documentazione professionale, ma non viene insegnata come secondo stile parallelo.

## 4. `ref()` e reattivita

```js
import { ref } from "vue";

const count = ref(0);

function increment() {
  count.value += 1;
}
```

Nel codice JavaScript il ref e un contenitore e si modifica tramite `.value`.

Nel template Vue effettua l'unwrapping:

```vue
<button @click="increment">{{ count }}</button>
```

## 5. Stato derivato: `computed()`

```js
const posts = ref([]);
const likedCount = computed(
  () => posts.value.filter(post => post.liked).length,
);
```

Regola del corso: **`computed` prima di `watch`**. Se un valore deriva soltanto da altro stato, non va mantenuto manualmente in una seconda variabile sincronizzata.

## 6. Template dichiarativo

### Interpolazione

```vue
<p>{{ post.text }}</p>
```

### Binding

```vue
<button :disabled="loading">Invia</button>
```

### Eventi

```vue
<form @submit.prevent="submitPost">
```

`.prevent` astrae il gia noto `event.preventDefault()`.

### Condizioni

```vue
<p v-if="error" role="alert">{{ error }}</p>
```

### Liste

```vue
<PostCard
  v-for="post in posts"
  :key="post.id"
  :post="post"
/>
```

Usiamo una key stabile del dominio, non l'indice dell'array quando esiste `post.id`.

## 7. `v-model`: binding + evento

```vue
<textarea v-model="draft"></textarea>
```

Va ricondotto a:

```text
value + input/change event -> v-model
```

## 8. Props ed emits

### Parent -> child: props

```vue
<script setup>
defineProps({
  post: { type: Object, required: true },
  canDelete: { type: Boolean, default: false },
});
</script>
```

Le props sono input. Il child non deve mutarle per cambiare lo stato autorevole del parent.

### Child -> parent: emits

```vue
<script setup>
const emit = defineEmits(["toggle-like", "delete"]);
</script>

<template>
  <button @click="emit('toggle-like', post)">Like</button>
</template>
```

Schema:

```text
parent state
   ↓ props
child
   ↑ emits
parent action
```

## 9. Stato locale, derivato e remoto

Nel client Feisbuc distinguiamo:

```text
locale
  draft, loading, error

derivato
  loggedIn, postCount, likedCount

remoto
  user, posts
```

`user` e `posts` sono copie client di risorse la cui fonte autorevole resta il backend.

## 10. API Feisbuc: il contratto resta invariato

```text
POST /api/auth/register
POST /api/auth/login
GET  /api/auth/me
POST /api/auth/logout

GET    /api/posts
POST   /api/posts
PATCH  /api/posts/:id
DELETE /api/posts/:id
```

Il session token resta nel cookie `HttpOnly`.

La SPA:

```text
NON legge document.cookie
NON salva token in localStorage/sessionStorage
NON sceglie authorId
```

Le richieste sono same-origin.

## 11. Feisbuc milestone 9: Vue SPA shell

```text
browser
  ↓
Vue App
  ├── AuthPanel
  ├── PostComposer
  └── PostCard * N
       ↓
api.js
       ↓
/api/* JSON
       ↓
sessione + Express + SQLite
```

Non introduciamo ancora:

- Vue Router;
- Pinia;
- TypeScript;
- WebSocket/Socket.IO;
- ORM.

Li aggiungiamo solo quando emerge un requisito osservabile.

## 12. `PostCard` come boundary

Responsabilita:

- mostra autore/testo/likes;
- riceve `post` e `canDelete`;
- emette `toggle-like` e `delete`;
- non conosce `fetch`;
- non conosce cookie/sessione;
- non muta direttamente il post ricevuto.

```text
PostCard
   ↓ intent
emit
   ↓
App
   ↓ operation
api.js
   ↓
HTTP
```

## 13. Auth nella SPA

All'avvio:

```text
GET /api/auth/me
  200 -> user autenticato -> carica posts
  401 -> mostra login/register
```

Il `401` iniziale e uno stato previsto dell'interfaccia, non necessariamente un errore inatteso.

Dopo register/login il server imposta il cookie e restituisce l'utente pubblico. Dopo logout il client azzera `user` e `posts`.

## 14. Like e delete

Like:

```text
PostCard emit
  -> App
  -> PATCH /api/posts/:id
  -> representation aggiornata
  -> sostituzione nello state
```

Delete:

```text
PostCard emit
  -> DELETE /api/posts/:id
  -> 204
  -> rimozione dallo state
```

Il bottone delete puo essere mostrato solo sui propri post come UX; l'authorization resta server-side.

## 15. Errori frequenti

### Mutare direttamente una prop

```js
props.post.liked = !props.post.liked;
```

Meglio: emit dell'intenzione al parent.

### Dimenticare `.value` nello script

```js
posts = [];
```

Corretto:

```js
posts.value = [];
```

### Duplicare un computed

```js
const postCount = ref(0);
```

sincronizzato a mano in piu punti e fragile.

Meglio:

```js
const postCount = computed(() => posts.value.length);
```

### `watch` per calcolare dati derivati

Se non c'e un side effect, probabilmente serve `computed`.

### App monolitica

Mettere tutto in `App.vue` non rende l'app ben progettata. I componenti devono avere contratti osservabili.

### Global state troppo presto

Pinia non entra finche props/emits e funzioni/composable locali sono sufficienti.

## 16. Debug

Tre domande distinte:

1. **reattivita** — il valore nel componente e quello atteso?
2. **component contract** — prop/evento viaggiano nella direzione giusta?
3. **rete** — method/status/body della request sono corretti?

Non correggere un 403 modificando un template; non correggere un prop sbagliato toccando il DB.

## 17. Esempio minimo

```vue
<script setup>
import { computed, ref } from "vue";

const count = ref(0);
const doubled = computed(() => count.value * 2);
</script>

<template>
  <button @click="count += 1">
    count={{ count }} doubled={{ doubled }}
  </button>
</template>
```

Nel template il ref viene unwrapped; nello script useremmo `count.value`.

## 18. Esercizi A-F

- **A** — osserva `ref` e `computed` in una app Vite minima;
- **B** — completa `PostCard` con props/emits;
- **C** — costruisci Feisbuc milestone 9 sopra API/auth esistenti;
- **D** — diagnostica bug di reattivita e component boundary;
- **E** — prossimo incremento: routing SPA e stati di navigazione;
- **F** — milestone integrata successiva con realtime.

## 19. Activity collegate

- `tpsi5-activity-a-vue-reactivity-microscope-001`;
- `tpsi5-activity-b-vue-post-card-001`;
- `tpsi5-activity-c-feisbuc-vue-spa-001`;
- `tpsi5-activity-d-debug-vue-reactivity-001`.

## 20. Verifica rapida

1. Perche Vue non rende inutile conoscere il DOM?
2. Qual e la differenza tra `ref` e il valore contenuto nel ref?
3. Quando usare `computed`?
4. Quale direzione seguono props ed emits?
5. Perche `PostCard` non dovrebbe chiamare direttamente l'API?
6. Perche la SPA non deve leggere il session cookie?
7. Perche nascondere il bottone delete non e authorization?
8. Quale requisito ci fara introdurre Vue Router?

## 21. Sintesi inclusiva

```text
state            -> ref/reactive
state derivato   -> computed
HTML dinamico    -> template
input             -> v-model
evento            -> @event
lista              -> v-for
condizione         -> v-if
modulo UI          -> componente
parent -> child    -> props
child -> parent    -> emits

API/auth/DB non cambiano perche cambia il presentation layer.
```

## 22. Fonti e collegamenti

- Vue Documentation: Quick Start, Reactivity Fundamentals, Computed Properties, Components, Props, Component Events, SFC;
- Vite Documentation: Getting Started e build;
- `doc/FRONTEND_FRAMEWORK_DECISION.md`;
- moduli UDA22–24 come prerequisiti concettuali.

## 23. Prossimo passo

```text
Vue SPA shell
   ↓
Vue Router
   ↓
URL/client navigation
   ↓
loading/error/not-found states
   ↓
TypeScript boundary decision
   ↓
realtime WebSocket/Socket.IO
```
