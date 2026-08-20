import type { Post } from "./domain";

export type RealtimeEvent =
  | { type: "post:created"; post: Post }
  | { type: "post:updated"; post: Post }
  | { type: "post:deleted"; postId: string };

function isRecord(value: unknown): value is Record<string, unknown> {
  return typeof value === "object" && value !== null;
}

function parsePost(value: unknown): Post {
  if (!isRecord(value)
    || typeof value.id !== "string"
    || typeof value.authorId !== "string"
    || typeof value.author !== "string"
    || typeof value.text !== "string"
    || typeof value.liked !== "boolean"
    || typeof value.likes !== "number") {
    throw new Error("Invalid realtime post payload");
  }
  return {
    id: value.id,
    authorId: value.authorId,
    author: value.author,
    text: value.text,
    liked: value.liked,
    likes: value.likes,
  };
}

export function parseRealtimeEvent(
  type: RealtimeEvent["type"],
  payload: unknown,
): RealtimeEvent {
  switch (type) {
    case "post:created":
      return { type, post: parsePost(payload) };
    case "post:updated":
      return { type, post: parsePost(payload) };
    case "post:deleted":
      if (!isRecord(payload) || typeof payload.postId !== "string") {
        throw new Error("Invalid realtime delete payload");
      }
      return { type, postId: payload.postId };
  }
}

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
