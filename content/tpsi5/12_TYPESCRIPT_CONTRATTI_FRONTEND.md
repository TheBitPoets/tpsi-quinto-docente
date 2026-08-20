# TypeScript mirato: contratti statici nei boundary frontend

Stato didattico: **draft**  
UDA: **25 — Frontend framework, SPA e realtime**

## Obiettivi

Al termine del modulo lo studente sa:

- spiegare cosa aggiunge TypeScript a JavaScript e cosa **non** aggiunge;
- sfruttare l'inferenza prima di introdurre annotazioni manuali;
- modellare dati applicativi con `type`, `interface`, union e literal type;
- usare `unknown` e narrowing al posto di `any` nei boundary non affidabili;
- distinguere tipo statico e validazione runtime;
- modellare `null`/`undefined` senza nasconderli con assertion arbitrarie;
- tipizzare `ref`, `computed`, props ed emits in Vue 3;
- tipizzare una navigation policy e `RouteMeta` di Vue Router;
- eseguire un type-check separato dalla build Vite;
- riconoscere quando TypeScript migliora un boundary e quando invece produce solo rumore.

## Prerequisiti

- JavaScript moderno, funzioni, oggetti, moduli e asincronia;
- `fetch` e contratti HTTP;
- Vue 3 Composition API e `<script setup>`;
- Vue Router, route meta e navigation guard;
- Feisbuc milestone 10 funzionante.

## Problema iniziale

La milestone 10 funziona, ma molti contratti esistono solo nella nostra testa:

```js
async function createPost(text) { ... }

function toggleLike(id) { ... }

const userState = ref(null)
```

Domande che JavaScript da solo non può verificare prima dell'esecuzione:

- `id` è una stringa o un numero?
- `userState` può contenere qualunque oggetto?
- `liked` è davvero boolean?
- una navigation decision può avere contemporaneamente `action: "allow"` e `name: "login"`?
- un componente può emettere `delete` con un oggetto invece che con un id?

TypeScript nasce per rendere molti di questi contratti controllabili **prima** del runtime.

---

## 1. TypeScript non sostituisce JavaScript

TypeScript è JavaScript con un sistema di tipi statici sovrapposto.

```ts
const title = "Feisbuc"
const count = 3
```

Non serve scrivere:

```ts
const title: string = "Feisbuc"
const count: number = 3
```

se il compilatore può già inferire i tipi.

### Regola del corso

> annota quando l'annotazione chiarisce un contratto o impedisce un errore; lascia inferire quando il tipo è già evidente.

Questo evita il falso obiettivo di “mettere un tipo su ogni variabile”.

---

## 2. Tipi di dominio

Feisbuc ha ormai concetti stabili. Possiamo renderli espliciti:

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

Un tipo di dominio non è un DTO casuale: descrive un concetto che attraversa più componenti.

### `type` oppure `interface`?

Per questo corso:

- `interface` per shape di oggetti di dominio estendibili;
- `type` per union, literal e composizioni.

Non trasformiamo questa distinzione in dogma: entrambi gli strumenti hanno aree sovrapposte.

---

## 3. Literal type e union

La sessione della milestone 10 aveva già tre stati reali:

```text
unknown
anonymous
authenticated
```

In TypeScript possiamo impedire stati inventati:

```ts
export type AuthStatus = "unknown" | "anonymous" | "authenticated"
```

Quindi:

```ts
const status = ref<AuthStatus>("unknown")
```

rifiuta:

```ts
status.value = "logged"
```

Il vantaggio non è scrivere più codice: è ridurre lo spazio degli stati possibili.

---

## 4. Discriminated union: modellare decisioni impossibili da confondere

La navigation policy restituisce decisioni differenti:

```ts
export type NavigationDecision =
  | { action: "allow" }
  | { action: "resolve-auth" }
  | { action: "redirect"; name: RouteName; redirect?: string }
```

La proprietà `action` discrimina i casi.

```ts
if (decision.action === "redirect") {
  console.log(decision.name)
}
```

Dentro quel ramo TypeScript sa che `name` esiste.

Fuori da quel ramo non possiamo usare `decision.name` senza verificare il caso.

Questo è più forte di un oggetto generico come:

```ts
{
  action: string,
  name?: string,
  redirect?: string
}
```

perché quest'ultimo permette combinazioni prive di significato.

---

## 5. `unknown` non è `any`

### `any`

```ts
function parsePayload(payload: any) {
  return payload.user.displayName.toUpperCase()
}
```

`any` disattiva gran parte del controllo statico.

### `unknown`

```ts
function parsePayload(payload: unknown) {
  // payload.user  // errore: non sappiamo ancora che cosa sia payload
}
```

Per usarlo dobbiamo restringere il tipo.

```ts
function isRecord(value: unknown): value is Record<string, unknown> {
  return typeof value === "object" && value !== null
}
```

Ora possiamo costruire controlli espliciti.

### Regola del boundary

> dato esterno non verificato → `unknown`; dopo narrowing/validation → tipo di dominio.

Questo principio vale per:

- JSON HTTP;
- `localStorage` quando usato per dati non sensibili;
- input utente;
- messaggi WebSocket che introdurremo dopo;
- dati provenienti da API di terze parti.

---

## 6. TypeScript non valida il JSON a runtime

Questo codice è staticamente comodo ma non rende vera la risposta:

```ts
const payload = await response.json() as Post
```

Se il server invia:

```json
{"id": 42, "liked": "yes"}
```

l'assertion `as Post` non modifica il dato.

### Due livelli diversi

```text
TypeScript
  controlla il nostro programma

runtime validation
  controlla il dato arrivato davvero
```

Nel corso iniziamo con parser/guard piccoli e leggibili; librerie di schema potranno essere confrontate più avanti, ma non vengono introdotte qui per nascondere il concetto.

---

## 7. Narrowing di un Post

Esempio volutamente esplicito:

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

Poi:

```ts
function parsePost(value: unknown): Post {
  if (!isPost(value)) throw new Error("Invalid post payload")
  return value
}
```

Non useremo parser manuali giganteschi per sempre. Qui servono a rendere visibile il boundary.

---

## 8. Nullability

Con `strictNullChecks`, `User` e `User | null` non sono la stessa cosa.

```ts
const user = ref<User | null>(null)
```

Questo impedisce:

```ts
user.value.displayName
```

finché non dimostriamo che `user.value` esiste.

```ts
if (user.value) {
  console.log(user.value.displayName)
}
```

### Evitare il riflesso `!`

```ts
user.value!.displayName
```

significa: “so più del compilatore”. È legittimo solo quando abbiamo una prova che TypeScript non può vedere; non è uno strumento per silenziare errori scomodi.

---

## 9. `strict` come baseline

Il corso usa una configurazione intenzionalmente severa:

```json
{
  "compilerOptions": {
    "strict": true,
    "noUncheckedIndexedAccess": true,
    "exactOptionalPropertyTypes": true
  }
}
```

`strict` abilita i principali controlli rigorosi; `noUncheckedIndexedAccess` ricorda che un accesso tramite indice può non trovare nulla; `exactOptionalPropertyTypes` distingue meglio proprietà assenti e proprietà presenti con valore `undefined`.

Non disabilitiamo `strict` per far passare il codice: correggiamo il modello.

---

## 10. Type-only imports

Quando importiamo solo un tipo:

```ts
import type { Post, User } from "./domain"
```

comunichiamo che quell'import non deve produrre una dipendenza runtime.

È particolarmente utile con una toolchain ESM/Vite.

---

## 11. Vite transpila; `vue-tsc` controlla

Vite sa trasformare `.ts`, ma la build Vite non garantisce da sola che il progetto sia type-safe.

Perciò separiamo:

```json
{
  "scripts": {
    "type-check": "vue-tsc --noEmit",
    "build": "npm run type-check && vite build"
  }
}
```

Il comando didatticamente importante è:

```bash
npm run type-check
```

`--noEmit` significa: verifica i tipi senza generare JavaScript.

---

## 12. Versione del corso

Baseline riproducibile di questa unità:

```text
Vue             3.5.40
Vue Router      5.2.0
Vite             8.2.1
plugin-vue       6.0.8
TypeScript       6.0.3
vue-tsc          3.3.8
Node            >=22.18
```

TypeScript 7 è già disponibile nel 2026, ma il tooling Vue CLI di type-check ha avuto incompatibilità documentate con la nuova implementazione. Il corso non insegue una versione solo perché più nuova: privilegia una combinazione verificata e aggiornerà il pin quando il boundary `vue-tsc`/TS7 sarà stabile.

---

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

Ora questi errori sono osservabili prima del browser:

```ts
emit("delete", 42)
emit("toggle")
```

---

## 14. `ref` e `computed`

Vue inferisce molti tipi:

```ts
const loading = ref(false)
const count = computed(() => posts.value.length)
```

Annotiamo quando lo stato iniziale non basta:

```ts
const posts = ref<Post[]>([])
const user = ref<User | null>(null)
```

Non scriviamo il tipo esplicito quando l'inferenza è già esatta.

---

## 15. Event handler DOM

Con `strict`, un parametro evento non tipizzato può diventare `any` implicito.

```ts
function onInput(event: Event) {
  const input = event.target as HTMLInputElement
  console.log(input.value)
}
```

Anche qui l'assertion è locale e motivata dal DOM element che ha generato l'evento.

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

La policy diventa:

```ts
export function decideNavigation(input: NavigationInput): NavigationDecision {
  // stessa logica della milestone 10
}
```

Il comportamento non cambia; cambia la capacità di verificare il contratto.

---

## 17. Route meta tipizzata

Vue Router permette di estendere `RouteMeta`:

```ts
import "vue-router"

declare module "vue-router" {
  interface RouteMeta {
    requiresAuth?: boolean
  }
}
```

Questo impedisce typo silenziosi come:

```ts
meta: { requireAuth: true }
```

che avevamo già usato intenzionalmente come bug nella Activity D del routing.

TypeScript qui chiude un cerchio didattico: un bug già osservato a runtime diventa un errore statico.

---

## 18. API adapter: contratto e runtime check

Il boundary HTTP è uno dei punti dove TypeScript vale di più.

```ts
async function requestJson(path: string, init?: RequestInit): Promise<unknown> {
  const response = await fetch(path, init)
  const payload: unknown = await response.json()
  if (!response.ok) throw toApiError(response.status, payload)
  return payload
}
```

Poi:

```ts
async function listPosts(): Promise<Post[]> {
  const payload = await requestJson("/api/posts")
  return parsePosts(payload)
}
```

Il codice comunica due cose:

1. la rete è un boundary non affidabile;
2. dopo il parser abbiamo un `Post[]` affidabile per il resto dell'app.

---

## 19. Errore frequente: duplicare i tipi

Non vogliamo:

```text
FeedView/Post
PostCard/Post
api/Post
session/User
router/User
```

Vogliamo una piccola sorgente comune:

```text
src/domain.ts
```

che rappresenta il linguaggio del frontend.

Quando il progetto crescerà, potremo separare domain, transport e UI model. Non anticipiamo cartelle senza un problema reale.

---

## 20. Errore frequente: `any` come via d'uscita

```ts
const payload: any = await response.json()
```

fa sparire gli errori ma anche la protezione.

Nel core TPSI5:

```text
any      -> eccezione da giustificare
unknown  -> default per boundary non tipizzato
```

---

## 21. Errore frequente: TypeScript come validatore server

Tipizzare:

```ts
interface CreatePostInput { text: string }
```

nel frontend **non autorizza** il backend a fidarsi del client.

Express deve continuare a:

- validare body;
- derivare l'identità dalla sessione;
- applicare ownership;
- produrre 400/401/403 quando necessario.

I tipi frontend migliorano il client; non spostano il trust boundary.

---

## 22. Errore frequente: type gymnastics premature

Fuori dal core di questa unità:

- conditional types complessi;
- mapped types avanzati;
- template literal types sofisticati;
- decorators;
- utility type annidati difficili da leggere;
- generic framework abstractions costruite prima del bisogno.

Questi argomenti possono entrare nel percorso senior, non nella verticale minima del quinto anno.

---

## 23. Feisbuc milestone 11

La nuova milestone non riscrive il sistema:

```text
milestone 10
Vue Router + JS
      ↓
milestone 11
boundary TypeScript
```

Restano invariati:

```text
HTTP contract
Express
session cookie HttpOnly
authorization
SQLite
```

Cambiano soprattutto:

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

Il secondo non è “migliore” perché ha più simboli. È migliore se quel contratto aiuta IDE, refactoring, review e prevenzione degli errori.

---

## 25. Errori frequenti

1. annotare ogni costante invece di usare inference;
2. usare `any` per silenziare il compilatore;
3. usare `as` per fingere validato un JSON esterno;
4. usare `!` per eliminare nullability senza prova;
5. credere che `vite build` equivalga a type-check;
6. duplicare `Post` e `User` in più componenti;
7. tipizzare il client e rimuovere validation/autorizzazione dal server;
8. introdurre tipi avanzati prima di aver stabilizzato i boundary.

---

## 26. Esercizi A–F

### A — osservazione

Esegui il microscope TypeScript e osserva errori intercettati da inference, union, nullability e `unknown`.

### B — modifica controllata

Tipizza la navigation policy già nota usando discriminated union e route-name literal.

### C — scrittura autonoma

Applica il boundary typing alla milestone 10 di Feisbuc e ottieni milestone 11.

### D — debugging

Diagnostica `any`, assertion unsafe, nullability nascosta e contratto emit errato prima di correggere il progetto.

### E — mini-project

Aggiungi una view profilo tipizzata partendo da un endpoint documentato, mantenendo `unknown` sul boundary rete.

### F — prodotto integrato

Nel capstone, documenta quali boundary meritano tipi condivisi, quali richiedono runtime validation e quali restano semplici tipi locali.

---

## 27. Laboratorio

Definition of done della milestone 11:

- `npm run type-check` verde;
- `npm run build` verde;
- `strict: true` non disabilitato;
- nessun `any` nei file core della milestone;
- `Post`, `User` e `AuthStatus` centralizzati;
- navigation decision modellata come discriminated union;
- `RouteMeta.requiresAuth` tipizzato;
- props/emits principali tipizzati;
- JSON API trattato come `unknown` prima del parser;
- nessun cambiamento a security/ownership server-side;
- deep-link `/vue/feed` ancora funzionante.

---

## 28. Verifica rapida

1. Perché `as Post` non valida una risposta HTTP?
2. Quando usare `unknown` invece di `any`?
3. Che vantaggio offre una discriminated union per la navigation policy?
4. Perché `User | null` è più corretto di `User` per una sessione non ancora nota?
5. Perché Vite build e type-check sono due gate separati?
6. Che cosa impedisce la tipizzazione di `RouteMeta`?
7. TypeScript può sostituire la validation Express? Perché?
8. Quando un'annotazione esplicita è rumore?

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

Riferimenti tecnici primari:

- TypeScript Handbook e compiler options;
- Vue — Using Vue with TypeScript;
- Vue — TypeScript with Composition API;
- Vue Router — typed routes e RouteMeta;
- Vite — TypeScript / transpile-only;
- Vue Language Tools — `vue-tsc`.

Collegamenti interni:

- `10_VUE3_COMPONENTI_REATTIVITA.md`;
- `11_VUE_ROUTER_NAVIGAZIONE_SPA.md`;
- Activity A `tpsi5-activity-a-typescript-contract-microscope-001`;
- Activity B `tpsi5-activity-b-typescript-navigation-policy-001`;
- Activity C `tpsi5-activity-c-feisbuc-typescript-boundaries-001`;
- Activity D `tpsi5-activity-d-debug-typescript-boundaries-001`.
