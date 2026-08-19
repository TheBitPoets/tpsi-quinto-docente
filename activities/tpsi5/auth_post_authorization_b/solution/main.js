import process from "node:process";

export function authorizePostAction(input) {
  const user = input?.user;
  const post = input?.post;
  const action = input?.action;

  if (!user || typeof user.id !== "string" || !user.id) {
    return { allowed: false, reason: "authentication-required" };
  }

  if (["read", "like", "create"].includes(action)) {
    return { allowed: true, reason: "allowed" };
  }

  if (["edit", "delete"].includes(action)) {
    const owned = post && typeof post.authorId === "string" && post.authorId === user.id;
    return owned
      ? { allowed: true, reason: "allowed" }
      : { allowed: false, reason: "ownership-required" };
  }

  return { allowed: false, reason: "action-unknown" };
}

const chunks = [];
for await (const chunk of process.stdin) chunks.push(chunk);
const raw = Buffer.concat(chunks).toString("utf8").trim();
console.log(JSON.stringify(authorizePostAction(raw ? JSON.parse(raw) : null)));
