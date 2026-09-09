import { Server } from "socket.io";
import { hashSessionToken, readCookie } from "./session.js";

export function attachRealtime({ httpServer, authStore, config, postEvents }) {
  const io = new Server(httpServer, { serveClient: false });

  // TODO 1: io.use(...) deve leggere il cookie HttpOnly dal handshake,
  // hashare il token e caricare la sessione da authStore.
  // Non usare userId dichiarati dal client.
  void readCookie;
  void hashSessionToken;
  void authStore;
  void config;

  // TODO 2: su connection salva/usa socket.data.user e gestisci expiry.

  // TODO 3: subscribe(postEvents) e inoltra created/updated/deleted
  // soltanto a sessioni ancora valide.
  void postEvents;

  return {
    io,
    close(callback) {
      io.close(callback);
    },
  };
}
