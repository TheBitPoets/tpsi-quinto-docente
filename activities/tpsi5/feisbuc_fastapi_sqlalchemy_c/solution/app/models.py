from pydantic import BaseModel, Field, field_validator


class PostCreate(BaseModel):
    text: str = Field(min_length=1, max_length=280)

    @field_validator("text", mode="before")
    @classmethod
    def normalize_text(cls, value):
        return value.strip() if isinstance(value, str) else value


class PostLikePatch(BaseModel):
    liked: bool


class Post(BaseModel):
    id: str
    text: str
    authorId: str
    author: str
    liked: bool
    likes: int = Field(ge=0)
