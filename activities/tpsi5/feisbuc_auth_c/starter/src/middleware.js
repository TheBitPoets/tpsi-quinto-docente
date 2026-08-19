import { randomUUID } from "node:crypto";
import { HttpError } from "./http-errors.js";

export function requestContext(req, res, next) {
  req.requestId = randomUUID();
  res.setHeader("X-Request-Id", req.requestId);
  next();
}

export function requestLogger(req, res, next) {
  const startedAt = Date.now();
  res.on("finish", () => console.log(JSON.stringify({
    requestId: req.requestId,
    method: req.method,
    path: req.originalUrl,
    status: res.statusCode,
    durationMs: Date.now() - startedAt,
  })));
  next();
}

export function requireJson(req, res, next) {
  if (!req.is("application/json")) {
    next(new HttpError(415, "unsupported-media-type", "Serve Content-Type application/json."));
    return;
  }
  next();
}

const SAFE_METHODS = new Set(["GET", "HEAD", "OPTIONS"]);
export function requireSameOriginForUnsafe(req, res, next) {
  if (SAFE_METHODS.has(req.method)) return next();
  const fetchSite = req.get("sec-fetch-site");
  if (fetchSite && !["same-origin", "same-site", "none"].includes(fetchSite)) {
    return next(new HttpError(403, "cross-site-request-blocked", "Request cross-site rifiutata."));
  }
  const origin = req.get("origin");
  if (origin && origin !== `${req.protocol}://${req.get("host")}`) {
    return next(new HttpError(403, "origin-mismatch", "Origin non consentita."));
  }
  next();
}

export function noStore(req, res, next) {
  res.set("Cache-Control", "no-store");
  next();
}

export function notFound(req, res, next) {
  next(new HttpError(404, "not-found", "Risorsa non trovata."));
}

export function errorHandler(error, req, res, next) {
  if (res.headersSent) return next(error);
  let status = 500;
  let code = "internal-error";
  let message = "Errore interno.";
  if (error?.type === "entity.parse.failed") {
    status = 400; code = "invalid-json"; message = "Body JSON non valido.";
  } else if (error instanceof HttpError) {
    status = error.status; code = error.code; message = error.message;
  }
  res.status(status).json({ error: { code, message, requestId: req.requestId ?? null } });
}
