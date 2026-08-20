import { io, type Socket } from "socket.io-client";
import type { Post } from "./domain";
import type { RealtimeEvent } from "./realtime-events";

interface ServerToClientEvents {
  "realtime:ready": (payload: { userId: string }) => void;
  "post:created": (post: Post) => void;
  "post:updated": (post: Post) => void;
  "post:deleted": (payload: { postId: string }) => void;
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

  const onCreated = (post: Post) => handlers?.onEvent({ type: "post:created", post });
  const onUpdated = (post: Post) => handlers?.onEvent({ type: "post:updated", post });
  const onDeleted = (payload: { postId: string }) => handlers?.onEvent({ type: "post:deleted", postId: payload.postId });
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
