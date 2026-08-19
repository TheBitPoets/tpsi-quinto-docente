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

router.get("/", (req, res) => {
  res.json(posts);
});

router.post("/", (req, res) => {
  const text = req.body.text.trim();
  const post = { id: `p${posts.length + 1}`, text, liked: false };
  posts.push(post);
  res.status(201).json(post);
});

router.get("/create", (req, res) => {
  const post = {
    id: `p${posts.length + 1}`,
    text: String(req.query.text ?? "Creato via GET"),
    liked: false,
  };
  posts.push(post);
  res.status(200).json(post);
});

router.get("/explode", async (req, res) => {
  throw new Error("boom-async");
});

router.get("/:id", (req, res) => {
  const post = posts.find((item) => item.id === req.query.id);
  if (!post) {
    res.status(404).json({ error: "post-not-found" });
    return;
  }
  res.json(post);
});

app.use("/api/posts", router);

// BUG: il parser arriva troppo tardi per le route sopra.
app.use(express.json());

// BUG: il 404 intercetta anche i file statici.
app.use((req, res) => {
  res.status(404).json({ error: "not-found" });
});

app.use(express.static(path.resolve(here, "public")));

// BUG: tre parametri, quindi non e un error-handling middleware Express.
app.use((error, req, res) => {
  res.status(500).json({ error: error.message });
});

const server = app.listen(port, "127.0.0.1", () => {
  const address = server.address();
  console.log(`READY http://127.0.0.1:${address.port}`);
});
