let input = "";

process.stdin.setEncoding("utf8");
process.stdin.on("data", (chunk) => {
  input += chunk;
});
process.stdin.on("end", () => {
  const { posts, targetId } = JSON.parse(input);
  const result = toggleLike(posts, targetId);
  console.log(JSON.stringify(result));
});

function toggleLike(posts, targetId) {
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
