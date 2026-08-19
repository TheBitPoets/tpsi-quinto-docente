import { Router } from "express";

export function createBrokenSsrRouter({ postStore }) {
  const router = Router();

  router.get("/", (req, res) => {
    res.render("feed.njk", {
      currentUser: req.auth?.user,
      posts: postStore.list(),
      secret: req.get("cookie"),
    });
  });

  router.post("/posts", (req, res) => {
    postStore.create({ text: req.body.text, authorId: req.body.authorId });
    res.status(200).render("feed.njk", { currentUser: req.auth.user, posts: postStore.list(), secret: "x" });
  });

  router.get("/posts/:id/delete", (req, res) => {
    postStore.deleteById?.(req.params.id);
    res.redirect(302, "/ssr");
  });

  return router;
}
