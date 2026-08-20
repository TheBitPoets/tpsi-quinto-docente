// Activity A — non e un client completo: e una traccia da leggere con DevTools e dispensa.

console.log("1. HTTP polling: il client decide quando chiedere novita");
console.log("2. WebSocket: handshake HTTP, poi canale persistente bidirezionale");
console.log("3. Socket.IO: eventi applicativi + reconnect/fallback sopra un proprio protocollo");
console.log("4. Reconnect != recovery: dopo una disconnessione serve una strategia di resync");

// Browser WebSocket API, esempio concettuale:
// const ws = new WebSocket("wss://example.test/realtime");
// ws.addEventListener("message", (event) => console.log(event.data));
// ws.send("hello");

// Socket.IO, esempio concettuale:
// const socket = io();
// socket.on("post:created", (post) => console.log(post));
// socket.on("connect", () => console.log("connected", socket.id));
// socket.on("disconnect", (reason) => console.log("disconnected", reason));
