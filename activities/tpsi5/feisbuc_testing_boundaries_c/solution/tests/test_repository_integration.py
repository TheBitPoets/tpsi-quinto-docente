from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.entities import Base
from app.store import SqlAlchemyPostStore


def test_repository_uses_real_sqlite_boundary(tmp_path):
    db_path = tmp_path / "repository.db"
    engine = create_engine(
        f"sqlite:///{db_path.as_posix()}",
        connect_args={"check_same_thread": False},
    )
    Base.metadata.create_all(engine)
    factory = sessionmaker(bind=engine, expire_on_commit=False)
    try:
        store = SqlAlchemyPostStore(factory)
        assert store.list() == []
        created = store.create("repository integration")
        assert created["id"] in {post["id"] for post in store.list()}
        assert db_path.is_file()
    finally:
        engine.dispose()
