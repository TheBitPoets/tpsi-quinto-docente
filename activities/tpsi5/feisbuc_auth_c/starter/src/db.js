import { readFileSync } from "node:fs";
import { DatabaseSync } from "node:sqlite";

export function openDatabase({ dbPath, schemaPath }) {
  const db = new DatabaseSync(dbPath);
  db.exec("PRAGMA foreign_keys = ON;");
  db.exec("PRAGMA journal_mode = WAL;");
  db.exec(readFileSync(schemaPath, "utf8"));
  return db;
}
