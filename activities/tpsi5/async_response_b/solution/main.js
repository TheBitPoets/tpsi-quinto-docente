let input = "";
process.stdin.setEncoding("utf8");
process.stdin.on("data", (chunk) => input += chunk);
process.stdin.on("end", () => {
  const meta = JSON.parse(input);
  const result = analyzeResponse(meta);
  process.stdout.write(JSON.stringify(result));
});

const analyzeResponse = (meta) => {
  const normalized = {
    status: Number(meta.status),
    contentType: String(meta.contentType ?? "")
  };

  const statusClass = `${Math.trunc(normalized.status / 100)}xx`;
  const ok = normalized.status >= 200 && normalized.status <= 299;
  const mediaType = normalized.contentType.split(";", 1)[0].trim().toLowerCase();
  const isJson = mediaType === "application/json" || mediaType.endsWith("+json");

  return {
    ok,
    statusClass,
    isJson,
    outcome: ok ? "accept" : "http-error"
  };
};
