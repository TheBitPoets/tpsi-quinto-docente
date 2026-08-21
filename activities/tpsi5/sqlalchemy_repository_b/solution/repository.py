from uuid import uuid4

from sqlalchemy import Boolean, Integer, String, select
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class PostRow(Base):
    __tablename__ = "posts"

    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    text: Mapped[str] = mapped_column(String(280), nullable=False)
    author_id: Mapped[str] = mapped_column(String(64), nullable=False)
    author: Mapped[str] = mapped_column(String(120), nullable=False)
    liked: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    likes: Mapped[int] = mapped_column(Integer, nullable=False, default=0)


def to_public_post(row: PostRow) -> dict:
    return {
        "id": row.id,
        "text": row.text,
        "authorId": row.author_id,
        "author": row.author,
        "liked": row.liked,
        "likes": row.likes,
    }


class SqlAlchemyPostStore:
    def __init__(self, session_factory):
        self._session_factory = session_factory

    def list(self) -> list[dict]:
        with self._session_factory() as session:
            rows = session.scalars(select(PostRow)).all()
            return [to_public_post(row) for row in rows]

    def create(self, text: str) -> dict:
        with self._session_factory() as session:
            row = PostRow(
                id=str(uuid4()),
                text=text,
                author_id="mirror-user",
                author="Mirror Student",
                liked=False,
                likes=0,
            )
            session.add(row)
            session.commit()
            return to_public_post(row)

    def set_liked(self, post_id: str, liked: bool) -> dict | None:
        with self._session_factory() as session:
            row = session.get(PostRow, post_id)
            if row is None:
                return None
            if row.liked != liked:
                row.likes += 1 if liked else -1
                row.liked = liked
            session.commit()
            return to_public_post(row)
