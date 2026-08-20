import { io, type Socket } from "socket.io-client";
import {
  parseRealtimeEvent,
  type RealtimeEvent,
} from "./realtime-events";

interface ServerToClientEvents {
  "realtime:ready": (payload: unknown) => void;
  "post:created": (payload: unknown) => void;
  "post:updated": (payload: unknown) => void;
  "post:deleted": (payload: unknown) => void;
}

interface ClientToServerEvents {}

export interface RealtimeHandlers {
  onEvent(event: RealtimeEvent): void;
  onConnect(): void;
  onReconnect(): void;
  onDisconnect(reason: string): void;
  onError(message: string): void;
}

export function createRealtimeClient() {
  const socket: Socket<ServerToClientEvents, ClientToServerEvents> = io({ autoConnect: false });

  return {
    start(handlers: RealtimeHandlers): void {
      // TODO:
      // - registra listener post:created/post:updated/post:deleted;
      // - ogni payload remoto entra come unknown e passa da parseRealtimeEvent;
      // - distingui primo connect da reconnect;
      // - propaga disconnect/connect_error;
      // - poi socket.connect().
      void parseRealtimeEvent;
      void handlers;
      socket.connect();
    },

    stop(): void {
      // TODO: rimuovi i listener registrati da start prima di disconnettere.
      socket.disconnect();
    },
  };
}
