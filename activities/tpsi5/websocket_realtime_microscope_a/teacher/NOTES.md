# Teacher notes — Activity A realtime

Punti attesi:

- polling: il client avvia le richieste; molte possono essere vuote; la latenza dipende dall'intervallo;
- WebSocket: handshake HTTP/upgrade e poi canale persistente bidirezionale;
- WebSocket non definisce eventi di dominio, rooms, recovery o strategia di reconnect;
- Socket.IO usa un proprio protocollo event-based, normalmente WebSocket quando disponibile e puo usare long-polling;
- reconnect automatico non equivale a recupero degli eventi persi;
- core TPSI5: al connect/reconnect si esegue `GET /api/posts` e si sostituisce lo snapshot locale;
- command path = REST; event path = Socket.IO; persistence = SQLite.

Misconception da correggere subito:

1. `Socket.IO e WebSocket`;
2. `se si riconnette non ha perso nulla`;
3. `realtime significa eliminare REST`;
4. `il socket client puo dichiarare authorId`.
