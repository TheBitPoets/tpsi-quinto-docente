# Vue Router: URL, navigazione e route protette nella SPA

<table align="center" width="100%"><tr><td>
<details>
<summary>&#128506; <strong>Orientamento della lezione</strong></summary>

<p align="justify"><strong>Contesto:</strong> la prima SPA possiede componenti e stato, ma non può ancora rappresentare viste differenti con URL condivisibili e navigazione avanti/indietro.</p>
<p align="justify"><strong>Domande guida:</strong> quale vista corrisponde a una URL? Che differenza c'è fra navigazione interna e deep link? Perché una route guard migliora la UX ma non sostituisce l'authorization del backend?</p>
<p align="justify"><strong>Obiettivi osservabili:</strong> definire route record, usare link e navigazione programmatica, configurare history e fallback, preservare la destinazione dopo il login e diagnosticare una 404 al livello corretto.</p>
<p align="justify"><strong>Prossimo passo:</strong> la lezione 12 renderà espliciti con TypeScript i contratti già stabilizzati nei boundary frontend.</p>

</details>
</td></tr></table>

## Obiettivi

<p align="justify">Al termine del modulo lo studente sa:</p>

<ul>
  <li>spiegare perche una SPA con piu viste deve rappresentare la navigazione nell'URL;</li>
  <li>distinguere navigazione browser, client-side routing e routing HTTP server-side;</li>
  <li>configurare Vue Router con <code>createRouter()</code> e <code>createWebHistory()</code>;</li>
  <li>usare route record, route name, <code>RouterLink</code> e <code>RouterView</code>;</li>
  <li>usare <code>router.push()</code>, <code>router.replace()</code>, <code>useRouter()</code> e <code>useRoute()</code>;</li>
  <li>distinguere path, params e query string;</li>
  <li>costruire una pagina 404 client-side con catch-all route;</li>
  <li>spiegare perche HTML5 history richiede un fallback server-side per i deep link;</li>
  <li>usare <code>meta.requiresAuth</code> e una navigation guard senza confonderla con authorization backend;</li>
  <li>gestire lo stato iniziale della sessione come <code>unknown</code>, <code>anonymous</code> o <code>authenticated</code>;</li>
  <li>preservare la destinazione richiesta dopo il login;</li>
  <li>usare lazy route components quando il progetto cresce;</li>
  <li>diagnosticare redirect loop, 404 server/client e guard incoerenti.</li>
</ul>

## Prerequisiti

<ul>
  <li><code>10_VUE3_COMPONENTI_REATTIVITA.md</code>;</li>
  <li>HTTP request/response e status code;</li>
  <li>History API concettuale;</li>
  <li>auth/session/authorization di UDA24;</li>
  <li>Feisbuc milestone 9.</li>
</ul>

## Orientamento nella documentazione

<p align="center">
  <img src="../../assets/tpsi5/lesson-documentation-depth.svg" alt="La dispensa seleziona nelle fonti ufficiali i contenuti da studiare ora, riconoscere, rimandare o dichiarare fuori confine">
</p>

<table align="center"><tr><td>
<details>
<summary>&#128279; <strong>Indice incrociato — Vue Router, URL e History API</strong></summary>

<table align="center">
<thead><tr><th>Dispensa</th><th>Documentazione ufficiale</th><th>Profondità</th></tr></thead>
<tbody>
<tr><td><a href="#lesson-router-model">Route record, router e route corrente</a></td><td><a href="https://router.vuejs.org/guide/essentials/dynamic-matching.html">Vue Router — Dynamic matching</a><br><a href="https://router.vuejs.org/guide/advanced/composition-api.html">Composition API</a></td><td>&#128994; studiare ora</td></tr>
<tr><td><a href="#lesson-router-navigation">Link e navigazione programmatica</a></td><td><a href="https://router.vuejs.org/guide/essentials/navigation.html">Programmatic navigation</a><br><a href="https://router.vuejs.org/guide/essentials/named-routes.html">Named routes</a></td><td>&#128994; studiare ora</td></tr>
<tr><td><a href="#lesson-router-history">History mode e deep link</a></td><td><a href="https://router.vuejs.org/guide/essentials/history-mode.html">Vue Router — History modes</a><br><a href="https://developer.mozilla.org/en-US/docs/Web/API/History_API">MDN — History API</a></td><td>&#128994; studiare ora</td></tr>
<tr><td><a href="#lesson-router-guards">Route meta e navigation guard</a></td><td><a href="https://router.vuejs.org/guide/advanced/navigation-guards.html">Navigation guards</a><br><a href="https://router.vuejs.org/guide/advanced/meta.html">Route meta fields</a></td><td>&#128994; studiare il caso del corso</td></tr>
<tr><td>Nested route avanzate, scroll behavior e data loader</td><td><a href="https://router.vuejs.org/guide/">Vue Router Guide</a></td><td>&#128993; riconoscere, fuori dal core</td></tr>
</tbody>
</table>

</details>
</td></tr></table>

## Problema iniziale

<p align="justify">Milestone 9 e una SPA, ma ha una sola vista applicativa:</p>

```text
/vue/
  -> auth se anonimo
  -> feed se autenticato
```

<p align="justify">Se aggiungiamo pagine distinte senza un router, possiamo nascondere/mostrare componenti con variabili locali:</p>

```text
currentView = "feed" | "about" | "login"
```

<p align="justify">ma il browser non sa quale vista stiamo mostrando.</p>

<p align="justify">Problemi:</p>

```text
refresh          -> perde la vista
bookmark         -> non rappresenta la vista
back/forward     -> non segue la navigazione applicativa
deep link        -> impossibile
condividi URL    -> impossibile
404 client       -> non modellato
```

<p align="justify">Il nuovo requisito e quindi:</p>

```text
URL <-> stato di navigazione della SPA
```

<a id="lesson-router-model"></a>
## 1. Tre routing diversi

<p align="justify">Non usare la parola "routing" senza precisare il livello.</p>

```text
HTTP server routing
GET /api/posts -> Express Router -> JSON

client-side routing
/vue/feed -> Vue Router -> FeedView

rete IP routing
packet -> router di rete -> next hop
```

<p align="justify">In questo modulo studiamo il <strong>client-side routing</strong>.</p>

## 2. Vue Router nel corso

<p align="justify">Baseline riproducibile:</p>

```text
Vue             3.5.40
Vue Router      5.2.0
Vite            8.2.1
@vitejs/plugin-vue 6.0.8
Node            >=22.18
```

<p align="justify">Dipendenza:</p>

```json
{
  "dependencies": {
    "vue": "3.5.40",
    "vue-router": "5.2.0"
  }
}
```

<p align="justify">Vue Router e il router ufficiale per Vue.</p>

## 3. Route record

<p align="justify">Una route collega una location a un componente:</p>

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

<p align="justify">Modello:</p>

```text
URL /feed
   ↓ match
route record
   ↓
FeedView
```

<p align="justify">I nomi evitano di spargere stringhe URL in tutta l'applicazione:</p>

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

<p align="justify">Poi:</p>

```js
createApp(App)
  .use(router)
  .mount("#app");
```

<p align="justify"><code>RouterView</code> indica dove renderizzare la view corrente:</p>

```vue
<main>
  <RouterView />
</main>
```

<p align="justify"><code>App.vue</code> diventa quindi soprattutto un <strong>layout applicativo</strong>.</p>

<a id="lesson-router-navigation"></a>
## 5. `RouterLink` non e soltanto un `<a>` decorato

```vue
<RouterLink :to="{ name: 'feed' }">Feed</RouterLink>
```

<p align="justify">Vue Router:</p>

<ul>
  <li>genera l'URL;</li>
  <li>aggiorna la History API senza reload completo;</li>
  <li>mantiene la semantica di link;</li>
  <li>gestisce classi active;</li>
  <li>supporta encoding e route name.</li>
</ul>

<p align="justify">Non sostituire sistematicamente i link con:</p>

```vue
<button @click="router.push('/feed')">Feed</button>
```

<p align="justify">se semanticamente stai navigando verso una risorsa/vista.</p>

## 6. Navigazione programmatica

<p align="justify">Dentro <code>&lt;script setup&gt;</code>:</p>

```js
import { useRouter } from "vue-router";

const router = useRouter();

await router.push({ name: "feed" });
```

<p align="justify"><code>push()</code> aggiunge una entry alla history.</p>

<p align="justify"><code>replace()</code> sostituisce quella corrente:</p>

```js
await router.replace({ name: "login" });
```

<p align="justify">Collegamento Web Platform:</p>

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

<p align="justify">Informazioni utili:</p>

```text
route.path
route.fullPath
route.name
route.params
route.query
route.meta
```

<p align="justify">Non copiare l'intero <code>route</code> in un altro <code>ref</code> solo per tenerlo sincronizzato: e gia reattivo.</p>

## 8. Params e query

<p align="justify">Path param:</p>

```text
/post/42
```

<p align="justify">route:</p>

```js
{
  path: "/post/:id",
  name: "post-detail",
  component: PostDetailView,
}
```

<p align="justify">navigation:</p>

```js
router.push({
  name: "post-detail",
  params: { id: "42" },
});
```

<p align="justify">Query:</p>

```text
/feed?liked=true
```

```js
route.query.liked
```

<p align="justify">Regola concettuale:</p>

```text
param -> identifica una parte del path/risorsa
query -> modifica filtro, ricerca o rappresentazione
```

<a id="lesson-router-history"></a>
## 9. HTML5 history e deep link

<table align="center"><tr><td>
<p align="justify"><strong><span style="font-size: 1.15em;">&#128279;</span> MDN sotto Vue Router:</strong> per l'API del router usa la documentazione ufficiale Vue Router; per comprendere URL e history del browser usa la <a href="GUIDA_USO_MDN.md#mdn-guide-source-choice">regola di scelta delle fonti</a>, la <a href="https://developer.mozilla.org/en-US/docs/Web/API/History_API">History API</a> e la reference di <a href="https://developer.mozilla.org/en-US/docs/Web/API/URL"><code>URL</code></a>.</p>
<p align="justify"><strong>Studia ora:</strong> history entry, navigazione avanti/indietro, path e query. <strong>Riconosci per dopo:</strong> i metodi nativi dettagliati che Vue Router incapsula. <strong>Prodotto atteso:</strong> spiega separatamente che cosa accade durante una navigazione interna e durante il caricamento diretto di un deep link.</p>
</td></tr></table>

<p align="justify">Con:</p>

```js
createWebHistory()
```

<p align="justify">la URL e pulita:</p>

```text
/vue/feed
/vue/about
```

<p align="justify">Ma c'e una differenza importante.</p>

<p align="justify">Navigazione interna:</p>

```text
/vue/ -> click Feed
Vue Router intercetta
-> /vue/feed
```

<p align="justify">Deep link/refesh:</p>

```text
browser -> GET /vue/feed HTTP
             ↓
          Express
```

<p align="justify">Il server deve quindi sapere che <code>/vue/feed</code> appartiene alla SPA e servire <code>index.html</code>.</p>

<p align="justify">Nel nostro Express 5 reference:</p>

```js
app.use("/vue", express.static(vueRoot));

app.get("/vue/{*splat}", (req, res) => {
  res.sendFile("index.html", { root: vueRoot });
});
```

<p align="justify">In Express 5 il wildcard di route deve essere <strong>nominato</strong>.</p>

## 10. Server fallback e client 404 sono problemi diversi

<p align="justify">Server fallback:</p>

```text
GET /vue/qualunque-cosa
       ↓
server restituisce SPA index.html
```

<p align="justify">Client catch-all:</p>

```js
{
  path: "/:pathMatch(.*)",
  name: "not-found",
  component: NotFoundView,
}
```

<p align="justify">Quindi:</p>

```text
server 200 index.html
       ↓
Vue Router
       ↓
NotFoundView
```

<p align="justify">Per una SPA statica semplice questa separazione e normale.</p>

## 11. Redirect iniziale

```js
{
  path: "/",
  redirect: { name: "feed" },
}
```

<p align="justify">Il redirect e un route record, non una view.</p>

<a id="lesson-router-guards"></a>
## 12. Route protette

<p align="justify">Il feed richiede una sessione valida:</p>

```js
{
  path: "/feed",
  name: "feed",
  component: FeedView,
  meta: { requiresAuth: true },
}
```

<p align="justify">La metadata descrive una proprieta della route.</p>

<p align="justify">Navigation guard:</p>

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

<p align="justify">La guard migliora UX:</p>

```text
anonimo -> /feed
          ↓
      redirect /login
```

<p align="justify">Ma un client puo sempre tentare direttamente:</p>

```http
GET /api/posts
```

<p align="justify">La sicurezza resta:</p>

```text
loadAuth
requireAuth
ownership
401 / 403 server-side
```

<p align="justify">Regola del corso:</p>

<blockquote>
<p align="justify">Una route guard protegge la navigazione dell'interfaccia. Non autorizza una API.</p>
</blockquote>

## 14. Il problema dello stato auth iniziale

<p align="justify">All'avvio non sappiamo ancora se il cookie HttpOnly corrisponde a una sessione valida.</p>

<p align="justify">Tre stati:</p>

```text
unknown
anonymous
authenticated
```

<p align="justify">Non ridurre subito tutto a:</p>

```js
const loggedIn = ref(false);
```

<p align="justify">perche <code>false</code> significherebbe contemporaneamente:</p>

<ul>
  <li>non abbiamo ancora chiesto <code>/me</code>;</li>
  <li>abbiamo chiesto <code>/me</code> e ricevuto 401.</li>
</ul>

## 15. Un composable piccolo prima di Pinia

<p align="justify">Per questo requisito basta un modulo condiviso:</p>

```js
const status = ref("unknown");
const user = ref(null);

export function useSession() {
  return { status, user, ensureKnown, login, register, logout };
}
```

<p align="justify">E una scelta consapevole:</p>

```text
problema piccolo di stato condiviso
       ↓
module/composable

problema di store piu ampio
       ↓
valuteremo Pinia
```

<p align="justify">Non introduciamo una libreria perche "nelle SPA si usa".</p>

## 16. Preservare la destinazione dopo login

<p align="justify">Utente anonimo visita:</p>

```text
/vue/feed?liked=true
```

<p align="justify">Guard:</p>

```text
/login?redirect=/feed?liked=true
```

<p align="justify">Dopo login:</p>

```js
await router.replace(safeRedirect(route.query.redirect));
```

<p align="justify">Non fidarti ciecamente di una destinazione arbitraria ricevuta dalla query.</p>

<p align="justify">Nel nostro caso accettiamo soltanto path interni:</p>

```js
function safeRedirect(value) {
  if (typeof value !== "string") return "/feed";
  if (!value.startsWith("/") || value.startsWith("//")) return "/feed";
  return value;
}
```

## 17. Login route e redirect loop

<p align="justify">Errore comune:</p>

```js
router.beforeEach(async to => {
  if (!user.value) return "/login";
});
```

<p align="justify">Quando il target e gia <code>/login</code>:</p>

```text
/login -> guard -> /login -> guard -> /login -> ...
```

<p align="justify">La policy deve distinguere route pubbliche/protette e utente autenticato/anonimo.</p>

## 18. Una policy di navigazione pura

<p align="justify">Prima della guard estraiamo:</p>

```js
decideNavigation({
  routeName,
  requiresAuth,
  authStatus,
  fullPath,
})
```

<p align="justify">Output possibile:</p>

```json
{"action":"allow"}
```

<p align="justify">oppure:</p>

```json
{
  "action":"redirect",
  "name":"login",
  "redirect":"/feed"
}
```

<p align="justify">Vantaggio:</p>

```text
policy pura -> test deterministico
Vue Router guard -> adapter/orchestrazione
```

## 19. Lazy route components

<p align="justify">Quando una view diventa una boundary naturale:</p>

```js
{
  path: "/about",
  component: () => import("./views/AboutView.vue"),
}
```

<p align="justify">Vite puo produrre chunk separati per route.</p>

<p align="justify">Nel corso non useremo lazy loading per nascondere concetti: prima route record e navigation, poi code splitting.</p>

## 20. Feisbuc milestone 10

<p align="justify">Struttura:</p>

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

<p align="justify">Route:</p>

```text
/             -> redirect feed
/login        -> public
/feed         -> requiresAuth
/about        -> public
/*            -> NotFoundView
```

## 21. FeedView

<p align="justify"><code>FeedView</code> possiede lo stato specifico del feed:</p>

```text
posts
loading feed
errore feed
```

<p align="justify">La sessione non appartiene al feed: e condivisa da router, layout e login.</p>

<p align="justify">Questo rende il confine piu chiaro:</p>

```text
session state -> composable condiviso
feed state    -> FeedView
```

## 22. LoginView

<p align="justify"><code>LoginView</code>:</p>

<ul>
  <li>usa <code>AuthPanel</code>;</li>
  <li>chiama login/register del session composable;</li>
  <li>legge <code>route.query.redirect</code>;</li>
  <li>naviga dopo successo;</li>
  <li>non legge il cookie.</li>
</ul>

## 23. App come layout

<p align="justify"><code>App.vue</code> non deve tornare a diventare un controller monolitico.</p>

```vue
<template>
  <header>
    <RouterLink :to="{ name: 'feed' }">Feed</RouterLink>
    <RouterLink :to="{ name: 'about' }">About</RouterLink>
  </header>

  <RouterView />
</template>
```

<p align="justify">Il layout puo mostrare utente/logout perche sono concern applicativi globali minimi.</p>

## 24. 401 durante una sessione gia caricata

<p align="justify">Una sessione puo scadere dopo che la SPA ha caricato <code>user</code>.</p>

<p align="justify">Se una request protetta riceve 401:</p>

```text
client state authenticated
backend session expired
```

<p align="justify">Il backend vince.</p>

<p align="justify">La SPA deve poter invalidare lo stato locale e tornare al login.</p>

<p align="justify">Non assumere:</p>

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

<p align="justify">Causa reload completo e bypassa il modello del router.</p>

### Hardcodare path ovunque

<p align="justify">Preferire route name per destinazioni stabili.</p>

### Dimenticare il server fallback

<p align="justify">Funziona cliccando dentro la SPA ma refresh <code>/vue/feed</code> produce 404 HTTP.</p>

### Catch-all server senza catch-all client

<p align="justify">Ogni URL restituisce index.html ma l'app non spiega all'utente che la route non esiste.</p>

### Redirect loop

<p align="justify">Guard che redirige anche la login route verso se stessa.</p>

### Duplicare auth state

```text
routerUser
appUser
loginUser
```

<p align="justify">che divergono.</p>

## 26. Debug in quattro livelli

<p align="justify">Quando <code>/vue/feed</code> non funziona:</p>

<ol>
  <li><strong>HTTP</strong> — il server restituisce <code>index.html</code> o 404?</li>
  <li><strong>route match</strong> — quale route record ha matchato?</li>
  <li><strong>guard</strong> — allow, redirect o loop?</li>
  <li><strong>view/API</strong> — la view monta e le request ricevono 200/401/403?</li>
</ol>

<p align="justify">Non correggere un server 404 modificando <code>RouterView</code>.</p>

## 27. Esercizi A-F

<ul>
  <li><strong>A</strong> — osserva URL, <code>RouterLink</code>, <code>RouterView</code>, back/forward e deep link;</li>
  <li><strong>B</strong> — implementa la navigation policy pura;</li>
  <li><strong>C</strong> — porta Feisbuc a milestone 10 con route protette e server fallback;</li>
  <li><strong>D</strong> — diagnostica redirect loop, 404 e guard incoerenti;</li>
  <li><strong>E</strong> — prossimo incremento: TypeScript mirato sui boundary Vue/API oppure state management se emerge un requisito reale;</li>
  <li><strong>F</strong> — integrazione realtime WebSocket/Socket.IO.</li>
</ul>

## 28. Activity collegate

<ul>
  <li><code>tpsi5-activity-a-vue-router-microscope-001</code>;</li>
  <li><code>tpsi5-activity-b-navigation-policy-001</code>;</li>
  <li><code>tpsi5-activity-c-feisbuc-vue-router-001</code>;</li>
  <li><code>tpsi5-activity-d-debug-vue-router-001</code>.</li>
</ul>

## 29. Verifica rapida

<ol>
  <li>Perche una SPA multi-view deve aggiornare l'URL?</li>
  <li>Differenza tra <code>RouterLink</code> e <code>RouterView</code>?</li>
  <li>Perche <code>createWebHistory()</code> richiede server fallback?</li>
  <li>Differenza tra server fallback e client 404?</li>
  <li>Perche <code>authStatus="unknown"</code> e diverso da <code>anonymous</code>?</li>
  <li>Una navigation guard protegge <code>/api/posts</code>?</li>
  <li>Perche usare route name?</li>
  <li>Quando serve <code>replace()</code> invece di <code>push()</code>?</li>
  <li>Perche non introduciamo ancora Pinia?</li>
  <li>Quali quattro livelli controlli quando un deep link non funziona?</li>
</ol>

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

<ul>
  <li>Vue Router official documentation — Getting Started, History Modes, Named Routes, Navigation Guards, Route Meta Fields, Lazy Loading;</li>
  <li>Express 5 migration guide — named wildcard syntax;</li>
  <li><code>10_VUE3_COMPONENTI_REATTIVITA.md</code>;</li>
  <li><code>08_AUTH_SESSIONI_SICUREZZA.md</code>.</li>
</ul>

## 32. Prossimo passo

<p align="justify">Dopo routing abbiamo finalmente una SPA con piu view e URL reale.</p>

<p align="justify">Il prossimo gate didattico e decidere se introdurre <strong>TypeScript mirato</strong> sui confini gia stabili (<code>Post</code>, <code>User</code>, route meta, props e payload API) prima del realtime.</p>

<p align="justify">Pinia resta rinviata: verra introdotta solo se il progetto sviluppa un requisito di stato condiviso piu complesso del piccolo session composable.</p>
