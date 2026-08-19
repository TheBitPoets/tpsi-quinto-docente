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

  const actions = document.createElement("div");
  actions.className = "d-flex flex-wrap gap-2";

  const likeButton = document.createElement("button");
  likeButton.type = "button";
  likeButton.dataset.action = "like";
  likeButton.className = post.liked
    ? "btn btn-primary"
    : "btn btn-outline-primary";
  likeButton.setAttribute("aria-pressed", String(post.liked));
  likeButton.textContent = `Mi piace (${post.likes})`;

  actions.append(likeButton);
  body.append(heading, text, actions);
  article.append(body);
  return article;
}

function renderPosts() {
  if (posts.length === 0) {
    const empty = document.createElement("p");
    empty.className = "text-body-secondary border rounded p-3";
    empty.textContent = "Nessun post. Pubblica il primo messaggio.";
    postList.replaceChildren(empty);
    return;
  }

  postList.replaceChildren(...posts.map(createPostElement));
}

function commitPosts(nextPosts, message) {
  posts = nextPosts;
  savePosts(posts);
  renderPosts();
  status.textContent = message;
}

form.addEventListener("submit", (event) => {
  event.preventDefault();

  const data = new FormData(form);
  const text = String(data.get("text") ?? "").trim();

  if (!text) {
    status.textContent = "Scrivi un testo prima di pubblicare.";
    return;
  }

  const post = createPost("Studente", text);
  commitPosts([post, ...posts], "Post pubblicato.");
  form.reset();
});

postList.addEventListener("click", (event) => {
  if (!(event.target instanceof Element)) {
    return;
  }

  const likeButton = event.target.closest("[data-action='like']");
  if (!likeButton || !postList.contains(likeButton)) {
    return;
  }

  const article = likeButton.closest("[data-post-id]");
  const postId = article?.dataset.postId;
  if (!postId) {
    return;
  }

  commitPosts(toggleLike(posts, postId), "Like aggiornato.");
});

renderPosts();
