import { createHash, randomBytes } from "node:crypto";
import { HttpError } from "./http-errors.js";

export function createSessionToken() {
  return randomBytes(32).toString("base64url");
}

export function hashSessionToken(token) {
  return createHash("sha256").update(token, "utf8").digest("hex");
}

export function readCookie(header, name) {
  if (!header) return null;
  for (const part of header.split(";")) {
    const [rawName, ...rest] = part.trim().split("=");
    if (rawName === name) return rest.join("=") || null;
  }
  return null;
}

export function sessionCookieOptions(config) {
  return {
    httpOnly: true,
    secure: config.cookieSecure,
    sameSite: "strict",
    path: "/",
  };
}

export function setSessionCookie(res, token, config) {
  res.cookie(config.cookieName, token, sessionCookieOptions(config));
  res.set("Cache-Control", "no-store");
}

export function clearSessionCookie(res, config) {
  res.clearCookie(config.cookieName, sessionCookieOptions(config));
  res.set("Cache-Control", "no-store");
}

export function loadAuth({ authStore, config }) {
  return (req, res, next) => {
    req.auth = { user: null, sessionHash: null };
    const token = readCookie(req.get("cookie"), config.cookieName);
    if (!token) {
      next();
      return;
    }

    const idHash = hashSessionToken(token);
    const session = authStore.findSessionUser(idHash, Date.now());
    if (!session) {
      next();
      return;
    }

    req.auth = { user: session.user, sessionHash: idHash };
    next();
  };
}

export function requireAuth(req, res, next) {
  if (!req.auth?.user) {
    next(new HttpError(401, "authentication-required", "Autenticazione richiesta."));
    return;
  }
  next();
}
