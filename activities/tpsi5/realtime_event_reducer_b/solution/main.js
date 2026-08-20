import process from "node:process";

export function applyRealtimeEvent(posts, event) {
  switch (event.type) {
    case "post:created":
      return posts.some((post) => post.id === event.post.id)
        ? [...posts]
        : [event.post, ...posts];
    case "post:updated":
      return posts.map((post) => post.id === event.post.id ? event.post : post);
    case "post:deleted":
      return posts.filter((post) => post.id !== event.postId);
    default:
      throw new Error(`Unsupported realtime event: ${String(event.type)}`);
  }
}

let input = "";
for await (const chunk of process.stdin) input += chunk;
const payload = JSON.parse(input);
console.log(JSON.stringify(applyRealtimeEvent(payload.posts, payload.event)));
