import express from "express";

export function installVueSpa(app, { vueRoot }) {
  app.use("/vue", express.static(vueRoot));
  // TODO: aggiungi il GET fallback per tutte le route /vue/... usando
  // la sintassi wildcard nominata di Express 5 e sendFile(index.html).
}
