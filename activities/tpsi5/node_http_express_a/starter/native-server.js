import { createServer } from "node:http";

const port = Number(process.env.PORT ?? 3000);

function sendJson(res, status, payload) {
  const body = JSON.stringify(payload);
  res.writeHead(status, {
    "Content-Type": "application/json; charset=utf-8",
    "Content-Length": Buffer.byteLength(body),
  });
  res.end(body);
}

async function readJson(req) {
  const contentType = String(req.headers["content-type"] ?? "").toLowerCase();
  if (!contentType.startsWith("application/json")) {
    const error = new Error("unsupported-media-type");
    error.status = 415;
    throw error;
  }

  let body = "";
  for await (const chunk of req) {
    body += chunk;
    if (body.length > 32 * 1024) {
      const error = new Error("payload-too-large");
      error.status = 413;
      throw error;
    }
  }

  try {
    return JSON.parse(body || "{}");
  } catch {
    const error = new Error("invalid-json");
    error.status = 400;
    throw error;
  }
}

const server = createServer(async (req, res) => {
  try {
    if (req.method === "GET" && req.url === "/api/health") {
      sendJson(res, 200, { ok: true, server: "node-http" });
      return;
    }

    if (req.method === "POST" && req.url === "/api/echo") {
      const payload = await readJson(req);
      sendJson(res, 200, { received: payload });
      return;
    }

    sendJson(res, 404, { error: "not-found" });
  } catch (error) {
    sendJson(res, Number(error.status ?? 500), {
      error: error.message ?? "internal-error",
    });
  }
});

server.listen(port, "127.0.0.1", () => {
  const address = server.address();
  console.log(`READY http://127.0.0.1:${address.port}`);
});
