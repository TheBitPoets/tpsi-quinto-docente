from uuid import uuid4

from sqlalchemy import Integer, String, create_engine
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column


class Base(DeclarativeBase):
    pass


class PostRow(Base):
    __tablename__ = "posts"

    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    text: Mapped[str] = mapped_column(String(280), nullable=False)
    likes: Mapped[int] = mapped_column(Integer, nullable=False, default=0)


# DIFETTO: nel progetto reale questa factory verrebbe chiamata dall'adapter
# per ogni operazione/request, ricreando infrastruttura e pool.
def make_store(database_url="sqlite:///./broken.db"):
    engine = create_engine(database_url)
    Base.metadata.create_all(engine)

    # DIFETTO: una Session viene creata una volta e riusata indefinitamente.
    session = Session(engine)

    class BrokenPostStore:
        def list(self):
            # DIFETTO: Query legacy come baseline 2.0.
            rows = session.query(PostRow).all()
            # DIFETTO: leakage dei dettagli ORM (_sa_instance_state).
            return [row.__dict__ for row in rows]

        def create(self, text):
            row = PostRow(id=str(uuid4()), text=text, likes=0)
            session.add(row)
            # DIFETTO: flush invia SQL nella transaction ma non la conferma.
            session.flush()
            return row.__dict__

        def create_with_bad_recovery(self, text):
            row = PostRow(id="fixed-id", text=text, likes=0)
            session.add(row)
            try:
                session.commit()
            except IntegrityError:
                # DIFETTO: la Session resta in failed transaction state.
                # Manca session.rollback().
                return None
            return row.__dict__

    return BrokenPostStore()
