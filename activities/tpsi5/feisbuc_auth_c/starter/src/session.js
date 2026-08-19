import { HttpError } from "./http-errors.js";

export function createSessionToken() {
  // TODO: token opaco con almeno 256 bit casuali.
  throw new Error("TODO createSessionToken");
}

export function hashSessionToken(token) {
  // TODO: SHA-256 del token prima della persistenza.
  return token;
}

export function loadAuth({ authStore, config }) {
  return (req, res, next) => {
    req.auth = { user: null, sessionHash: null };
    // TODO: cookie -> hash -> lookup sessione non scaduta.
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

export function setSessionCookie(res, token, config) {
  // TODO: HttpOnly + SameSite=Strict + Secure da config + Path=/.
  throw new Error("TODO setSessionCookie");
}

export function clearSessionCookie(res, config) {
  // TODO: stessi attributi di scope usati nel set.
}
