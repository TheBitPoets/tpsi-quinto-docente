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
  if (!input || typeof input !== "object" || Array.isArray(input)) {
    return { ok: false, error: "body-invalid" };
  }

  const text = typeof input.text === "string" ? input.text.trim() : "";

  if (!text) {
    return { ok: false, error: "text-required" };
  }

  if (text.length > 280) {
    return { ok: false, error: "text-too-long" };
  }

  return {
    ok: true,
    value: { text },
  };
}
