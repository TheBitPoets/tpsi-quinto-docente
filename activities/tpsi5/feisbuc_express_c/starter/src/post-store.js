import { randomUUID } from "node:crypto";

export class MemoryPostStore {
  constructor(seed = []) {
    this.posts = seed.map((post) => ({ ...post }));
  }

  list({ liked } = {}) {
    // TODO: restituisci copie dei post; applica filtro liked quando boolean.
    return [];
  }

  create({ text, author = "Studente" }) {
    // TODO: crea id server-side e salva il post.
    throw new Error("TODO create");
  }

  setLiked(id, liked) {
    // TODO: aggiorna liked/likes e restituisci copia; null se id non esiste.
    return null;
  }
}

export const seedPosts = [
  {
    id: "seed-1",
    author: "Docente",
    text: "Feisbuc ora usa Express dietro lo stesso contratto HTTP.",
    likes: 1,
    liked: false,
  },
];
