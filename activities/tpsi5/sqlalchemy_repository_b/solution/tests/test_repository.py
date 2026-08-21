from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from repository import Base, SqlAlchemyPostStore


def make_store():
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(engine)
    factory = sessionmaker(bind=engine, expire_on_commit=False)
    return engine, SqlAlchemyPostStore(factory)


def test_repository_create_list_like_and_missing():
    engine, store = make_store()
    try:
        assert store.list() == []

        created = store.create("repository")
        assert created["text"] == "repository"
        assert created["authorId"] == "mirror-user"
        assert created["liked"] is False
        assert created["likes"] == 0

        listed = {post["id"]: post for post in store.list()}
        assert created["id"] in listed

        liked = store.set_liked(created["id"], True)
        assert liked is not None
        assert liked["liked"] is True
        assert liked["likes"] == 1

        repeated = store.set_liked(created["id"], True)
        assert repeated is not None
        assert repeated["likes"] == 1

        unliked = store.set_liked(created["id"], False)
        assert unliked is not None
        assert unliked["liked"] is False
        assert unliked["likes"] == 0

        assert store.set_liked("missing", True) is None
    finally:
        engine.dispose()
