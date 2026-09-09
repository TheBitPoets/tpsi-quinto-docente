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
  // TODO: se posts è vuoto mostra un messaggio esplicito.
  // Altrimenti sostituisci i figli di #post-list con gli article
  // creati da createPostElement.
}

function commitPosts(nextPosts, message) {
  // TODO: usa un solo punto per:
  // 1. rendere nextPosts il nuovo stato;
  // 2. salvare e controllare il booleano restituito da savePosts;
  // 3. renderizzare;
  // 4. aggiornare #feed-status, segnalando un eventuale errore di salvataggio.
}

form.addEventListener("submit", (event) => {
  // TODO:
  // 1. preventDefault
  // 2. FormData
  // 3. trim e validazione testo
  // 4. createPost
  // 5. usa commitPosts per confermare il nuovo stato
  // 6. form.reset e focus sul controllo text
});

postList.addEventListener("click", (event) => {
  // TODO: event delegation.
  // Cerca il button [data-action="like"] con closest().
  // Risali all'article [data-post-id].
  // Aggiorna lo state con toggleLike e passa il risultato a commitPosts.
});

renderPosts();
