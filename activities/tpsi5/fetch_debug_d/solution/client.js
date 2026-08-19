const output = document.querySelector("#output");
const buttons = document.querySelectorAll("[data-case]");

const print = (value) => {
  output.textContent = typeof value === "string" ? value : JSON.stringify(value, null, 2);
};

async function readPayload(response) {
  if (response.status === 204 || response.status === 205) return null;

  const contentType = response.headers.get("content-type") ?? "";
  if (contentType.toLowerCase().includes("application/json")) {
    return response.json();
  }
  return response.text();
}

async function request(url, options) {
  const response = await fetch(url, options);
  const payload = await readPayload(response);

  if (!response.ok) {
    const message = payload && typeof payload === "object"
      ? payload.message ?? payload.error ?? `HTTP ${response.status}`
      : `HTTP ${response.status}`;
    const error = new Error(message);
    error.kind = "http";
    error.status = response.status;
    throw error;
  }

  return payload;
}

async function run(label, operation) {
  try {
    const result = await operation();
    print({ case: label, success: true, result });
  } catch (error) {
    if (error.kind === "http") {
      print({ case: label, success: false, kind: "http", status: error.status, message: error.message });
      return;
    }
    print({ case: label, success: false, kind: "network-or-runtime", message: error.message });
  }
}

async function loadMissing() {
  return request("/api/posts/missing");
}

async function createPost() {
  return request("/api/posts", {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({ text: "Nuovo post" })
  });
}

async function loadNoContent() {
  return request("/api/no-content");
}

buttons.forEach((button) => {
  button.addEventListener("click", () => {
    if (button.dataset.case === "missing") run("missing", loadMissing);
    if (button.dataset.case === "create") run("create", createPost);
    if (button.dataset.case === "empty") run("empty", loadNoContent);
  });
});
