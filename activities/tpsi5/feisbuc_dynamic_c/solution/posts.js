export function createPost(author, text) {
  return {
    id: crypto.randomUUID(),
    author,
    text,
    likes: 0,
    liked: false,
  };
}

export function toggleLike(posts, targetId) {
  return posts.map((post) => {
    if (post.id !== targetId) {
      return post;
    }

    const liked = !post.liked;
    const likes = liked ? post.likes + 1 : Math.max(0, post.likes - 1);

    return {
      ...post,
      liked,
      likes,
    };
  });
}
