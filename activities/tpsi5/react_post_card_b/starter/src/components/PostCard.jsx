export function PostCard({ post, canDelete, onToggleLike, onDelete }) {
  return (
    <article>
      <p>{post.text}</p>
      <p>{post.likes} like</p>
      {/* TODO: traduci toggle-like e delete dal contratto Vue. */}
    </article>
  );
}
