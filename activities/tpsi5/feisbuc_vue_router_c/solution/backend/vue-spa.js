import express from "express";

export function installVueSpa(app, { vueRoot }) {
  app.use("/vue", express.static(vueRoot));
  app.get("/vue/{*splat}", (req, res) => {
    res.sendFile("index.html", { root: vueRoot });
  });
}
