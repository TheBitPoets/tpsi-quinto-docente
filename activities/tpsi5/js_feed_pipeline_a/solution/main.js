let input = "";

process.stdin.setEncoding("utf8");
process.stdin.on("data", (chunk) => {
  input += chunk;
});
process.stdin.on("end", () => {
  const posts = JSON.parse(input);
  const result = prepareFeed(posts);
  console.log(JSON.stringify(result));
});

function prepareFeed(posts) {
  return posts
    .filter(({ published }) => published === true)
    .map(({ id, author, text, likes }) => ({
      id,
      label: `${author}: ${text.trim()}`,
      popular: likes >= 5,
    }));
}
