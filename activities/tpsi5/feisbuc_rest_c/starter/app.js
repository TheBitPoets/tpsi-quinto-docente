import { createApi } from "./api.js";

const api = createApi();
const form = document.querySelector("#composer-form");
const postList = document.querySelector("#post-list");
const status = document.querySelector("#feed-status");
const alertBox = document.querySelector("#feed-alert");

if (!form || !postList || !status || !alertBox) {
  throw new Error("Markup Feisbuc incompleto");
}

let posts = [];

function createPostElement(post) {
  // TODO: riusa il pattern DOM della milestone 3.
  const article = document.createElement("article");
  article.className = "card mb-3";
  article.dataset.postId = post.id;
  return article;
}

function renderPosts() {
  // TODO: renderizza lo stato senza leggere dati da localStorage.
}

function showError(message) {
  alertBox.textContent = message;
  alertBox.className = "alert alert-danger";
  status.textContent = message;
}

async function loadFeed() {
  // TODO: loading state -> api.getPosts() -> state -> render -> error handling.
}

form.addEventListener("submit", async (event) => {
  event.preventDefault();
  // TODO: crea un post via HTTP e aggiorna lo stato locale dalla representation restituita.
});

postList.addEventListener("click", async (event) => {
  // TODO: event delegation come in UDA 22, ma il cambio like passa da PATCH HTTP.
});

await loadFeed();
