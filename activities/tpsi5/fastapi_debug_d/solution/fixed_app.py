from uuid import uuid4

from fastapi import FastAPI, HTTPException, Response, status
from pydantic import BaseModel, Field, field_validator

app = FastAPI()


class PostCreate(BaseModel):
    text: str = Field(min_length=1, max_length=280)

    @field_validator("text", mode="before")
    @classmethod
    def normalize_text(cls, value):
        return value.strip() if isinstance(value, str) else value


class Post(BaseModel):
    id: str
    text: str
    authorId: str
    author: str
    liked: bool
    likes: int


posts = {
    "p1": {
        "id": "p1",
        "text": "seed",
        "authorId": "server-user",
        "author": "Server User",
        "liked": False,
        "likes": 0,
        "internalSecret": "resta interno",
    }
}


@app.post("/api/posts", response_model=Post, status_code=status.HTTP_201_CREATED)
def create_post(command: PostCreate, response: Response):
    post = {
        "id": str(uuid4()),
        "text": command.text,
        "authorId": "server-user",
        "author": "Server User",
        "liked": False,
        "likes": 0,
        "internalSecret": "resta interno",
    }
    posts[post["id"]] = post
    response.headers["Location"] = f"/api/posts/{post['id']}"
    return post


@app.get("/api/posts/{post_id}", response_model=Post)
def get_post(post_id: str):
    post = posts.get(post_id)
    if post is None:
        raise HTTPException(status_code=404, detail={"code": "post-not-found"})
    return post
