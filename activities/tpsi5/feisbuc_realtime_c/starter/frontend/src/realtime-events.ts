import type { Post } from "./domain";

export type RealtimeEvent =
  | { type: "post:created"; post: Post }
  | { type: "post:updated"; post: Post }
  | { type: "post:deleted"; postId: string };

export function applyRealtimeEvent(posts: Post[], event: RealtimeEvent): Post[] {
  // TODO: implementa created/update/delete senza mutare posts.
  // Ricorda che post:created deve essere idempotente per post.id.
  void event;
  return [...posts];
}
