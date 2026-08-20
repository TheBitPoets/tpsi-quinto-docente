import { Router } from "express";
import { HttpError } from "./http-errors.js";
import { requireJson } from "./middleware.js";
import { requireAuth } from "./session.js";
import { validateLikePatch, validateNewPost } from "./validation.js";

const validationMessage = (code) => ({
  "body-invalid": "Il body deve essere un oggetto JSON.",
  "text-required": "Il testo del post e obbligatorio.",
  "text-too-long": "Il testo del post supera 280 caratteri.",
  "liked-required": "liked deve essere boolean.",
}[code] ?? "Request non valida.");

const requireValid = (result) => {
  if (!result.ok) throw new HttpError(400, result.error, validationMessage(result.error));
  return result.value;
};

export function createPostsRouter({ postStore, postEvents }) {
  const router = Router();
  router.use(requireAuth);

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
    const created = postStore.create({ text: input.text, authorId: req.auth.user.id });
    // TODO: pubblica post:created DOPO la mutazione riuscita.
    void postEvents;
    res.location(`/api/posts/${encodeURIComponent(created.id)}`);
    res.status(201).json(created);
  });

  router.patch("/:id", requireJson, (req, res) => {
    const input = requireValid(validateLikePatch(req.body));
    const updated = postStore.setLiked(req.params.id, input.liked);
    if (!updated) throw new HttpError(404, "post-not-found", "Post non trovato.");
    // TODO: pubblica post:updated.
    res.status(200).json(updated);
  });

  router.delete("/:id", (req, res) => {
    const result = postStore.deleteOwned(req.params.id, req.auth.user.id);
    if (result.status === "not-found") throw new HttpError(404, "post-not-found", "Post non trovato.");
    if (result.status === "forbidden") throw new HttpError(403, "forbidden", "Non puoi eliminare il post di un altro utente.");
    // TODO: pubblica post:deleted con postId.
    res.status(204).end();
  });

  return router;
}
