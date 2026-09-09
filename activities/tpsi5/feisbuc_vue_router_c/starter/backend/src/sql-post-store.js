import { randomUUID } from "node:crypto";

const SELECT_COLUMNS = `
  posts.id,
  posts.author_id,
  users.display_name AS author,
  posts.text,
  posts.likes,
  posts.liked,
  posts.created_at
`;

const toPost = (row) => row ? {
  id: row.id,
  authorId: row.author_id,
  author: row.author,
  text: row.text,
  likes: Number(row.likes),
  liked: Boolean(row.liked),
  createdAt: row.created_at,
} : null;

export class SqlPostStore {
  constructor({ db }) {
    this.db = db;
    this.statements = {
      listAll: db.prepare(`
        SELECT ${SELECT_COLUMNS}
        FROM posts
        JOIN users ON users.id = posts.author_id
        ORDER BY posts.created_at DESC, posts.id DESC
      `),
      listLiked: db.prepare(`
        SELECT ${SELECT_COLUMNS}
        FROM posts
        JOIN users ON users.id = posts.author_id
        WHERE posts.liked = ?
        ORDER BY posts.created_at DESC, posts.id DESC
      `),
      byId: db.prepare(`
        SELECT ${SELECT_COLUMNS}
        FROM posts
        JOIN users ON users.id = posts.author_id
        WHERE posts.id = ?
      `),
      ownerById: db.prepare(`SELECT author_id FROM posts WHERE id = ?`),
      insertPost: db.prepare(`
        INSERT INTO posts(id, author_id, text, likes, liked)
        VALUES(?, ?, ?, 0, 0)
      `),
      setLiked: db.prepare(`
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
      deleteById: db.prepare(`DELETE FROM posts WHERE id = ?`),
    };
  }

  list({ liked } = {}) {
    const rows = typeof liked === "boolean"
      ? this.statements.listLiked.all(liked ? 1 : 0)
      : this.statements.listAll.all();
    return rows.map(toPost);
  }

  create({ text, authorId }) {
    const id = randomUUID();
    this.statements.insertPost.run(id, authorId, text);
    return toPost(this.statements.byId.get(id));
  }

  setLiked(id, liked) {
    const flag = liked ? 1 : 0;
    const result = this.statements.setLiked.run(flag, flag, flag, id);
    if (Number(result.changes) === 0) return null;
    return toPost(this.statements.byId.get(id));
  }

  deleteOwned(id, userId) {
    const owner = this.statements.ownerById.get(id);
    if (!owner) return { status: "not-found" };
    if (owner.author_id !== userId) return { status: "forbidden" };
    this.statements.deleteById.run(id);
    return { status: "deleted" };
  }
}
