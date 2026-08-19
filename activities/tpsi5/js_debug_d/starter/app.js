const form = document.querySelector("#composer-form");
const feed = document.querySelector("#feed");
const status = document.querySelector("#status");
const STORAGE_KEY = "feisbuc.debug.posts";
let counter = 0;

function renderSavedPosts() {
  const saved = localStorage.getItem(STORAGE_KEY) || [];

  saved.forEach((post) => {
    appendPost(post.text, post.likes || 0);
  });
}

function appendPost(text, likes = 0) {
  const article = document.createElement("article");
  const heading = document.createElement("h2");
  const paragraph = document.createElement("p");
  const likeButton = document.createElement("button");

  article.id = `post_${counter}`;
  heading.textContent = `Post ${counter + 1}`;
  paragraph.innerHTML = text;
  likeButton.type = "button";
  likeButton.id = `like_button_${counter}`;
  likeButton.className = "like-button";
  likeButton.textContent = `Mi piace (${likes})`;

  article.append(heading, paragraph, likeButton);
  feed.append(article);
  counter += 1;
}

form.addEventListener("submit", (e) => {
  event.preventDefault();
  const textarea = document.querySelector("#post-text");
  appendPost(textarea.value);
  localStorage.setItem(STORAGE_KEY, { text: textarea.value, likes: 0 });
  textarea.value = "";
  status.textContent = "Post pubblicato";
});

const likeButtons = document.querySelectorAll(".like-button");
likeButtons.forEach((button) => {
  button.addEventListener("click", (e) => {
    const current = Number(e.target.textContent.match(/\d+/)?.[0] || 0);
    e.target.textContent = `Mi piace (${current + 1})`;
    e.target.disabled = true;
  });
});

renderSavedPosts();
