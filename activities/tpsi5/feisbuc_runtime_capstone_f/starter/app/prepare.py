from .database import build_database
from .entities import Base
from .settings import load_settings
from .store import ensure_seed

def prepare_database(settings=None) -> None:
    settings=settings or load_settings()
    engine, session_factory=build_database(settings.database_url)
    try:
        Base.metadata.create_all(engine)
        ensure_seed(session_factory)
    finally:
        engine.dispose()

if __name__ == "__main__":
    prepare_database()
