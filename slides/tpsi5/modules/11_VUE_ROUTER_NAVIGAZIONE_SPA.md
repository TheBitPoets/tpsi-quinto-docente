---
marp: true
paginate: true
size: 16:9
title: 11 — Vue Router: URL e navigazione SPA
---

# 11 — Vue Router
## URL, navigazione e route protette nella SPA

UDA 25 — Frontend application

---

# Richiamo

Abbiamo una SPA Vue, ma se tutto vive in una sola view manca una cosa importante:

> l'URL non rappresenta ancora lo stato di navigazione.

---

# Obiettivi

Alla fine dovrai saper:

- definire route;
- usare params e query;
- spiegare l'URL come stato condivisibile;
- usare layout e not-found;
- applicare navigation guard;
- distinguere guard frontend da autorizzazione backend.

---

# URL come stato

```text
/feed
/posts/42
/profile/mario
```

Un buon URL permette:

- refresh;
- bookmark;
- back/forward;
- link condivisibile.

---

# Route table

```js
const routes = [
  { path: '/feed', component: FeedView },
  { path: '/posts/:id', component: PostView },
  { path: '/:pathMatch(.*)*', component: NotFoundView }
];
```

---

# Parametri

URL:

```text
/posts/42
```

Route param:

```js
const route = useRoute();
const id = route.params.id;
```

Il parametro arriva come input esterno: va trattato con attenzione.

---

# RouterLink

```vue
<RouterLink :to="`/posts/${post.id}`">
  Apri post
</RouterLink>
```

Navigazione SPA senza costruire manualmente listener e History API.

---

# Layout

Struttura tipica:

```vue
<AppShell>
  <RouterView />
</AppShell>
```

Il layout resta stabile; cambia la view associata all'URL.

---

# Navigation guard

```js
router.beforeEach((to) => {
  if (to.meta.requiresAuth && !session.user) {
    return '/login';
  }
});
```

Serve per UX e flusso applicativo.

Non sostituisce authz server-side.

---

# Frontend guard ≠ sicurezza

Un utente può bypassare il client e chiamare direttamente l'API.

Quindi:

```text
frontend guard -> esperienza utente
backend authz -> sicurezza reale
```

---

# Errore tipico: stato duplicato con l'URL

Se la view selezionata è già rappresentata da `/posts/42`, evitare un secondo `selectedPostId` non necessario.

Quando possibile, l'URL può essere la fonte del dato di navigazione.

---

# Checkpoint

Dove dovrebbe vivere:

1. post selezionato tramite `/posts/:id`;
2. controllo ownership;
3. redirect a login;
4. pagina 404;
5. layout comune.

---

# Feisbuc milestone

Feisbuc ottiene:

- feed route;
- detail route;
- login/navigation flow;
- route guard;
- not found;
- URL coerenti con lo stato.

---

# Handoff al laboratorio

1. definisci route;
2. aggiungi detail param;
3. implementa not-found;
4. prova una guard;
5. dimostra che il backend continua a proteggere l'API.

---

# Recap

Vue Router rende la navigazione parte esplicita dell'architettura.

Da ricordare:

- URL = stato;
- route params = input;
- guard = UX;
- authz = server.

Prossimo modulo: **TypeScript mirato nei boundary frontend**.