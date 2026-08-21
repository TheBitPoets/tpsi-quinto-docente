from sqlalchemy import Boolean, Integer, String, create_engine, select
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column
from sqlalchemy.pool import StaticPool


class Base(DeclarativeBase):
    pass


class PostRow(Base):
    __tablename__ = "posts"

    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    text: Mapped[str] = mapped_column(String(280), nullable=False)
    liked: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    likes: Mapped[int] = mapped_column(Integer, nullable=False, default=0)


engine = create_engine(
    "sqlite://",
    echo=True,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

print("\n--- METADATA / CREATE TABLE ---")
Base.metadata.create_all(engine)

print("\n--- NEW OBJECT / INSERT ---")
with Session(engine) as session:
    row = PostRow(id="p1", text="Primo post ORM", liked=False, likes=0)
    session.add(row)
    print("pending before commit:", row in session.new)
    session.commit()
    print("pending after commit:", row in session.new)

print("\n--- NEW SESSION / SELECT ---")
with Session(engine) as session:
    statement = select(PostRow).where(PostRow.id == "p1")
    row = session.scalar(statement)
    assert row is not None
    print(
        {
            "id": row.id,
            "text": row.text,
            "liked": row.liked,
            "likes": row.likes,
        }
    )

print("\nOsserva nell'echo: CREATE TABLE, INSERT, COMMIT, SELECT e i boundary della Session.")
