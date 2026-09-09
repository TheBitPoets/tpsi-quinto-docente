export class ApiError extends Error {
  constructor(status, code, message) {
    super(message);
    this.name = "ApiError";
    this.status = status;
    this.code = code;
  }
}

async function request(path, { method = "GET", body } = {}) {
  const response = await fetch(path, {
    method,
    credentials: "same-origin",
    headers: body === undefined ? {} : { "Content-Type": "application/json" },
    body: body === undefined ? undefined : JSON.stringify(body),
  });
  let payload = null;
  if (response.status !== 204) {
    const type = response.headers.get("content-type") ?? "";
    payload = type.includes("application/json") ? await response.json() : await response.text();
  }
  if (!response.ok) {
    throw new ApiError(response.status, payload?.error?.code ?? "http-error", payload?.error?.message ?? `HTTP ${response.status}`);
  }
  return payload;
}

export const api = {
  me: () => request("/api/auth/me"),
  register: (credentials) => request("/api/auth/register", { method: "POST", body: credentials }),
  login: (credentials) => request("/api/auth/login", { method: "POST", body: credentials }),
  logout: () => request("/api/auth/logout", { method: "POST" }),
  listPosts: () => request("/api/posts"),
  createPost: (text) => request("/api/posts", { method: "POST", body: { text } }),
  setLiked: (id, liked) => request(`/api/posts/${encodeURIComponent(id)}`, { method: "PATCH", body: { liked } }),
  deletePost: (id) => request(`/api/posts/${encodeURIComponent(id)}`, { method: "DELETE" }),
};
