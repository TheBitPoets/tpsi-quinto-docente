// Pattern di riferimento, non server completo.
import { createHash, randomBytes } from "node:crypto";

export const newSessionToken = () => randomBytes(32).toString("base64url");
export const sessionHash = (token) => createHash("sha256").update(token).digest("hex");

export const sessionCookie = Object.freeze({
  httpOnly: true,
  secure: true,
  sameSite: "strict",
  path: "/",
});

export function authorForCreate(req) {
  if (!req.auth?.user) throw new Error("authentication-required");
  return req.auth.user.id;
}

export function canDelete(req, post) {
  return Boolean(req.auth?.user && post && post.authorId === req.auth.user.id);
}

export const publicLoginError = Object.freeze({
  code: "invalid-credentials",
  message: "Credenziali non valide.",
});
