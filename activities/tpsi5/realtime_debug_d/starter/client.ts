import { io } from "socket.io-client";
import type { Post } from "./domain";

const socket = io();
const posts: Post[] = [];

export function mountFeed(): void {
  // BUG: ogni mount aggiunge un nuovo listener, senza cleanup.
  socket.on("post:created", (post: Post) => {
    // BUG: duplicate event = duplicate row locale.
    posts.unshift(post);
  });

  socket.on("connect", () => {
    // BUG DELIVERY: reconnect trattato come se non fosse successo nulla.
    console.log("connected", socket.id);
  });
}

export function createPost(text: string, authorId: string): void {
  // BUG: command di dominio via socket + identity client-trusted.
  socket.emit("post:create", { text, authorId });
}
