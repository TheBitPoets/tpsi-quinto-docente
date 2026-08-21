---
marp: true
paginate: true
size: 16:9
title: 13 — WebSocket e Socket.IO realtime
---

# 13 — WebSocket e Socket.IO
## Dal request/response al realtime

UDA 25 — Frontend application

---

# Richiamo

Con HTTP il client chiede e il server risponde.

```text
client -> request -> server
client <- response <- server
```

Ma come fa il server a dire a un client:

> “È appena arrivato un nuovo post”

senza aspettare una nuova request?

---

# Obiettivi

Alla fine dovrai saper:

- distinguere HTTP request/response e canale persistente;
- spiegare il ruolo di Socket.IO;
- separare command path ed event path;
- gestire payload remoti con validation;
- capire reconnect e recovery;
- usare un resync REST autorevole.

---

# Canale persistente

```text
client <================> server
        connessione viva
```

Il server può inviare eventi quando lo stato cambia.

---

# WebSocket vs Socket.IO

WebSocket è un protocollo/API di base.

Socket.IO aggiunge convenzioni e funzionalità come:

- eventi nominati;
- reconnect;
- rooms;
- ack;
- fallback/gestione trasporto.

Nel corso usiamo Socket.IO per osservare questi pattern.

---

# Command path

Le mutazioni restano esplicite via REST:

```text
POST /posts
DELETE /posts/:id
```

Perché?

- status HTTP chiari;
- validation già definita;
- authz già definita;
- contratti testabili.

---

# Event path

Dopo una mutazione riuscita:

```text
server -> event post:created -> clients
```

L'evento dice:

> “Lo stato autorevole è cambiato.”

Non sostituisce necessariamente il command path.

---

# Payload remoto = input esterno

```ts
socket.on('post:created', (payload: unknown) => {
  const post = parsePost(payload);
  applyPostCreated(post);
});
```

Anche un evento realtime attraversa un trust boundary.

---

# Reducer idempotente

Se lo stesso evento arriva due volte, non vogliamo duplicare il post.

```ts
function upsertPost(posts, incoming) {
  const existing = posts.findIndex(p => p.id === incoming.id);
  if (existing >= 0) posts[existing] = incoming;
  else posts.unshift(incoming);
}
```

---

# Reconnect

Durante una disconnessione potresti perdere eventi.

Quindi dopo reconnect:

```text
socket reconnect
→ GET /posts
→ snapshot autorevole
→ sostituisci/riallinea stato
```

Il realtime accelera gli aggiornamenti; REST può ricostruire la verità.

---

# Errore tipico: tutto via socket

Se usiamo Socket.IO anche per ogni command senza motivo, perdiamo una parte della chiarezza già costruita con HTTP.

Nel nostro modello:

```text
REST = command / authoritative fetch
Socket.IO = notification / event distribution
```

---

# Due client

Scenario di prova:

1. client A pubblica un post via REST;
2. server salva;
3. server emette `post:created`;
4. client B riceve;
5. client B aggiorna il feed senza refresh.

Questa è un'evidenza reale del realtime.

---

# Checkpoint

Quale canale useresti?

1. creare un post;
2. notificare agli altri client che il post esiste;
3. ricostruire lo stato dopo 30 secondi offline;
4. cancellare un post con ownership;
5. segnalare che un post è stato cancellato.

---

# Feisbuc milestone

Feisbuc diventa multiutente realtime:

```text
REST command
→ backend + DB
→ Socket.IO event
→ altri client
```

Con recovery:

```text
reconnect -> REST snapshot
```

---

# Handoff al laboratorio

1. osserva connessione/eventi;
2. prova due client;
3. valida payload;
4. gestisci evento duplicato;
5. simula disconnessione e resync.

---

# Recap

Realtime robusto significa:

- command path chiaro;
- eventi validati;
- reducer idempotente;
- reconnect previsto;
- snapshot autorevole disponibile.

Prossimo modulo: **React translation/comparison lab**.