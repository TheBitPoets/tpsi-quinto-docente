import { api } from "./api.js";

const authPanel = document.querySelector("#auth-panel");
const feedShell = document.querySelector("#feed-shell");
const userPanel = document.querySelector("#user-panel");
const currentUserLabel = document.querySelector("#current-user");
const logoutButton = document.querySelector("#logout-button");
const registerForm = document.querySelector("#register-form");
const loginForm = document.querySelector("#login-form");
const composerForm = document.querySelector("#composer-form");
const postList = document.querySelector("#post-list");
const alertBox = document.querySelector("#app-alert");
const status = document.querySelector("#app-status");

let currentUser = null;
let posts = [];

function showError(message) {
  alertBox.textContent = message;
  alertBox.className = "alert alert-danger";
  status.textContent = message;
}

function clearError() {
  alertBox.textContent = "";
  alertBox.className = "alert d-none";
}

function applyAuthState(user) {
  currentUser = user;
  const authenticated = Boolean(user);
  authPanel.classList.toggle("d-none", authenticated);
  feedShell.classList.toggle("d-none", !authenticated);
  userPanel.classList.toggle("d-none", !authenticated);
  userPanel.classList.toggle("d-flex", authenticated);
  currentUserLabel.textContent = user ? `${user.displayName} · ${user.email}` : "";
  if (!authenticated) {
    posts = [];
    postList.replaceChildren();
  }
}

function postElement(post) {
  const article = document.createElement("article");
  article.className = "card mb-3";
  article.dataset.postId = post.id;

  const body = document.createElement("div");
  body.className = "card-body";

  const heading = document.createElement("h3");
  heading.className = "h5";
  heading.textContent = post.author;

  const text = document.createElement("p");
  text.textContent = post.text;

  const actions = document.createElement("div");
  actions.className = "d-flex flex-wrap gap-2";

  const like = document.createElement("button");
  like.type = "button";
  like.dataset.action = "like";
  like.className = post.liked ? "btn btn-primary btn-sm" : "btn btn-outline-primary btn-sm";
  like.setAttribute("aria-pressed", String(post.liked));
  like.textContent = `Mi piace (${post.likes})`;
  actions.append(like);

  if (currentUser && post.authorId === currentUser.id) {
    const remove = document.createElement("button");
    remove.type = "button";
    remove.dataset.action = "delete";
    remove.className = "btn btn-outline-danger btn-sm";
    remove.textContent = "Elimina";
    actions.append(remove);
  }

  body.append(heading, text, actions);
  article.append(body);
  return article;
}

function renderPosts() {
  if (!posts.length) {
    const empty = document.createElement("p");
    empty.className = "border rounded p-3 text-body-secondary";
    empty.textContent = "Nessun post. Pubblica il primo.";
    postList.replaceChildren(empty);
    return;
  }
  postList.replaceChildren(...posts.map(postElement));
}

async function loadFeed() {
  posts = await api.getPosts();
  renderPosts();
  status.textContent = "Feed autenticato caricato.";
}

async function establishUser(payload) {
  applyAuthState(payload.user);
  await loadFeed();
}

registerForm.addEventListener("submit", async (event) => {
  event.preventDefault();
  clearError();
  const data = new FormData(registerForm);
  try {
    const payload = await api.register(
      String(data.get("displayName") ?? ""),
      String(data.get("email") ?? ""),
      String(data.get("password") ?? ""),
    );
    registerForm.reset();
    await establishUser(payload);
  } catch (error) {
    showError(error.message);
  }
});

loginForm.addEventListener("submit", async (event) => {
  event.preventDefault();
  clearError();
  const data = new FormData(loginForm);
  try {
    const payload = await api.login(
      String(data.get("email") ?? ""),
      String(data.get("password") ?? ""),
    );
    loginForm.reset();
    await establishUser(payload);
  } catch (error) {
    showError(error.message);
  }
});

logoutButton.addEventListener("click", async () => {
  clearError();
  try {
    await api.logout();
  } finally {
    applyAuthState(null);
    status.textContent = "Sessione terminata.";
  }
});

composerForm.addEventListener("submit", async (event) => {
  event.preventDefault();
  clearError();
  const data = new FormData(composerForm);
  const text = String(data.get("text") ?? "").trim();
  if (!text) return;
  try {
    const created = await api.createPost(text);
    posts = [created, ...posts];
    composerForm.reset();
    renderPosts();
  } catch (error) {
    showError(error.message);
  }
});

postList.addEventListener("click", async (event) => {
  if (!(event.target instanceof Element)) return;
  const button = event.target.closest("[data-action]");
  if (!button) return;
  const article = button.closest("[data-post-id]");
  const id = article?.dataset.postId;
  if (!id) return;

  const current = posts.find((post) => post.id === id);
  if (!current) return;
  clearError();

  try {
    if (button.dataset.action === "like") {
      const updated = await api.setLiked(id, !current.liked);
      posts = posts.map((post) => post.id === id ? updated : post);
    } else if (button.dataset.action === "delete") {
      await api.deletePost(id);
      posts = posts.filter((post) => post.id !== id);
    }
    renderPosts();
  } catch (error) {
    showError(error.message);
  }
});

async function boot() {
  clearError();
  try {
    const payload = await api.me();
    await establishUser(payload);
  } catch (error) {
    if (error.status === 401) {
      applyAuthState(null);
      status.textContent = "Accedi o registrati.";
      return;
    }
    showError(error.message);
  }
}

await boot();
