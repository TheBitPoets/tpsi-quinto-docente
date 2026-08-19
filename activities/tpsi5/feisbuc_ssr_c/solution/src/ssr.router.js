import { Router } from "express";
import { HttpError } from "./http-errors.js";
import { requireAuth } from "./session.js";
import { validateNewPost } from "./validation.js";

const validationMessage = (code) => ({
  "body-invalid": "Form non valido.",
  "text-required": "Il testo del post e obbligatorio.",
  "text-too-long": "Il testo del post supera 280 caratteri.",
}[code] ?? "Request non valida.");

function requireValid(result) {
  if (!result.ok) throw new HttpError(400, result.error, validationMessage(result.error));
  return result.value;
}

export function buildFeedViewModel(user, posts) {
  return {
    currentUser: { id: user.id, displayName: user.displayName, email: user.email },
    posts: posts.map((post) => ({
      ...post,
      canDelete: post.authorId === user.id,
      likedLabel: post.liked ? "Non mi piace piu" : "Mi piace",
    })),
  };
}

export function createSsrRouter({ postStore }) {
  const router = Router();
  router.use(requireAuth);

  router.get("/", (req, res) => {
    const model = buildFeedViewModel(req.auth.user, postStore.list());
    res.status(200).render("feed.njk", model);
  });

  router.post("/posts", (req, res) => {
    const input = requireValid(validateNewPost({ text: req.body?.text }));
    postStore.create({ text: input.text, authorId: req.auth.user.id });
    res.redirect(303, "/ssr");
  });

  router.post("/posts/:id/delete", (req, res) => {
    const result = postStore.deleteOwned(req.params.id, req.auth.user.id);
    if (result.status === "not-found") throw new HttpError(404, "post-not-found", "Post non trovato.");
    if (result.status === "forbidden") throw new HttpError(403, "forbidden", "Operazione non consentita.");
    res.redirect(303, "/ssr");
  });

  return router;
}
