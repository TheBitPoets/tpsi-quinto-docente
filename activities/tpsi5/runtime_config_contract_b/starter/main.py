import json
import sys

ALLOWED_ENVS = {"development", "test", "production"}
DEFAULT_DATABASE_URL = "sqlite:///./feisbuc-mirror.db"

def resolve_runtime_config(env):
    environment = str(env.get("FEISBUC_ENV", "development")).strip().lower()
    # TODO: validate environment
    database_url = env.get("FEISBUC_DATABASE_URL")
    if isinstance(database_url, str):
        database_url = database_url.strip() or None
    elif database_url is not None:
        database_url = None
    # TODO: production must fail fast without database URL
    database_url = database_url or DEFAULT_DATABASE_URL
    build_sha = env.get("FEISBUC_BUILD_SHA", "dev")
    build_sha = build_sha.strip() if isinstance(build_sha, str) else ""
    return {"ok": True, "environment": environment, "databaseUrl": database_url, "buildSha": build_sha or "dev"}

def main():
    payload = json.loads(sys.stdin.read() or "{}")
    env = payload.get("env", {})
    if not isinstance(env, dict):
        env = {}
    print(json.dumps(resolve_runtime_config(env), ensure_ascii=False, separators=(",", ":")))

if __name__ == "__main__":
    main()
