import process from "node:process";

export function validateCredentials(input) {
  // TODO: implementa il contratto descritto nel README.
  return { ok: false, email: "", errors: ["TODO"] };
}

const chunks = [];
for await (const chunk of process.stdin) chunks.push(chunk);
const raw = Buffer.concat(chunks).toString("utf8").trim();
const input = raw ? JSON.parse(raw) : null;
console.log(JSON.stringify(validateCredentials(input)));
