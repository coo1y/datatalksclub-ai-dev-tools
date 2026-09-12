from typing import Iterator

from sqlmodel import Session, SQLModel, create_engine

from app.config import DATABASE_URL

engine = create_engine(DATABASE_URL)


def create_db_and_tables() -> None:
    SQLModel.metadata.create_all(engine)


def get_session() -> Iterator[Session]:
    with Session(engine) as session:
        yield session
