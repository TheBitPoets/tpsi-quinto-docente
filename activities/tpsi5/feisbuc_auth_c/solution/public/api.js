const requestJson = async (path, options = {}) => {
  const response = await fetch(path, {
    credentials: "same-origin",
    ...options,
  });
  const contentType = response.headers.get("content-type") ?? "";
  const isJson = contentType.toLowerCase().includes("application/json");
  let payload = null;
  if (response.status !== 204 && response.status !== 205) {
    payload = isJson ? await response.json() : await response.text();
  }
  if (!response.ok) {
    const message = isJson && payload?.error?.message
      ? payload.error.message
      : `HTTP ${response.status}`;
    const error = new Error(message);
    error.status = response.status;
    error.payload = payload;
    throw error;
  }
  return payload;
};

const jsonOptions = (method, body) => ({
  method,
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify(body),
});

export const api = {
  me: () => requestJson("/api/auth/me"),
  register: (displayName, email, password) => requestJson(
    "/api/auth/register",
    jsonOptions("POST", { displayName, email, password }),
  ),
  login: (email, password) => requestJson(
    "/api/auth/login",
    jsonOptions("POST", { email, password }),
  ),
  logout: () => requestJson("/api/auth/logout", { method: "POST" }),
  getPosts: () => requestJson("/api/posts"),
  createPost: (text) => requestJson("/api/posts", jsonOptions("POST", { text })),
  setLiked: (id, liked) => requestJson(`/api/posts/${encodeURIComponent(id)}`, jsonOptions("PATCH", { liked })),
  deletePost: (id) => requestJson(`/api/posts/${encodeURIComponent(id)}`, { method: "DELETE" }),
};
