# Vue 3: reattivita, componenti e prima SPA Feisbuc

<table align="center" width="100%"><tr><td>
<details>
<summary>&#128506; <strong>Orientamento della lezione</strong></summary>

<p align="justify"><strong>Contesto:</strong> abbiamo già costruito stato, rendering, eventi e chiamate HTTP senza framework. Vue organizza gli stessi problemi con componenti dichiarativi e reattività.</p>
<p align="justify"><strong>Domande guida:</strong> quale stato appartiene a un componente? Quando un valore è derivato? Come comunicano parent e child senza creare fonti di verità concorrenti?</p>
<p align="justify"><strong>Obiettivi osservabili:</strong> leggere un Single File Component, usare <code>ref</code> e <code>computed</code>, progettare props ed emits e collegare la SPA alla stessa API Feisbuc.</p>
<p align="justify"><strong>Prossimo passo:</strong> la lezione 11 renderà l'URL parte dello stato applicativo con Vue Router.</p>

</details>
</td></tr></table>

## Obiettivi

<p align="justify">Al termine del modulo lo studente sa:</p>

<ul>
  <li>spiegare perche un framework frontend diventa utile dopo avere implementato manualmente <code>state -&gt; render</code>;</li>
  <li>creare una applicazione Vue 3 con Vite;</li>
  <li>leggere e scrivere un Single File Component (<code>.vue</code>);</li>
  <li>usare Composition API con <code>&lt;script setup&gt;</code>;</li>
  <li>usare <code>ref()</code> per stato locale e <code>computed()</code> per stato derivato;</li>
  <li>usare template dichiarativi con interpolazione, <code>v-if</code>, <code>v-for</code>, binding ed eventi;</li>
  <li>separare componenti tramite <code>props</code> ed <code>emits</code>;</li>
  <li>usare <code>v-model</code> mantenendo il collegamento concettuale con <code>value</code> + evento;</li>
  <li>riusare l'API Feisbuc esistente senza modificare autenticazione, sessione, autorizzazione o persistenza;</li>
  <li>distinguere stato locale, derivato e remoto;</li>
  <li>fare debug di reattivita, component contract e rete.</li>
</ul>

## Prerequisiti

<ul>
  <li>UDA21: HTML/CSS/Bootstrap;</li>
  <li>UDA22: JavaScript, DOM, eventi, moduli, <code>state -&gt; render</code>;</li>
  <li>UDA23: HTTP, <code>fetch</code>, REST;</li>
  <li>UDA24: Express, SQL, auth/session/authorization e confronto SSR.</li>
</ul>

## Orientamento nella documentazione

<p align="center">
  <img src="../../assets/tpsi5/lesson-documentation-depth.svg" alt="La dispensa seleziona nelle fonti ufficiali i contenuti da studiare ora, riconoscere, rimandare o dichiarare fuori confine">
</p>

<table align="center"><tr><td>
<details>
<summary>&#128279; <strong>Indice incrociato — Vue 3 ↔ Web Platform</strong></summary>

<table align="center">
<thead><tr><th>Dispensa</th><th>Documentazione ufficiale</th><th>Profondità</th></tr></thead>
<tbody>
<tr><td><a href="#lesson-vue-reactivity">Reattività e stato derivato</a></td><td><a href="https://vuejs.org/guide/essentials/reactivity-fundamentals.html">Vue — Reactivity fundamentals</a><br><a href="https://vuejs.org/guide/essentials/computed.html">Vue — Computed properties</a></td><td>&#128994; studiare ora</td></tr>
<tr><td><a href="#lesson-vue-template">Template, binding, eventi e form</a></td><td><a href="https://vuejs.org/guide/essentials/template-syntax.html">Vue — Template syntax</a><br><a href="https://vuejs.org/guide/essentials/forms.html">Vue — Form input bindings</a></td><td>&#128994; studiare ora</td></tr>
<tr><td><a href="#lesson-vue-components">Componenti, props ed emits</a></td><td><a href="https://vuejs.org/guide/essentials/component-basics.html">Vue — Components basics</a><br><a href="https://vuejs.org/guide/components/props.html">Vue — Props</a></td><td>&#128994; studiare ora</td></tr>
<tr><td><a href="#lesson-vue-lifecycle">Lifecycle e side effect</a></td><td><a href="https://vuejs.org/guide/essentials/lifecycle.html">Vue — Lifecycle hooks</a><br><a href="https://vuejs.org/guide/essentials/watchers.html">Vue — Watchers</a></td><td>&#128994; lifecycle minimo; watcher mirato</td></tr>
<tr><td>Provide/inject, plugin, custom directive e state manager</td><td><a href="https://vuejs.org/guide/introduction.html">Vue Guide</a></td><td>&#128993; riconoscere o studiare più avanti</td></tr>
</tbody>
</table>

</details>
</td></tr></table>

## Problema iniziale

<p align="justify">Nelle milestone precedenti Feisbuc funziona, ma il client dinamico coordina manualmente molte responsabilita:</p>

```text
state
  -> render()
  -> DOM
  -> event listener
  -> fetch
  -> aggiorna state
  -> render() di nuovo
```

<p align="justify">Questa architettura e fondamentale per capire il browser. Quando pero l'interfaccia cresce, vogliamo rendere dichiarativi e componibili concetti che conosciamo gia.</p>

## 1. Vue non sostituisce la Web Platform

<p align="justify">Mapping didattico:</p>

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

<p align="justify">Il framework non rende inutili i fondamenti: li organizza.</p>

<table align="center"><tr><td>
<p align="justify"><strong><span style="font-size: 1.15em;">&#128279;</span> MDN e documentazione Vue:</strong> la <a href="GUIDA_USO_MDN.md#mdn-guide-source-choice">guida trasversale</a> spiega come scegliere la fonte. Per <code>ref()</code>, <code>computed()</code>, props, emits e direttive usa la documentazione ufficiale Vue; per elementi HTML, eventi DOM, Fetch e comportamento del browser usa MDN.</p>
<p align="justify"><strong>Prodotto atteso:</strong> quando incontri un costrutto Vue, indica quale concetto della Web Platform organizza e quale documentazione definisce ciascuno dei due livelli.</p>
</td></tr></table>

## 2. Tooling del corso

<p align="justify">Per il primo blocco pinniamo:</p>

```text
Vue 3.5.40
Vite 8.2.1
@vitejs/plugin-vue 6.0.8
Node >= 22.18
```

<p align="justify">La documentazione Vue corrente usa Vite come build setup per le SPA con Single File Components.</p>

<p align="justify">Progetto minimo:</p>

```text
index.html
package.json
vite.config.js
src/
  main.js
  App.vue
```

<p align="justify">Comandi essenziali:</p>

```bash
npm install
npm run dev
npm run build
npm run preview
```

<p align="justify">La CI deve eseguire davvero <code>npm run build</code> sulle reference del corso.</p>

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

<p align="justify">Nel core usiamo Composition API + <code>&lt;script setup&gt;</code>. Options API resta leggibile come documentazione professionale, ma non viene insegnata come secondo stile parallelo.</p>

<a id="lesson-vue-reactivity"></a>
## 4. `ref()` e reattivita

```js
import { ref } from "vue";

const count = ref(0);

function increment() {
  count.value += 1;
}
```

<p align="justify">Nel codice JavaScript il ref e un contenitore e si modifica tramite <code>.value</code>.</p>

<p align="justify">Nel template Vue effettua l'unwrapping:</p>

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

<p align="justify">Regola del corso: <strong><code>computed</code> prima di <code>watch</code></strong>. Se un valore deriva soltanto da altro stato, non va mantenuto manualmente in una seconda variabile sincronizzata.</p>

<a id="lesson-vue-template"></a>
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

<p align="justify"><code>.prevent</code> astrae il gia noto <code>event.preventDefault()</code>.</p>

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

<p align="justify">Usiamo una key stabile del dominio, non l'indice dell'array quando esiste <code>post.id</code>.</p>

## 7. `v-model`: binding + evento

```vue
<textarea v-model="draft"></textarea>
```

<p align="justify">Va ricondotto a:</p>

```text
value + input/change event -> v-model
```

<a id="lesson-vue-components"></a>
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

<p align="justify">Le props sono input. Il child non deve mutarle per cambiare lo stato autorevole del parent.</p>

### Child -> parent: emits

```vue
<script setup>
const emit = defineEmits(["toggle-like", "delete"]);
</script>

<template>
  <button @click="emit('toggle-like', post)">Like</button>
</template>
```

<p align="justify">Schema:</p>

```text
parent state
   ↓ props
child
   ↑ emits
parent action
```

## 9. Stato locale, derivato e remoto

<p align="justify">Nel client Feisbuc distinguiamo:</p>

```text
locale
  draft, loading, error

derivato
  loggedIn, postCount, likedCount

remoto
  user, posts
```

<p align="justify"><code>user</code> e <code>posts</code> sono copie client di risorse la cui fonte autorevole resta il backend.</p>

<a id="lesson-vue-lifecycle"></a>
### Lifecycle minimo e side effect

<p align="justify">Un componente viene creato, montato nel DOM, aggiornato quando cambia lo stato e infine smontato. Non dobbiamo memorizzare tutti gli hook: dobbiamo riconoscere <strong>quando una risorsa esterna deve essere avviata e ripulita</strong>.</p>

```vue
<script setup>
import { onMounted, onUnmounted, ref } from "vue";

const online = ref(navigator.onLine);
const updateStatus = () => { online.value = navigator.onLine; };

onMounted(() => {
  window.addEventListener("online", updateStatus);
  window.addEventListener("offline", updateStatus);
});

onUnmounted(() => {
  window.removeEventListener("online", updateStatus);
  window.removeEventListener("offline", updateStatus);
});
</script>
```

<ul>
  <li><code>onMounted</code> serve quando il lavoro dipende dal DOM gia creato o da un'integrazione esterna;</li>
  <li><code>onUnmounted</code> rimuove listener, timer, subscription e connessioni possedute dal componente;</li>
  <li><code>computed</code> descrive un valore derivato senza effetti;</li>
  <li><code>watch</code> osserva un cambiamento per coordinare un <strong>side effect</strong>, non per duplicare un valore calcolabile;</li>
  <li>una richiesta dati non va spostata automaticamente in <code>onMounted</code>: la posizione dipende da chi possiede il caricamento e da quali dipendenze usa.</li>
</ul>

<p align="justify">Nella documentazione Vue studia <a href="https://vuejs.org/guide/essentials/lifecycle.html">Lifecycle Hooks</a> e la sezione iniziale di <a href="https://vuejs.org/guide/essentials/watchers.html">Watchers</a>. Gli hook avanzati restano da consultare quando compare un'esigenza concreta.</p>

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

<p align="justify">Il session token resta nel cookie <code>HttpOnly</code>.</p>

<p align="justify">La SPA:</p>

```text
NON legge document.cookie
NON salva token in localStorage/sessionStorage
NON sceglie authorId
```

<p align="justify">Le richieste sono same-origin.</p>

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

<p align="justify">Non introduciamo ancora:</p>

<ul>
  <li>Vue Router;</li>
  <li>Pinia;</li>
  <li>TypeScript;</li>
  <li>WebSocket/Socket.IO;</li>
  <li>ORM.</li>
</ul>

<p align="justify">Li aggiungiamo solo quando emerge un requisito osservabile.</p>

## 12. `PostCard` come boundary

<p align="justify">Responsabilita:</p>

<ul>
  <li>mostra autore/testo/likes;</li>
  <li>riceve <code>post</code> e <code>canDelete</code>;</li>
  <li>emette <code>toggle-like</code> e <code>delete</code>;</li>
  <li>non conosce <code>fetch</code>;</li>
  <li>non conosce cookie/sessione;</li>
  <li>non muta direttamente il post ricevuto.</li>
</ul>

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

<p align="justify">All'avvio:</p>

```text
GET /api/auth/me
  200 -> user autenticato -> carica posts
  401 -> mostra login/register
```

<p align="justify">Il <code>401</code> iniziale e uno stato previsto dell'interfaccia, non necessariamente un errore inatteso.</p>

<p align="justify">Dopo register/login il server imposta il cookie e restituisce l'utente pubblico. Dopo logout il client azzera <code>user</code> e <code>posts</code>.</p>

## 14. Like e delete

<p align="justify">Like:</p>

```text
PostCard emit
  -> App
  -> PATCH /api/posts/:id
  -> representation aggiornata
  -> sostituzione nello state
```

<p align="justify">Delete:</p>

```text
PostCard emit
  -> DELETE /api/posts/:id
  -> 204
  -> rimozione dallo state
```

<p align="justify">Il bottone delete puo essere mostrato solo sui propri post come UX; l'authorization resta server-side.</p>

## 15. Errori frequenti

### Mutare direttamente una prop

```js
props.post.liked = !props.post.liked;
```

<p align="justify">Meglio: emit dell'intenzione al parent.</p>

### Dimenticare `.value` nello script

```js
posts = [];
```

<p align="justify">Corretto:</p>

```js
posts.value = [];
```

### Duplicare un computed

```js
const postCount = ref(0);
```

<p align="justify">sincronizzato a mano in piu punti e fragile.</p>

<p align="justify">Meglio:</p>

```js
const postCount = computed(() => posts.value.length);
```

### `watch` per calcolare dati derivati

<p align="justify">Se non c'e un side effect, probabilmente serve <code>computed</code>.</p>

### App monolitica

<p align="justify">Mettere tutto in <code>App.vue</code> non rende l'app ben progettata. I componenti devono avere contratti osservabili.</p>

### Global state troppo presto

<p align="justify">Pinia non entra finche props/emits e funzioni/composable locali sono sufficienti.</p>

## 16. Debug

<p align="justify">Tre domande distinte:</p>

<ol>
  <li><strong>reattivita</strong> — il valore nel componente e quello atteso?</li>
  <li><strong>component contract</strong> — prop/evento viaggiano nella direzione giusta?</li>
  <li><strong>rete</strong> — method/status/body della request sono corretti?</li>
</ol>

<p align="justify">Non correggere un 403 modificando un template; non correggere un prop sbagliato toccando il DB.</p>

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

<p align="justify">Nel template il ref viene unwrapped; nello script useremmo <code>count.value</code>.</p>

## 18. Esercizi A-F

<ul>
  <li><strong>A</strong> — osserva <code>ref</code> e <code>computed</code> in una app Vite minima;</li>
  <li><strong>B</strong> — completa <code>PostCard</code> con props/emits;</li>
  <li><strong>C</strong> — costruisci Feisbuc milestone 9 sopra API/auth esistenti;</li>
  <li><strong>D</strong> — diagnostica bug di reattivita e component boundary;</li>
  <li><strong>E</strong> — prossimo incremento: routing SPA e stati di navigazione;</li>
  <li><strong>F</strong> — milestone integrata successiva con realtime.</li>
</ul>

## 19. Activity collegate

<ul>
  <li><code>tpsi5-activity-a-vue-reactivity-microscope-001</code>;</li>
  <li><code>tpsi5-activity-b-vue-post-card-001</code>;</li>
  <li><code>tpsi5-activity-c-feisbuc-vue-spa-001</code>;</li>
  <li><code>tpsi5-activity-d-debug-vue-reactivity-001</code>.</li>
</ul>

## 20. Verifica rapida

<ol>
  <li>Perche Vue non rende inutile conoscere il DOM?</li>
  <li>Qual e la differenza tra <code>ref</code> e il valore contenuto nel ref?</li>
  <li>Quando usare <code>computed</code>?</li>
  <li>Quale direzione seguono props ed emits?</li>
  <li>Perche <code>PostCard</code> non dovrebbe chiamare direttamente l'API?</li>
  <li>Perche la SPA non deve leggere il session cookie?</li>
  <li>Perche nascondere il bottone delete non e authorization?</li>
  <li>Quale requisito ci fara introdurre Vue Router?</li>
</ol>

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

<ul>
  <li>Vue Documentation: Quick Start, Reactivity Fundamentals, Computed Properties, Components, Props, Component Events, SFC;</li>
  <li>Vite Documentation: Getting Started e build;</li>
  <li><code>doc/FRONTEND_FRAMEWORK_DECISION.md</code>;</li>
  <li>moduli UDA22–24 come prerequisiti concettuali.</li>
</ul>

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
