import process from "node:process";

export function applyRealtimeEvent(posts, event) {
  // TODO: restituisci sempre un nuovo array coerente con event.type.
  // post:created deve essere idempotente per post.id.
  return posts;
}

let input = "";
for await (const chunk of process.stdin) input += chunk;
const payload = JSON.parse(input);
console.log(JSON.stringify(applyRealtimeEvent(payload.posts, payload.event)));
