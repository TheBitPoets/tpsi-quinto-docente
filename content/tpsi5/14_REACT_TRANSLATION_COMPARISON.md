# React translation lab: stessi concetti, altra sintassi

Stato didattico: **draft**.

## Obiettivi

Al termine del laboratorio lo studente sa:

- riconoscere gli stessi concetti di UI dichiarativa in Vue e React senza trattarli come due mondi separati;
- tradurre state locale, valori derivati, props, eventi/callback, rendering condizionale, liste e input controllati;
- mantenere **ownership dello state nel parent** e componenti child privi di mutazioni nascoste;
- distinguere un valore derivato da nuovo state e da una ottimizzazione;
- spiegare perche React e professionalmente rilevante senza diventare un secondo framework core TPSI5;
- leggere la documentazione React cercando concetti gia noti invece di memorizzare una seconda sintassi completa.

## Prerequisiti

- JavaScript moderno, array/object spread e callback;
- modello `state -> render`;
- Vue 3: `ref`, `computed`, props, emits, `v-if`, `v-for`, `v-model`;
- componenti e one-way data flow gia osservati nella `PostCard` Vue.

## Problema iniziale

Hai gia costruito una feature in Vue. Domani entri in un team che usa React.

La domanda sbagliata e:

> devo ricominciare da zero?

La domanda utile e:

> quali concetti conosco gia e come vengono espressi qui?

Il laboratorio non costruisce un secondo Feisbuc. Prende una feature piccola e gia compresa e la traduce.

```text
stesso problema UI
      │
      ├── Vue
      └── React
```

Cambiano API e sintassi del presentation layer; non cambiano dominio, ownership dello state, HTTP, auth o database.

---

## 1. Mappa Vue -> React

| Concetto | Vue | React |
| --- | --- | --- |
| state locale | `ref(...)` | `useState(...)` |
| valore derivato | `computed(() => ...)` | espressione derivata durante il render |
| input al componente | props | props |
| output dal child | `emit(...)` | callback prop |
| condizione | `v-if` | espressione/ternario JSX |
| lista | `v-for` | `array.map(...)` |
| identita lista | `:key="item.id"` | `key={item.id}` |
| input two-way ergonomico | `v-model` | `value` + `onChange` |
| componente | SFC `.vue` | funzione che restituisce JSX |

Questa tabella non dice che le implementazioni interne siano identiche. Dice che lo **stesso problema di progettazione UI** ricompare.

---

## 2. `ref` e `useState`

Vue:

```vue
<script setup>
import { ref } from "vue";

const count = ref(0);
</script>

<template>
  <button @click="count++">{{ count }}</button>
</template>
```

React:

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

In entrambi i casi abbiamo:

```text
evento
  ↓
aggiornamento state
  ↓
nuovo render dichiarativo
```

Non stiamo modificando manualmente `textContent`.

---

## 3. `computed` non significa automaticamente `useMemo`

Vue:

```js
const doubled = computed(() => count.value * 2);
```

Nel caso semplice React:

```jsx
const doubled = count * 2;
```

Il valore non e una seconda source of truth. Si ricava dallo state durante il render.

Errore didattico da evitare:

```jsx
const [count, setCount] = useState(0);
const [doubled, setDoubled] = useState(0); // state duplicato
```

Adesso ogni update deve mantenere due valori sincronizzati.

Anche questo non e il default corretto:

```jsx
const doubled = useMemo(() => count * 2, [count]);
```

`useMemo` e uno strumento di ottimizzazione/cache con un costo concettuale. Non serve per rendere "reattivo" un calcolo banale.

Regola del laboratorio:

> **se un valore puo essere calcolato economicamente dallo state corrente, calcolalo durante il render.**

---

## 4. Template Vue e JSX

Vue separa le espressioni nel template:

```vue
<p>{{ post.text }}</p>
```

React usa JSX:

```jsx
<p>{post.text}</p>
```

JSX non e una stringa HTML. E sintassi JavaScript trasformata dal toolchain.

Per questo possiamo usare espressioni:

```jsx
{canDelete ? <button>Elimina</button> : null}
```

e liste:

```jsx
{posts.map((post) => (
  <PostCard key={post.id} post={post} />
))}
```

La `key` continua a rappresentare l'identita stabile dell'elemento, esattamente il problema gia incontrato con `v-for`.

---

## 5. Props down, output up

Vue child:

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

React child:

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

Il contratto architetturale e lo stesso:

```text
parent state
    │
    └── props ──► child
                  │
                  └── evento/callback ──► parent handler
```

Il child non decide dove persistere il dato e non deve fare `fetch` solo perche puo farlo.

---

## 6. Aggiornare lo state senza mutare gli oggetti ricevuti

React rende molto visibile la regola dell'immutabilita degli aggiornamenti.

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

Non:

```jsx
post.liked = !post.liked;
```

Il parent produce il nuovo state. Il child continua a ricevere props.

---

## 7. `v-if` e rendering condizionale

Vue:

```vue
<button v-if="canDelete">Elimina</button>
```

React:

```jsx
{canDelete ? <button>Elimina</button> : null}
```

Oppure, quando non esiste un ramo `else` significativo:

```jsx
{canDelete && <button>Elimina</button>}
```

La domanda importante non e la sintassi. E:

> da quale state/prop dipende la presenza di questo elemento?

---

## 8. `v-for` e `map`

Vue:

```vue
<PostCard
  v-for="post in posts"
  :key="post.id"
  :post="post"
/>
```

React:

```jsx
{posts.map((post) => (
  <PostCard
    key={post.id}
    post={post}
  />
))}
```

In entrambi:

- l'array appartiene al parent;
- ogni item produce un componente;
- la key deve essere stabile;
- usare l'indice come key quando l'identita del dominio esiste e un errore concettuale.

---

## 9. `v-model` e controlled input

Vue:

```vue
<input v-model="text" />
```

React:

```jsx
const [text, setText] = useState("");

<input
  value={text}
  onChange={(event) => setText(event.target.value)}
/>
```

React rende espliciti i due lati:

```text
state -> value
event -> setState
```

E lo stesso ciclo state/render gia studiato.

---

## 10. Rendering puro ed effetti

Durante il render un componente dovrebbe descrivere UI a partire da props e state.

Non vogliamo:

```jsx
function PostCard({ post }) {
  fetch("/api/log"); // side effect durante render: no
  return <p>{post.text}</p>;
}
```

React dispone di `useEffect` per sincronizzazioni con sistemi esterni, ma **non e il tema di questo translation lab**.

La nostra `PostCard`:

- non chiama API;
- non apre socket;
- non registra listener globali;
- non duplica la logica Feisbuc.

Questi problemi sono gia stati studiati nel percorso Vue/realtime e non vanno duplicati solo per cambiare framework.

---

## 11. Toolchain reference

Baseline riproducibile 2026/27:

```text
React                19.2.8
react-dom             19.2.8
@vitejs/plugin-react   6.0.5
Vite                   8.2.1
Node                  >=22.18
```

Sono versioni pin della reference docente. Il concetto didattico non dipende da una patch release specifica.

---

## 12. Cosa resta volutamente fuori

Questo laboratorio **non** introduce:

- React Router;
- Redux, Zustand o altro global store;
- Next.js;
- Server Components;
- React Compiler;
- una seconda SPA Feisbuc;
- una seconda integrazione Socket.IO;
- una nuova API o un nuovo database;
- una duplicazione TypeScript del frontend.

Se uno di questi strumenti comparira in un corso futuro, dovra rispondere a un requisito concreto.

---

## 13. Activity A — translation microscope

Esegui il piccolo counter React e confrontalo col sorgente Vue fornito.

Individua:

- state;
- update dello state;
- valore derivato;
- event binding;
- rendering dichiarativo.

Poi compila la mappa concettuale Vue -> React.

---

## 14. Activity B — PostCard translation

Traduci il contratto gia noto della `PostCard`:

```text
input:
  post
  canDelete

output:
  toggleLike(post.id)
  delete(post.id)
```

In React l'output diventa callback prop:

```text
onToggleLike(post.id)
onDelete(post.id)
```

Definition of Done:

- parent owns `posts`;
- child riceve props;
- child chiama callback;
- nessuna mutazione della prop `post`;
- nessun `fetch` nel child;
- delete e renderizzato solo se `canDelete`;
- lista usa `key={post.id}`;
- aggiornamenti parent producono nuovi array/oggetti.

---

## 15. Verifica rapida

1. Perche `const doubled = count * 2` e preferibile a un secondo `useState`?
2. Qual e l'equivalente architetturale di `emit("delete", id)`?
3. Chi deve possedere l'array `posts` nel nostro esempio?
4. Perche `key={post.id}` e migliore di `key={index}`?
5. Quando un valore derivato semplice richiede `useMemo`? Risposta attesa: **non automaticamente**.
6. Perche questo laboratorio non aggiunge React Router?

## Sintesi inclusiva

Se ricordi una sola mappa:

```text
Vue ref       -> React useState
computed      -> valore derivato
props         -> props
emit          -> callback prop
v-if          -> condizione JSX
v-for         -> map + key
v-model       -> value + onChange
```

Il framework cambia. I problemi di state, ownership, data flow e rendering restano riconoscibili.

## Fonti e locator

- React official docs: `https://react.dev/learn` — Describing the UI, Adding Interactivity, Sharing State Between Components.
- Vue official docs: reactivity fundamentals, computed, components, props, events.
- Vite official docs: React plugin e production build.
- `doc/FRONTEND_FRAMEWORK_DECISION.md` — decisione D1 e boundary del translation lab.
