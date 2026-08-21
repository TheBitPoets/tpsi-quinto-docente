import { useState } from "react";
import { PostCard } from "./components/PostCard.jsx";

const initialPosts = [
  { id: "p1", text: "Primo post", liked: false, likes: 0, author: "Alice" },
  { id: "p2", text: "Secondo post", liked: true, likes: 3, author: "Bob" },
];

export default function App() {
  const [posts, setPosts] = useState(initialPosts);
  const currentUser = "Alice";

  function toggleLike(id) {
    setPosts((current) =>
      current.map((post) =>
        post.id === id
          ? {
              ...post,
              liked: !post.liked,
              likes: post.liked ? post.likes - 1 : post.likes + 1,
            }
          : post,
      ),
    );
  }

  function deletePost(id) {
    setPosts((current) => current.filter((post) => post.id !== id));
  }

  return (
    <main>
      <h1>React PostCard translation</h1>
      {posts.map((post) => (
        <PostCard
          key={post.id}
          post={post}
          canDelete={post.author === currentUser}
          onToggleLike={toggleLike}
          onDelete={deletePost}
        />
      ))}
    </main>
  );
}
