import { spawn } from "node:child_process";
import { mkdtemp, rm } from "node:fs/promises";
import { tmpdir } from "node:os";
import path from "node:path";
import process from "node:process";
import { io } from "socket.io-client";

const referenceRoot = path.resolve(process.argv[2] ?? "_realtime-reference");
const temp = await mkdtemp(path.join(tmpdir(), "tpsi5-realtime-"));
const dbPath = path.join(temp, "realtime.db");
let child;
let aliceSocket;
let bobSocket;

const delay = (ms) => new Promise((resolve) => setTimeout(resolve, ms));

function waitForReady(proc) {
  return new Promise((resolve, reject) => {
    let stdout = "";
    let stderr = "";
    const timeout = setTimeout(() => reject(new Error(`backend READY timeout: ${stdout} ${stderr}`)), 10000);
    proc.stderr.on("data", (chunk) => { stderr += chunk.toString(); });
    proc.stdout.on("data", (chunk) => {
      stdout += chunk.toString();
      for (const line of stdout.split(/\r?\n/)) {
        if (line.startsWith("READY http://")) {
          clearTimeout(timeout);
          resolve(line.slice("READY ".length).trim());
          return;
        }
      }
    });
    proc.once("exit", (code) => {
      clearTimeout(timeout);
      reject(new Error(`backend exited ${code}: ${stdout} ${stderr}`));
    });
  });
}

async function call(base, cookie, pathname, { method = "GET", body } = {}) {
  const headers = {};
  if (cookie) headers.Cookie = cookie;
  if (body !== undefined) headers["Content-Type"] = "application/json";
  const response = await fetch(`${base}${pathname}`, {
    method,
    headers,
    body: body === undefined ? undefined : JSON.stringify(body),
    redirect: "manual",
  });
  const raw = await response.text();
  const payload = raw && (response.headers.get("content-type") ?? "").includes("application/json")
    ? JSON.parse(raw)
    : raw;
  return { response, payload };
}

async function register(base, displayName, email) {
  const { response, payload } = await call(base, null, "/api/auth/register", {
    method: "POST",
    body: {
      displayName,
      email,
      password: `passphrase ${displayName} realtime sufficientemente lunga 2026`,
    },
  });
  if (response.status !== 201) throw new Error(`register ${displayName}: ${response.status} ${JSON.stringify(payload)}`);
  const setCookie = response.headers.get("set-cookie");
  if (!setCookie) throw new Error(`register ${displayName}: Set-Cookie mancante`);
  return { cookie: setCookie.split(";", 1)[0], user: payload.user };
}

function connect(base, cookie) {
  const socket = io(base, {
    transports: ["websocket"],
    forceNew: true,
    reconnection: false,
    extraHeaders: cookie ? { Cookie: cookie } : {},
  });
  return new Promise((resolve, reject) => {
    const timer = setTimeout(() => {
      socket.close();
      reject(new Error("socket connect timeout"));
    }, 5000);
    socket.once("connect", () => {
      clearTimeout(timer);
      resolve(socket);
    });
    socket.once("connect_error", (error) => {
      clearTimeout(timer);
      socket.close();
      reject(error);
    });
  });
}

function expectConnectError(base) {
  const socket = io(base, {
    transports: ["websocket"],
    forceNew: true,
    reconnection: false,
  });
  return new Promise((resolve, reject) => {
    const timer = setTimeout(() => {
      socket.close();
      reject(new Error("anonymous socket was not rejected"));
    }, 5000);
    socket.once("connect", () => {
      clearTimeout(timer);
      socket.close();
      reject(new Error("anonymous socket connected unexpectedly"));
    });
    socket.once("connect_error", (error) => {
      clearTimeout(timer);
      socket.close();
      resolve(error.message);
    });
  });
}

function waitEvent(socket, name, predicate = () => true) {
  return new Promise((resolve, reject) => {
    const timer = setTimeout(() => {
      socket.off(name, handler);
      reject(new Error(`timeout waiting ${name}`));
    }, 5000);
    const handler = (payload) => {
      if (!predicate(payload)) return;
      clearTimeout(timer);
      socket.off(name, handler);
      resolve(payload);
    };
    socket.on(name, handler);
  });
}

try {
  child = spawn(process.execPath, ["src/server.js"], {
    cwd: referenceRoot,
    env: {
      ...process.env,
      PORT: "0",
      DB_PATH: dbPath,
      NODE_ENV: "development",
      COOKIE_SECURE: "false",
    },
    stdio: ["ignore", "pipe", "pipe"],
  });
  const base = await waitForReady(child);

  const anonymousError = await expectConnectError(base);
  if (!anonymousError.includes("authentication-required")) {
    throw new Error(`unexpected anonymous error: ${anonymousError}`);
  }

  const alice = await register(base, "Alice", "alice-realtime@example.test");
  const bob = await register(base, "Bob", "bob-realtime@example.test");
  aliceSocket = await connect(base, alice.cookie);
  bobSocket = await connect(base, bob.cookie);

  const aliceCreated = waitEvent(aliceSocket, "post:created");
  const bobCreated = waitEvent(bobSocket, "post:created");
  const create = await call(base, alice.cookie, "/api/posts", {
    method: "POST",
    body: { text: "realtime P1", authorId: "spoofed" },
  });
  if (create.response.status !== 201) throw new Error(`create failed ${create.response.status}`);
  if (create.payload.authorId !== alice.user.id) throw new Error("REST author spoofing accepted");
  const createdId = create.payload.id;
  const [createdA, createdB] = await Promise.all([aliceCreated, bobCreated]);
  if (createdA.id !== createdId || createdB.id !== createdId) throw new Error("created event mismatch");

  const aliceUpdated = waitEvent(aliceSocket, "post:updated", (post) => post.id === createdId);
  const bobUpdated = waitEvent(bobSocket, "post:updated", (post) => post.id === createdId);
  const update = await call(base, bob.cookie, `/api/posts/${encodeURIComponent(createdId)}`, {
    method: "PATCH",
    body: { liked: true },
  });
  if (update.response.status !== 200 || update.payload.likes !== 1) throw new Error("like update failed");
  const [updatedA, updatedB] = await Promise.all([aliceUpdated, bobUpdated]);
  if (!updatedA.liked || !updatedB.liked) throw new Error("updated event mismatch");

  // Un comando Socket.IO inventato non deve modificare il dominio.
  bobSocket.emit("post:create", { text: "FORGED SOCKET COMMAND", authorId: bob.user.id });
  await delay(150);
  const afterForged = await call(base, bob.cookie, "/api/posts");
  if (afterForged.payload.some((post) => post.text === "FORGED SOCKET COMMAND")) {
    throw new Error("socket command path unexpectedly mutates posts");
  }

  const aliceDeleted = waitEvent(aliceSocket, "post:deleted", (payload) => payload.postId === createdId);
  const bobDeleted = waitEvent(bobSocket, "post:deleted", (payload) => payload.postId === createdId);
  const deletion = await call(base, alice.cookie, `/api/posts/${encodeURIComponent(createdId)}`, { method: "DELETE" });
  if (deletion.response.status !== 204) throw new Error(`delete failed ${deletion.response.status}`);
  await Promise.all([aliceDeleted, bobDeleted]);

  // Bob perde la connessione: Alice modifica lo stato mentre Bob e offline.
  bobSocket.disconnect();
  const aliceP2 = waitEvent(aliceSocket, "post:created", (post) => post.text === "offline P2");
  const createOffline = await call(base, alice.cookie, "/api/posts", {
    method: "POST",
    body: { text: "offline P2" },
  });
  if (createOffline.response.status !== 201) throw new Error("offline create failed");
  const p2 = await aliceP2;

  // Recovery baseline del corso: al reconnect si rilegge lo snapshot REST.
  bobSocket = await connect(base, bob.cookie);
  const snapshot = await call(base, bob.cookie, "/api/posts");
  if (snapshot.response.status !== 200 || !snapshot.payload.some((post) => post.id === p2.id)) {
    throw new Error("REST resync did not recover offline event");
  }

  console.log(JSON.stringify({
    ok: true,
    anonymousRejected: true,
    created: createdId,
    updated: true,
    deleted: true,
    forgedSocketCommandRejected: true,
    resyncRecovered: p2.id,
  }));
} finally {
  aliceSocket?.disconnect();
  bobSocket?.disconnect();
  if (child && child.exitCode === null) {
    child.kill("SIGTERM");
    await new Promise((resolve) => {
      const timer = setTimeout(() => {
        child.kill("SIGKILL");
        resolve();
      }, 5000);
      child.once("exit", () => {
        clearTimeout(timer);
        resolve();
      });
    });
  }
  await rm(temp, { recursive: true, force: true });
}
