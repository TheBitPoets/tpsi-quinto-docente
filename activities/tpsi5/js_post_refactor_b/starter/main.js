let input = "";

process.stdin.setEncoding("utf8");
process.stdin.on("data", (chunk) => {
  input += chunk;
});
process.stdin.on("end", () => {
  const { posts, targetId } = JSON.parse(input);
  const result = toggleLike(posts, targetId);
  console.log(JSON.stringify(result));
});

function toggleLike(posts, targetId) {
  // TODO: restituisci un nuovo array con map.
  // Soltanto il post con id === targetId deve cambiare.
  // Crea il post aggiornato con object spread.
  // false -> true: likes + 1
  // true -> false: likes - 1, mai sotto 0
  return posts;
}
