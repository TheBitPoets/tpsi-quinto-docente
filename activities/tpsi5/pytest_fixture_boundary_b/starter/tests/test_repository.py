import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from repository import Base, SqlAlchemyPostStore


# TODO 1: trasformare questo helper in una fixture pytest function-scoped.
# TODO 2: usare tmp_path e un file SQLite diverso per ogni test.
# TODO 3: garantire engine.dispose() nel teardown anche se un assert fallisce.
def make_store():
    engine = create_engine("sqlite:///./shared-test.db", connect_args={"check_same_thread": False})
    Base.metadata.create_all(engine)
    factory = sessionmaker(bind=engine, expire_on_commit=False)
    return engine, SqlAlchemyPostStore(factory)


def test_create_and_list():
    engine, store = make_store()
    created = store.create("fixture")
    assert created["id"] in {p["id"] for p in store.list()}
    engine.dispose()


def test_starts_empty():
    engine, store = make_store()
    # Questo test puo dipendere da quello precedente: correggi il boundary.
    assert store.list() == []
    engine.dispose()
