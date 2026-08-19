import { mkdirSync } from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { SqlAuthStore } from "./auth-store.js";
import { createApp } from "./app.js";
import { loadConfig } from "./config.js";
import { openDatabase } from "./db.js";
import { SqlPostStore } from "./sql-post-store.js";

const config = loadConfig();
const here = path.dirname(fileURLToPath(import.meta.url));
const projectRoot = path.resolve(here, "..");
const staticDir = path.join(projectRoot, "public");
const schemaPath = path.join(here, "schema.sql");
const dbPath = config.dbPath === ":memory:"
  ? ":memory:"
  : path.resolve(projectRoot, config.dbPath);

if (dbPath !== ":memory:") mkdirSync(path.dirname(dbPath), { recursive: true });

const db = openDatabase({ dbPath, schemaPath });
const authStore = new SqlAuthStore({ db });
const postStore = new SqlPostStore({ db });
const app = createApp({ authStore, postStore, config, staticDir });

const server = app.listen(config.port, "127.0.0.1", () => {
  const address = server.address();
  console.log(`READY http://127.0.0.1:${address.port}`);
});

function shutdown() {
  server.close(() => db.close());
}

process.once("SIGINT", shutdown);
process.once("SIGTERM", shutdown);
