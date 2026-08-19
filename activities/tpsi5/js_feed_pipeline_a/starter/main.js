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
  // TODO 1: mantieni soltanto i post con published === true.
  // TODO 2: trasforma ogni post in { id, label, popular }.
  // label = "Autore: testo senza spazi iniziali/finali"
  // popular = true se likes >= 5.
  // Non modificare posts e non cambiare il codice stdin/stdout sopra.
  return posts;
}
