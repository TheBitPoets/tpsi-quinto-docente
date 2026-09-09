import type {
  LoginCredentials,
  Post,
  RegistrationCredentials,
  User,
} from "./domain";

export class ApiError extends Error {
  constructor(
    public readonly status: number,
    public readonly code: string,
    message: string,
  ) {
    super(message);
    this.name = "ApiError";
  }
}

type RequestOptions = {
  method?: "GET" | "POST" | "PATCH" | "DELETE";
  body?: unknown;
};

function isRecord(value: unknown): value is Record<string, unknown> {
  return typeof value === "object" && value !== null;
}

function parseUser(value: unknown): User {
  // TODO: restringi unknown verificando id/email/displayName.
  void value;
  throw new Error("TODO parseUser");
}

function parsePost(value: unknown): Post {
  // TODO: restringi unknown verificando tutti i campi di Post.
  void value;
  throw new Error("TODO parsePost");
}

function parseAuthEnvelope(value: unknown): { user: User } {
  if (!isRecord(value) || !("user" in value)) throw new Error("Invalid auth payload");
  return { user: parseUser(value.user) };
}

function parsePosts(value: unknown): Post[] {
  if (!Array.isArray(value)) throw new Error("Invalid posts payload");
  return value.map(parsePost);
}

function parseError(value: unknown, status: number): ApiError {
  if (isRecord(value) && isRecord(value.error)) {
    const code = typeof value.error.code === "string" ? value.error.code : "http-error";
    const message = typeof value.error.message === "string" ? value.error.message : `HTTP ${status}`;
    return new ApiError(status, code, message);
  }
  return new ApiError(status, "http-error", `HTTP ${status}`);
}

async function request(path: string, options: RequestOptions = {}): Promise<unknown> {
  const init: RequestInit = {
    method: options.method ?? "GET",
    credentials: "same-origin",
    ...(options.body === undefined ? {} : {
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(options.body),
    }),
  };
  const response = await fetch(path, init);
  let payload: unknown = null;
  if (response.status !== 204) {
    const contentType = response.headers.get("content-type") ?? "";
    payload = contentType.includes("application/json") ? await response.json() as unknown : await response.text();
  }
  if (!response.ok) throw parseError(payload, response.status);
  return payload;
}

export const api = {
  me: async (): Promise<{ user: User }> => parseAuthEnvelope(await request("/api/auth/me")),
  register: async (credentials: RegistrationCredentials): Promise<{ user: User }> => parseAuthEnvelope(await request("/api/auth/register", { method: "POST", body: credentials })),
  login: async (credentials: LoginCredentials): Promise<{ user: User }> => parseAuthEnvelope(await request("/api/auth/login", { method: "POST", body: credentials })),
  logout: async (): Promise<void> => { await request("/api/auth/logout", { method: "POST" }); },
  listPosts: async (): Promise<Post[]> => parsePosts(await request("/api/posts")),
  createPost: async (text: string): Promise<Post> => parsePost(await request("/api/posts", { method: "POST", body: { text } })),
  setLiked: async (id: string, liked: boolean): Promise<Post> => parsePost(await request(`/api/posts/${encodeURIComponent(id)}`, { method: "PATCH", body: { liked } })),
  deletePost: async (id: string): Promise<void> => { await request(`/api/posts/${encodeURIComponent(id)}`, { method: "DELETE" }); },
};
