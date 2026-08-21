from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from app.entities import PostRow

def add_operational_routes(app: FastAPI, engine, session_factory, build_sha: str):
    @app.get("/health")
    def health():
        return {"status":"ok","build":build_sha}
    @app.get("/ready")
    def ready():
        try:
            with session_factory() as session:
                session.execute(select(PostRow.id).limit(1)).first()
        except SQLAlchemyError:
            raise HTTPException(status_code=503, detail={"code":"not-ready"})
        return {"status":"ready","build":build_sha}
