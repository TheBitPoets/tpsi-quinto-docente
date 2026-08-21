from sqlalchemy import Boolean, CheckConstraint, Integer, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class PostRow(Base):
    __tablename__ = "posts"
    __table_args__ = (
        CheckConstraint("length(trim(text)) BETWEEN 1 AND 280", name="ck_posts_text_length"),
        CheckConstraint("likes >= 0", name="ck_posts_likes_nonnegative"),
    )

    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    text: Mapped[str] = mapped_column(String(280), nullable=False)
    author_id: Mapped[str] = mapped_column(String(64), nullable=False)
    author: Mapped[str] = mapped_column(String(120), nullable=False)
    liked: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    likes: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
