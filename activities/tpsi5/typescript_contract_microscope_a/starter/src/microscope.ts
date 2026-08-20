type AuthStatus = "unknown" | "anonymous" | "authenticated";

interface User {
  id: string;
  displayName: string;
}

interface Post {
  id: string;
  text: string;
  liked: boolean;
}

const title = "Feisbuc";
const count = 3;

// Inference: title e string, count e number.
// @ts-expect-error number non e assegnabile a string
const wrongTitle: string = count;

let status: AuthStatus = "unknown";
status = "authenticated";
// @ts-expect-error stato fuori dalla union
status = "logged";

const user: User | null = null;
// @ts-expect-error user puo essere null
console.log(user.displayName);

function isRecord(value: unknown): value is Record<string, unknown> {
  return typeof value === "object" && value !== null;
}

function isPost(value: unknown): value is Post {
  if (!isRecord(value)) return false;
  return typeof value.id === "string"
    && typeof value.text === "string"
    && typeof value.liked === "boolean";
}

function parsePost(value: unknown): Post {
  if (!isPost(value)) throw new Error("Invalid post payload");
  return value;
}

const networkPayload: unknown = { id: "p1", text: "ciao", liked: false };
const parsed = parsePost(networkPayload);
console.log(title, parsed.id);

// @ts-expect-error unknown deve essere ristretto prima dell'uso
console.log(networkPayload.id);

const posts: Post[] = [parsed];
const first = posts[0];
// noUncheckedIndexedAccess: first e Post | undefined
if (first) console.log(first.text);
