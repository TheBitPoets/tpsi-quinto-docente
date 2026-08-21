from dataclasses import dataclass
import os

ALLOWED_ENVS={"development","test","production"}
DEFAULT_DATABASE_URL="sqlite:///./feisbuc-mirror.db"

class RuntimeConfigError(ValueError):
    pass

@dataclass(frozen=True)
class RuntimeSettings:
    environment: str
    database_url: str
    build_sha: str

def load_settings(environ=None) -> RuntimeSettings:
    env=os.environ if environ is None else environ
    environment=str(env.get("FEISBUC_ENV","development")).strip().lower()
    if environment not in ALLOWED_ENVS:
        raise RuntimeConfigError("invalid FEISBUC_ENV")
    raw_db=env.get("FEISBUC_DATABASE_URL")
    database_url=raw_db.strip() if isinstance(raw_db,str) and raw_db.strip() else None
    if environment=="production" and not database_url:
        raise RuntimeConfigError("FEISBUC_DATABASE_URL is required in production")
    build=env.get("FEISBUC_BUILD_SHA","dev")
    build_sha=build.strip() if isinstance(build,str) and build.strip() else "dev"
    return RuntimeSettings(environment, database_url or DEFAULT_DATABASE_URL, build_sha)
