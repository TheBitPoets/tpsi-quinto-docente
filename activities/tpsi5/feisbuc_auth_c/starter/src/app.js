import express from "express";
import { createAuthRouter } from "./auth.router.js";
import { createPostsRouter } from "./posts.router.js";
import {
  errorHandler,
  noStore,
  notFound,
  requestContext,
  requestLogger,
  requireSameOriginForUnsafe,
} from "./middleware.js";
import { loadAuth } from "./session.js";

export function createApp({ authStore, postStore, config, staticDir }) {
  const app = express();
  app.disable("x-powered-by");
  if (config.trustProxy) app.set("trust proxy", 1);
  app.use(requestContext);
  app.use(requestLogger);
  app.use(requireSameOriginForUnsafe);
  app.use(express.json({ limit: "32kb" }));

  // TODO: monta loadAuth PRIMA dei Router privati.
  void loadAuth;

  app.use(express.static(staticDir));
  app.use("/api/auth", noStore, createAuthRouter({ authStore, config }));
  app.use("/api/posts", noStore, createPostsRouter({ postStore }));
  app.use(notFound);
  app.use(errorHandler);
  return app;
}
