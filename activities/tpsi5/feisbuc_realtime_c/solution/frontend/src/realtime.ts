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
  const socket: Socket<ServerToClientEvents, ClientToServerEvents> = io({
    autoConnect: false,
  });
  let handlers: RealtimeHandlers | null = null;
  let connectedOnce = false;

  const dispatch = (type: RealtimeEvent["type"], payload: unknown) => {
    if (!handlers) return;
    try {
      handlers.onEvent(parseRealtimeEvent(type, payload));
    } catch (cause: unknown) {
      handlers.onError(cause instanceof Error ? cause.message : "Invalid realtime payload");
    }
  };
  const onCreated = (payload: unknown) => dispatch("post:created", payload);
  const onUpdated = (payload: unknown) => dispatch("post:updated", payload);
  const onDeleted = (payload: unknown) => dispatch("post:deleted", payload);
  const onConnect = () => {
    if (!handlers) return;
    if (connectedOnce) handlers.onReconnect();
    else {
      connectedOnce = true;
      handlers.onConnect();
    }
  };
  const onDisconnect = (reason: string) => handlers?.onDisconnect(reason);
  const onConnectError = (error: Error) => handlers?.onError(error.message);

  return {
    start(nextHandlers: RealtimeHandlers): void {
      if (handlers) throw new Error("Realtime client already started");
      handlers = nextHandlers;
      socket.on("post:created", onCreated);
      socket.on("post:updated", onUpdated);
      socket.on("post:deleted", onDeleted);
      socket.on("connect", onConnect);
      socket.on("disconnect", onDisconnect);
      socket.on("connect_error", onConnectError);
      socket.connect();
    },

    stop(): void {
      socket.off("post:created", onCreated);
      socket.off("post:updated", onUpdated);
      socket.off("post:deleted", onDeleted);
      socket.off("connect", onConnect);
      socket.off("disconnect", onDisconnect);
      socket.off("connect_error", onConnectError);
      socket.disconnect();
      handlers = null;
      connectedOnce = false;
    },
  };
}
