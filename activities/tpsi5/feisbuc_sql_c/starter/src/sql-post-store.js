import { randomUUID } from "node:crypto";
import { readFileSync } from "node:fs";
import { DatabaseSync } from "node:sqlite";

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

    // TODO: prepara qui statement riutilizzabili per:
    // - list all
    // - list by liked
    // - select by id
    // - insert seed idempotente
    // - insert nuovo post
    // - update atomico liked/likes

    // TODO: applica il seed con INSERT OR IGNORE e binding.
  }

  list({ liked } = {}) {
    // TODO: restituisci oggetti dominio e converti liked 0/1 -> boolean.
    return [];
  }

  create({ text, author = "Studente" }) {
    const id = randomUUID();
    // TODO: INSERT bindato e SELECT dello stato canonico.
    throw new Error(`TODO create ${id} ${author} ${text}`);
  }

  setLiked(id, liked) {
    // TODO: UPDATE mirato con binding; null se id non esiste.
    return null;
  }

  close() {
    this.db.close();
  }
}

export function openSqlPostStore({ dbPath, schemaPath, seed = seedPosts }) {
  const schemaSql = readFileSync(schemaPath, "utf-8");
  return new SqlPostStore({ dbPath, schemaSql, seed });
}
