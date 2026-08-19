import process from "node:process";

export function buildFeedViewModel(input) {
  const user = input?.user ?? null;
  const posts = Array.isArray(input?.posts) ? input.posts : [];
  return {
    user,
    posts: posts.map((post) => ({
      ...post,
      canDelete: Boolean(user && post.authorId === user.id),
      likedLabel: post.liked ? "Non mi piace piu" : "Mi piace",
    })),
  };
}

const chunks = [];
for await (const chunk of process.stdin) chunks.push(chunk);
const raw = Buffer.concat(chunks).toString("utf8").trim();
const input = raw ? JSON.parse(raw) : { user: null, posts: [] };
console.log(JSON.stringify(buildFeedViewModel(input)));
