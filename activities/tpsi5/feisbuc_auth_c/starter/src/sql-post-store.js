import { randomUUID } from "node:crypto";

export class SqlPostStore {
  constructor({ db }) {
    this.db = db;
    // TODO: prepara query JOIN users, insert con author_id, like e delete ownership.
  }

  list({ liked } = {}) {
    void liked;
    return [];
  }

  create({ text, authorId }) {
    const id = randomUUID();
    void text;
    void authorId;
    throw new Error(`TODO create ${id}`);
  }

  setLiked(id, liked) {
    void id;
    void liked;
    return null;
  }

  deleteOwned(id, userId) {
    void id;
    void userId;
    return { status: "not-found" };
  }
}
