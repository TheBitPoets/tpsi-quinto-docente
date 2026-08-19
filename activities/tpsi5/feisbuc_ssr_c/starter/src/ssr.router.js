import { Router } from "express";
import { HttpError } from "./http-errors.js";
import { requireAuth } from "./session.js";
import { validateNewPost } from "./validation.js";

export function buildFeedViewModel(user, posts) {
  // TODO
  return { currentUser: user, posts };
}

export function createSsrRouter({ postStore }) {
  const router = Router();
  router.use(requireAuth);

  // TODO GET / -> render feed.njk
  // TODO POST /posts -> validate, create con req.auth.user.id, redirect 303 /ssr
  // TODO POST /posts/:id/delete -> deleteOwned + 403/404 + redirect 303

  void postStore;
  void HttpError;
  void validateNewPost;
  return router;
}
