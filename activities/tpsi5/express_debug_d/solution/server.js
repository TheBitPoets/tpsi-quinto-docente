import express, { Router } from "express";
import { fileURLToPath } from "node:url";
import path from "node:path";

const port = Number(process.env.PORT ?? 3000);
const here = path.dirname(fileURLToPath(import.meta.url));
const app = express();
const router = Router();

const posts = [
  { id: "p1", text: "Primo post", liked: false },
];

app.use(express.json());
app.use(express.static(path.resolve(here, "public")));

router.get("/", (req, res) => {
  res.json(posts);
});

router.post("/", (req, res) => {
  const text = typeof req.body?.text === "string" ? req.body.text.trim() : "";
  if (!text) {
    res.status(400).json({ error: { code: "text-required" } });
    return;
  }
  const post = { id: `p${posts.length + 1}`, text, liked: false };
  posts.push(post);
  res.status(201).json(post);
});

router.get("/explode", async (req, res) => {
  throw new Error("boom-async");
});

router.get("/:id", (req, res) => {
  const post = posts.find((item) => item.id === req.params.id);
  if (!post) {
    res.status(404).json({ error: { code: "post-not-found" } });
    return;
  }
  res.json(post);
});

app.use("/api/posts", router);

app.use((req, res) => {
  res.status(404).json({ error: { code: "not-found" } });
});

app.use((error, req, res, next) => {
  res.status(500).json({
    error: {
      code: "internal-error",
      message: error.message,
    },
  });
});

const server = app.listen(port, "127.0.0.1", () => {
  const address = server.address();
  console.log(`READY http://127.0.0.1:${address.port}`);
});
