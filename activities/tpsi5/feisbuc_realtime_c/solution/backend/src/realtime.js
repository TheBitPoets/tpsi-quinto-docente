import { Server } from "socket.io";
import { hashSessionToken, readCookie } from "./session.js";

function emitDomainEvent(socket, event) {
  switch (event.type) {
    case "post:created":
      socket.emit("post:created", event.post);
      return;
    case "post:updated":
      socket.emit("post:updated", event.post);
      return;
    case "post:deleted":
      socket.emit("post:deleted", { postId: event.postId });
      return;
    default:
      throw new Error(`Unsupported post event: ${String(event.type)}`);
  }
}

export function attachRealtime({ httpServer, authStore, config, postEvents }) {
  const io = new Server(httpServer, {
    serveClient: false,
  });

  io.use((socket, next) => {
    const token = readCookie(socket.request.headers.cookie, config.cookieName);
    if (!token) {
      next(new Error("authentication-required"));
      return;
    }

    const sessionHash = hashSessionToken(token);
    const session = authStore.findSessionUser(sessionHash, Date.now());
    if (!session) {
      next(new Error("authentication-required"));
      return;
    }

    socket.data.user = session.user;
    socket.data.sessionHash = sessionHash;
    socket.data.sessionExpiresAt = session.expiresAt;
    next();
  });

  io.on("connection", (socket) => {
    const remaining = Math.max(0, socket.data.sessionExpiresAt - Date.now());
    const expiryTimer = setTimeout(() => socket.disconnect(true), remaining);
    socket.on("disconnect", () => clearTimeout(expiryTimer));
    socket.emit("realtime:ready", { userId: socket.data.user.id });
  });

  const unsubscribe = postEvents.subscribe((event) => {
    const now = Date.now();
    for (const socket of io.sockets.sockets.values()) {
      const session = authStore.findSessionUser(socket.data.sessionHash, now);
      if (!session) {
        socket.disconnect(true);
        continue;
      }
      emitDomainEvent(socket, event);
    }
  });

  return {
    io,
    close(callback) {
      unsubscribe();
      io.close(callback);
    },
  };
}
