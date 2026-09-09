let input = "";
process.stdin.setEncoding("utf8");
process.stdin.on("data", (chunk) => input += chunk);
process.stdin.on("end", () => {
  const meta = JSON.parse(input);
  const result = analyzeResponse(meta);
  process.stdout.write(JSON.stringify(result));
});

const analyzeResponse = (meta) => {
  // Restituisci:
  // {
  //   ok: boolean,
  //   statusClass: "2xx" | "4xx" | ...,
  //   isJson: boolean,
  //   outcome: "accept" | "http-error"
  // }
  return meta;
};
