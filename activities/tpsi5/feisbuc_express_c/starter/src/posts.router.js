import { Router } from "express";
import { HttpError } from "./http-errors.js";
import { requireJson } from "./middleware.js";
import { validateLikePatch, validateNewPost } from "./validation.js";

export function createPostsRouter({ postStore }) {
  const router = Router();

  router.get("/", (req, res) => {
    // TODO: interpreta ?liked=true|false e usa postStore.list().
    res.json([]);
  });

  router.post("/", requireJson, (req, res) => {
    // TODO: validateNewPost(req.body), create, 201, Location, JSON.
    res.status(501).json({ error: "todo" });
  });

  router.patch("/:id", requireJson, (req, res) => {
    // TODO: validateLikePatch, postStore.setLiked, 404 quando id non esiste.
    res.status(501).json({ error: "todo" });
  });

  return router;
}
