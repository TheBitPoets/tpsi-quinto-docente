import process from "node:process";

const EMAIL_RE = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

export function validateCredentials(input) {
  if (!input || typeof input !== "object" || Array.isArray(input)) {
    return { ok: false, email: "", errors: ["body-invalid"] };
  }

  const email = typeof input.email === "string"
    ? input.email.trim().toLowerCase()
    : "";
  const password = typeof input.password === "string" ? input.password : "";
  const errors = [];

  if (!EMAIL_RE.test(email)) errors.push("email-invalid");

  const passwordLength = Array.from(password).length;
  if (passwordLength < 15) errors.push("password-too-short");
  if (passwordLength > 128) errors.push("password-too-long");

  return { ok: errors.length === 0, email, errors };
}

const chunks = [];
for await (const chunk of process.stdin) chunks.push(chunk);
const raw = Buffer.concat(chunks).toString("utf8").trim();
const input = raw ? JSON.parse(raw) : null;
console.log(JSON.stringify(validateCredentials(input)));
