from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException, Response, status
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from .database import build_database
from .entities import PostRow
from .models import Post, PostCreate, PostLikePatch
from .settings import RuntimeSettings, load_settings
from .store import SqlAlchemyPostStore

def create_app(settings: RuntimeSettings | None = None) -> FastAPI:
    settings=settings or load_settings()
    engine, session_factory=build_database(settings.database_url)
    post_store=SqlAlchemyPostStore(session_factory)
    @asynccontextmanager
    async def lifespan(app: FastAPI):
        yield
        engine.dispose()
    app=FastAPI(title="Feisbuc runtime capstone mirror", version="0.4.0", description="Feature-neutral runtime capstone for the posts contract.", lifespan=lifespan)
    app.state.engine=engine; app.state.session_factory=session_factory; app.state.post_store=post_store; app.state.settings=settings
    # TODO /health and /ready
    @app.get("/api/posts", response_model=list[Post])
    def list_posts() -> list[dict]: return post_store.list()
    @app.post("/api/posts", response_model=Post, status_code=status.HTTP_201_CREATED)
    def create_post(command: PostCreate, response: Response) -> dict:
        post=post_store.create(command.text); response.headers["Location"]=f"/api/posts/{post['id']}"; return post
    @app.patch("/api/posts/{post_id}", response_model=Post)
    def set_liked(post_id: str, command: PostLikePatch) -> dict:
        post=post_store.set_liked(post_id, command.liked)
        if post is None: raise HTTPException(status_code=404, detail={"code":"post-not-found"})
        return post
    return app

app=create_app()
