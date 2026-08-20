import type { Post } from "./domain";

export type RealtimeEvent =
  | { type: "post:created"; post: Post }
  | { type: "post:updated"; post: Post }
  | { type: "post:deleted"; postId: string };

export function applyRealtimeEvent(posts: Post[], event: RealtimeEvent): Post[] {
  switch (event.type) {
    case "post:created":
      return posts.some((post) => post.id === event.post.id)
        ? [...posts]
        : [event.post, ...posts];
    case "post:updated":
      return posts.map((post) => post.id === event.post.id ? event.post : post);
    case "post:deleted":
      return posts.filter((post) => post.id !== event.postId);
  }
}
