const form = document.querySelector("#composer-form");
const feed = document.querySelector("#feed");
const status = document.querySelector("#status");
const STORAGE_KEY = "feisbuc.debug.posts";

if (!form || !feed || !status) {
  throw new Error("Markup Feisbuc incompleto");
}

let posts = loadPosts();

function loadPosts() {
  try {
    const raw = localStorage.getItem(STORAGE_KEY);
    if (!raw) {
      return [];
    }
    const value = JSON.parse(raw);
    return Array.isArray(value) ? value : [];
  } catch (error) {
    console.error("Storage non leggibile", error);
    return [];
  }
}

function savePosts() {
  localStorage.setItem(STORAGE_KEY, JSON.stringify(posts));
}

function createPost(text) {
  return {
    id: crypto.randomUUID(),
    text,
    likes: 0,
    liked: false,
  };
}

function toggleLike(targetId) {
  posts = posts.map((post) => {
    if (post.id !== targetId) {
      return post;
    }

    const liked = !post.liked;
    return {
      ...post,
      liked,
      likes: liked ? post.likes + 1 : Math.max(0, post.likes - 1),
    };
  });
}

function createPostElement(post, index) {
  const article = document.createElement("article");
  article.dataset.postId = post.id;

  const heading = document.createElement("h2");
  heading.textContent = `Post ${index + 1}`;

  const paragraph = document.createElement("p");
  paragraph.textContent = post.text;

  const likeButton = document.createElement("button");
  likeButton.type = "button";
  likeButton.dataset.action = "like";
  likeButton.setAttribute("aria-pressed", String(post.liked));
  likeButton.textContent = `Mi piace (${post.likes})`;

  article.append(heading, paragraph, likeButton);
  return article;
}

function renderPosts() {
  feed.replaceChildren(...posts.map(createPostElement));
}

function commit(nextStatus) {
  savePosts();
  renderPosts();
  status.textContent = nextStatus;
}

form.addEventListener("submit", (event) => {
  event.preventDefault();

  const data = new FormData(form);
  const text = String(data.get("text") ?? "").trim();
  if (!text) {
    status.textContent = "Scrivi un testo.";
    return;
  }

  posts = [createPost(text), ...posts];
  commit("Post pubblicato.");
  form.reset();
});

feed.addEventListener("click", (event) => {
  if (!(event.target instanceof Element)) {
    return;
  }

  const button = event.target.closest("[data-action='like']");
  if (!button || !feed.contains(button)) {
    return;
  }

  const article = button.closest("[data-post-id]");
  const postId = article?.dataset.postId;
  if (!postId) {
    return;
  }

  toggleLike(postId);
  commit("Like aggiornato.");
});

renderPosts();
