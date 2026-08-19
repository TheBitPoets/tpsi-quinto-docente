let raw = "";
process.stdin.setEncoding("utf8");
process.stdin.on("data", (chunk) => {
  raw += chunk;
});
process.stdin.on("end", () => {
  const input = JSON.parse(raw || "null");
  console.log(JSON.stringify(validateNewPost(input)));
});

function validateNewPost(input) {
  // TODO: completa la validation senza conoscere Express o HTTP.
  return { ok: false, error: "todo" };
}
