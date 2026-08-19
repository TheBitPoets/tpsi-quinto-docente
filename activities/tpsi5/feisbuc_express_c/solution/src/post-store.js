import { randomUUID } from "node:crypto";

const clone = (post) => ({ ...post });

export class MemoryPostStore {
  constructor(seed = []) {
    this.posts = seed.map(clone);
  }

  list({ liked } = {}) {
    const values = typeof liked === "boolean"
      ? this.posts.filter((post) => post.liked === liked)
      : this.posts;
    return values.map(clone);
  }

  create({ text, author = "Studente" }) {
    const post = {
      id: randomUUID(),
      author,
      text,
      likes: 0,
      liked: false,
    };
    this.posts.unshift(post);
    return clone(post);
  }

  setLiked(id, liked) {
    const index = this.posts.findIndex((post) => post.id === id);
    if (index < 0) {
      return null;
    }

    const current = this.posts[index];
    const likes = liked === current.liked
      ? current.likes
      : liked
        ? current.likes + 1
        : Math.max(0, current.likes - 1);

    const updated = {
      ...current,
      liked,
      likes,
    };
    this.posts[index] = updated;
    return clone(updated);
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
