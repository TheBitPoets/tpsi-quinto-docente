import express from "express";
import { createAuthRouter } from "./auth.router.js";
import { createPostsRouter } from "./posts.router.js";
import { errorHandler, noStore, notFound, requestContext, requestLogger, requireSameOriginForUnsafe } from "./middleware.js";
import { loadAuth } from "./session.js";
import { createSsrRouter } from "./ssr.router.js";
import { installViewEngine } from "./view-engine.js";

export function createApp({ authStore, postStore, config, staticDir, viewsDir }) {
  const app = express();
  app.disable("x-powered-by");
  if (config.trustProxy) app.set("trust proxy", 1);
  app.use(requestContext);
  app.use(requestLogger);
  app.use(requireSameOriginForUnsafe);
  app.use(express.json({ limit: "32kb" }));
  app.use(express.urlencoded({ extended: false, limit: "16kb" }));
  app.use(loadAuth({ authStore, config }));
  installViewEngine({ app, viewsDir });
  app.use(express.static(staticDir));
  app.use("/api/auth", noStore, createAuthRouter({ authStore, config }));
  app.use("/api/posts", noStore, createPostsRouter({ postStore }));
  // TODO: monta /ssr usando createSsrRouter({ postStore })
  void createSsrRouter;
  app.use(notFound);
  app.use(errorHandler);
  return app;
}
