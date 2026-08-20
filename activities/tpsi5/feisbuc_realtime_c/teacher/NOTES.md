# Teacher notes — Feisbuc milestone 12

## Review prioritaria

1. **REST resta command path**: nessun command handler Socket.IO per create/like/delete.
2. Il socket deriva l'identita da `cookie -> session hash -> authStore`, mai dal payload client.
3. Il broadcaster rivalida `sessionHash` prima di ogni evento; sessioni non valide vengono disconnesse.
4. Gli eventi derivano da mutazioni gia completate nel `SqlPostStore`.
5. `post:created` e idempotente nel reducer, perche il client autore riceve sia HTTP response sia broadcast.
6. `onUnmounted -> realtime.stop()` evita listener duplicati.
7. Reconnect esegue snapshot REST: nessuna assunzione exactly-once.
8. Nessun Pinia: il feed ha ancora un owner naturale (`FeedView`).

## Test manuale consigliato

Usare due profili browser separati o normale + incognito.

- Alice crea P1;
- Bob vede P1;
- Bob like P1;
- Alice vede likes=1;
- Alice elimina P1;
- Bob non vede piu P1;
- Bob offline;
- Alice crea P2;
- Bob online;
- snapshot REST riporta P2.

## Anti-pattern da respingere

- `io.on('connection', socket => socket.on('post:create', ...))` come secondo command path;
- `socket.handshake.auth.userId` trusted come identita;
- CORS `*` aggiunto senza requisito;
- `socket.on(...)` dentro callback eseguita piu volte senza `off`;
- optimistic create + broadcast non deduplicato;
- assenza di recovery/resync;
- introdurre Pinia solo perche e entrato Socket.IO.
