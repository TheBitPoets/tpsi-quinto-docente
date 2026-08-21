---
marp: true
paginate: true
size: 16:9
title: 10 — Vue 3: reattività e componenti
---

# 10 — Vue 3
## Reattività, componenti e prima SPA Feisbuc

UDA 25 — Frontend application

---

# Richiamo

Con JavaScript nativo abbiamo già usato:

```text
stato -> render -> eventi -> nuovo stato
```

Vue non inventa questo ciclo: lo rende più dichiarativo e modulare.

---

# Obiettivi

Alla fine dovrai saper:

- spiegare la reattività;
- usare `ref` e `computed`;
- costruire componenti;
- distinguere props ed emits;
- evitare stato duplicato;
- trasformare Feisbuc in una prima SPA Vue.

---

# Da render manuale a template dichiarativo

JS nativo:

```js
feed.replaceChildren(...posts.map(renderPost));
```

Vue:

```vue
<PostCard
  v-for="post in posts"
  :key="post.id"
  :post="post"
/>
```

Descriviamo la UI attesa a partire dallo stato.

---

# ref

```js
import { ref } from 'vue';

const posts = ref([]);
```

Quando `posts.value` cambia, Vue sa quali parti della UI dipendono da quel dato.

---

# computed

```js
const postCount = computed(() => posts.value.length);
```

Un valore derivato non dovrebbe diventare un secondo stato da sincronizzare manualmente.

---

# Componenti

Un componente dovrebbe avere una responsabilità chiara.

Esempi Feisbuc:

- `PostCard`;
- `PostComposer`;
- `FeedView`;
- `AppShell`.

Separare componenti non significa spezzare ogni `<div>` in un file.

---

# Props

```vue
<script setup>
const props = defineProps({
  post: Object
});
</script>
```

Le props portano dati **dal parent al child**.

---

# Emits

```js
const emit = defineEmits(['delete']);

emit('delete', props.post.id);
```

Il child segnala un evento; il parent decide cosa fare.

---

# Flusso dati

```text
parent state
   ↓ props
child component
   ↑ event
parent handler
```

Questo mantiene chiara la proprietà dello stato.

---

# Errore tipico: duplicare stato derivato

Da evitare:

```js
const posts = ref([]);
const postCount = ref(0);
```

se `postCount` dipende solo da `posts`.

Meglio `computed`.

---

# Feisbuc milestone

La UI diventa SPA Vue:

- componenti;
- stato reattivo;
- form;
- feed;
- consumo API già esistente;
- auth/backend invariati.

---

# Checkpoint

Classifica:

1. lista post ricevuta dal parent;
2. evento delete dal child;
3. numero di post;
4. testo del composer;
5. risposta API che aggiorna il feed.

Props? emit? state? computed? side effect?

---

# Handoff al laboratorio

1. osserva reattività minima;
2. costruisci `PostCard`;
3. collega props/emits;
4. migra una parte del feed;
5. diagnostica un bug di stato o binding.

---

# Recap

Vue rende espliciti:

- stato reattivo;
- UI dichiarativa;
- componenti;
- props/emits;
- valori derivati.

Prossimo modulo: **Vue Router e navigazione SPA**.