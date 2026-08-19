export const createApi = (baseUrl = "") => {
  const requestJson = async (path, options = {}) => {
    // TODO:
    // 1. costruisci URL relativo o assoluto;
    // 2. await fetch;
    // 3. leggi Content-Type;
    // 4. interpreta JSON soltanto quando appropriato;
    // 5. se !response.ok genera un Error con messaggio utile;
    // 6. restituisci il payload in caso di successo.
    throw new Error("TODO requestJson");
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
