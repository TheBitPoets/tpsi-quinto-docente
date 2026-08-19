let input = "";
process.stdin.setEncoding("utf8");
process.stdin.on("data", (chunk) => input += chunk);
process.stdin.on("end", async () => {
  const meta = JSON.parse(input);
  const result = await analyzeResponse(meta);
  process.stdout.write(JSON.stringify(result));
});

const analyzeResponse = async (meta) => {
  const normalized = await Promise.resolve({
    status: Number(meta.status),
    contentType: String(meta.contentType ?? "")
  });

  const statusClass = `${Math.trunc(normalized.status / 100)}xx`;
  const ok = normalized.status >= 200 && normalized.status <= 299;
  const isJson = normalized.contentType.toLowerCase().includes("application/json");

  return {
    ok,
    statusClass,
    isJson,
    outcome: ok ? "accept" : "http-error"
  };
};
