import { createServer } from "node:http";
import { readFile } from "node:fs/promises";

let posts = [{ id: "p1", text: "Debug HTTP" }];

const sendJson = (response, status, payload) => {
  const body = JSON.stringify(payload);
  response.writeHead(status, {
    "Content-Type": "application/json; charset=utf-8",
    "Content-Length": Buffer.byteLength(body)
  });
  response.end(body);
};

const readBody = async (request) => {
  const chunks = [];
  for await (const chunk of request) chunks.push(chunk);
  return Buffer.concat(chunks).toString("utf8");
};

const serveFile = async (response, name, type) => {
  try {
    const body = await readFile(new URL(`./${name}`, import.meta.url));
    response.writeHead(200, { "Content-Type": type, "Content-Length": body.length });
    response.end(body);
  } catch {
    response.writeHead(404);
    response.end();
  }
};

const server = createServer(async (request, response) => {
  const url = new URL(request.url ?? "/", `http://${request.headers.host ?? "localhost"}`);

  if (request.method === "GET" && url.pathname === "/") {
    await serveFile(response, "index.html", "text/html; charset=utf-8");
    return;
  }

  if (request.method === "GET" && url.pathname === "/client.js") {
    await serveFile(response, "client.js", "text/javascript; charset=utf-8");
    return;
  }

  if (request.method === "GET" && url.pathname === "/api/posts") {
    sendJson(response, 200, posts);
    return;
  }

  if (request.method === "GET" && url.pathname === "/api/posts/missing") {
    sendJson(response, 404, { error: "post-not-found", message: "Post non trovato" });
    return;
  }

  if (request.method === "GET" && url.pathname === "/api/no-content") {
    response.writeHead(204);
    response.end();
    return;
  }

  if (request.method === "POST" && url.pathname === "/api/posts") {
    const contentType = request.headers["content-type"] ?? "";
    if (!contentType.toLowerCase().startsWith("application/json")) {
      sendJson(response, 415, { error: "unsupported-media-type", message: "Atteso application/json" });
      return;
    }

    try {
      const payload = JSON.parse(await readBody(request));
      const post = { id: `p${posts.length + 1}`, text: String(payload.text ?? "") };
      posts = [...posts, post];
      sendJson(response, 201, post);
    } catch {
      sendJson(response, 400, { error: "invalid-json", message: "Body JSON non valido" });
    }
    return;
  }

  sendJson(response, 404, { error: "not-found", message: "Route non trovata" });
});

const port = Number(process.env.PORT ?? 3000);
server.listen(port, "127.0.0.1", () => {
  const address = server.address();
  const actualPort = typeof address === "object" && address ? address.port : port;
  console.log(`READY http://127.0.0.1:${actualPort}`);
});
