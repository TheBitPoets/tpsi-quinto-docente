# WebSocket e Socket.IO: dal request/response al realtime

Stato didattico: **draft**.

## Obiettivi

Al termine del modulo lo studente sa:

- distinguere polling, HTTP request/response, Server-Sent Events, WebSocket e Socket.IO a livello concettuale;
- spiegare perche WebSocket crea un canale bidirezionale persistente ma non definisce da solo eventi applicativi, riconnessione, rooms o recovery;
- spiegare perche Socket.IO **non e semplicemente WebSocket**: normalmente usa WebSocket quando disponibile, puo usare HTTP long-polling e aggiunge semantica event-based, riconnessione e broadcasting;
- progettare eventi applicativi piccoli e versionabili;
- mantenere separati **command path** e **event path**;
- autenticare una connessione realtime usando la stessa sessione server-side gia verificata dal backend;
- evitare di fidarsi di identita o mutazioni dichiarate dal client realtime;
- gestire disconnessione e riconnessione senza assumere consegna perfetta degli eventi;
- integrare Socket.IO in Feisbuc senza cambiare il contratto REST, l'authorization o SQLite.

## Prerequisiti

- UDA23: HTTP, status, fetch e REST;
- UDA24: Express, SQLite, sessioni HttpOnly e authorization;
- UDA25: Vue 3, Vue Router e TypeScript boundary typing;
- modello `state -> render` e idea di source of truth.

## Problema iniziale

Feisbuc milestone 11 e corretta ma ogni browser conosce solo cio che ha appena richiesto al server.

Supponiamo che Alice e Bob abbiano entrambi aperto `/vue/feed`.

1. Alice crea un post con `POST /api/posts`;
2. il database contiene subito il nuovo post;
3. Alice aggiorna il proprio state con la response `201`;
4. Bob non sa ancora che il post esiste.

Bob potrebbe fare polling:

```text
ogni 2 s -> GET /api/posts
```

ma molte request non riporterebbero alcuna novita.

Il requisito nuovo e diverso:

> quando lo stato condiviso cambia, il server deve poter notificare i client connessi senza aspettare una nuova request applicativa.

Questo e il problema del **realtime push**.

---

## 1. HTTP request/response non scompare

L'introduzione del realtime non rende REST inutile.

Nel nostro progetto REST continua a essere adatto per i **comandi**:

```text
POST   /api/posts       crea
PATCH  /api/posts/:id   modifica like
DELETE /api/posts/:id   elimina
GET    /api/posts       snapshot corrente
```

Il realtime aggiunge un secondo flusso:

```text
server -> client
post:created
post:updated
post:deleted
```

Quindi:

```text
COMMAND PATH
browser -> HTTP -> authorization -> transaction/store -> response

EVENT PATH
                                     stato gia modificato
                                             ↓
server -> realtime event -> altri client -> local state
```

Regola TPSI5:

> **un evento realtime annuncia una mutazione gia autorizzata e completata; non sostituisce automaticamente la API dei comandi.**

Questo evita di duplicare validation, status HTTP e authorization dentro handler socket improvvisati.

---

## 2. Polling, push e connessione persistente

### Polling

```text
client -> server: ci sono novita?
server -> client: no
client -> server: ci sono novita?
server -> client: no
client -> server: ci sono novita?
server -> client: si
```

E semplice e robusto ma puo produrre traffico e latenza inutili.

### WebSocket

Un WebSocket crea un canale persistente e bidirezionale:

```text
HTTP handshake
      ↓ upgrade
WebSocket aperto
client <----------> server
```

Dopo l'handshake, entrambi i lati possono inviare messaggi senza aprire una nuova request HTTP applicativa per ogni messaggio.

Il browser espone l'API `WebSocket`:

```js
const ws = new WebSocket("wss://example.test/realtime");

ws.addEventListener("message", (event) => {
  console.log(event.data);
});

ws.send("hello");
```

Ma WebSocket non decide per noi:

- come chiamare gli eventi;
- come serializzare il dominio;
- come fare broadcast;
- come raggruppare client;
- come riconnettersi;
- come recuperare eventi persi;
- come rappresentare acknowledgements applicativi.

Queste sono responsabilita del protocollo/applicazione costruita sopra WebSocket.

---

## 3. Socket.IO non e un alias di WebSocket

Socket.IO fornisce un modello ad eventi ispirato a `EventEmitter`:

```js
socket.on("post:created", (post) => {
  // aggiorna lo state locale
});
```

Sul server:

```js
io.emit("post:created", post);
```

In condizioni normali la connessione puo usare WebSocket; Socket.IO puo anche usare HTTP long-polling quando necessario e aggiunge funzionalita come riconnessione automatica e broadcasting.

Per questo e scorretto insegnare:

```text
Socket.IO = wrapper WebSocket
```

Meglio:

```text
WebSocket = protocollo/canale bidirezionale
Socket.IO = protocollo + libreria event-based con fallback e servizi applicativi
```

### Baseline riproducibile del corso

La reference 2026/27 pinna:

```text
socket.io         4.8.3
socket.io-client  4.8.3
Vue               3.5.40
Vue Router        5.2.0
TypeScript        6.0.3
vue-tsc           3.3.8
Vite              8.2.1
Node              >=22.18
```

---

## 4. Evento applicativo != riga del database

Un buon evento dice **che cosa e successo nel dominio**.

Per Feisbuc useremo un contratto piccolo:

```ts
export type RealtimeEvent =
  | { type: "post:created"; post: Post }
  | { type: "post:updated"; post: Post }
  | { type: "post:deleted"; postId: string };
```

Non inviamo:

```text
SQL statement
row interna con password/session data
req/res Express
oggetto DatabaseSync
```

L'evento usa lo stesso modello pubblico `Post` gia esposto dalla API.

---

## 5. Reducer realtime: evento -> nuovo state

Prima di aprire un socket separiamo la logica pura.

```ts
function applyRealtimeEvent(posts: Post[], event: RealtimeEvent): Post[] {
  switch (event.type) {
    case "post:created":
      return posts.some((post) => post.id === event.post.id)
        ? posts
        : [event.post, ...posts];

    case "post:updated":
      return posts.map((post) =>
        post.id === event.post.id ? event.post : post
      );

    case "post:deleted":
      return posts.filter((post) => post.id !== event.postId);
  }
}
```

Perche evitare semplicemente:

```ts
posts.value.push(event.post);
```

Perche una UI realtime deve ragionare anche su:

- eventi duplicati;
- update di un elemento esistente;
- delete;
- source of truth;
- riconnessione e snapshot.

---

## 6. Command path ed event path

Quando Alice crea un post:

```text
Alice
  │
  │ POST /api/posts
  ▼
Express Router
  │
  ├─ requireAuth
  ├─ validation
  └─ SqlPostStore.create
           │
           ▼
        SQLite commit
           │
           ├──────────────► HTTP 201 ad Alice
           │
           └──────────────► post:created
                                   │
                                   ├─► Alice
                                   └─► Bob
```

La REST response resta importante per chi ha eseguito il comando.

L'evento permette agli altri client di convergere sul nuovo stato.

### Duplicazione apparente

Alice puo ricevere:

1. la response HTTP con il post creato;
2. l'evento `post:created` dello stesso post.

Per questo il reducer deve essere idempotente rispetto allo stesso `post.id`.

---

## 7. Non fidarsi del socket client

Il modello insicuro sarebbe:

```js
socket.on("post:create", ({ authorId, text }) => {
  // NON FARE
  postStore.create({ authorId, text });
});
```

Problemi:

- duplica la API POST;
- rischia di saltare validation;
- rischia identity spoofing;
- rende piu difficile esprimere errori HTTP e audit;
- crea due command path differenti per la stessa operazione.

Nel core TPSI5 il client socket **non esegue mutazioni di dominio**.

Le mutazioni passano dalla API gia protetta.

---

## 8. Autenticare il handshake realtime

La SPA usa gia una sessione server-side:

```text
browser cookie HttpOnly
      ↓
SHA-256(token)
      ↓
sessions table
      ↓
user
```

La connessione Socket.IO same-origin invia l'header Cookie durante il handshake.

Il server puo riusare lo stesso modello:

```text
socket.request.headers.cookie
      ↓
readCookie(cookieName)
      ↓
hashSessionToken(token)
      ↓
authStore.findSessionUser(...)
      ↓
socket.data.user
```

Se la sessione non e valida:

```text
handshake -> connect_error(authentication-required)
```

Non creiamo quindi una seconda identita realtime.

---

## 9. Broadcast

Dopo una mutazione autorizzata:

```js
io.emit("post:created", created);
```

significa: invia l'evento ai socket connessi nel namespace corrente.

Socket.IO supporta anche room e namespace, ma Feisbuc core non ne ha ancora bisogno.

Principio:

> non introdurre una room solo per poter dire di avere usato una room.

Una futura feature `classroom:<id>` potrebbe invece giustificarla.

---

## 10. Disconnessione: il caso che rompe le demo ingenue

Un client realtime **non e sempre connesso**.

Scenario:

```text
Bob online
Alice crea P1 -> Bob riceve evento

Bob perde rete
Alice crea P2
Alice elimina P1

Bob si riconnette
```

Se Bob assume che la riconnessione significhi "ho ricevuto tutto", il suo state puo essere sbagliato.

La strategia core del corso e intenzionalmente semplice:

```text
socket connect/reconnect
        ↓
GET /api/posts
        ↓
snapshot autorevole
        ↓
replace local state
        ↓
continua ad applicare eventi live
```

Quindi:

```text
REST snapshot = recovery baseline
Socket events  = aggiornamenti fra snapshot
```

Socket.IO offre anche connection state recovery e strategie di delivery piu avanzate: le studieremo come estensione, non come prerequisito della prima app realtime.

---

## 11. Ordering e delivery

Non confondiamo:

- **ordine degli eventi durante una connessione**;
- **consegna degli eventi durante una disconnessione**.

L'applicazione deve sempre progettare il recovery.

Nel nostro caso il recovery e `GET /api/posts`.

Questo produce un modello facile da spiegare:

```text
connect
  ↓
snapshot
  ↓
live events
  ↓
disconnect
  ↓
(non so cosa ho perso)
  ↓
reconnect
  ↓
nuovo snapshot
```

---

## 12. Socket lifecycle nel frontend

Non vogliamo listener duplicati ad ogni mount.

Un adapter realtime deve avere lifecycle esplicito:

```ts
const realtime = createRealtimeClient();

realtime.start({
  onEvent(event) { ... },
  onReconnect() { ... },
});

// quando non serve piu
realtime.stop();
```

Errori frequenti:

```text
socket.on(...) dentro una funzione chiamata piu volte
senza socket.off(...)
```

oppure:

```text
ogni render -> nuovo socket
```

---

## 13. Stato condiviso e Pinia

Il realtime aumenta lo stato condiviso, ma non significa automaticamente che dobbiamo aggiungere Pinia.

Milestone 12 mantiene:

```text
session singleton/composable
FeedView owns posts
realtime adapter aggiorna FeedView
```

Se in seguito piu route indipendenti avranno bisogno dello stesso feed/cache, avremo un requisito concreto per valutare uno store globale.

---

## 14. Debugging realtime

Usare contemporaneamente:

- DevTools Network;
- tab WS/frames quando il browser la espone;
- log di `connect`, `disconnect`, `connect_error`;
- server log con `socket.id` e `socket.data.user.id`;
- due browser/profili separati;
- simulazione offline/online;
- snapshot REST di controllo.

Domande utili:

1. il comando HTTP ha avuto successo?
2. il server ha pubblicato l'evento?
3. il client era connesso?
4. il listener era registrato una sola volta?
5. il reducer ha applicato l'evento?
6. il client deve fare resync?

---

## 15. Errori frequenti

### Trattare Socket.IO come WebSocket puro

Nasconde fallback, protocollo e servizi aggiunti dalla libreria.

### Eseguire tutte le mutazioni via socket

Duplica il backend REST senza un requisito architetturale.

### Fidarsi di `authorId` inviato dal client

Viola il trust model costruito in UDA24.

### Assumere exactly-once

Una riconnessione richiede una strategia di recupero/sincronizzazione.

### Aggiungere listener ad ogni mount senza cleanup

Produce eventi elaborati piu volte.

### Fare optimistic update + applicare ciecamente lo stesso broadcast

Puo duplicare lo stesso post.

### Introdurre Pinia solo perche "le SPA lo usano"

Uno store e una risposta a un problema di ownership/condivisione dello state, non una decorazione tecnologica.

---

## 16. Esercizi A-F

### A — osservazione

Disegnare la timeline HTTP/polling/WebSocket/Socket.IO e identificare handshake, push e reconnect.

### B — modifica controllata

Implementare `applyRealtimeEvent(posts, event)` come funzione pura e idempotente.

### C — scrittura autonoma

Integrare Socket.IO nella milestone 11 mantenendo REST come command path.

### D — debugging

Diagnosticare listener duplicati, auth handshake mancante, evento trusted dal client e resync assente.

### E — mini-progetto

Aggiungere presence online come evento **volatile/non persistente**, motivando perche non deve entrare nella tabella posts.

### F — progetto integrato

Feisbuc realtime multiutente con evidence di due client, disconnect/reconnect e stato finale convergente.

---

## 17. Laboratorio milestone 12

Definition of Done:

- Socket.IO server/client pinned;
- HTTP server esplicito con Express + Socket.IO sullo stesso origin;
- socket handshake autenticato tramite la sessione esistente;
- client anonimo rifiutato;
- POST/PATCH/DELETE restano API REST;
- eventi `post:created`, `post:updated`, `post:deleted` derivano da mutazioni riuscite;
- nessun `authorId` trusted dal socket client;
- reducer client idempotente;
- reconnect esegue snapshot REST;
- nessun Pinia;
- TypeScript strict resta verde;
- due client autenticati convergono sullo stesso feed.

---

## 18. Verifica rapida

1. Qual e la differenza fra HTTP polling e server push?
2. Perche Socket.IO non e sinonimo di WebSocket?
3. Perche Feisbuc conserva REST come command path?
4. Dove viene autenticato il socket?
5. Perche `io.emit()` dopo una mutazione non sostituisce la response HTTP?
6. Che cosa succede a Bob se perde rete mentre Alice modifica il feed?
7. Perche il reconnect deve fare un nuovo snapshot?
8. Perche un reducer idempotente e utile?
9. Che differenza c'e fra navigation guard e socket authentication?
10. Perche Pinia non entra ancora automaticamente?

---

## 19. Sintesi inclusiva

```text
HTTP REST
  = chiedi/esegui un comando e ricevi una risposta

WebSocket
  = canale persistente bidirezionale

Socket.IO
  = comunicazione event-based con WebSocket quando possibile,
    fallback/reconnect/broadcasting e altre funzionalita

Feisbuc milestone 12
  comando: REST
  evento: Socket.IO
  identita: stessa sessione
  recovery: REST snapshot dopo reconnect
```

---

## 20. Fonti e collegamenti

Riferimenti tecnici, non testo da copiare:

- WHATWG WebSockets Standard;
- Socket.IO 4.x documentation e tutorial;
- Socket.IO emitting/listening/broadcasting documentation;
- Socket.IO handling disconnections e connection state recovery;
- Node.js HTTP/ESM documentation;
- precedente modulo `05_HTTP_ASYNC_FETCH_REST.md`;
- `08_AUTH_SESSIONI_SICUREZZA.md`;
- `12_TYPESCRIPT_CONTRATTI_FRONTEND.md`.

Activity correlate:

- `tpsi5-activity-a-websocket-realtime-microscope-001`;
- `tpsi5-activity-b-realtime-event-reducer-001`;
- `tpsi5-activity-c-feisbuc-socketio-realtime-001`;
- `tpsi5-activity-d-debug-realtime-boundaries-001`.
