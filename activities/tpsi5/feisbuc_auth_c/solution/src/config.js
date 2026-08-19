const parseBoolean = (value, fallback = false) => {
  if (value === undefined) return fallback;
  if (value === "true") return true;
  if (value === "false") return false;
  throw new Error("Valore booleano non valido");
};

export function loadConfig(env = process.env) {
  const port = Number(env.PORT ?? 3000);
  if (!Number.isInteger(port) || port < 0 || port > 65535) {
    throw new Error("PORT non valida");
  }

  const nodeEnv = env.NODE_ENV ?? "development";
  const production = nodeEnv === "production";
  const cookieSecure = parseBoolean(env.COOKIE_SECURE, false);
  if (production && !cookieSecure) {
    throw new Error("In production COOKIE_SECURE deve essere true");
  }

  const sessionTtlMs = Number(env.SESSION_TTL_MS ?? 8 * 60 * 60 * 1000);
  if (!Number.isSafeInteger(sessionTtlMs) || sessionTtlMs < 60_000) {
    throw new Error("SESSION_TTL_MS non valida");
  }

  return {
    port,
    nodeEnv,
    dbPath: env.DB_PATH ?? "data/feisbuc.db",
    cookieSecure,
    cookieName: production ? "__Host-feisbuc.sid" : "feisbuc.sid",
    sessionTtlMs,
    trustProxy: parseBoolean(env.TRUST_PROXY, false),
  };
}
