import { Server } from "socket.io";

// La verifica concreta cookie -> session hash -> user resta nel middleware/adapter auth del progetto.
export function installRealtime(httpServer, { verifySocketSession, subscribePostEvents }) {
  const io = new Server(httpServer, { serveClient: false });

  io.use(async (socket, next) => {
    try {
      socket.data.auth = await verifySocketSession(socket.request.headers.cookie);
      next();
    } catch {
      next(new Error("authentication-required"));
    }
  });

  // Nessun socket.on("post:create|update|delete"): i comandi restano REST.
  const unsubscribe = subscribePostEvents((event) => {
    switch (event.type) {
      case "post:created": io.emit("post:created", event.post); break;
      case "post:updated": io.emit("post:updated", event.post); break;
      case "post:deleted": io.emit("post:deleted", { postId: event.postId }); break;
    }
  });

  return {
    close(callback) {
      unsubscribe();
      io.close(callback);
    },
  };
}
