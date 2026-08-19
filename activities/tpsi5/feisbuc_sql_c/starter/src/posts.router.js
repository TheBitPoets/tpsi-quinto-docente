import { Router } from "express";
import { HttpError } from "./http-errors.js";
import { requireJson } from "./middleware.js";
import { validateLikePatch, validateNewPost } from "./validation.js";

const validationMessage = (code) => ({
  "body-invalid": "Il body deve essere un oggetto JSON.",
  "text-required": "Il testo del post e obbligatorio.",
  "text-too-long": "Il testo del post supera 280 caratteri.",
  "liked-required": "liked deve essere boolean.",
}[code] ?? "Request non valida.");

const requireValid = (result) => {
  if (!result.ok) {
    throw new HttpError(400, result.error, validationMessage(result.error));
  }
  return result.value;
};

export function createPostsRouter({ postStore }) {
  const router = Router();

  router.get("/", (req, res) => {
    let liked;
    if (req.query.liked !== undefined) {
      if (req.query.liked === "true") liked = true;
      else if (req.query.liked === "false") liked = false;
      else throw new HttpError(400, "liked-filter-invalid", "liked deve essere true oppure false.");
    }
    res.status(200).json(postStore.list({ liked }));
  });

  router.post("/", requireJson, (req, res) => {
    const input = requireValid(validateNewPost(req.body));
    const created = postStore.create(input);
    res.location(`/api/posts/${encodeURIComponent(created.id)}`);
    res.status(201).json(created);
  });

  router.patch("/:id", requireJson, (req, res) => {
    const input = requireValid(validateLikePatch(req.body));
    const updated = postStore.setLiked(req.params.id, input.liked);
    if (!updated) {
      throw new HttpError(404, "post-not-found", "Post non trovato.");
    }
    res.status(200).json(updated);
  });

  return router;
}
