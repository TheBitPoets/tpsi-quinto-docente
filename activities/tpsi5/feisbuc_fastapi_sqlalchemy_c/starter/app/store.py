from uuid import uuid4

from sqlalchemy import select

from .entities import PostRow


def to_public_post(row: PostRow) -> dict:
    return {
        "id": row.id,
        "text": row.text,
        "authorId": row.author_id,
        "author": row.author,
        "liked": row.liked,
        "likes": row.likes,
    }


def ensure_seed(session_factory) -> None:
    with session_factory() as session:
        if session.get(PostRow, "seed-1") is not None:
            return
        session.add(
            PostRow(
                id="seed-1",
                text="Post iniziale del mirror",
                author_id="mirror-user",
                author="Mirror Student",
                liked=False,
                likes=0,
            )
        )
        session.commit()


class SqlAlchemyPostStore:
    def __init__(self, session_factory):
        self._session_factory = session_factory

    def list(self) -> list[dict]:
        # TODO C1: select(PostRow), session.scalars(...).all(), mapping pubblico.
        raise NotImplementedError

    def create(self, text: str) -> dict:
        # TODO C2: costruisci PostRow, add, commit, mapping pubblico.
        raise NotImplementedError

    def set_liked(self, post_id: str, liked: bool) -> dict | None:
        # TODO C3: Session.get, None se manca, transizione idempotente, commit.
        raise NotImplementedError
