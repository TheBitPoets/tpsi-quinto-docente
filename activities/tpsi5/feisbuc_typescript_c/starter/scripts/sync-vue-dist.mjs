import { cpSync, existsSync, mkdirSync, rmSync } from "node:fs";
import path from "node:path";

const source = path.resolve("frontend", "dist");
const destination = path.resolve("backend", "public", "vue");

if (!existsSync(source)) {
  throw new Error("Build frontend mancante: esegui npm run build dalla root dello starter.");
}

rmSync(destination, { recursive: true, force: true });
mkdirSync(path.dirname(destination), { recursive: true });
cpSync(source, destination, { recursive: true });
console.log(`Frontend integrato in ${destination}`);
