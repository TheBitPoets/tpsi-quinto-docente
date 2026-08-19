import { fileURLToPath } from "node:url";
import path from "node:path";
import { createApp } from "./app.js";
import { loadConfig } from "./config.js";
import { MemoryPostStore, seedPosts } from "./post-store.js";

const config = loadConfig();
const here = path.dirname(fileURLToPath(import.meta.url));
const staticDir = path.resolve(here, "../public");
const postStore = new MemoryPostStore(seedPosts);
const app = createApp({ postStore, staticDir });

const server = app.listen(config.port, "127.0.0.1", () => {
  const address = server.address();
  console.log(`READY http://127.0.0.1:${address.port}`);
});
