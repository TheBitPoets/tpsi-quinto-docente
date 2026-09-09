const apiBase = document.querySelector("#api-base");
const status = document.querySelector("#status");
const output = document.querySelector("#output");

const cases = {
  list: ["/api/posts", {}],
  missing: ["/api/posts/missing", {}],
  create: ["/api/posts", {
    method: "POST",
    headers: { "Content-Type": "application/json", Accept: "application/json" },
    body: JSON.stringify({ text: "Post dal browser" })
  }],
  "wrong-type": ["/api/posts", {
    method: "POST",
    headers: { "Content-Type": "text/plain" },
    body: JSON.stringify({ text: "Media type errato" })
  }],
  delete: ["/api/posts", { method: "DELETE" }]
};

document.addEventListener("click", async (event) => {
  const button = event.target.closest("[data-case]");
  if (!button) return;

  const [path, options] = cases[button.dataset.case];
  const url = new URL(path, apiBase.value).toString();
  status.textContent = `Invio ${options.method ?? "GET"} ${url}`;
  output.textContent = "Attendo la risposta…";

  try {
    const response = await fetch(url, options);
    const body = await response.text();
    output.textContent = JSON.stringify({
      ok: response.ok,
      status: response.status,
      contentType: response.headers.get("content-type"),
      allow: response.headers.get("allow"),
      body
    }, null, 2);
    status.textContent = "Response ricevuta: verifica lo scambio in Network.";
  } catch (error) {
    output.textContent = JSON.stringify({ kind: "fetch-rejection", message: error.message }, null, 2);
    status.textContent = "Nessuna Response esposta allo script: controlla Console e Network.";
  }
});
