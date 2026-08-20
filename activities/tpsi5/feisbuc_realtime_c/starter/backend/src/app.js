import path from "node:path";
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
import { installVueSpa } from "./vue-spa.js";

export function createApp({ authStore, postStore, postEvents, config, staticDir }) {
  const app = express();
  app.disable("x-powered-by");
  if (config.trustProxy) app.set("trust proxy", 1);

  app.use(requestContext);
  app.use(requestLogger);
  app.use(requireSameOriginForUnsafe);
  app.use(express.json({ limit: "32kb" }));
  app.use(loadAuth({ authStore, config }));
  app.use(express.static(staticDir));

  app.use("/api/auth", noStore, createAuthRouter({ authStore, config }));
  app.use("/api/posts", noStore, createPostsRouter({ postStore, postEvents }));

  installVueSpa(app, { vueRoot: path.join(staticDir, "vue") });
  app.use(notFound);
  app.use(errorHandler);
  return app;
}
