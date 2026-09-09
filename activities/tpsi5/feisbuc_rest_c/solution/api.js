const toUrl = (baseUrl, path) => {
  if (!baseUrl) return path;
  return new URL(path, baseUrl).toString();
};

export const createApi = (baseUrl = "") => {
  const readPayload = async (response, method) => {
    if (method === "HEAD" || response.status === 204 || response.status === 205) {
      return null;
    }

    const contentType = response.headers.get("content-type") ?? "";
    const mediaType = contentType.split(";", 1)[0].trim().toLowerCase();
    const isJson = mediaType === "application/json" || mediaType.endsWith("+json");

    try {
      return isJson ? await response.json() : await response.text();
    } catch (cause) {
      const error = new Error(`Rappresentazione ${mediaType || "sconosciuta"} non valida`);
      error.kind = "representation";
      error.cause = cause;
      throw error;
    }
  };

  const requestJson = async (path, options = {}) => {
    const method = String(options.method ?? "GET").toUpperCase();
    const response = await fetch(toUrl(baseUrl, path), options);
    const payload = await readPayload(response, method);

    if (!response.ok) {
      const message = payload && typeof payload === "object"
        ? payload.message ?? payload.error ?? `HTTP ${response.status}`
        : `HTTP ${response.status}`;
      const error = new Error(message);
      error.kind = "http";
      error.status = response.status;
      error.payload = payload;
      throw error;
    }

    return payload;
  };

  const assertPost = (value) => {
    const valid = value && typeof value === "object"
      && typeof value.id === "string"
      && typeof value.author === "string"
      && typeof value.text === "string"
      && Number.isInteger(value.likes)
      && typeof value.liked === "boolean";
    if (!valid) {
      const error = new Error("Il server ha restituito un post non conforme al contratto");
      error.kind = "data-contract";
      throw error;
    }
    return value;
  };

  const assertPosts = (value) => {
    if (!Array.isArray(value)) {
      const error = new Error("Il server non ha restituito una lista di post");
      error.kind = "data-contract";
      throw error;
    }
    return value.map(assertPost);
  };

  return {
    getPosts: async () => assertPosts(await requestJson("/api/posts")),
    createPost: async (text) => assertPost(await requestJson("/api/posts", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ text })
    })),
    setLiked: async (id, liked) => assertPost(await requestJson(`/api/posts/${encodeURIComponent(id)}`, {
      method: "PATCH",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ liked })
    }))
  };
};
