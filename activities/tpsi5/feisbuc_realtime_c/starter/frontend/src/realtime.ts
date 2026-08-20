import { io } from "socket.io-client";
import type { RealtimeEvent } from "./realtime-events";

export interface RealtimeHandlers {
  onEvent(event: RealtimeEvent): void;
  onConnect(): void;
  onReconnect(): void;
  onDisconnect(reason: string): void;
  onError(message: string): void;
}

export function createRealtimeClient() {
  const socket = io({ autoConnect: false });

  return {
    start(handlers: RealtimeHandlers): void {
      // TODO:
      // - registra listener post:created/post:updated/post:deleted;
      // - distingui primo connect da reconnect;
      // - propaga disconnect/connect_error;
      // - poi socket.connect().
      void handlers;
      socket.connect();
    },

    stop(): void {
      // TODO: rimuovi i listener registrati da start prima di disconnettere.
      socket.disconnect();
    },
  };
}
