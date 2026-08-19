import { randomUUID } from "node:crypto";

const toPublicUser = (row) => row ? {
  id: row.id,
  email: row.email,
  displayName: row.display_name,
} : null;

export class SqlAuthStore {
  constructor({ db }) {
    this.db = db;
    this.statements = {
      userByEmail: db.prepare(`
        SELECT id, email, display_name, password_hash
        FROM users
        WHERE email = ?
      `),
      userById: db.prepare(`
        SELECT id, email, display_name
        FROM users
        WHERE id = ?
      `),
      insertUser: db.prepare(`
        INSERT INTO users(id, email, display_name, password_hash)
        VALUES(?, ?, ?, ?)
      `),
      insertSession: db.prepare(`
        INSERT INTO sessions(id_hash, user_id, created_at, expires_at)
        VALUES(?, ?, ?, ?)
      `),
      sessionUser: db.prepare(`
        SELECT
          sessions.id_hash,
          sessions.expires_at,
          users.id,
          users.email,
          users.display_name
        FROM sessions
        JOIN users ON users.id = sessions.user_id
        WHERE sessions.id_hash = ? AND sessions.expires_at > ?
      `),
      deleteSession: db.prepare(`DELETE FROM sessions WHERE id_hash = ?`),
      deleteExpired: db.prepare(`DELETE FROM sessions WHERE expires_at <= ?`),
    };
  }

  findCredentialByEmail(email) {
    const row = this.statements.userByEmail.get(email);
    return row ? {
      user: toPublicUser(row),
      passwordHash: row.password_hash,
    } : null;
  }

  findUserById(id) {
    return toPublicUser(this.statements.userById.get(id));
  }

  createUser({ email, displayName, passwordHash }) {
    const id = randomUUID();
    this.statements.insertUser.run(id, email, displayName, passwordHash);
    return this.findUserById(id);
  }

  createSession({ idHash, userId, createdAt, expiresAt }) {
    this.statements.deleteExpired.run(createdAt);
    this.statements.insertSession.run(idHash, userId, createdAt, expiresAt);
  }

  findSessionUser(idHash, now = Date.now()) {
    const row = this.statements.sessionUser.get(idHash, now);
    if (!row) return null;
    return {
      idHash: row.id_hash,
      expiresAt: Number(row.expires_at),
      user: toPublicUser(row),
    };
  }

  deleteSession(idHash) {
    this.statements.deleteSession.run(idHash);
  }
}
