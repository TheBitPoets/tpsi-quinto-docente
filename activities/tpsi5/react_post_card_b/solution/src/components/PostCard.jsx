export function PostCard({ post, canDelete, onToggleLike, onDelete }) {
  return (
    <article>
      <p>{post.text}</p>
      <p>{post.likes} like</p>

      <button type="button" onClick={() => onToggleLike(post.id)}>
        {post.liked ? "Togli like" : "Like"}
      </button>

      {canDelete ? (
        <button type="button" onClick={() => onDelete(post.id)}>
          Elimina
        </button>
      ) : null}
    </article>
  );
}
