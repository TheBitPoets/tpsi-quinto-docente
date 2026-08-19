# Vue Router: URL, navigazione e route protette nella SPA

## Obiettivi

Al termine del modulo lo studente sa:

- spiegare perche una SPA con piu viste deve rappresentare la navigazione nell'URL;
- distinguere navigazione browser, client-side routing e routing HTTP server-side;
- configurare Vue Router con `createRouter()` e `createWebHistory()`;
- usare route record, route name, `RouterLink` e `RouterView`;
- usare `router.push()`, `router.replace()`, `useRouter()` e `useRoute()`;
- distinguere path, params e query string;
- costruire una pagina 404 client-side con catch-all route;
- spiegare perche HTML5 history richiede un fallback server-side per i deep link;
- usare `meta.requiresAuth` e una navigation guard senza confonderla con authorization backend;
- gestire lo stato iniziale della sessione come `unknown`, `anonymous` o `authenticated`;
- preservare la destinazione richiesta dopo il login;
- usare lazy route components quando il progetto cresce;
- diagnosticare redirect loop, 404 server/client e guard incoerenti.

## Prerequisiti

- `10_VUE3_COMPONENTI_REATTIVITA.md`;
- HTTP request/response e status code;
- History API concettuale;
- auth/session/authorization di UDA24;
- Feisbuc milestone 9.

## Problema iniziale

Milestone 9 e una SPA, ma ha una sola vista applicativa:

```text
/vue/
  -> auth se anonimo
  -> feed se autenticato
```

Se aggiungiamo pagine distinte senza un router, possiamo nascondere/mostrare componenti con variabili locali:

```text
currentView = "feed" | "about" | "login"
```

ma il browser non sa quale vista stiamo mostrando.

Problemi:

```text
refresh          -> perde la vista
bookmark         -> non rappresenta la vista
back/forward     -> non segue la navigazione applicativa
deep link        -> impossibile
condividi URL    -> impossibile
404 client       -> non modellato
```

Il nuovo requisito e quindi:

```text
URL <-> stato di navigazione della SPA
```

## 1. Tre routing diversi

Non usare la parola "routing" senza precisare il livello.

```text
HTTP server routing
GET /api/posts -> Express Router -> JSON

client-side routing
/vue/feed -> Vue Router -> FeedView

rete IP routing
packet -> router di rete -> next hop
```

In questo modulo studiamo il **client-side routing**.

## 2. Vue Router nel corso

Baseline riproducibile:

```text
Vue             3.5.40
Vue Router      5.2.0
Vite            8.2.1
@vitejs/plugin-vue 6.0.8
Node            >=22.18
```

Dipendenza:

```json
{
  "dependencies": {
    "vue": "3.5.40",
    "vue-router": "5.2.0"
  }
}
```

Vue Router e il router ufficiale per Vue.

## 3. Route record

Una route collega una location a un componente:

```js
const routes = [
  {
    path: "/feed",
    name: "feed",
    component: FeedView,
  },
  {
    path: "/about",
    name: "about",
    component: AboutView,
  },
];
```

Modello:

```text
URL /feed
   ↓ match
route record
   ↓
FeedView
```

I nomi evitano di spargere stringhe URL in tutta l'applicazione:

```vue
<RouterLink :to="{ name: 'feed' }">Feed</RouterLink>
```

## 4. Router instance

```js
import { createRouter, createWebHistory } from "vue-router";

export const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes,
});
```

Poi:

```js
createApp(App)
  .use(router)
  .mount("#app");
```

`RouterView` indica dove renderizzare la view corrente:

```vue
<main>
  <RouterView />
</main>
```

`App.vue` diventa quindi soprattutto un **layout applicativo**.

## 5. `RouterLink` non e soltanto un `<a>` decorato

```vue
<RouterLink :to="{ name: 'feed' }">Feed</RouterLink>
```

Vue Router:

- genera l'URL;
- aggiorna la History API senza reload completo;
- mantiene la semantica di link;
- gestisce classi active;
- supporta encoding e route name.

Non sostituire sistematicamente i link con:

```vue
<button @click="router.push('/feed')">Feed</button>
```

se semanticamente stai navigando verso una risorsa/vista.

## 6. Navigazione programmatica

Dentro `<script setup>`:

```js
import { useRouter } from "vue-router";

const router = useRouter();

await router.push({ name: "feed" });
```

`push()` aggiunge una entry alla history.

`replace()` sostituisce quella corrente:

```js
await router.replace({ name: "login" });
```

Collegamento Web Platform:

```text
router.push()    ~ history.pushState()
router.replace() ~ history.replaceState()
router.back()    ~ history.back()
```

## 7. Route corrente

```js
import { useRoute } from "vue-router";

const route = useRoute();
```

Informazioni utili:

```text
route.path
route.fullPath
route.name
route.params
route.query
route.meta
```

Non copiare l'intero `route` in un altro `ref` solo per tenerlo sincronizzato: e gia reattivo.

## 8. Params e query

Path param:

```text
/post/42
```

route:

```js
{
  path: "/post/:id",
  name: "post-detail",
  component: PostDetailView,
}
```

navigation:

```js
router.push({
  name: "post-detail",
  params: { id: "42" },
});
```

Query:

```text
/feed?liked=true
```

```js
route.query.liked
```

Regola concettuale:

```text
param -> identifica una parte del path/risorsa
query -> modifica filtro, ricerca o rappresentazione
```

## 9. HTML5 history e deep link

Con:

```js
createWebHistory()
```

la URL e pulita:

```text
/vue/feed
/vue/about
```

Ma c'e una differenza importante.

Navigazione interna:

```text
/vue/ -> click Feed
Vue Router intercetta
-> /vue/feed
```

Deep link/refesh:

```text
browser -> GET /vue/feed HTTP
             ↓
          Express
```

Il server deve quindi sapere che `/vue/feed` appartiene alla SPA e servire `index.html`.

Nel nostro Express 5 reference:

```js
app.use("/vue", express.static(vueRoot));

app.get("/vue/{*splat}", (req, res) => {
  res.sendFile("index.html", { root: vueRoot });
});
```

In Express 5 il wildcard di route deve essere **nominato**.

## 10. Server fallback e client 404 sono problemi diversi

Server fallback:

```text
GET /vue/qualunque-cosa
       ↓
server restituisce SPA index.html
```

Client catch-all:

```js
{
  path: "/:pathMatch(.*)",
  name: "not-found",
  component: NotFoundView,
}
```

Quindi:

```text
server 200 index.html
       ↓
Vue Router
       ↓
NotFoundView
```

Per una SPA statica semplice questa separazione e normale.

## 11. Redirect iniziale

```js
{
  path: "/",
  redirect: { name: "feed" },
}
```

Il redirect e un route record, non una view.

## 12. Route protette

Il feed richiede una sessione valida:

```js
{
  path: "/feed",
  name: "feed",
  component: FeedView,
  meta: { requiresAuth: true },
}
```

La metadata descrive una proprieta della route.

Navigation guard:

```js
router.beforeEach(async (to) => {
  await session.ensureKnown();

  if (to.meta.requiresAuth && !session.user.value) {
    return {
      name: "login",
      query: { redirect: to.fullPath },
    };
  }
});
```

## 13. Guard != sicurezza del backend

La guard migliora UX:

```text
anonimo -> /feed
          ↓
      redirect /login
```

Ma un client puo sempre tentare direttamente:

```http
GET /api/posts
```

La sicurezza resta:

```text
loadAuth
requireAuth
ownership
401 / 403 server-side
```

Regola del corso:

> Una route guard protegge la navigazione dell'interfaccia. Non autorizza una API.

## 14. Il problema dello stato auth iniziale

All'avvio non sappiamo ancora se il cookie HttpOnly corrisponde a una sessione valida.

Tre stati:

```text
unknown
anonymous
authenticated
```

Non ridurre subito tutto a:

```js
const loggedIn = ref(false);
```

perche `false` significherebbe contemporaneamente:

- non abbiamo ancora chiesto `/me`;
- abbiamo chiesto `/me` e ricevuto 401.

## 15. Un composable piccolo prima di Pinia

Per questo requisito basta un modulo condiviso:

```js
const status = ref("unknown");
const user = ref(null);

export function useSession() {
  return { status, user, ensureKnown, login, register, logout };
}
```

E una scelta consapevole:

```text
problema piccolo di stato condiviso
       ↓
module/composable

problema di store piu ampio
       ↓
valuteremo Pinia
```

Non introduciamo una libreria perche "nelle SPA si usa".

## 16. Preservare la destinazione dopo login

Utente anonimo visita:

```text
/vue/feed?liked=true
```

Guard:

```text
/login?redirect=/feed?liked=true
```

Dopo login:

```js
await router.replace(safeRedirect(route.query.redirect));
```

Non fidarti ciecamente di una destinazione arbitraria ricevuta dalla query.

Nel nostro caso accettiamo soltanto path interni:

```js
function safeRedirect(value) {
  if (typeof value !== "string") return "/feed";
  if (!value.startsWith("/") || value.startsWith("//")) return "/feed";
  return value;
}
```

## 17. Login route e redirect loop

Errore comune:

```js
router.beforeEach(async to => {
  if (!user.value) return "/login";
});
```

Quando il target e gia `/login`:

```text
/login -> guard -> /login -> guard -> /login -> ...
```

La policy deve distinguere route pubbliche/protette e utente autenticato/anonimo.

## 18. Una policy di navigazione pura

Prima della guard estraiamo:

```js
decideNavigation({
  routeName,
  requiresAuth,
  authStatus,
  fullPath,
})
```

Output possibile:

```json
{"action":"allow"}
```

oppure:

```json
{
  "action":"redirect",
  "name":"login",
  "redirect":"/feed"
}
```

Vantaggio:

```text
policy pura -> test deterministico
Vue Router guard -> adapter/orchestrazione
```

## 19. Lazy route components

Quando una view diventa una boundary naturale:

```js
{
  path: "/about",
  component: () => import("./views/AboutView.vue"),
}
```

Vite puo produrre chunk separati per route.

Nel corso non useremo lazy loading per nascondere concetti: prima route record e navigation, poi code splitting.

## 20. Feisbuc milestone 10

Struttura:

```text
App.vue
  ├── nav
  └── RouterView
        ├── LoginView
        ├── FeedView
        ├── AboutView
        └── NotFoundView

router.js
  ↓
navigation-policy.js
  ↓
useSession()
  ↓
api.js
  ↓
/api/*
```

Route:

```text
/             -> redirect feed
/login        -> public
/feed         -> requiresAuth
/about        -> public
/*            -> NotFoundView
```

## 21. FeedView

`FeedView` possiede lo stato specifico del feed:

```text
posts
loading feed
errore feed
```

La sessione non appartiene al feed: e condivisa da router, layout e login.

Questo rende il confine piu chiaro:

```text
session state -> composable condiviso
feed state    -> FeedView
```

## 22. LoginView

`LoginView`:

- usa `AuthPanel`;
- chiama login/register del session composable;
- legge `route.query.redirect`;
- naviga dopo successo;
- non legge il cookie.

## 23. App come layout

`App.vue` non deve tornare a diventare un controller monolitico.

```vue
<template>
  <header>
    <RouterLink :to="{ name: 'feed' }">Feed</RouterLink>
    <RouterLink :to="{ name: 'about' }">About</RouterLink>
  </header>

  <RouterView />
</template>
```

Il layout puo mostrare utente/logout perche sono concern applicativi globali minimi.

## 24. 401 durante una sessione gia caricata

Una sessione puo scadere dopo che la SPA ha caricato `user`.

Se una request protetta riceve 401:

```text
client state authenticated
backend session expired
```

Il backend vince.

La SPA deve poter invalidare lo stato locale e tornare al login.

Non assumere:

```text
user != null -> sessione sicuramente valida per sempre
```

## 25. Errori frequenti

### Confondere route guard e API authorization

```text
bottone nascosto / guard -> UX
401/403 backend           -> security
```

### Usare `window.location` per navigazione interna

Causa reload completo e bypassa il modello del router.

### Hardcodare path ovunque

Preferire route name per destinazioni stabili.

### Dimenticare il server fallback

Funziona cliccando dentro la SPA ma refresh `/vue/feed` produce 404 HTTP.

### Catch-all server senza catch-all client

Ogni URL restituisce index.html ma l'app non spiega all'utente che la route non esiste.

### Redirect loop

Guard che redirige anche la login route verso se stessa.

### Duplicare auth state

```text
routerUser
appUser
loginUser
```

che divergono.

## 26. Debug in quattro livelli

Quando `/vue/feed` non funziona:

1. **HTTP** — il server restituisce `index.html` o 404?
2. **route match** — quale route record ha matchato?
3. **guard** — allow, redirect o loop?
4. **view/API** — la view monta e le request ricevono 200/401/403?

Non correggere un server 404 modificando `RouterView`.

## 27. Esercizi A-F

- **A** — osserva URL, `RouterLink`, `RouterView`, back/forward e deep link;
- **B** — implementa la navigation policy pura;
- **C** — porta Feisbuc a milestone 10 con route protette e server fallback;
- **D** — diagnostica redirect loop, 404 e guard incoerenti;
- **E** — prossimo incremento: TypeScript mirato sui boundary Vue/API oppure state management se emerge un requisito reale;
- **F** — integrazione realtime WebSocket/Socket.IO.

## 28. Activity collegate

- `tpsi5-activity-a-vue-router-microscope-001`;
- `tpsi5-activity-b-navigation-policy-001`;
- `tpsi5-activity-c-feisbuc-vue-router-001`;
- `tpsi5-activity-d-debug-vue-router-001`.

## 29. Verifica rapida

1. Perche una SPA multi-view deve aggiornare l'URL?
2. Differenza tra `RouterLink` e `RouterView`?
3. Perche `createWebHistory()` richiede server fallback?
4. Differenza tra server fallback e client 404?
5. Perche `authStatus="unknown"` e diverso da `anonymous`?
6. Una navigation guard protegge `/api/posts`?
7. Perche usare route name?
8. Quando serve `replace()` invece di `push()`?
9. Perche non introduciamo ancora Pinia?
10. Quali quattro livelli controlli quando un deep link non funziona?

## 30. Sintesi inclusiva

```text
URL              -> stato di navigazione
route record     -> URL -> view
RouterLink       -> navigazione dichiarativa
RouterView       -> punto di rendering
router.push      -> nuova history entry
router.replace   -> sostituisce history entry
meta             -> dati della route
beforeEach       -> navigation policy adapter
createWebHistory -> URL pulita + server fallback
catch-all route  -> 404 client-side
route guard      -> UX/navigation
401/403 backend  -> sicurezza
```

## 31. Fonti e collegamenti

- Vue Router official documentation — Getting Started, History Modes, Named Routes, Navigation Guards, Route Meta Fields, Lazy Loading;
- Express 5 migration guide — named wildcard syntax;
- `10_VUE3_COMPONENTI_REATTIVITA.md`;
- `08_AUTH_SESSIONI_SICUREZZA.md`.

## 32. Prossimo passo

Dopo routing abbiamo finalmente una SPA con piu view e URL reale.

Il prossimo gate didattico e decidere se introdurre **TypeScript mirato** sui confini gia stabili (`Post`, `User`, route meta, props e payload API) prima del realtime.

Pinia resta rinviata: verra introdotta solo se il progetto sviluppa un requisito di stato condiviso piu complesso del piccolo session composable.