from uuid import uuid4
from sqlalchemy import select
from .entities import PostRow

def to_public_post(row: PostRow) -> dict:
    return {"id":row.id,"text":row.text,"authorId":row.author_id,"author":row.author,"liked":row.liked,"likes":row.likes}

def ensure_seed(session_factory) -> None:
    with session_factory() as session:
        if session.get(PostRow, "seed-1") is not None:
            return
        session.add(PostRow(id="seed-1", text="Post iniziale del mirror", author_id="mirror-user", author="Mirror Student", liked=False, likes=0))
        session.commit()

class SqlAlchemyPostStore:
    def __init__(self, session_factory): self._session_factory=session_factory
    def list(self) -> list[dict]:
        with self._session_factory() as session:
            rows=session.scalars(select(PostRow).order_by(PostRow.id)).all()
            return [to_public_post(row) for row in rows]
    def create(self, text: str) -> dict:
        with self._session_factory() as session:
            row=PostRow(id=str(uuid4()), text=text, author_id="mirror-user", author="Mirror Student", liked=False, likes=0)
            session.add(row); session.commit(); return to_public_post(row)
    def set_liked(self, post_id: str, liked: bool) -> dict | None:
        with self._session_factory() as session:
            row=session.get(PostRow, post_id)
            if row is None: return None
            if row.liked != liked:
                row.likes = row.likes + 1 if liked else max(0, row.likes - 1)
                row.liked=liked
            session.commit(); return to_public_post(row)
