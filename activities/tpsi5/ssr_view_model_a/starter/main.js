import process from "node:process";

export function buildFeedViewModel(input) {
  // TODO: restituisci {user, posts} senza mutare input.
  // Ogni post deve aggiungere canDelete e likedLabel.
  return input;
}

const chunks = [];
for await (const chunk of process.stdin) chunks.push(chunk);
const raw = Buffer.concat(chunks).toString("utf8").trim();
const input = raw ? JSON.parse(raw) : { user: null, posts: [] };
console.log(JSON.stringify(buildFeedViewModel(input)));
