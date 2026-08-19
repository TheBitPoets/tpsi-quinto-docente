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
const dbPath = config.dbPath === ":memory:" ? ":memory:" : path.resolve(projectRoot, config.dbPath);
if (dbPath !== ":memory:") mkdirSync(path.dirname(dbPath), { recursive: true });

const db = openDatabase({ dbPath, schemaPath: path.join(here, "schema.sql") });
const authStore = new SqlAuthStore({ db });
const postStore = new SqlPostStore({ db });

// TODO: crea app con authStore/postStore/config/staticDir e avvia su PORT.
void createApp;
void authStore;
void postStore;
console.log("TODO avvio server auth");
