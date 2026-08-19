export function loadConfig(env = process.env) {
  const port = Number(env.PORT ?? 3000);
  if (!Number.isInteger(port) || port < 0 || port > 65535) {
    throw new Error("PORT non valida");
  }

  return {
    port,
    nodeEnv: env.NODE_ENV ?? "development",
    dbPath: env.DB_PATH ?? "data/feisbuc.db",
  };
}
