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
  const article = document.createElement("article");
  article.className = "card mb-3";
  article.dataset.postId = post.id;
  const body = document.createElement("div");
  body.className = "card-body";
  const heading = document.createElement("h3");
  heading.className = "card-title h5";
  heading.textContent = post.author;
  const text = document.createElement("p");
  text.className = "card-text";
  text.textContent = post.text;
  const likeButton = document.createElement("button");
  likeButton.type = "button";
  likeButton.dataset.action = "like";
  likeButton.className = post.liked ? "btn btn-primary" : "btn btn-outline-primary";
  likeButton.setAttribute("aria-pressed", String(post.liked));
  likeButton.textContent = `Mi piace (${post.likes})`;
  body.append(heading, text, likeButton);
  article.append(body);
  return article;
}

function renderPosts() {
  postList.setAttribute("aria-busy", "false");
  if (posts.length === 0) {
    const empty = document.createElement("p");
    empty.textContent = "Nessun post.";
    postList.replaceChildren(empty);
    return;
  }
  postList.replaceChildren(...posts.map(createPostElement));
}

function clearError() {
  alertBox.textContent = "";
  alertBox.className = "alert d-none";
}

function showError(message) {
  alertBox.textContent = message;
  alertBox.className = "alert alert-danger";
  status.textContent = message;
}

async function loadFeed() {
  postList.setAttribute("aria-busy", "true");
  clearError();
  try {
    posts = await api.getPosts();
    renderPosts();
    status.textContent = "Feed caricato.";
  } catch (error) {
    postList.setAttribute("aria-busy", "false");
    showError(error.message);
  }
}

form.addEventListener("submit", async (event) => {
  event.preventDefault();
  clearError();
  const data = new FormData(form);
  const text = String(data.get("text") ?? "").trim();
  if (!text) return showError("Scrivi un testo prima di pubblicare.");
  try {
    const created = await api.createPost(text);
    posts = [created, ...posts];
    renderPosts();
    form.reset();
    status.textContent = "Post persistito via API.";
  } catch (error) {
    showError(error.message);
  }
});

postList.addEventListener("click", async (event) => {
  if (!(event.target instanceof Element)) return;
  const button = event.target.closest("[data-action='like']");
  if (!button || !postList.contains(button)) return;
  const article = button.closest("[data-post-id]");
  const id = article?.dataset.postId;
  const current = posts.find((post) => post.id === id);
  if (!id || !current) return;
  clearError();
  try {
    const updated = await api.setLiked(id, !current.liked);
    posts = posts.map((post) => post.id === updated.id ? updated : post);
    renderPosts();
  } catch (error) {
    showError(error.message);
  }
});

await loadFeed();
