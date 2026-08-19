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
  app.use(requestContext);
  app.use(requestLogger);
  app.use(express.json({ limit: "32kb" }));
  app.use(express.static(staticDir));
  app.use("/api/posts", createPostsRouter({ postStore }));
  app.use(notFound);
  app.use(errorHandler);

  return app;
}
