import { createServer } from "node:http";

const initialPosts = [
  { id: "p1", text: "HTTP prima di Express", likes: 1, liked: false },
  { id: "p2", text: "Status e header fanno parte del contratto", likes: 3, liked: true }
];

let posts = structuredClone(initialPosts);
let nextId = 3;

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

const readBody = async (request) => {
  const chunks = [];
  for await (const chunk of request) chunks.push(chunk);
  return Buffer.concat(chunks).toString("utf8");
};

const server = createServer(async (request, response) => {
  const url = new URL(request.url ?? "/", `http://${request.headers.host ?? "localhost"}`);

  if (request.method === "GET" && url.pathname === "/api/posts") {
    sendJson(response, 200, posts);
    return;
  }

  if (request.method === "GET" && url.pathname === "/api/posts/missing") {
    sendJson(response, 404, {
      error: "post-not-found",
      message: "Il post richiesto non esiste"
    });
    return;
  }

  if (request.method === "POST" && url.pathname === "/api/posts") {
    const contentType = request.headers["content-type"] ?? "";
    if (!contentType.toLowerCase().startsWith("application/json")) {
      sendJson(response, 415, {
        error: "unsupported-media-type",
        message: "Usa Content-Type: application/json"
      });
      return;
    }

    let parsed;
    try {
      parsed = JSON.parse(await readBody(request));
    } catch {
      sendJson(response, 400, {
        error: "invalid-json",
        message: "Il body non contiene JSON valido"
      });
      return;
    }

    const text = String(parsed?.text ?? "").trim();
    if (!text) {
      sendJson(response, 400, {
        error: "invalid-post",
        message: "text e obbligatorio"
      });
      return;
    }

    const post = { id: `p${nextId++}`, text, likes: 0, liked: false };
    posts = [post, ...posts];
    sendJson(response, 201, post, { Location: `/api/posts/${post.id}` });
    return;
  }

  if (request.method === "POST" && url.pathname === "/__reset") {
    posts = structuredClone(initialPosts);
    nextId = 3;
    sendJson(response, 200, { ok: true });
    return;
  }

  response.setHeader("Allow", "GET, POST");
  sendJson(response, 405, {
    error: "method-not-allowed",
    message: "Metodo non ammesso sulla risorsa richiesta"
  });
});

const port = Number(process.env.PORT ?? 3000);
server.listen(port, "127.0.0.1", () => {
  const address = server.address();
  const actualPort = typeof address === "object" && address ? address.port : port;
  console.log(`READY http://127.0.0.1:${actualPort}`);
});
