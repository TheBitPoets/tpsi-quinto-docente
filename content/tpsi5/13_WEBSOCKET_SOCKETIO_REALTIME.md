# WebSocket e Socket.IO: dal request/response al realtime

<table align="center" width="100%"><tr><td>
<details>
<summary>&#128506; <strong>Orientamento della lezione</strong></summary>

<p align="justify"><strong>Contesto:</strong> REST aggiorna correttamente il server, ma gli altri browser non conoscono la mutazione finché non eseguono una nuova richiesta. Il realtime aggiunge un event path senza eliminare il command path HTTP.</p>
<p align="justify"><strong>Domande guida:</strong> che cosa aggiunge WebSocket al modello di comunicazione? Che cosa aggiunge Socket.IO a WebSocket? Come recupera lo stato un client che ha perso eventi?</p>
<p align="justify"><strong>Obiettivi osservabili:</strong> separare protocollo e libreria, progettare eventi piccoli, autenticare il handshake, aggiornare lo stato con un reducer idempotente e usare uno snapshot REST dopo reconnect.</p>
<p align="justify"><strong>Prossimo passo:</strong> la lezione 14 tradurrà gli stessi concetti di componenti e stato da Vue a React per distinguere il modello dalla sintassi.</p>

</details>
</td></tr></table>

<p align="justify">Stato didattico: <strong>draft</strong>.</p>

## Obiettivi

<p align="justify">Al termine del modulo lo studente sa:</p>

<ul>
  <li>distinguere polling, HTTP request/response, Server-Sent Events, WebSocket e Socket.IO a livello concettuale;</li>
  <li>spiegare perche WebSocket crea un canale bidirezionale persistente ma non definisce da solo eventi applicativi, riconnessione, rooms o recovery;</li>
  <li>spiegare perche Socket.IO <strong>non e semplicemente WebSocket</strong>: normalmente usa WebSocket quando disponibile, puo usare HTTP long-polling e aggiunge semantica event-based, riconnessione e broadcasting;</li>
  <li>progettare eventi applicativi piccoli e versionabili;</li>
  <li>mantenere separati <strong>command path</strong> e <strong>event path</strong>;</li>
  <li>autenticare una connessione realtime usando la stessa sessione server-side gia verificata dal backend;</li>
  <li>evitare di fidarsi di identita o mutazioni dichiarate dal client realtime;</li>
  <li>gestire disconnessione e riconnessione senza assumere consegna perfetta degli eventi;</li>
  <li>integrare Socket.IO in Feisbuc senza cambiare il contratto REST, l'authorization o SQLite.</li>
</ul>

## Prerequisiti

<ul>
  <li>UDA23: HTTP, status, fetch e REST;</li>
  <li>UDA24: Express, SQLite, sessioni HttpOnly e authorization;</li>
  <li>UDA25: Vue 3, Vue Router e TypeScript boundary typing;</li>
  <li>modello <code>state -&gt; render</code> e idea di source of truth.</li>
</ul>

## Orientamento nella documentazione

<p align="center">
  <img src="../../assets/tpsi5/lesson-documentation-depth.svg" alt="La dispensa seleziona nelle fonti ufficiali i contenuti da studiare ora, riconoscere, rimandare o dichiarare fuori confine">
</p>

<table align="center"><tr><td>
<p align="justify"><strong><span style="font-size: 1.15em;">&#128279;</span> MDN e Socket.IO:</strong> usa la <a href="GUIDA_USO_MDN.md#mdn-guide-source-choice">guida alla scelta delle fonti</a>. MDN documenta il protocollo e l'API WebSocket disponibile nel browser; la documentazione Socket.IO definisce eventi, riconnessione, transport fallback, rooms e API della libreria.</p>
<ul>
  <li><strong>Studia:</strong> la panoramica della <a href="https://developer.mozilla.org/en-US/docs/Web/API/WebSockets_API">WebSocket API</a> e la reference di <a href="https://developer.mozilla.org/en-US/docs/Web/API/WebSocket"><code>WebSocket</code></a>;</li>
  <li><strong>riconosci:</strong> apertura, messaggi, errori e chiusura nell'esempio <a href="https://developer.mozilla.org/en-US/docs/Web/API/WebSockets_API/Writing_WebSocket_client_applications">Writing WebSocket client applications</a>;</li>
  <li><strong>confronta:</strong> ciò che appartiene allo standard WebSocket con ciò che Socket.IO aggiunge come libreria applicativa.</li>
</ul>
<p align="justify"><strong>Prodotto atteso:</strong> costruisci una tabella a due colonne “WebSocket” e “Socket.IO” e assegna ogni caratteristica al livello corretto.</p>
</td></tr></table>

<table align="center"><tr><td>
<details>
<summary>&#128279; <strong>Indice incrociato — WebSocket, Socket.IO e recovery</strong></summary>

<table align="center">
<thead><tr><th>Dispensa</th><th>Documentazione ufficiale</th><th>Profondità</th></tr></thead>
<tbody>
<tr><td><a href="#lesson-realtime-model">Polling, push e canale persistente</a></td><td><a href="https://developer.mozilla.org/en-US/docs/Web/API/WebSockets_API">MDN — WebSocket API</a></td><td>&#128994; studiare il modello</td></tr>
<tr><td><a href="#lesson-realtime-socketio">WebSocket e Socket.IO</a></td><td><a href="https://socket.io/docs/v4/">Socket.IO documentation</a><br><a href="https://socket.io/docs/v4/how-it-works/">How it works</a></td><td>&#128994; distinguere i livelli</td></tr>
<tr><td><a href="#lesson-realtime-events">Eventi, reducer e broadcast</a></td><td><a href="https://socket.io/docs/v4/emitting-events/">Emitting events</a><br><a href="https://socket.io/docs/v4/broadcasting-events/">Broadcasting events</a></td><td>&#128994; studiare ora</td></tr>
<tr><td><a href="#lesson-realtime-recovery">Disconnessione, delivery e recovery</a></td><td><a href="https://socket.io/docs/v4/tutorial/handling-disconnections">Handling disconnections</a><br><a href="https://socket.io/docs/v4/delivery-guarantees/">Delivery guarantees</a></td><td>&#128994; baseline REST; recovery avanzata da riconoscere</td></tr>
<tr><td>Room, namespace e scaling multi-processo</td><td><a href="https://socket.io/docs/v4/rooms/">Socket.IO — Rooms</a></td><td>&#128993; riconoscere, fuori dal core</td></tr>
</tbody>
</table>

</details>
</td></tr></table>

## Problema iniziale

<p align="justify">Feisbuc milestone 11 e corretta ma ogni browser conosce solo cio che ha appena richiesto al server.</p>

<p align="justify">Supponiamo che Alice e Bob abbiano entrambi aperto <code>/vue/feed</code>.</p>

<ol>
  <li>Alice crea un post con <code>POST /api/posts</code>;</li>
  <li>il database contiene subito il nuovo post;</li>
  <li>Alice aggiorna il proprio state con la response <code>201</code>;</li>
  <li>Bob non sa ancora che il post esiste.</li>
</ol>

<p align="justify">Bob potrebbe fare polling:</p>

```text
ogni 2 s -> GET /api/posts
```

<p align="justify">ma molte request non riporterebbero alcuna novita.</p>

<p align="justify">Il requisito nuovo e diverso:</p>

<blockquote>
<p align="justify">quando lo stato condiviso cambia, il server deve poter notificare i client connessi senza aspettare una nuova request applicativa.</p>
</blockquote>

<p align="justify">Questo e il problema del <strong>realtime push</strong>.</p>

---

## 1. HTTP request/response non scompare

<p align="justify">L'introduzione del realtime non rende REST inutile.</p>

<p align="justify">Nel nostro progetto REST continua a essere adatto per i <strong>comandi</strong>:</p>

```text
POST   /api/posts       crea
PATCH  /api/posts/:id   modifica like
DELETE /api/posts/:id   elimina
GET    /api/posts       snapshot corrente
```

<p align="justify">Il realtime aggiunge un secondo flusso:</p>

```text
server -> client
post:created
post:updated
post:deleted
```

<p align="justify">Quindi:</p>

```text
COMMAND PATH
browser -> HTTP -> authorization -> transaction/store -> response

EVENT PATH
                                     stato gia modificato
                                             ↓
server -> realtime event -> altri client -> local state
```

<p align="justify">Regola TPSI5:</p>

<blockquote>
<p align="justify"><strong>un evento realtime annuncia una mutazione gia autorizzata e completata; non sostituisce automaticamente la API dei comandi.</strong></p>
</blockquote>

<p align="justify">Questo evita di duplicare validation, status HTTP e authorization dentro handler socket improvvisati.</p>

---

<a id="lesson-realtime-model"></a>
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

<p align="justify">E semplice e robusto ma puo produrre traffico e latenza inutili.</p>

### WebSocket

<p align="justify">Un WebSocket crea un canale persistente e bidirezionale:</p>

```text
HTTP handshake
      ↓ upgrade
WebSocket aperto
client <----------> server
```

<p align="justify">Dopo l'handshake, entrambi i lati possono inviare messaggi senza aprire una nuova request HTTP applicativa per ogni messaggio.</p>

<p align="justify">Il browser espone l'API <code>WebSocket</code>:</p>

```js
const ws = new WebSocket("wss://example.test/realtime");

ws.addEventListener("message", (event) => {
  console.log(event.data);
});

ws.send("hello");
```

<p align="justify">Ma WebSocket non decide per noi:</p>

<ul>
  <li>come chiamare gli eventi;</li>
  <li>come serializzare il dominio;</li>
  <li>come fare broadcast;</li>
  <li>come raggruppare client;</li>
  <li>come riconnettersi;</li>
  <li>come recuperare eventi persi;</li>
  <li>come rappresentare acknowledgements applicativi.</li>
</ul>

<p align="justify">Queste sono responsabilita del protocollo/applicazione costruita sopra WebSocket.</p>

---

<a id="lesson-realtime-socketio"></a>
## 3. Socket.IO non e un alias di WebSocket

<p align="justify">Socket.IO fornisce un modello ad eventi ispirato a <code>EventEmitter</code>:</p>

```js
socket.on("post:created", (post) => {
  // aggiorna lo state locale
});
```

<p align="justify">Sul server:</p>

```js
io.emit("post:created", post);
```

<p align="justify">In condizioni normali la connessione puo usare WebSocket; Socket.IO puo anche usare HTTP long-polling quando necessario e aggiunge funzionalita come riconnessione automatica e broadcasting.</p>

<p align="justify">Per questo e scorretto insegnare:</p>

```text
Socket.IO = wrapper WebSocket
```

<p align="justify">Meglio:</p>

```text
WebSocket = protocollo/canale bidirezionale
Socket.IO = protocollo + libreria event-based con fallback e servizi applicativi
```

### Baseline riproducibile del corso

<p align="justify">La reference 2026/27 pinna:</p>

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

<a id="lesson-realtime-events"></a>
## 4. Evento applicativo != riga del database

<p align="justify">Un buon evento dice <strong>che cosa e successo nel dominio</strong>.</p>

<p align="justify">Per Feisbuc useremo un contratto piccolo:</p>

```ts
export type RealtimeEvent =
  | { type: "post:created"; post: Post }
  | { type: "post:updated"; post: Post }
  | { type: "post:deleted"; postId: string };
```

<p align="justify">Non inviamo:</p>

```text
SQL statement
row interna con password/session data
req/res Express
oggetto DatabaseSync
```

<p align="justify">L'evento usa lo stesso modello pubblico <code>Post</code> gia esposto dalla API.</p>

---

## 5. Reducer realtime: evento -> nuovo state

<p align="justify">Prima di aprire un socket separiamo la logica pura.</p>

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

<p align="justify">Perche evitare semplicemente:</p>

```ts
posts.value.push(event.post);
```

<p align="justify">Perche una UI realtime deve ragionare anche su:</p>

<ul>
  <li>eventi duplicati;</li>
  <li>update di un elemento esistente;</li>
  <li>delete;</li>
  <li>source of truth;</li>
  <li>riconnessione e snapshot.</li>
</ul>

---

## 6. Command path ed event path

<p align="justify">Quando Alice crea un post:</p>

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

<p align="justify">La REST response resta importante per chi ha eseguito il comando.</p>

<p align="justify">L'evento permette agli altri client di convergere sul nuovo stato.</p>

### Duplicazione apparente

<p align="justify">Alice puo ricevere:</p>

<ol>
  <li>la response HTTP con il post creato;</li>
  <li>l'evento <code>post:created</code> dello stesso post.</li>
</ol>

<p align="justify">Per questo il reducer deve essere idempotente rispetto allo stesso <code>post.id</code>.</p>

---

## 7. Non fidarsi del socket client

<p align="justify">Il modello insicuro sarebbe:</p>

```js
socket.on("post:create", ({ authorId, text }) => {
  // NON FARE
  postStore.create({ authorId, text });
});
```

<p align="justify">Problemi:</p>

<ul>
  <li>duplica la API POST;</li>
  <li>rischia di saltare validation;</li>
  <li>rischia identity spoofing;</li>
  <li>rende piu difficile esprimere errori HTTP e audit;</li>
  <li>crea due command path differenti per la stessa operazione.</li>
</ul>

<p align="justify">Nel core TPSI5 il client socket <strong>non esegue mutazioni di dominio</strong>.</p>

<p align="justify">Le mutazioni passano dalla API gia protetta.</p>

---

## 8. Autenticare il handshake realtime

<p align="justify">La SPA usa gia una sessione server-side:</p>

```text
browser cookie HttpOnly
      ↓
SHA-256(token)
      ↓
sessions table
      ↓
user
```

<p align="justify">La connessione Socket.IO same-origin invia l'header Cookie durante il handshake.</p>

<p align="justify">Il server puo riusare lo stesso modello:</p>

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

<p align="justify">Se la sessione non e valida:</p>

```text
handshake -> connect_error(authentication-required)
```

<p align="justify">Non creiamo quindi una seconda identita realtime.</p>

---

## 9. Broadcast

<p align="justify">Dopo una mutazione autorizzata:</p>

```js
io.emit("post:created", created);
```

<p align="justify">significa: invia l'evento ai socket connessi nel namespace corrente.</p>

<p align="justify">Socket.IO supporta anche room e namespace, ma Feisbuc core non ne ha ancora bisogno.</p>

<p align="justify">Principio:</p>

<blockquote>
<p align="justify">non introdurre una room solo per poter dire di avere usato una room.</p>
</blockquote>

<p align="justify">Una futura feature <code>classroom:&lt;id&gt;</code> potrebbe invece giustificarla.</p>

---

<a id="lesson-realtime-recovery"></a>
## 10. Disconnessione: il caso che rompe le demo ingenue

<p align="justify">Un client realtime <strong>non e sempre connesso</strong>.</p>

<p align="justify">Scenario:</p>

```text
Bob online
Alice crea P1 -> Bob riceve evento

Bob perde rete
Alice crea P2
Alice elimina P1

Bob si riconnette
```

<p align="justify">Se Bob assume che la riconnessione significhi "ho ricevuto tutto", il suo state puo essere sbagliato.</p>

<p align="justify">La strategia core del corso e intenzionalmente semplice:</p>

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

<p align="justify">Quindi:</p>

```text
REST snapshot = recovery baseline
Socket events  = aggiornamenti fra snapshot
```

<p align="justify">Socket.IO offre anche connection state recovery e strategie di delivery piu avanzate: le studieremo come estensione, non come prerequisito della prima app realtime.</p>

---

## 11. Ordering e delivery

<p align="justify">Non confondiamo:</p>

<ul>
  <li><strong>ordine degli eventi durante una connessione</strong>;</li>
  <li><strong>consegna degli eventi durante una disconnessione</strong>.</li>
</ul>

<p align="justify">L'applicazione deve sempre progettare il recovery.</p>

<p align="justify">Nel nostro caso il recovery e <code>GET /api/posts</code>.</p>

<p align="justify">Questo produce un modello facile da spiegare:</p>

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

<p align="justify">Non vogliamo listener duplicati ad ogni mount.</p>

<p align="justify">Un adapter realtime deve avere lifecycle esplicito:</p>

```ts
const realtime = createRealtimeClient();

realtime.start({
  onEvent(event) { ... },
  onReconnect() { ... },
});

// quando non serve piu
realtime.stop();
```

<p align="justify">Errori frequenti:</p>

```text
socket.on(...) dentro una funzione chiamata piu volte
senza socket.off(...)
```

<p align="justify">oppure:</p>

```text
ogni render -> nuovo socket
```

---

## 13. Stato condiviso e Pinia

<p align="justify">Il realtime aumenta lo stato condiviso, ma non significa automaticamente che dobbiamo aggiungere Pinia.</p>

<p align="justify">Milestone 12 mantiene:</p>

```text
session singleton/composable
FeedView owns posts
realtime adapter aggiorna FeedView
```

<p align="justify">Se in seguito piu route indipendenti avranno bisogno dello stesso feed/cache, avremo un requisito concreto per valutare uno store globale.</p>

---

## 14. Debugging realtime

<p align="justify">Usare contemporaneamente:</p>

<ul>
  <li>DevTools Network;</li>
  <li>tab WS/frames quando il browser la espone;</li>
  <li>log di <code>connect</code>, <code>disconnect</code>, <code>connect_error</code>;</li>
  <li>server log con <code>socket.id</code> e <code>socket.data.user.id</code>;</li>
  <li>due browser/profili separati;</li>
  <li>simulazione offline/online;</li>
  <li>snapshot REST di controllo.</li>
</ul>

<p align="justify">Domande utili:</p>

<ol>
  <li>il comando HTTP ha avuto successo?</li>
  <li>il server ha pubblicato l'evento?</li>
  <li>il client era connesso?</li>
  <li>il listener era registrato una sola volta?</li>
  <li>il reducer ha applicato l'evento?</li>
  <li>il client deve fare resync?</li>
</ol>

---

## 15. Errori frequenti

### Trattare Socket.IO come WebSocket puro

<p align="justify">Nasconde fallback, protocollo e servizi aggiunti dalla libreria.</p>

### Eseguire tutte le mutazioni via socket

<p align="justify">Duplica il backend REST senza un requisito architetturale.</p>

### Fidarsi di `authorId` inviato dal client

<p align="justify">Viola il trust model costruito in UDA24.</p>

### Assumere exactly-once

<p align="justify">Una riconnessione richiede una strategia di recupero/sincronizzazione.</p>

### Aggiungere listener ad ogni mount senza cleanup

<p align="justify">Produce eventi elaborati piu volte.</p>

### Fare optimistic update + applicare ciecamente lo stesso broadcast

<p align="justify">Puo duplicare lo stesso post.</p>

### Introdurre Pinia solo perche "le SPA lo usano"

<p align="justify">Uno store e una risposta a un problema di ownership/condivisione dello state, non una decorazione tecnologica.</p>

---

## 16. Esercizi A-F

### A — osservazione

<p align="justify">Disegnare la timeline HTTP/polling/WebSocket/Socket.IO e identificare handshake, push e reconnect.</p>

### B — modifica controllata

<p align="justify">Implementare <code>applyRealtimeEvent(posts, event)</code> come funzione pura e idempotente.</p>

### C — scrittura autonoma

<p align="justify">Integrare Socket.IO nella milestone 11 mantenendo REST come command path.</p>

### D — debugging

<p align="justify">Diagnosticare listener duplicati, auth handshake mancante, evento trusted dal client e resync assente.</p>

### E — mini-progetto

<p align="justify">Aggiungere presence online come evento <strong>volatile/non persistente</strong>, motivando perche non deve entrare nella tabella posts.</p>

### F — progetto integrato

<p align="justify">Feisbuc realtime multiutente con evidence di due client, disconnect/reconnect e stato finale convergente.</p>

---

## 17. Laboratorio milestone 12

<p align="justify">Definition of Done:</p>

<ul>
  <li>Socket.IO server/client pinned;</li>
  <li>HTTP server esplicito con Express + Socket.IO sullo stesso origin;</li>
  <li>socket handshake autenticato tramite la sessione esistente;</li>
  <li>client anonimo rifiutato;</li>
  <li>POST/PATCH/DELETE restano API REST;</li>
  <li>eventi <code>post:created</code>, <code>post:updated</code>, <code>post:deleted</code> derivano da mutazioni riuscite;</li>
  <li>nessun <code>authorId</code> trusted dal socket client;</li>
  <li>reducer client idempotente;</li>
  <li>reconnect esegue snapshot REST;</li>
  <li>nessun Pinia;</li>
  <li>TypeScript strict resta verde;</li>
  <li>due client autenticati convergono sullo stesso feed.</li>
</ul>

---

## 18. Verifica rapida

<ol>
  <li>Qual e la differenza fra HTTP polling e server push?</li>
  <li>Perche Socket.IO non e sinonimo di WebSocket?</li>
  <li>Perche Feisbuc conserva REST come command path?</li>
  <li>Dove viene autenticato il socket?</li>
  <li>Perche <code>io.emit()</code> dopo una mutazione non sostituisce la response HTTP?</li>
  <li>Che cosa succede a Bob se perde rete mentre Alice modifica il feed?</li>
  <li>Perche il reconnect deve fare un nuovo snapshot?</li>
  <li>Perche un reducer idempotente e utile?</li>
  <li>Che differenza c'e fra navigation guard e socket authentication?</li>
  <li>Perche Pinia non entra ancora automaticamente?</li>
</ol>

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

<p align="justify">Riferimenti tecnici, non testo da copiare:</p>

<ul>
  <li>WHATWG WebSockets Standard;</li>
  <li>Socket.IO 4.x documentation e tutorial;</li>
  <li>Socket.IO emitting/listening/broadcasting documentation;</li>
  <li>Socket.IO handling disconnections e connection state recovery;</li>
  <li>Node.js HTTP/ESM documentation;</li>
  <li>precedente modulo <code>05_HTTP_ASYNC_FETCH_REST.md</code>;</li>
  <li><code>08_AUTH_SESSIONI_SICUREZZA.md</code>;</li>
  <li><code>12_TYPESCRIPT_CONTRATTI_FRONTEND.md</code>.</li>
</ul>

<p align="justify">Activity correlate:</p>

<ul>
  <li><code>tpsi5-activity-a-websocket-realtime-microscope-001</code>;</li>
  <li><code>tpsi5-activity-b-realtime-event-reducer-001</code>;</li>
  <li><code>tpsi5-activity-c-feisbuc-socketio-realtime-001</code>;</li>
  <li><code>tpsi5-activity-d-debug-realtime-boundaries-001</code>.</li>
</ul>
