import { Server } from "socket.io";

export function installRealtime(httpServer, postStore) {
  const io = new Server(httpServer, { cors: { origin: "*" } });

  // BUG: nessuna autenticazione del handshake.
  io.on("connection", (socket) => {
    // BUG ARCHITETTURA + SECURITY: secondo command path che salta la REST API.
    socket.on("post:create", (payload) => {
      const created = postStore.create({
        text: payload.text,
        authorId: payload.authorId, // BUG: identity spoofing.
      });
      io.emit("post:created", created);
    });
  });

  return io;
}
