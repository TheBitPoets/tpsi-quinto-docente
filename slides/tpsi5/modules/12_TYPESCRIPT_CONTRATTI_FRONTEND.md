---
marp: true
paginate: true
size: 16:9
title: 12 — TypeScript mirato nei boundary frontend
---

# 12 — TypeScript mirato
## Contratti statici nei boundary frontend

UDA 25 — Frontend application

---

# Richiamo

La SPA riceve dati da URL, API, storage ed eventi realtime.

Domanda:

> possiamo fidarci del tipo di un dato solo perché il nostro editor “pensa” che sia corretto?

No: i dati esterni arrivano a runtime.

---

# Obiettivi

Alla fine dovrai saper:

- distinguere type checking e runtime validation;
- usare tipi per DTO e domain model;
- trattare input esterno come `unknown` quando serve;
- scrivere parser/narrowing semplici;
- tipare route policy e payload remoti;
- evitare TypeScript “ovunque per principio”.

---

# Perché mirato

Il corso usa TypeScript dove rende visibile un confine:

```text
API response
route params
realtime payload
component contract
navigation policy
```

Non trasformiamo tutto il backend o ogni dettaglio in TypeScript avanzato.

---

# Tipo di dominio

```ts
interface Post {
  id: string;
  author: string;
  text: string;
  createdAt: string;
}
```

Questo descrive ciò che il codice **si aspetta**.

Non dimostra che un JSON esterno lo rispetti davvero.

---

# unknown

```ts
const data: unknown = await response.json();
```

`unknown` costringe a verificare prima di usare.

È più sicuro di `any`, che disattiva il controllo.

---

# Runtime parser

```ts
function parsePost(value: unknown): Post {
  if (!value || typeof value !== 'object') {
    throw new Error('invalid post');
  }

  // controlli mirati sui campi...
  return value as Post;
}
```

Il parser collega dato reale e tipo statico.

---

# DTO vs dominio

Il server può restituire:

```ts
interface PostDto {
  id: string;
  author_name: string;
  text: string;
}
```

Il frontend può trasformarlo in:

```ts
interface Post {
  id: string;
  author: string;
  text: string;
}
```

Il boundary è il punto giusto per adattare.

---

# Route params

```ts
const id = route.params.id;
```

Il tipo atteso non rende automaticamente valido il valore.

Serve una policy:

```ts
function parsePostId(value: unknown): string { ... }
```

---

# Component contracts

```ts
const props = defineProps<{
  post: Post;
}>();

const emit = defineEmits<{
  delete: [id: string];
}>();
```

TypeScript rende esplicito il contratto parent ↔ child.

---

# Errore tipico: cast come scorciatoia

```ts
const post = data as Post;
```

Il cast dice al compilatore “fidati di me”.

Non verifica niente a runtime.

Usarlo senza validation su input esterno può nascondere bug.

---

# Checkpoint

Quali dati meritano runtime validation?

1. costante scritta nel codice;
2. JSON da API;
3. prop interna già costruita da un parser;
4. route param;
5. payload Socket.IO;
6. valore derivato da `posts.length`.

---

# Feisbuc milestone

TypeScript entra nei boundary:

- API DTO;
- parser;
- route params;
- props/emits;
- navigation policy;
- eventi realtime nel modulo successivo.

Il comportamento del prodotto non cambia: aumenta la visibilità dei contratti.

---

# Handoff al laboratorio

1. osserva un boundary non tipato;
2. introduci `unknown`;
3. scrivi un parser semplice;
4. tipa props/emits o navigation policy;
5. correggi un bug mascherato da `any`/cast.

---

# Recap

TypeScript ci aiuta quando:

- rende un contratto leggibile;
- impedisce usi incoerenti;
- lavora insieme alla validation runtime.

Type checking **non sostituisce** runtime validation.

Prossimo modulo: **WebSocket e Socket.IO realtime**.