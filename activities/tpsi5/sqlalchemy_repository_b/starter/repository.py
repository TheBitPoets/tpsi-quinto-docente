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
        # TODO B1: apri una Session dalla factory, esegui select(PostRow)
        # e restituisci una lista di dict pubblici.
        raise NotImplementedError

    def create(self, text: str) -> dict:
        # TODO B2: costruisci PostRow con identity server-side,
        # session.add(row), commit e ritorna to_public_post(row).
        raise NotImplementedError

    def set_liked(self, post_id: str, liked: bool) -> dict | None:
        # TODO B3: Session.get(PostRow, post_id), None se manca.
        # Cambia likes solo quando cambia liked; poi commit.
        raise NotImplementedError
