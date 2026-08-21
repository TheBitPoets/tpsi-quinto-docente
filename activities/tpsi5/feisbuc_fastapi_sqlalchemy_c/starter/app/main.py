import os

from fastapi import FastAPI, HTTPException, Response, status

from .database import build_database
from .models import Post, PostCreate, PostLikePatch
from .store import SqlAlchemyPostStore, ensure_seed


def create_app(database_url: str) -> FastAPI:
    engine, session_factory = build_database(database_url)
    ensure_seed(session_factory)
    post_store = SqlAlchemyPostStore(session_factory)

    app = FastAPI(
        title="Feisbuc FastAPI SQLAlchemy mirror",
        version="0.2.0",
        description="Mirror didattico persistente del contratto posts.",
    )
    app.state.engine = engine

    @app.get("/api/posts", response_model=list[Post])
    def list_posts() -> list[dict]:
        return post_store.list()

    @app.post("/api/posts", response_model=Post, status_code=status.HTTP_201_CREATED)
    def create_post(command: PostCreate, response: Response) -> dict:
        post = post_store.create(command.text)
        response.headers["Location"] = f"/api/posts/{post['id']}"
        return post

    @app.patch("/api/posts/{post_id}", response_model=Post)
    def set_liked(post_id: str, command: PostLikePatch) -> dict:
        post = post_store.set_liked(post_id, command.liked)
        if post is None:
            raise HTTPException(status_code=404, detail={"code": "post-not-found"})
        return post

    return app


app = create_app(os.getenv("DATABASE_URL", "sqlite:///./feisbuc-mirror.db"))
