import process from "node:process";

export function authorizePostAction(input) {
  // TODO: implementa default deny + ownership.
  return { allowed: false, reason: "TODO" };
}

const chunks = [];
for await (const chunk of process.stdin) chunks.push(chunk);
const raw = Buffer.concat(chunks).toString("utf8").trim();
console.log(JSON.stringify(authorizePostAction(raw ? JSON.parse(raw) : null)));
