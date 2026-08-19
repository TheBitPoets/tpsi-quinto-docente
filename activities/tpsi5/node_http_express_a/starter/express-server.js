import express from "express";

const port = Number(process.env.PORT ?? 3000);
const app = express();

app.disable("x-powered-by");
app.use(express.json({ limit: "32kb" }));

app.get("/api/health", (req, res) => {
  res.status(200).json({ ok: true, server: "express" });
});

app.post("/api/echo", (req, res) => {
  res.status(200).json({ received: req.body });
});

app.use((req, res) => {
  res.status(404).json({ error: "not-found" });
});

app.use((error, req, res, next) => {
  const status = error.type === "entity.parse.failed" ? 400 : 500;
  res.status(status).json({
    error: status === 400 ? "invalid-json" : "internal-error",
  });
});

const server = app.listen(port, "127.0.0.1", () => {
  const address = server.address();
  console.log(`READY http://127.0.0.1:${address.port}`);
});
