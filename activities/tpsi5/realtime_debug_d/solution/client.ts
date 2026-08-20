import { io } from "socket.io-client";
import type { Post } from "./domain";

const socket = io({ autoConnect: false });
let posts: Post[] = [];
let started = false;
let connectedOnce = false;

function applyCreated(post: Post): void {
  if (!posts.some((current) => current.id === post.id)) {
    posts = [post, ...posts];
  }
}

const onCreated = (post: Post) => applyCreated(post);
const onConnect = async () => {
  if (connectedOnce) {
    // Recovery: lo snapshot REST corregge cio che puo essere stato perso offline.
    const response = await fetch("/api/posts", { credentials: "same-origin" });
    if (response.ok) posts = await response.json() as Post[];
  } else {
    connectedOnce = true;
  }
};

export function startFeedRealtime(): void {
  if (started) return;
  started = true;
  socket.on("post:created", onCreated);
  socket.on("connect", onConnect);
  socket.connect();
}

export function stopFeedRealtime(): void {
  if (!started) return;
  socket.off("post:created", onCreated);
  socket.off("connect", onConnect);
  socket.disconnect();
  connectedOnce = false;
  started = false;
}

export async function createPost(text: string): Promise<Post> {
  const response = await fetch("/api/posts", {
    method: "POST",
    credentials: "same-origin",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ text }),
  });
  if (!response.ok) throw new Error(`HTTP ${response.status}`);
  const created = await response.json() as Post;
  applyCreated(created);
  return created;
}
