from uuid import uuid4

from fastapi import FastAPI, Response, status
from pydantic import BaseModel, Field, field_validator

app = FastAPI(title="TPSI5 FastAPI microscope", version="1.0.0")


class PostCreate(BaseModel):
    text: str = Field(min_length=1, max_length=280)

    @field_validator("text", mode="before")
    @classmethod
    def normalize_text(cls, value):
        return value.strip() if isinstance(value, str) else value


class Post(BaseModel):
    id: str
    text: str
    liked: bool = False
    likes: int = 0


posts: list[Post] = [Post(id="p1", text="Primo post")]


@app.get("/api/posts", response_model=list[Post])
def list_posts() -> list[Post]:
    return posts


@app.post("/api/posts", response_model=Post, status_code=status.HTTP_201_CREATED)
def create_post(command: PostCreate, response: Response) -> Post:
    post = Post(id=str(uuid4()), text=command.text)
    posts.insert(0, post)
    response.headers["Location"] = f"/api/posts/{post.id}"
    return post
