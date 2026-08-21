from uuid import uuid4

from sqlalchemy import Integer, String, select
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, sessionmaker


class Base(DeclarativeBase):
    pass


class PostRow(Base):
    __tablename__ = "posts"

    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    text: Mapped[str] = mapped_column(String(280), nullable=False)
    likes: Mapped[int] = mapped_column(Integer, nullable=False, default=0)


def to_public_post(row: PostRow) -> dict:
    return {"id": row.id, "text": row.text, "likes": row.likes}


def make_store(engine):
    Base.metadata.create_all(engine)
    session_factory = sessionmaker(bind=engine, expire_on_commit=False)

    class PostStore:
        def list(self):
            with session_factory() as session:
                rows = session.scalars(select(PostRow)).all()
                return [to_public_post(row) for row in rows]

        def create(self, text):
            with session_factory() as session:
                row = PostRow(id=str(uuid4()), text=text, likes=0)
                session.add(row)
                session.commit()
                return to_public_post(row)

        def create_fixed_id(self, text):
            with session_factory() as session:
                row = PostRow(id="fixed-id", text=text, likes=0)
                session.add(row)
                try:
                    session.commit()
                except Exception:
                    session.rollback()
                    raise
                return to_public_post(row)

    return PostStore()
