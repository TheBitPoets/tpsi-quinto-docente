let input = "";
process.stdin.setEncoding("utf8");
process.stdin.on("data", (chunk) => input += chunk);
process.stdin.on("end", async () => {
  const meta = JSON.parse(input);
  const result = await analyzeResponse(meta);
  process.stdout.write(JSON.stringify(result));
});

const analyzeResponse = async (meta) => {
  // TODO: usa await almeno una volta per rendere esplicito il confine asincrono.
  // Restituisci:
  // {
  //   ok: boolean,
  //   statusClass: "2xx" | "4xx" | ...,
  //   isJson: boolean,
  //   outcome: "accept" | "http-error"
  // }
  return meta;
};
