import { randomUUID } from "node:crypto";

export class SqlAuthStore {
  constructor({ db }) {
    this.db = db;
    // TODO: prepara query user/session. Nessuna concatenazione di input esterno.
  }

  findCredentialByEmail(email) {
    throw new Error("TODO findCredentialByEmail");
  }

  findUserById(id) {
    throw new Error("TODO findUserById");
  }

  createUser({ email, displayName, passwordHash }) {
    const id = randomUUID();
    // TODO INSERT prepared + ritorno user pubblico.
    throw new Error(`TODO createUser ${id}`);
  }

  createSession({ idHash, userId, createdAt, expiresAt }) {
    throw new Error("TODO createSession");
  }

  findSessionUser(idHash, now = Date.now()) {
    return null;
  }

  deleteSession(idHash) {
    // TODO invalidazione server-side.
  }
}
