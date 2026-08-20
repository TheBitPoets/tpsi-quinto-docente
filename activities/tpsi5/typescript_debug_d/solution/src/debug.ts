type AuthStatus = "unknown" | "anonymous" | "authenticated";

interface Post {
  id: string;
  text: string;
}

const status: AuthStatus = "unknown";
console.log(status);

const posts: Post[] = [];
const first = posts[0];
if (first) console.log(first.text);

function isRecord(value: unknown): value is Record<string, unknown> {
  return typeof value === "object" && value !== null;
}

function readId(payload: unknown): string {
  if (!isRecord(payload) || typeof payload.id !== "string") {
    throw new Error("Invalid id payload");
  }
  return payload.id;
}

console.log(readId({ id: "p1" }));
