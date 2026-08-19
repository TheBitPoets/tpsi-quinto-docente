import { createServer } from "node:http";
import { readFile } from "node:fs/promises";
import { extname, join } from "node:path";
import { fileURLToPath } from "node:url";

const root = fileURLToPath(new URL("./", import.meta.url));
const initialPosts = [
  { id: "p1", author: "Ada", text: "Ora il feed arriva via HTTP.", likes: 2, liked: false },
  { id: "p2", author: "Linus", text: "Il client controlla status e Content-Type.", likes: 4, liked: true }
];

let posts = structuredClone(initialPosts);
let nextId = 3;

const mime = {
  ".html": "text/html; charset=utf-8",
  ".js": "text/javascript; charset=utf-8",
  ".css": "text/css; charset=utf-8"
};

const sendJson = (response, status, payload, headers = {}) => {
  const body = JSON.stringify(payload);
  response.writeHead(status, {
    "Content-Type": "application/json; charset=utf-8",
    "Content-Length": Buffer.byteLength(body),
    "Cache-Control": "no-store",
    ...headers
  });
  response.end(body);
};

const readJson = async (request, response) => {
  const contentType = request.headers["content-type"] ?? "";
  if (!contentType.toLowerCase().startsWith("application/json")) {
    sendJson(response, 415, {
      error: "unsupported-media-type",
      message: "Usa Content-Type: application/json"
    });
    return null;
  }

  const chunks = [];
  for await (const chunk of request) chunks.push(chunk);
  try {
    return JSON.parse(Buffer.concat(chunks).toString("utf8"));
  } catch {
    sendJson(response, 400, { error: "invalid-json", message: "JSON non valido" });
    return null;
  }
};

const serveStatic = async (pathname, response) => {
  const relative = pathname === "/" ? "index.html" : pathname.slice(1);
  const allowed = new Set(["index.html", "app.js", "api.js", "custom.css"]);
  if (!allowed.has(relative)) return false;

  try {
    const body = await readFile(join(root, relative));
    response.writeHead(200, {
      "Content-Type": mime[extname(relative)] ?? "application/octet-stream",
      "Content-Length": body.length
    });
    response.end(body);
  } catch {
    response.writeHead(404);
    response.end();
  }
  return true;
};

const server = createServer(async (request, response) => {
  const url = new URL(request.url ?? "/", `http://${request.headers.host ?? "localhost"}`);

  if (request.method === "GET" && url.pathname === "/api/posts") {
    const liked = url.searchParams.get("liked");
    const visible = liked === null
      ? posts
      : posts.filter((post) => post.liked === (liked === "true"));
    sendJson(response, 200, visible);
    return;
  }

  if (request.method === "POST" && url.pathname === "/api/posts") {
    const payload = await readJson(request, response);
    if (payload === null) return;

    const text = String(payload.text ?? "").trim();
    if (!text || text.length > 280) {
      sendJson(response, 400, {
        error: "invalid-post",
        message: "text e obbligatorio e deve avere massimo 280 caratteri"
      });
      return;
    }

    const post = {
      id: `p${nextId++}`,
      author: "Studente",
      text,
      likes: 0,
      liked: false
    };
    posts = [post, ...posts];
    sendJson(response, 201, post, { Location: `/api/posts/${post.id}` });
    return;
  }

  const postMatch = url.pathname.match(/^\/api\/posts\/([^/]+)$/);
  if (request.method === "PATCH" && postMatch) {
    const payload = await readJson(request, response);
    if (payload === null) return;

    const index = posts.findIndex((post) => post.id === postMatch[1]);
    if (index < 0) {
      sendJson(response, 404, {
        error: "post-not-found",
        message: "Il post richiesto non esiste"
      });
      return;
    }

    if (typeof payload.liked !== "boolean") {
      sendJson(response, 400, {
        error: "invalid-liked",
        message: "liked deve essere boolean"
      });
      return;
    }

    const current = posts[index];
    const likes = payload.liked === current.liked
      ? current.likes
      : Math.max(0, current.likes + (payload.liked ? 1 : -1));
    const updated = { ...current, liked: payload.liked, likes };
    posts = posts.map((post) => post.id === updated.id ? updated : post);
    sendJson(response, 200, updated);
    return;
  }

  if (request.method === "POST" && url.pathname === "/__reset") {
    posts = structuredClone(initialPosts);
    nextId = 3;
    sendJson(response, 200, { ok: true });
    return;
  }

  if (request.method === "GET" && await serveStatic(url.pathname, response)) {
    return;
  }

  if (url.pathname.startsWith("/api/")) {
    sendJson(response, 404, { error: "not-found", message: "Risorsa API non trovata" });
    return;
  }

  response.writeHead(404, { "Content-Type": "text/plain; charset=utf-8" });
  response.end("Not found");
});

const port = Number(process.env.PORT ?? 3000);
server.listen(port, "127.0.0.1", () => {
  const address = server.address();
  const actualPort = typeof address === "object" && address ? address.port : port;
  console.log(`READY http://127.0.0.1:${actualPort}`);
});
