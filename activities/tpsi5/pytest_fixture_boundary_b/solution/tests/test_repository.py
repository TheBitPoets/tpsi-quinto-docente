import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from repository import Base, SqlAlchemyPostStore


@pytest.fixture
def store(tmp_path):
    db_path = tmp_path / "posts.db"
    engine = create_engine(
        f"sqlite:///{db_path.as_posix()}",
        connect_args={"check_same_thread": False},
    )
    Base.metadata.create_all(engine)
    factory = sessionmaker(bind=engine, expire_on_commit=False)
    try:
        yield SqlAlchemyPostStore(factory)
    finally:
        engine.dispose()


def test_create_and_list(store):
    assert store.list() == []
    created = store.create("fixture")
    assert created["id"] in {p["id"] for p in store.list()}


def test_each_test_starts_empty(store):
    assert store.list() == []


@pytest.mark.parametrize(
    ("sequence", "expected"),
    [
        ([True], (True, 1)),
        ([True, True], (True, 1)),
        ([True, False], (False, 0)),
    ],
)
def test_like_transition_is_idempotent(store, sequence, expected):
    created = store.create("like")
    current = created
    for liked in sequence:
        current = store.set_liked(created["id"], liked)
        assert current is not None
    assert (current["liked"], current["likes"]) == expected
