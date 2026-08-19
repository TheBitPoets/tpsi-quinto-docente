import { randomUUID } from "node:crypto";
import { HttpError } from "./http-errors.js";

export function requestContext(req, res, next) {
  // TODO: genera req.requestId e invia X-Request-Id.
  next();
}

export function requestLogger(req, res, next) {
  // TODO: registra method, originalUrl, status e durata senza loggare body/password.
  next();
}

export function requireJson(req, res, next) {
  // TODO: per request con body JSON atteso, rifiuta media type non application/json con 415.
  next();
}

export function notFound(req, res, next) {
  next(new HttpError(404, "not-found", "Risorsa non trovata."));
}

export function errorHandler(error, req, res, next) {
  // TODO: gestisci JSON parse error e HttpError; fallback 500.
  res.status(500).json({
    error: {
      code: "todo",
      message: "TODO",
      requestId: req.requestId ?? null,
    },
  });
}
