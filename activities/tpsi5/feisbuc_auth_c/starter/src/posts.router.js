import { Router } from "express";
import { HttpError } from "./http-errors.js";
import { requireJson } from "./middleware.js";
import { validateLikePatch, validateNewPost } from "./validation.js";

export function createPostsRouter({ postStore }) {
  const router = Router();
  // TODO: monta requireAuth sull'intero Router.

  router.get("/", (req, res) => {
    res.status(200).json(postStore.list());
  });

  router.post("/", requireJson, (req, res) => {
    const checked = validateNewPost(req.body);
    if (!checked.ok) throw new HttpError(400, checked.error, "Post non valido.");
    // TODO: authorId deve provenire esclusivamente da req.auth.user.id.
    throw new Error("TODO create authenticated post");
  });

  router.patch("/:id", requireJson, (req, res) => {
    const checked = validateLikePatch(req.body);
    if (!checked.ok) throw new HttpError(400, checked.error, "Like non valido.");
    const updated = postStore.setLiked(req.params.id, checked.value.liked);
    if (!updated) throw new HttpError(404, "post-not-found", "Post non trovato.");
    res.status(200).json(updated);
  });

  router.delete("/:id", (req, res) => {
    // TODO: chiama deleteOwned(id, req.auth.user.id) e mappa 403/404/204.
    res.status(501).end();
  });

  return router;
}
