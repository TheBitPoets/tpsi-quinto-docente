const toUrl = (baseUrl, path) => {
  if (!baseUrl) return path;
  return new URL(path, baseUrl).toString();
};

export const createApi = (baseUrl = "") => {
  const requestJson = async (path, options = {}) => {
    const response = await fetch(toUrl(baseUrl, path), options);
    const contentType = response.headers.get("content-type") ?? "";
    const isJson = contentType.toLowerCase().includes("application/json");

    let payload = null;
    if (response.status !== 204 && response.status !== 205) {
      payload = isJson ? await response.json() : await response.text();
    }

    if (!response.ok) {
      const message = isJson && payload && typeof payload === "object"
        ? payload.message ?? payload.error?.message ?? payload.error ?? `HTTP ${response.status}`
        : `HTTP ${response.status}`;
      const error = new Error(message);
      error.status = response.status;
      error.payload = payload;
      throw error;
    }

    return payload;
  };

  return {
    getPosts: async () => requestJson("/api/posts"),
    createPost: async (text) => requestJson("/api/posts", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ text })
    }),
    setLiked: async (id, liked) => requestJson(`/api/posts/${encodeURIComponent(id)}`, {
      method: "PATCH",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ liked })
    })
  };
};
