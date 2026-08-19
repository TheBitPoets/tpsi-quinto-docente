const output = document.querySelector("#output");
const buttons = document.querySelectorAll("[data-case]");

const print = (value) => {
  output.textContent = typeof value === "string" ? value : JSON.stringify(value, null, 2);
};

async function loadMissing() {
  try {
    const response = await fetch("/api/posts/missing");
    const payload = await response.json();
    print({ success: true, payload });
  } catch (error) {
    print(`Network error: ${error.message}`);
  }
}

async function createBroken() {
  try {
    const response = await fetch("/api/posts", {
      method: "POST",
      headers: {
        "Content-Type": "text/plain"
      },
      body: { text: "Nuovo post" }
    });
    const payload = await response.json();
    print(payload);
  } catch (error) {
    print(`Network error: ${error.message}`);
  }
}

async function parseNoContent() {
  try {
    const response = await fetch("/api/no-content");
    const payload = await response.json();
    print(payload);
  } catch (error) {
    print(`Network error: ${error.message}`);
  }
}

buttons.forEach((button) => {
  button.addEventListener("click", () => {
    if (button.dataset.case === "missing") loadMissing();
    if (button.dataset.case === "create") createBroken();
    if (button.dataset.case === "empty") parseNoContent();
  });
});
