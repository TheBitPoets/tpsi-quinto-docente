---
marp: true
paginate: true
size: 16:9
title: 14 — React translation/comparison lab
---

# 14 — React translation lab
## Stessi concetti, altra sintassi

UDA 25 — Frontend application

---

# Perché questo modulo è breve

React non diventa il secondo framework core del corso.

Lo usiamo per verificare una competenza più importante:

> sai trasferire concetti architetturali da un framework a un altro?

---

# Obiettivi

Alla fine dovrai saper:

- riconoscere gli stessi concetti in Vue e React;
- tradurre state/derived state;
- tradurre props e callback;
- leggere JSX;
- costruire un piccolo componente equivalente;
- distinguere concetto da sintassi/framework API.

---

# Mapping principale

| Concetto | Vue | React |
|---|---|---|
| stato | `ref()` | `useState()` |
| derivato | `computed()` | calcolo/`useMemo` quando serve |
| input child | props | props |
| output child | emit | callback prop |
| template | SFC template | JSX |

---

# Stato

Vue:

```js
const text = ref('');
```

React:

```js
const [text, setText] = useState('');
```

Il concetto è lo stesso: stato che influenza la UI.

---

# Derived value

Vue:

```js
const count = computed(() => posts.value.length);
```

React:

```js
const count = posts.length;
```

Non ogni valore derivato richiede un hook speciale.

---

# Props

Vue:

```js
const props = defineProps({ post: Object });
```

React:

```jsx
function PostCard({ post }) {
  return <article>{post.text}</article>;
}
```

---

# Child → parent

Vue:

```js
emit('delete', post.id);
```

React:

```jsx
<button onClick={() => onDelete(post.id)}>
  Elimina
</button>
```

In React il callback arriva come prop.

---

# Controlled input

```jsx
<input
  value={text}
  onChange={event => setText(event.target.value)}
/>
```

Confrontalo con `v-model`.

Stesso problema: collegare input UI e stato.

---

# JSX

```jsx
return (
  <article className="post">
    <h2>{post.author}</h2>
    <p>{post.text}</p>
  </article>
);
```

JSX mescola markup dichiarativo e JavaScript in una sintassi diversa dal template Vue.

---

# Errore tipico: imparare API senza concetti

Se ricordi solo:

```text
Vue = ref
React = useState
```

ma non sai spiegare **stato**, non hai trasferito davvero la competenza.

---

# Checkpoint

Traduci concettualmente:

1. `computed`;
2. `emit`;
3. `v-model`;
4. `v-for`;
5. prop tipata.

Prima descrivi il concetto, poi proponi una sintassi React possibile.

---

# Collegamento a Feisbuc

Non riscriviamo l'intera applicazione Feisbuc in React.

Prendiamo **un solo boundary già noto**, per esempio `PostCard`, e manteniamo invariati:

- DTO del post;
- responsabilità del componente;
- azione delete verso il parent;
- contratto HTTP/backend;
- comportamento osservabile.

Se cambia il framework ma non il contratto, possiamo confrontare davvero le architetture.

---

# Mini-lab

Prendi un `PostCard` Vue di Feisbuc e riscrivilo in React mantenendo:

- stessi dati in input;
- stessa azione delete;
- stesso output visuale;
- nessuna nuova feature.

Il test è sulla **traduzione**, non sul framework più bello.

---

# Recap

Obiettivo raggiunto se sai dire:

- cosa è framework-specific;
- cosa è un pattern UI generale;
- cosa resta identico a livello di boundary.

Prossimo modulo: **FastAPI e OpenAPI mirror**.
