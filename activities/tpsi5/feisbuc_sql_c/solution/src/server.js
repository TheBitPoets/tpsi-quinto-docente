import { mkdirSync } from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { createApp } from "./app.js";
import { loadConfig } from "./config.js";
import { openSqlPostStore } from "./sql-post-store.js";

const config = loadConfig();
const here = path.dirname(fileURLToPath(import.meta.url));
const projectRoot = path.resolve(here, "..");
const staticDir = path.join(projectRoot, "public");
const schemaPath = path.join(here, "schema.sql");
const dbPath = config.dbPath === ":memory:"
  ? ":memory:"
  : path.resolve(projectRoot, config.dbPath);

if (dbPath !== ":memory:") {
  mkdirSync(path.dirname(dbPath), { recursive: true });
}

const postStore = openSqlPostStore({ dbPath, schemaPath });
const app = createApp({ postStore, staticDir });

const server = app.listen(config.port, "127.0.0.1", () => {
  const address = server.address();
  console.log(`READY http://127.0.0.1:${address.port}`);
});

function shutdown() {
  server.close(() => {
    postStore.close();
  });
}

process.once("SIGINT", shutdown);
process.once("SIGTERM", shutdown);
