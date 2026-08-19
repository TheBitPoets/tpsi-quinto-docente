import { randomUUID } from "node:crypto";
import { readFileSync } from "node:fs";
import { DatabaseSync } from "node:sqlite";

const COLUMNS = "id, author, text, likes, liked, created_at";

const toPost = (row) => row ? {
  id: row.id,
  author: row.author,
  text: row.text,
  likes: Number(row.likes),
  liked: Boolean(row.liked),
  createdAt: row.created_at,
} : null;

export const seedPosts = [
  {
    id: "seed-1",
    author: "Docente",
    text: "Feisbuc ora persiste i post con SQL raw.",
    likes: 1,
    liked: false,
  },
];

export class SqlPostStore {
  constructor({ dbPath = ":memory:", schemaSql, seed = seedPosts }) {
    this.db = new DatabaseSync(dbPath);
    this.db.exec("PRAGMA foreign_keys = ON;");
    this.db.exec(schemaSql);

    this.statements = {
      listAll: this.db.prepare(`
        SELECT ${COLUMNS}
        FROM posts
        ORDER BY created_at DESC, id DESC
      `),
      listLiked: this.db.prepare(`
        SELECT ${COLUMNS}
        FROM posts
        WHERE liked = ?
        ORDER BY created_at DESC, id DESC
      `),
      byId: this.db.prepare(`
        SELECT ${COLUMNS}
        FROM posts
        WHERE id = ?
      `),
      insertSeed: this.db.prepare(`
        INSERT OR IGNORE INTO posts(id, author, text, likes, liked)
        VALUES(?, ?, ?, ?, ?)
      `),
      insertPost: this.db.prepare(`
        INSERT INTO posts(id, author, text, likes, liked)
        VALUES(?, ?, ?, 0, 0)
      `),
      setLiked: this.db.prepare(`
        UPDATE posts
        SET
          likes = CASE
            WHEN liked = ? THEN likes
            WHEN ? = 1 THEN likes + 1
            WHEN likes > 0 THEN likes - 1
            ELSE 0
          END,
          liked = ?
        WHERE id = ?
      `),
    };

    for (const post of seed) {
      this.statements.insertSeed.run(
        post.id,
        post.author,
        post.text,
        post.likes,
        post.liked ? 1 : 0,
      );
    }
  }

  list({ liked } = {}) {
    const rows = typeof liked === "boolean"
      ? this.statements.listLiked.all(liked ? 1 : 0)
      : this.statements.listAll.all();
    return rows.map(toPost);
  }

  create({ text, author = "Studente" }) {
    const id = randomUUID();
    this.statements.insertPost.run(id, author, text);
    return toPost(this.statements.byId.get(id));
  }

  setLiked(id, liked) {
    const flag = liked ? 1 : 0;
    const result = this.statements.setLiked.run(flag, flag, flag, id);
    if (Number(result.changes) === 0) {
      return null;
    }
    return toPost(this.statements.byId.get(id));
  }

  close() {
    this.db.close();
  }
}

export function openSqlPostStore({ dbPath, schemaPath, seed = seedPosts }) {
  const schemaSql = readFileSync(schemaPath, "utf-8");
  return new SqlPostStore({ dbPath, schemaSql, seed });
}
