import type { Post } from "./domain";

export type RealtimeEvent =
  | { type: "post:created"; post: Post }
  | { type: "post:updated"; post: Post }
  | { type: "post:deleted"; postId: string };

export function parseRealtimeEvent(
  type: RealtimeEvent["type"],
  payload: unknown,
): RealtimeEvent {
  // TODO: il dato arriva dalla rete, quindi NON usare `as Post`.
  // Valida a runtime shape e tipi prima di costruire RealtimeEvent.
  void type;
  void payload;
  throw new Error("TODO parse realtime payload");
}

export function applyRealtimeEvent(posts: Post[], event: RealtimeEvent): Post[] {
  // TODO: implementa created/update/delete senza mutare posts.
  // Ricorda che post:created deve essere idempotente per post.id.
  void event;
  return [...posts];
}
