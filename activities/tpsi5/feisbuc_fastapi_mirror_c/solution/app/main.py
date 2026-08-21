from fastapi import FastAPI, HTTPException, Response, status

from .models import Post, PostCreate, PostLikePatch
from .store import MemoryPostStore

app = FastAPI(
    title="Feisbuc FastAPI mirror",
    version="0.1.0",
    description="Mirror didattico del contratto posts; auth e persistence restano nel backend principale.",
)
post_store = MemoryPostStore()


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
