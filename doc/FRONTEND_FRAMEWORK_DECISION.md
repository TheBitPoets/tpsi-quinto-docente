# Decisione frontend TPSI5 — Vue 3 + Vite

Stato: **deciso**.

## Decisione

Il framework frontend principale di UDA25 e **Vue 3 con Vite**.

React non viene insegnato come secondo framework core. Viene mantenuto come **translation/comparison lab professionale** dopo che gli studenti hanno costruito almeno una feature completa in Vue.

## Perche Vue nel percorso TPSI5

Il corso arriva a UDA25 dopo avere costruito esplicitamente:

```text
HTML -> CSS -> Bootstrap -> JavaScript -> DOM/eventi
     -> HTTP/fetch/REST -> Express -> SQL -> auth -> SSR
```

Vue deve quindi essere presentato come una nuova astrazione sopra concetti gia osservati, non come un nuovo mondo separato.

Mapping didattico principale:

```text
state -> render manuale      -> reattivita Vue
createElement/template HTML  -> template dichiarativo
listener DOM                 -> event binding
form/value                   -> v-model
array + render loop          -> v-for
condizionale DOM             -> v-if
moduli JS                    -> componenti/SFC
funzioni di stato derivato   -> computed
confini UI                   -> props + emits
```

## Stack UDA25

Core previsto:

- Vue 3;
- Vite;
- Single File Components;
- Composition API;
- `<script setup>`;
- props ed emits;
- `ref` / `reactive` dove appropriato;
- `computed` prima di `watch`;
- form e validation client-side;
- data fetching verso la API Feisbuc esistente;
- sessione same-origin gia costruita in UDA24;
- routing SPA;
- stato condiviso solo quando emerge un requisito reale;
- realtime successivamente nello stesso UDA.

## Boundary TypeScript

La scelta Vue **non congela ancora TypeScript**.

Direzione preferita: introduzione mirata nella seconda parte del blocco Vue sui tipi di dominio e sui confini applicativi:

```text
Post
User
props
payload API
response HTTP
```

Da evitare:

- duplicare ogni esercizio JS in TS;
- anticipare generics/type-level programming non necessario;
- sacrificare routing, API, testing o realtime per il tooling.

## Boundary React

React resta rilevante professionalmente. Il corso deve rendere esplicita la trasferibilita dei concetti senza aprire un secondo percorso completo.

Translation lab previsto:

```text
Vue ref          <-> React state
Vue computed     <-> derived value
Vue props        <-> React props
Vue emits        <-> callback prop
v-if             <-> conditional JSX
v-for            <-> array.map()
v-model          <-> controlled input
SFC component    <-> React component
```

Obiettivo: lo studente deve uscire sapendo **perche esiste un framework frontend** e quali problemi risolve, non soltanto ricordando direttive Vue.

## Feisbuc

Il prossimo step longitudinale e:

```text
milestone 8 — SSR/Nunjucks
          ↓
milestone 9 — Vue SPA
          ↓
realtime — WebSocket/Socket.IO
```

La SPA Vue deve riusare il contratto HTTP, la sessione, l'autorizzazione e il database gia costruiti. Nessuna nuova identita o persistence strategy viene introdotta perche cambia il presentation layer.

## Decisioni ancora aperte

- profondita TypeScript;
- ORM Node;
- ampiezza precisa del mirror FastAPI/SQLAlchemy;
- eventuale estrazione del blocco SQL in corso dedicato.
