# Runbook — Feisbuc mirror 04

## Install
`python -m pip install -r requirements.txt`

## Development
`export FEISBUC_ENV=development`
`TODO: command prestart`
`python -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --workers 1`

## Production-like
Impostare `FEISBUC_ENV=production`, `FEISBUC_DATABASE_URL` e `FEISBUC_BUILD_SHA`. Eseguire prima `python -m app.prepare`, poi Uvicorn senza `--reload`.

## Verify
`python -m pytest -q tests`
`python tests/probe_live.py`
`python scripts/build_evidence.py --output evidence --build-sha <sha>`

## Operational probes
- `/health`: processo vivo, nessuna query DB.
- `/ready`: dipendenza DB/schema disponibile.

## Deliberate limits
No auth/session Python, Socket.IO Python, Alembic, PostgreSQL, async ORM, Docker Compose, Kubernetes, reverse proxy o TLS termination in questo mirror.
