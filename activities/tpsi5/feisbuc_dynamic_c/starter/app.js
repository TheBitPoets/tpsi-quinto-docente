import { createPost, toggleLike } from "./posts.js";
import { loadPosts, savePosts } from "./storage.js";

const form = document.querySelector("#composer-form");
const postList = document.querySelector("#post-list");
const status = document.querySelector("#feed-status");

if (!form || !postList || !status) {
  throw new Error("Markup Feisbuc incompleto");
}

let posts = loadPosts();

function createPostElement(post) {
  // TODO: crea un article Bootstrap semanticamente corretto.
  // Usa data-post-id, h3, p con textContent e un button
  // data-action="like" con aria-pressed.
  return document.createElement("article");
}

function renderPosts() {
  // TODO: se posts e vuoto mostra un messaggio esplicito.
  // Altrimenti sostituisci i figli di #post-list con gli article
  // creati da createPostElement.
}

form.addEventListener("submit", (event) => {
  // TODO:
  // 1. preventDefault
  // 2. FormData
  // 3. trim e validazione testo
  // 4. createPost
  // 5. aggiorna posts
  // 6. savePosts + renderPosts + form.reset
});

postList.addEventListener("click", (event) => {
  // TODO: event delegation.
  // Cerca il button [data-action="like"] con closest().
  // Risali all'article [data-post-id].
  // Aggiorna lo state con toggleLike, salva e renderizza.
});

renderPosts();
