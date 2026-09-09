import { spawn } from "node:child_process";
import path from "node:path";

const backendRoot = path.resolve("backend");
const child = spawn(process.execPath, ["src/server.js"], {
  cwd: backendRoot,
  env: { ...process.env, PORT: process.env.PORT ?? "3333" },
  stdio: "inherit",
});

for (const signal of ["SIGINT", "SIGTERM"]) {
  process.once(signal, () => child.kill(signal));
}

child.once("exit", (code, signal) => {
  if (signal) process.kill(process.pid, signal);
  else process.exitCode = code ?? 1;
});
