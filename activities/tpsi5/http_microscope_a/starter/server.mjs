import { createServer } from "node:http";
import { readFile } from "node:fs/promises";

const initialPosts = [
  { id: "p1", text: "HTTP prima di Express", likes: 1, liked: false },
  { id: "p2", text: "Status e header fanno parte del contratto", likes: 3, liked: true }
];

let posts = structuredClone(initialPosts);
let nextId = 3;

const allowedOrigins = new Set([
  "http://127.0.0.1:5173",
  "http://localhost:5173"
]);

const corsHeaders = (request) => {
  const origin = request.headers.origin;
  return origin && allowedOrigins.has(origin)
    ? { "Access-Control-Allow-Origin": origin, Vary: "Origin" }
    : {};
};

const sendJson = (request, response, status, payload, headers = {}) => {
  const body = JSON.stringify(payload);
  response.writeHead(status, {
    "Content-Type": "application/json; charset=utf-8",
    "Content-Length": Buffer.byteLength(body),
    "Cache-Control": "no-store",
    ...corsHeaders(request),
    ...headers
  });
  response.end(body);
};

const readBody = async (request) => {
  const chunks = [];
  for await (const chunk of request) chunks.push(chunk);
  return Buffer.concat(chunks).toString("utf8");
};

const server = createServer(async (request, response) => {
  const url = new URL(request.url ?? "/", `http://${request.headers.host ?? "localhost"}`);
  const send = (status, payload, headers = {}) => sendJson(request, response, status, payload, headers);

  if (request.method === "GET" && (url.pathname === "/" || url.pathname === "/observer.html")) {
    const body = await readFile(new URL("./observer.html", import.meta.url));
    response.writeHead(200, { "Content-Type": "text/html; charset=utf-8" });
    response.end(body);
    return;
  }

  if (request.method === "GET" && url.pathname === "/observer.mjs") {
    const body = await readFile(new URL("./observer.mjs", import.meta.url));
    response.writeHead(200, { "Content-Type": "text/javascript; charset=utf-8" });
    response.end(body);
    return;
  }

  if (request.method === "OPTIONS" && url.pathname.startsWith("/api/")) {
    const origin = request.headers.origin;
    if (!origin || !allowedOrigins.has(origin)) {
      send(403, { error: "cors-origin-denied", message: "Origin non consentita" });
      return;
    }
    response.writeHead(204, {
      ...corsHeaders(request),
      "Access-Control-Allow-Methods": "GET, POST, PATCH, OPTIONS",
      "Access-Control-Allow-Headers": "Content-Type, Accept",
      "Access-Control-Max-Age": "600"
    });
    response.end();
    return;
  }

  if (request.method === "GET" && url.pathname === "/api/posts") {
    send(200, posts);
    return;
  }

  if (request.method === "GET" && url.pathname === "/api/posts/missing") {
    send(404, {
      error: "post-not-found",
      message: "Il post richiesto non esiste"
    });
    return;
  }

  if (request.method === "POST" && url.pathname === "/api/posts") {
    const contentType = request.headers["content-type"] ?? "";
    if (!contentType.toLowerCase().startsWith("application/json")) {
      send(415, {
        error: "unsupported-media-type",
        message: "Usa Content-Type: application/json"
      });
      return;
    }

    let parsed;
    try {
      parsed = JSON.parse(await readBody(request));
    } catch {
      send(400, {
        error: "invalid-json",
        message: "Il body non contiene JSON valido"
      });
      return;
    }

    const text = String(parsed?.text ?? "").trim();
    if (!text) {
      send(400, {
        error: "invalid-post",
        message: "text è obbligatorio"
      });
      return;
    }

    const post = { id: `p${nextId++}`, text, likes: 0, liked: false };
    posts = [post, ...posts];
    send(201, post, { Location: `/api/posts/${post.id}` });
    return;
  }

  if (request.method === "POST" && url.pathname === "/__reset") {
    posts = structuredClone(initialPosts);
    nextId = 3;
    send(200, { ok: true });
    return;
  }

  if (url.pathname === "/api/posts") {
    send(405, {
      error: "method-not-allowed",
      message: "Metodo non ammesso sulla risorsa richiesta"
    }, { Allow: "GET, POST, OPTIONS" });
    return;
  }

  send(404, {
    error: "route-not-found",
    message: "La risorsa richiesta non esiste"
  });
});

const port = Number(process.env.PORT ?? 3000);
server.listen(port, "127.0.0.1", () => {
  const address = server.address();
  const actualPort = typeof address === "object" && address ? address.port : port;
  console.log(`READY http://127.0.0.1:${actualPort}`);
});
