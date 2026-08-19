import express from "express";
import { createPostsRouter } from "./posts.router.js";
import {
  errorHandler,
  notFound,
  requestContext,
  requestLogger,
} from "./middleware.js";

export function createApp({ postStore, staticDir }) {
  const app = express();

  app.disable("x-powered-by");

  // TODO: monta nell'ordine corretto:
  // requestContext
  // requestLogger
  // express.json({ limit: "32kb" })
  // express.static(staticDir)
  // /api/posts router
  // notFound
  // errorHandler

  return app;
}
