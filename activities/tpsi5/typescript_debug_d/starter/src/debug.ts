type AuthStatus = "unknown" | "anonymous" | "authenticated";

interface Post {
  id: string;
  text: string;
}

// Bug 1: valore fuori dalla union.
let status: AuthStatus = "logged";
console.log(status);

const posts: Post[] = [];
// Bug 2: con noUncheckedIndexedAccess posts[0] puo essere undefined.
console.log(posts[0].text);

// Bug 3: unknown usato senza narrowing.
function readId(payload: unknown): string {
  return payload.id;
}

console.log(readId({ id: "p1" }));
