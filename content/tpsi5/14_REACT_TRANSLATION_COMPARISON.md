# React translation lab: stessi concetti, altra sintassi

<table align="center" width="100%"><tr><td>
<details>
<summary>&#128506; <strong>Orientamento della lezione</strong></summary>

<p align="justify"><strong>Contesto:</strong> questo è un laboratorio di traduzione, non un secondo percorso frontend completo. Partiamo da componenti Vue già compresi e cerchiamo gli stessi concetti in React.</p>
<p align="justify"><strong>Domande guida:</strong> quale parte del codice esprime stato, input, output e rendering? Quali differenze sono sintattiche e quali cambiano il modello mentale? Quando serve davvero un Effect?</p>
<p align="justify"><strong>Obiettivi osservabili:</strong> tradurre state, props, callback, rendering condizionale, liste e controlled input e spiegare le differenze senza dichiarare automaticamente migliore uno dei framework.</p>
<p align="justify"><strong>Prossimo passo:</strong> la lezione 15 sposterà il confronto sul backend, esprimendo lo stesso contratto HTTP con FastAPI e OpenAPI.</p>

</details>
</td></tr></table>

<p align="justify">Stato didattico: <strong>draft</strong>.</p>

## Obiettivi

<p align="justify">Al termine del laboratorio lo studente sa:</p>

<ul>
  <li>riconoscere gli stessi concetti di UI dichiarativa in Vue e React senza trattarli come due mondi separati;</li>
  <li>tradurre state locale, valori derivati, props, eventi/callback, rendering condizionale, liste e input controllati;</li>
  <li>mantenere <strong>ownership dello state nel parent</strong> e componenti child privi di mutazioni nascoste;</li>
  <li>distinguere un valore derivato da nuovo state e da una ottimizzazione;</li>
  <li>spiegare perche React e professionalmente rilevante senza diventare un secondo framework core TPSI5;</li>
  <li>leggere la documentazione React cercando concetti gia noti invece di memorizzare una seconda sintassi completa.</li>
</ul>

## Prerequisiti

<ul>
  <li>JavaScript moderno, array/object spread e callback;</li>
  <li>modello <code>state -&gt; render</code>;</li>
  <li>Vue 3: <code>ref</code>, <code>computed</code>, props, emits, <code>v-if</code>, <code>v-for</code>, <code>v-model</code>;</li>
  <li>componenti e one-way data flow gia osservati nella <code>PostCard</code> Vue.</li>
</ul>

## Orientamento nella documentazione

<p align="center">
  <img src="../../assets/tpsi5/lesson-documentation-depth.svg" alt="La dispensa seleziona nelle fonti ufficiali i contenuti da studiare ora, riconoscere, rimandare o dichiarare fuori confine">
</p>

<table align="center"><tr><td>
<details>
<summary>&#128279; <strong>Indice incrociato — concetti Vue ↔ React</strong></summary>

<table align="center">
<thead><tr><th>Dispensa</th><th>Documentazione ufficiale</th><th>Profondità</th></tr></thead>
<tbody>
<tr><td><a href="#lesson-react-map">Mappa Vue → React</a></td><td><a href="https://react.dev/learn/describing-the-ui">React — Describing the UI</a></td><td>&#128994; studiare la corrispondenza</td></tr>
<tr><td><a href="#lesson-react-state">State e valori derivati</a></td><td><a href="https://react.dev/learn/state-a-components-memory">State: A Component's Memory</a><br><a href="https://react.dev/learn/choosing-the-state-structure">Choosing the State Structure</a></td><td>&#128994; studiare ora</td></tr>
<tr><td><a href="#lesson-react-rendering">JSX, condizioni, liste e input</a></td><td><a href="https://react.dev/learn/conditional-rendering">Conditional Rendering</a><br><a href="https://react.dev/learn/rendering-lists">Rendering Lists</a></td><td>&#128994; studiare ora</td></tr>
<tr><td><a href="#lesson-react-effects">Rendering puro ed Effect</a></td><td><a href="https://react.dev/learn/keeping-components-pure">Keeping Components Pure</a><br><a href="https://react.dev/learn/synchronizing-with-effects">Synchronizing with Effects</a></td><td>&#128994; comprendere il confine</td></tr>
<tr><td>Router, state manager, Suspense e framework React</td><td><a href="https://react.dev/learn">React Learn</a></td><td>&#128993; fuori dal translation lab</td></tr>
</tbody>
</table>

</details>
</td></tr></table>

## Problema iniziale

<p align="justify">Hai gia costruito una feature in Vue. Domani entri in un team che usa React.</p>

<p align="justify">La domanda sbagliata e:</p>

<blockquote>
<p align="justify">devo ricominciare da zero?</p>
</blockquote>

<p align="justify">La domanda utile e:</p>

<blockquote>
<p align="justify">quali concetti conosco gia e come vengono espressi qui?</p>
</blockquote>

<p align="justify">Il laboratorio non costruisce un secondo Feisbuc. Prende una feature piccola e gia compresa e la traduce.</p>

```text
stesso problema UI
      │
      ├── Vue
      └── React
```

<p align="justify">Cambiano API e sintassi del presentation layer; non cambiano dominio, ownership dello state, HTTP, auth o database.</p>

---

<a id="lesson-react-map"></a>
## 1. Mappa Vue -> React

<table align="center">
<thead>
<tr>
<th>Concetto</th>
<th>Vue</th>
<th>React</th>
</tr>
</thead>
<tbody>
<tr>
<td>state locale</td>
<td><code>ref(...)</code></td>
<td><code>useState(...)</code></td>
</tr>
<tr>
<td>valore derivato</td>
<td><code>computed(() =&gt; ...)</code></td>
<td>espressione derivata durante il render</td>
</tr>
<tr>
<td>input al componente</td>
<td>props</td>
<td>props</td>
</tr>
<tr>
<td>output dal child</td>
<td><code>emit(...)</code></td>
<td>callback prop</td>
</tr>
<tr>
<td>condizione</td>
<td><code>v-if</code></td>
<td>espressione/ternario JSX</td>
</tr>
<tr>
<td>lista</td>
<td><code>v-for</code></td>
<td><code>array.map(...)</code></td>
</tr>
<tr>
<td>identita lista</td>
<td><code>:key="item.id"</code></td>
<td><code>key={item.id}</code></td>
</tr>
<tr>
<td>input two-way ergonomico</td>
<td><code>v-model</code></td>
<td><code>value</code> + <code>onChange</code></td>
</tr>
<tr>
<td>componente</td>
<td>SFC <code>.vue</code></td>
<td>funzione che restituisce JSX</td>
</tr>
</tbody>
</table>

<p align="justify">Questa tabella non dice che le implementazioni interne siano identiche. Dice che lo <strong>stesso problema di progettazione UI</strong> ricompare.</p>

---

<a id="lesson-react-state"></a>
## 2. `ref` e `useState`

<p align="justify">Vue:</p>

```vue
<script setup>
import { ref } from "vue";

const count = ref(0);
</script>

<template>
  <button @click="count++">{{ count }}</button>
</template>
```

<p align="justify">React:</p>

```jsx
import { useState } from "react";

export default function Counter() {
  const [count, setCount] = useState(0);

  return (
    <button type="button" onClick={() => setCount((value) => value + 1)}>
      {count}
    </button>
  );
}
```

<p align="justify">In entrambi i casi abbiamo:</p>

```text
evento
  ↓
aggiornamento state
  ↓
nuovo render dichiarativo
```

<p align="justify">Non stiamo modificando manualmente <code>textContent</code>.</p>

---

## 3. `computed` non significa automaticamente `useMemo`

<p align="justify">Vue:</p>

```js
const doubled = computed(() => count.value * 2);
```

<p align="justify">Nel caso semplice React:</p>

```jsx
const doubled = count * 2;
```

<p align="justify">Il valore non e una seconda source of truth. Si ricava dallo state durante il render.</p>

<p align="justify">Errore didattico da evitare:</p>

```jsx
const [count, setCount] = useState(0);
const [doubled, setDoubled] = useState(0); // state duplicato
```

<p align="justify">Adesso ogni update deve mantenere due valori sincronizzati.</p>

<p align="justify">Anche questo non e il default corretto:</p>

```jsx
const doubled = useMemo(() => count * 2, [count]);
```

<p align="justify"><code>useMemo</code> e uno strumento di ottimizzazione/cache con un costo concettuale. Non serve per rendere "reattivo" un calcolo banale.</p>

<p align="justify">Regola del laboratorio:</p>

<blockquote>
<p align="justify"><strong>se un valore puo essere calcolato economicamente dallo state corrente, calcolalo durante il render.</strong></p>
</blockquote>

---

<a id="lesson-react-rendering"></a>
## 4. Template Vue e JSX

<p align="justify">Vue separa le espressioni nel template:</p>

```vue
<p>{{ post.text }}</p>
```

<p align="justify">React usa JSX:</p>

```jsx
<p>{post.text}</p>
```

<p align="justify">JSX non e una stringa HTML. E sintassi JavaScript trasformata dal toolchain.</p>

<p align="justify">Per questo possiamo usare espressioni:</p>

```jsx
{canDelete ? <button>Elimina</button> : null}
```

<p align="justify">e liste:</p>

```jsx
{posts.map((post) => (
  <PostCard key={post.id} post={post} />
))}
```

<p align="justify">La <code>key</code> continua a rappresentare l'identita stabile dell'elemento, esattamente il problema gia incontrato con <code>v-for</code>.</p>

---

## 5. Props down, output up

<p align="justify">Vue child:</p>

```vue
<script setup>
const props = defineProps({
  post: Object,
  canDelete: Boolean,
});

const emit = defineEmits(["toggle-like", "delete"]);
</script>

<template>
  <button @click="emit('toggle-like', post.id)">Like</button>
</template>
```

<p align="justify">React child:</p>

```jsx
export function PostCard({ post, canDelete, onToggleLike, onDelete }) {
  return (
    <article>
      <p>{post.text}</p>

      <button type="button" onClick={() => onToggleLike(post.id)}>
        Like
      </button>

      {canDelete ? (
        <button type="button" onClick={() => onDelete(post.id)}>
          Elimina
        </button>
      ) : null}
    </article>
  );
}
```

<p align="justify">Il contratto architetturale e lo stesso:</p>

```text
parent state
    │
    └── props ──► child
                  │
                  └── evento/callback ──► parent handler
```

<p align="justify">Il child non decide dove persistere il dato e non deve fare <code>fetch</code> solo perche puo farlo.</p>

---

## 6. Aggiornare lo state senza mutare gli oggetti ricevuti

<p align="justify">React rende molto visibile la regola dell'immutabilita degli aggiornamenti.</p>

```jsx
function toggleLike(id) {
  setPosts((current) =>
    current.map((post) =>
      post.id === id
        ? {
            ...post,
            liked: !post.liked,
            likes: post.liked ? post.likes - 1 : post.likes + 1,
          }
        : post
    )
  );
}
```

<p align="justify">Non:</p>

```jsx
post.liked = !post.liked;
```

<p align="justify">Il parent produce il nuovo state. Il child continua a ricevere props.</p>

---

## 7. `v-if` e rendering condizionale

<p align="justify">Vue:</p>

```vue
<button v-if="canDelete">Elimina</button>
```

<p align="justify">React:</p>

```jsx
{canDelete ? <button>Elimina</button> : null}
```

<p align="justify">Oppure, quando non esiste un ramo <code>else</code> significativo:</p>

```jsx
{canDelete && <button>Elimina</button>}
```

<p align="justify">La domanda importante non e la sintassi. E:</p>

<blockquote>
<p align="justify">da quale state/prop dipende la presenza di questo elemento?</p>
</blockquote>

---

## 8. `v-for` e `map`

<p align="justify">Vue:</p>

```vue
<PostCard
  v-for="post in posts"
  :key="post.id"
  :post="post"
/>
```

<p align="justify">React:</p>

```jsx
{posts.map((post) => (
  <PostCard
    key={post.id}
    post={post}
  />
))}
```

<p align="justify">In entrambi:</p>

<ul>
  <li>l'array appartiene al parent;</li>
  <li>ogni item produce un componente;</li>
  <li>la key deve essere stabile;</li>
  <li>usare l'indice come key quando l'identita del dominio esiste e un errore concettuale.</li>
</ul>

---

## 9. `v-model` e controlled input

<p align="justify">Vue:</p>

```vue
<input v-model="text" />
```

<p align="justify">React:</p>

```jsx
const [text, setText] = useState("");

<input
  value={text}
  onChange={(event) => setText(event.target.value)}
/>
```

<p align="justify">React rende espliciti i due lati:</p>

```text
state -> value
event -> setState
```

<p align="justify">E lo stesso ciclo state/render gia studiato.</p>

---

<a id="lesson-react-effects"></a>
## 10. Rendering puro ed effetti

<p align="justify">Durante il render un componente dovrebbe descrivere UI a partire da props e state.</p>

<p align="justify">Non vogliamo:</p>

```jsx
function PostCard({ post }) {
  fetch("/api/log"); // side effect durante render: no
  return <p>{post.text}</p>;
}
```

<p align="justify">React dispone di <code>useEffect</code> per sincronizzazioni con sistemi esterni, ma <strong>non e il tema di questo translation lab</strong>.</p>

<p align="justify">La nostra <code>PostCard</code>:</p>

<ul>
  <li>non chiama API;</li>
  <li>non apre socket;</li>
  <li>non registra listener globali;</li>
  <li>non duplica la logica Feisbuc.</li>
</ul>

<p align="justify">Questi problemi sono gia stati studiati nel percorso Vue/realtime e non vanno duplicati solo per cambiare framework.</p>

---

## 11. Toolchain reference

<p align="justify">Baseline riproducibile 2026/27:</p>

```text
React                19.2.8
react-dom             19.2.8
@vitejs/plugin-react   6.0.5
Vite                   8.2.1
Node                  >=22.18
```

<p align="justify">Sono versioni pin della reference docente. Il concetto didattico non dipende da una patch release specifica.</p>

---

## 12. Cosa resta volutamente fuori

<p align="justify">Questo laboratorio <strong>non</strong> introduce:</p>

<ul>
  <li>React Router;</li>
  <li>Redux, Zustand o altro global store;</li>
  <li>Next.js;</li>
  <li>Server Components;</li>
  <li>React Compiler;</li>
  <li>una seconda SPA Feisbuc;</li>
  <li>una seconda integrazione Socket.IO;</li>
  <li>una nuova API o un nuovo database;</li>
  <li>una duplicazione TypeScript del frontend.</li>
</ul>

<p align="justify">Se uno di questi strumenti comparira in un corso futuro, dovra rispondere a un requisito concreto.</p>

---

## 13. Activity A — translation microscope

<p align="justify">Esegui il piccolo counter React e confrontalo col sorgente Vue fornito.</p>

<p align="justify">Individua:</p>

<ul>
  <li>state;</li>
  <li>update dello state;</li>
  <li>valore derivato;</li>
  <li>event binding;</li>
  <li>rendering dichiarativo.</li>
</ul>

<p align="justify">Poi compila la mappa concettuale Vue -> React.</p>

---

## 14. Activity B — PostCard translation

<p align="justify">Traduci il contratto gia noto della <code>PostCard</code>:</p>

```text
input:
  post
  canDelete

output:
  toggleLike(post.id)
  delete(post.id)
```

<p align="justify">In React l'output diventa callback prop:</p>

```text
onToggleLike(post.id)
onDelete(post.id)
```

<p align="justify">Definition of Done:</p>

<ul>
  <li>parent owns <code>posts</code>;</li>
  <li>child riceve props;</li>
  <li>child chiama callback;</li>
  <li>nessuna mutazione della prop <code>post</code>;</li>
  <li>nessun <code>fetch</code> nel child;</li>
  <li>delete e renderizzato solo se <code>canDelete</code>;</li>
  <li>lista usa <code>key={post.id}</code>;</li>
  <li>aggiornamenti parent producono nuovi array/oggetti.</li>
</ul>

---

## 15. Verifica rapida

<ol>
  <li>Perche <code>const doubled = count * 2</code> e preferibile a un secondo <code>useState</code>?</li>
  <li>Qual e l'equivalente architetturale di <code>emit("delete", id)</code>?</li>
  <li>Chi deve possedere l'array <code>posts</code> nel nostro esempio?</li>
  <li>Perche <code>key={post.id}</code> e migliore di <code>key={index}</code>?</li>
  <li>Quando un valore derivato semplice richiede <code>useMemo</code>? Risposta attesa: <strong>non automaticamente</strong>.</li>
  <li>Perche questo laboratorio non aggiunge React Router?</li>
</ol>

## Sintesi inclusiva

<p align="justify">Se ricordi una sola mappa:</p>

```text
Vue ref       -> React useState
computed      -> valore derivato
props         -> props
emit          -> callback prop
v-if          -> condizione JSX
v-for         -> map + key
v-model       -> value + onChange
```

<p align="justify">Il framework cambia. I problemi di state, ownership, data flow e rendering restano riconoscibili.</p>

## Fonti e locator

<ul>
  <li>React official docs: <code>https://react.dev/learn</code> — Describing the UI, Adding Interactivity, Sharing State Between Components.</li>
  <li>Vue official docs: reactivity fundamentals, computed, components, props, events.</li>
  <li>Vite official docs: React plugin e production build.</li>
  <li><code>doc/FRONTEND_FRAMEWORK_DECISION.md</code> — decisione D1 e boundary del translation lab.</li>
</ul>
