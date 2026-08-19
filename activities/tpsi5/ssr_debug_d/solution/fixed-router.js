router.get("/", requireAuth, (req, res) => {
  res.render("feed.njk", buildFeedViewModel(req.auth.user, postStore.list()));
});

router.post("/posts", requireAuth, (req, res) => {
  const input = requireValid(validateNewPost({ text: req.body.text }));
  postStore.create({ text: input.text, authorId: req.auth.user.id });
  res.redirect(303, "/ssr");
});

router.post("/posts/:id/delete", requireAuth, (req, res) => {
  const result = postStore.deleteOwned(req.params.id, req.auth.user.id);
  if (result.status === "forbidden") throw new HttpError(403, "forbidden", "Operazione non consentita.");
  if (result.status === "not-found") throw new HttpError(404, "post-not-found", "Post non trovato.");
  res.redirect(303, "/ssr");
});
