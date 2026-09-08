# TypeScript mirato: contratti statici nei boundary frontend

<table align="center" width="100%"><tr><td>
<details>
<summary>&#128506; <strong>Orientamento della lezione</strong></summary>

<p align="justify"><strong>Contesto:</strong> dominio, API, route e componenti esistono già. TypeScript viene introdotto ora per rendere verificabili questi confini, non per riscrivere l'intera applicazione o sostituire la validation runtime.</p>
<p align="justify"><strong>Domande guida:</strong> quali stati impossibili possiamo escludere? Perché un JSON esterno resta <code>unknown</code>? Dove conviene concentrare tipi e narrowing?</p>
<p align="justify"><strong>Obiettivi osservabili:</strong> modellare DTO e union, restringere valori <code>unknown</code>, mantenere <code>strict</code>, tipizzare props, route meta e adapter API e distinguere compilazione da validazione.</p>
<p align="justify"><strong>Prossimo passo:</strong> la lezione 13 userà questi boundary per gestire payload ed eventi realtime.</p>

</details>
</td></tr></table>

<p align="justify">Stato didattico: <strong>draft</strong> UDA: <strong>25 — Frontend framework, SPA e realtime</strong></p>

## Obiettivi

<p align="justify">Al termine del modulo lo studente sa:</p>

<ul>
  <li>spiegare cosa aggiunge TypeScript a JavaScript e cosa <strong>non</strong> aggiunge;</li>
  <li>sfruttare l'inferenza prima di introdurre annotazioni manuali;</li>
  <li>modellare dati applicativi con <code>type</code>, <code>interface</code>, union e literal type;</li>
  <li>usare <code>unknown</code> e narrowing al posto di <code>any</code> nei boundary non affidabili;</li>
  <li>distinguere tipo statico e validazione runtime;</li>
  <li>modellare <code>null</code>/<code>undefined</code> senza nasconderli con assertion arbitrarie;</li>
  <li>tipizzare <code>ref</code>, <code>computed</code>, props ed emits in Vue 3;</li>
  <li>tipizzare una navigation policy e <code>RouteMeta</code> di Vue Router;</li>
  <li>eseguire un type-check separato dalla build Vite;</li>
  <li>riconoscere quando TypeScript migliora un boundary e quando invece produce solo rumore.</li>
</ul>

## Prerequisiti

<ul>
  <li>JavaScript moderno, funzioni, oggetti, moduli e asincronia;</li>
  <li><code>fetch</code> e contratti HTTP;</li>
  <li>Vue 3 Composition API e <code>&lt;script setup&gt;</code>;</li>
  <li>Vue Router, route meta e navigation guard;</li>
  <li>Feisbuc milestone 10 funzionante.</li>
</ul>

## Orientamento nella documentazione

<p align="center">
  <img src="../../assets/tpsi5/lesson-documentation-depth.svg" alt="La dispensa seleziona nelle fonti ufficiali i contenuti da studiare ora, riconoscere, rimandare o dichiarare fuori confine">
</p>

<table align="center"><tr><td>
<details>
<summary>&#128279; <strong>Indice incrociato — TypeScript, Vue e validation runtime</strong></summary>

<table align="center">
<thead><tr><th>Dispensa</th><th>Documentazione ufficiale</th><th>Profondità</th></tr></thead>
<tbody>
<tr><td><a href="#lesson-ts-modeling">Tipi di dominio, literal e union</a></td><td><a href="https://www.typescriptlang.org/docs/handbook/2/everyday-types.html">TypeScript — Everyday Types</a></td><td>&#128994; studiare ora</td></tr>
<tr><td><a href="#lesson-ts-narrowing"><code>unknown</code> e narrowing</a></td><td><a href="https://www.typescriptlang.org/docs/handbook/2/narrowing.html">TypeScript — Narrowing</a></td><td>&#128994; studiare ora</td></tr>
<tr><td><a href="#lesson-ts-strict">Nullability e modalità strict</a></td><td><a href="https://www.typescriptlang.org/tsconfig/strict.html">TSConfig — strict</a><br><a href="https://www.typescriptlang.org/tsconfig/strictNullChecks.html">strictNullChecks</a></td><td>&#128994; studiare ora</td></tr>
<tr><td><a href="#lesson-ts-vue">Boundary Vue e API</a></td><td><a href="https://vuejs.org/guide/typescript/composition-api.html">Vue — TypeScript with Composition API</a></td><td>&#128994; studiare i pattern del corso</td></tr>
<tr><td>Generics avanzati, conditional type e type-level programming</td><td><a href="https://www.typescriptlang.org/docs/handbook/2/types-from-types.html">Creating Types from Types</a></td><td>&#128993; riconoscere, fuori dal core</td></tr>
</tbody>
</table>

</details>
</td></tr></table>

## Problema iniziale

<p align="justify">La milestone 10 funziona, ma molti contratti esistono solo nella nostra testa:</p>

```js
async function createPost(text) { ... }

function toggleLike(id) { ... }

const userState = ref(null)
```

<p align="justify">Domande che JavaScript da solo non può verificare prima dell'esecuzione:</p>

<ul>
  <li><code>id</code> è una stringa o un numero?</li>
  <li><code>userState</code> può contenere qualunque oggetto?</li>
  <li><code>liked</code> è davvero boolean?</li>
  <li>una navigation decision può avere contemporaneamente <code>action: "allow"</code> e <code>name: "login"</code>?</li>
  <li>un componente può emettere <code>delete</code> con un oggetto invece che con un id?</li>
</ul>

<p align="justify">TypeScript nasce per rendere molti di questi contratti controllabili <strong>prima</strong> del runtime.</p>

---

## 1. TypeScript non sostituisce JavaScript

<p align="justify">TypeScript è JavaScript con un sistema di tipi statici sovrapposto.</p>

```ts
const title = "Feisbuc"
const count = 3
```

<p align="justify">Non serve scrivere:</p>

```ts
const title: string = "Feisbuc"
const count: number = 3
```

<p align="justify">se il compilatore può già inferire i tipi.</p>

### Regola del corso

<blockquote>
<p align="justify">annota quando l'annotazione chiarisce un contratto o impedisce un errore; lascia inferire quando il tipo è già evidente.</p>
</blockquote>

<p align="justify">Questo evita il falso obiettivo di “mettere un tipo su ogni variabile”.</p>

---

<a id="lesson-ts-modeling"></a>
## 2. Tipi di dominio

<p align="justify">Feisbuc ha ormai concetti stabili. Possiamo renderli espliciti:</p>

```ts
export interface User {
  id: string
  email: string
  displayName: string
}

export interface Post {
  id: string
  authorId: string
  author: string
  text: string
  liked: boolean
  likes: number
}
```

<p align="justify">Un tipo di dominio non è un DTO casuale: descrive un concetto che attraversa più componenti.</p>

### `type` oppure `interface`?

<p align="justify">Per questo corso:</p>

<ul>
  <li><code>interface</code> per shape di oggetti di dominio estendibili;</li>
  <li><code>type</code> per union, literal e composizioni.</li>
</ul>

<p align="justify">Non trasformiamo questa distinzione in dogma: entrambi gli strumenti hanno aree sovrapposte.</p>

---

## 3. Literal type e union

<p align="justify">La sessione della milestone 10 aveva già tre stati reali:</p>

```text
unknown
anonymous
authenticated
```

<p align="justify">In TypeScript possiamo impedire stati inventati:</p>

```ts
export type AuthStatus = "unknown" | "anonymous" | "authenticated"
```

<p align="justify">Quindi:</p>

```ts
const status = ref<AuthStatus>("unknown")
```

<p align="justify">rifiuta:</p>

```ts
status.value = "logged"
```

<p align="justify">Il vantaggio non è scrivere più codice: è ridurre lo spazio degli stati possibili.</p>

---

## 4. Discriminated union: modellare decisioni impossibili da confondere

<p align="justify">La navigation policy restituisce decisioni differenti:</p>

```ts
export type NavigationDecision =
  | { action: "allow" }
  | { action: "resolve-auth" }
  | { action: "redirect"; name: RouteName; redirect?: string }
```

<p align="justify">La proprietà <code>action</code> discrimina i casi.</p>

```ts
if (decision.action === "redirect") {
  console.log(decision.name)
}
```

<p align="justify">Dentro quel ramo TypeScript sa che <code>name</code> esiste.</p>

<p align="justify">Fuori da quel ramo non possiamo usare <code>decision.name</code> senza verificare il caso.</p>

<p align="justify">Questo è più forte di un oggetto generico come:</p>

```ts
{
  action: string,
  name?: string,
  redirect?: string
}
```

<p align="justify">perché quest'ultimo permette combinazioni prive di significato.</p>

---

<a id="lesson-ts-narrowing"></a>
## 5. `unknown` non è `any`

### `any`

```ts
function parsePayload(payload: any) {
  return payload.user.displayName.toUpperCase()
}
```

<p align="justify"><code>any</code> disattiva gran parte del controllo statico.</p>

### `unknown`

```ts
function parsePayload(payload: unknown) {
  // payload.user  // errore: non sappiamo ancora che cosa sia payload
}
```

<p align="justify">Per usarlo dobbiamo restringere il tipo.</p>

```ts
function isRecord(value: unknown): value is Record<string, unknown> {
  return typeof value === "object" && value !== null
}
```

<p align="justify">Ora possiamo costruire controlli espliciti.</p>

### Regola del boundary

<blockquote>
<p align="justify">dato esterno non verificato → <code>unknown</code>; dopo narrowing/validation → tipo di dominio.</p>
</blockquote>

<p align="justify">Questo principio vale per:</p>

<ul>
  <li>JSON HTTP;</li>
  <li><code>localStorage</code> quando usato per dati non sensibili;</li>
  <li>input utente;</li>
  <li>messaggi WebSocket che introdurremo dopo;</li>
  <li>dati provenienti da API di terze parti.</li>
</ul>

---

## 6. TypeScript non valida il JSON a runtime

<p align="justify">Questo codice è staticamente comodo ma non rende vera la risposta:</p>

```ts
const payload = await response.json() as Post
```

<p align="justify">Se il server invia:</p>

```json
{"id": 42, "liked": "yes"}
```

<p align="justify">l'assertion <code>as Post</code> non modifica il dato.</p>

### Due livelli diversi

```text
TypeScript
  controlla il nostro programma

runtime validation
  controlla il dato arrivato davvero
```

<p align="justify">Nel corso iniziamo con parser/guard piccoli e leggibili; librerie di schema potranno essere confrontate più avanti, ma non vengono introdotte qui per nascondere il concetto.</p>

---

## 7. Narrowing di un Post

<p align="justify">Esempio volutamente esplicito:</p>

```ts
function isPost(value: unknown): value is Post {
  if (!isRecord(value)) return false

  return (
    typeof value.id === "string" &&
    typeof value.authorId === "string" &&
    typeof value.author === "string" &&
    typeof value.text === "string" &&
    typeof value.liked === "boolean" &&
    typeof value.likes === "number"
  )
}
```

<p align="justify">Poi:</p>

```ts
function parsePost(value: unknown): Post {
  if (!isPost(value)) throw new Error("Invalid post payload")
  return value
}
```

<p align="justify">Non useremo parser manuali giganteschi per sempre. Qui servono a rendere visibile il boundary.</p>

---

## 8. Nullability

<p align="justify">Con <code>strictNullChecks</code>, <code>User</code> e <code>User | null</code> non sono la stessa cosa.</p>

```ts
const user = ref<User | null>(null)
```

<p align="justify">Questo impedisce:</p>

```ts
user.value.displayName
```

<p align="justify">finché non dimostriamo che <code>user.value</code> esiste.</p>

```ts
if (user.value) {
  console.log(user.value.displayName)
}
```

### Evitare il riflesso `!`

```ts
user.value!.displayName
```

<p align="justify">significa: “so più del compilatore”. È legittimo solo quando abbiamo una prova che TypeScript non può vedere; non è uno strumento per silenziare errori scomodi.</p>

---

<a id="lesson-ts-strict"></a>
## 9. `strict` come baseline

<p align="justify">Il corso usa una configurazione intenzionalmente severa:</p>

```json
{
  "compilerOptions": {
    "strict": true,
    "noUncheckedIndexedAccess": true,
    "exactOptionalPropertyTypes": true
  }
}
```

<p align="justify"><code>strict</code> abilita i principali controlli rigorosi; <code>noUncheckedIndexedAccess</code> ricorda che un accesso tramite indice può non trovare nulla; <code>exactOptionalPropertyTypes</code> distingue meglio proprietà assenti e proprietà presenti con valore <code>undefined</code>.</p>

<p align="justify">Non disabilitiamo <code>strict</code> per far passare il codice: correggiamo il modello.</p>

---

## 10. Type-only imports

<p align="justify">Quando importiamo solo un tipo:</p>

```ts
import type { Post, User } from "./domain"
```

<p align="justify">comunichiamo che quell'import non deve produrre una dipendenza runtime.</p>

<p align="justify">È particolarmente utile con una toolchain ESM/Vite.</p>

---

## 11. Vite transpila; `vue-tsc` controlla

<p align="justify">Vite sa trasformare <code>.ts</code>, ma la build Vite non garantisce da sola che il progetto sia type-safe.</p>

<p align="justify">Perciò separiamo:</p>

```json
{
  "scripts": {
    "type-check": "vue-tsc --noEmit",
    "build": "npm run type-check && vite build"
  }
}
```

<p align="justify">Il comando didatticamente importante è:</p>

```bash
npm run type-check
```

<p align="justify"><code>--noEmit</code> significa: verifica i tipi senza generare JavaScript.</p>

---

## 12. Versione del corso

<p align="justify">Baseline riproducibile di questa unità:</p>

```text
Vue             3.5.40
Vue Router      5.2.0
Vite             8.2.1
plugin-vue       6.0.8
TypeScript       6.0.3
vue-tsc          3.3.8
Node            >=22.18
```

<p align="justify">TypeScript 7 è già disponibile nel 2026, ma il tooling Vue CLI di type-check ha avuto incompatibilità documentate con la nuova implementazione. Il corso non insegue una versione solo perché più nuova: privilegia una combinazione verificata e aggiornerà il pin quando il boundary <code>vue-tsc</code>/TS7 sarà stabile.</p>

---

<a id="lesson-ts-vue"></a>
## 13. Vue: `<script setup lang="ts">`

```vue
<script setup lang="ts">
import type { Post } from "../domain"

const props = defineProps<{
  post: Post
  canDelete?: boolean
}>()

const emit = defineEmits<{
  "toggle-like": [id: string]
  delete: [id: string]
}>()
</script>
```

<p align="justify">Ora questi errori sono osservabili prima del browser:</p>

```ts
emit("delete", 42)
emit("toggle")
```

---

## 14. `ref` e `computed`

<p align="justify">Vue inferisce molti tipi:</p>

```ts
const loading = ref(false)
const count = computed(() => posts.value.length)
```

<p align="justify">Annotiamo quando lo stato iniziale non basta:</p>

```ts
const posts = ref<Post[]>([])
const user = ref<User | null>(null)
```

<p align="justify">Non scriviamo il tipo esplicito quando l'inferenza è già esatta.</p>

---

## 15. Event handler DOM

<p align="justify">Con <code>strict</code>, un parametro evento non tipizzato può diventare <code>any</code> implicito.</p>

```ts
function onInput(event: Event) {
  const input = event.target as HTMLInputElement
  console.log(input.value)
}
```

<p align="justify">Anche qui l'assertion è locale e motivata dal DOM element che ha generato l'evento.</p>

---

## 16. Navigation policy tipizzata

```ts
export type RouteName = "login" | "feed" | "about" | "not-found"

export interface NavigationInput {
  routeName: RouteName
  requiresAuth: boolean
  authStatus: AuthStatus
  fullPath: string
}
```

<p align="justify">La policy diventa:</p>

```ts
export function decideNavigation(input: NavigationInput): NavigationDecision {
  // stessa logica della milestone 10
}
```

<p align="justify">Il comportamento non cambia; cambia la capacità di verificare il contratto.</p>

---

## 17. Route meta tipizzata

<p align="justify">Vue Router permette di estendere <code>RouteMeta</code>:</p>

```ts
import "vue-router"

declare module "vue-router" {
  interface RouteMeta {
    requiresAuth?: boolean
  }
}
```

<p align="justify">Questo impedisce typo silenziosi come:</p>

```ts
meta: { requireAuth: true }
```

<p align="justify">che avevamo già usato intenzionalmente come bug nella Activity D del routing.</p>

<p align="justify">TypeScript qui chiude un cerchio didattico: un bug già osservato a runtime diventa un errore statico.</p>

---

## 18. API adapter: contratto e runtime check

<p align="justify">Il boundary HTTP è uno dei punti dove TypeScript vale di più.</p>

```ts
async function requestJson(path: string, init?: RequestInit): Promise<unknown> {
  const response = await fetch(path, init)
  const payload: unknown = await response.json()
  if (!response.ok) throw toApiError(response.status, payload)
  return payload
}
```

<p align="justify">Poi:</p>

```ts
async function listPosts(): Promise<Post[]> {
  const payload = await requestJson("/api/posts")
  return parsePosts(payload)
}
```

<p align="justify">Il codice comunica due cose:</p>

<ol>
  <li>la rete è un boundary non affidabile;</li>
  <li>dopo il parser abbiamo un <code>Post[]</code> affidabile per il resto dell'app.</li>
</ol>

---

## 19. Errore frequente: duplicare i tipi

<p align="justify">Non vogliamo:</p>

```text
FeedView/Post
PostCard/Post
api/Post
session/User
router/User
```

<p align="justify">Vogliamo una piccola sorgente comune:</p>

```text
src/domain.ts
```

<p align="justify">che rappresenta il linguaggio del frontend.</p>

<p align="justify">Quando il progetto crescerà, potremo separare domain, transport e UI model. Non anticipiamo cartelle senza un problema reale.</p>

---

## 20. Errore frequente: `any` come via d'uscita

```ts
const payload: any = await response.json()
```

<p align="justify">fa sparire gli errori ma anche la protezione.</p>

<p align="justify">Nel core TPSI5:</p>

```text
any      -> eccezione da giustificare
unknown  -> default per boundary non tipizzato
```

---

## 21. Errore frequente: TypeScript come validatore server

<p align="justify">Tipizzare:</p>

```ts
interface CreatePostInput { text: string }
```

<p align="justify">nel frontend <strong>non autorizza</strong> il backend a fidarsi del client.</p>

<p align="justify">Express deve continuare a:</p>

<ul>
  <li>validare body;</li>
  <li>derivare l'identità dalla sessione;</li>
  <li>applicare ownership;</li>
  <li>produrre 400/401/403 quando necessario.</li>
</ul>

<p align="justify">I tipi frontend migliorano il client; non spostano il trust boundary.</p>

---

## 22. Errore frequente: type gymnastics premature

<p align="justify">Fuori dal core di questa unità:</p>

<ul>
  <li>conditional types complessi;</li>
  <li>mapped types avanzati;</li>
  <li>template literal types sofisticati;</li>
  <li>decorators;</li>
  <li>utility type annidati difficili da leggere;</li>
  <li>generic framework abstractions costruite prima del bisogno.</li>
</ul>

<p align="justify">Questi argomenti possono entrare nel percorso senior, non nella verticale minima del quinto anno.</p>

---

## 23. Feisbuc milestone 11

<p align="justify">La nuova milestone non riscrive il sistema:</p>

```text
milestone 10
Vue Router + JS
      ↓
milestone 11
boundary TypeScript
```

<p align="justify">Restano invariati:</p>

```text
HTTP contract
Express
session cookie HttpOnly
authorization
SQLite
```

<p align="justify">Cambiano soprattutto:</p>

```text
src/domain.ts
src/api.ts
src/navigation-policy.ts
src/session.ts
src/router.ts
<script setup lang="ts">
props / emits
```

### Invariante architetturale

```text
unknown external data
        ↓
runtime narrowing/parser
        ↓
typed domain
        ↓
Vue views/components
        ↓
API server-side security invariata
```

---

## 24. Confronto prima/dopo

### Prima

```js
const posts = ref([])
async function createPost(text) { ... }
```

### Dopo

```ts
const posts = ref<Post[]>([])
async function createPost(text: string): Promise<Post> { ... }
```

<p align="justify">Il secondo non è “migliore” perché ha più simboli. È migliore se quel contratto aiuta IDE, refactoring, review e prevenzione degli errori.</p>

---

## 25. Errori frequenti

<ol>
  <li>annotare ogni costante invece di usare inference;</li>
  <li>usare <code>any</code> per silenziare il compilatore;</li>
  <li>usare <code>as</code> per fingere validato un JSON esterno;</li>
  <li>usare <code>!</code> per eliminare nullability senza prova;</li>
  <li>credere che <code>vite build</code> equivalga a type-check;</li>
  <li>duplicare <code>Post</code> e <code>User</code> in più componenti;</li>
  <li>tipizzare il client e rimuovere validation/autorizzazione dal server;</li>
  <li>introdurre tipi avanzati prima di aver stabilizzato i boundary.</li>
</ol>

---

## 26. Esercizi A–F

### A — osservazione

<p align="justify">Esegui il microscope TypeScript e osserva errori intercettati da inference, union, nullability e <code>unknown</code>.</p>

### B — modifica controllata

<p align="justify">Tipizza la navigation policy già nota usando discriminated union e route-name literal.</p>

### C — scrittura autonoma

<p align="justify">Applica il boundary typing alla milestone 10 di Feisbuc e ottieni milestone 11.</p>

### D — debugging

<p align="justify">Diagnostica <code>any</code>, assertion unsafe, nullability nascosta e contratto emit errato prima di correggere il progetto.</p>

### E — mini-project

<p align="justify">Aggiungi una view profilo tipizzata partendo da un endpoint documentato, mantenendo <code>unknown</code> sul boundary rete.</p>

### F — prodotto integrato

<p align="justify">Nel capstone, documenta quali boundary meritano tipi condivisi, quali richiedono runtime validation e quali restano semplici tipi locali.</p>

---

## 27. Laboratorio

<p align="justify">Definition of done della milestone 11:</p>

<ul>
  <li><code>npm run type-check</code> verde;</li>
  <li><code>npm run build</code> verde;</li>
  <li><code>strict: true</code> non disabilitato;</li>
  <li>nessun <code>any</code> nei file core della milestone;</li>
  <li><code>Post</code>, <code>User</code> e <code>AuthStatus</code> centralizzati;</li>
  <li>navigation decision modellata come discriminated union;</li>
  <li><code>RouteMeta.requiresAuth</code> tipizzato;</li>
  <li>props/emits principali tipizzati;</li>
  <li>JSON API trattato come <code>unknown</code> prima del parser;</li>
  <li>nessun cambiamento a security/ownership server-side;</li>
  <li>deep-link <code>/vue/feed</code> ancora funzionante.</li>
</ul>

---

## 28. Verifica rapida

<ol>
  <li>Perché <code>as Post</code> non valida una risposta HTTP?</li>
  <li>Quando usare <code>unknown</code> invece di <code>any</code>?</li>
  <li>Che vantaggio offre una discriminated union per la navigation policy?</li>
  <li>Perché <code>User | null</code> è più corretto di <code>User</code> per una sessione non ancora nota?</li>
  <li>Perché Vite build e type-check sono due gate separati?</li>
  <li>Che cosa impedisce la tipizzazione di <code>RouteMeta</code>?</li>
  <li>TypeScript può sostituire la validation Express? Perché?</li>
  <li>Quando un'annotazione esplicita è rumore?</li>
</ol>

---

## 29. Sintesi inclusiva

```text
TypeScript = JavaScript + controlli statici

inference prima
annotation quando serve

union = stati possibili espliciti
unknown = dato non ancora affidabile
narrowing = prova prima dell'uso

Vue:
ref<T>
props typed
emits typed
RouteMeta typed

Vite transpila
vue-tsc controlla

TypeScript NON valida la rete
TypeScript NON sostituisce il backend
```

---

## 30. Fonti e collegamenti

<p align="justify">Riferimenti tecnici primari:</p>

<ul>
  <li>TypeScript Handbook e compiler options;</li>
  <li>Vue — Using Vue with TypeScript;</li>
  <li>Vue — TypeScript with Composition API;</li>
  <li>Vue Router — typed routes e RouteMeta;</li>
  <li>Vite — TypeScript / transpile-only;</li>
  <li>Vue Language Tools — <code>vue-tsc</code>.</li>
</ul>

<p align="justify">Collegamenti interni:</p>

<ul>
  <li><code>10_VUE3_COMPONENTI_REATTIVITA.md</code>;</li>
  <li><code>11_VUE_ROUTER_NAVIGAZIONE_SPA.md</code>;</li>
  <li>Activity A <code>tpsi5-activity-a-typescript-contract-microscope-001</code>;</li>
  <li>Activity B <code>tpsi5-activity-b-typescript-navigation-policy-001</code>;</li>
  <li>Activity C <code>tpsi5-activity-c-feisbuc-typescript-boundaries-001</code>;</li>
  <li>Activity D <code>tpsi5-activity-d-debug-typescript-boundaries-001</code>.</li>
</ul>
