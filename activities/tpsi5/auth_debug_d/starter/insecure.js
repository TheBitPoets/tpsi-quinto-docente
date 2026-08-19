// CODICE DELIBERATAMENTE INSICURO — solo per Activity D.
import express from "express";
import { DatabaseSync } from "node:sqlite";

const app = express();
const db = new DatabaseSync("users.db");
app.use(express.json());

db.exec(`
  CREATE TABLE IF NOT EXISTS users(
    id TEXT PRIMARY KEY,
    email TEXT UNIQUE,
    password TEXT
  );
`);

app.post("/register", (req, res) => {
  const id = String(Date.now());
  db.prepare("INSERT INTO users(id,email,password) VALUES(?,?,?)")
    .run(id, req.body.email, req.body.password); // plaintext
  res.status(201).json({ id, email: req.body.email, password: req.body.password });
});

app.post("/login", (req, res) => {
  const user = db.prepare("SELECT * FROM users WHERE email = ?").get(req.body.email);
  if (!user) return res.status(404).json({ error: "email-not-found" });
  if (user.password !== req.body.password) return res.status(401).json({ error: "wrong-password" });

  const sessionId = user.id; // prevedibile e uguale all'user id
  res.cookie("sid", sessionId); // no HttpOnly/Secure/SameSite
  res.json({ user, sessionId }); // token e password esposti
});

app.post("/api/posts", (req, res) => {
  // Il client sceglie l'identita dell'autore.
  res.status(201).json({
    id: String(Date.now()),
    authorId: req.body.authorId,
    text: req.body.text,
  });
});

app.delete("/api/posts/:id", (req, res) => {
  // Il client dichiara chi e: nessuna sessione verificata.
  if (req.body.userId !== req.body.authorId) {
    return res.status(403).json({ error: "forbidden" });
  }
  res.status(204).end();
});

app.listen(3000);
