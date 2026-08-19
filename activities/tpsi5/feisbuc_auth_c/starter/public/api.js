const requestJson = async (path, options = {}) => {
  const response = await fetch(path, { credentials: "same-origin", ...options });
  const type = response.headers.get("content-type") ?? "";
  const isJson = type.includes("application/json");
  const payload = response.status === 204 ? null : isJson ? await response.json() : await response.text();
  if (!response.ok) {
    const error = new Error(payload?.error?.message ?? `HTTP ${response.status}`);
    error.status = response.status;
    error.payload = payload;
    throw error;
  }
  return payload;
};
const json = (method, body) => ({ method, headers:{"Content-Type":"application/json"}, body:JSON.stringify(body) });
export const api = {
  me: () => requestJson("/api/auth/me"),
  register: (displayName,email,password) => requestJson("/api/auth/register", json("POST",{displayName,email,password})),
  login: (email,password) => requestJson("/api/auth/login", json("POST",{email,password})),
  logout: () => requestJson("/api/auth/logout", {method:"POST"}),
  getPosts: () => requestJson("/api/posts"),
  createPost: (text) => requestJson("/api/posts", json("POST",{text})),
  setLiked: (id,liked) => requestJson(`/api/posts/${encodeURIComponent(id)}`, json("PATCH",{liked})),
  deletePost: (id) => requestJson(`/api/posts/${encodeURIComponent(id)}`, {method:"DELETE"}),
};
