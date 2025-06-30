from typing import Any, Generator

from sqlmodel import create_engine, SQLModel, Session

from app.configs.settings import settings

DATABASE_URL = settings.DATABASE_URL

engine = create_engine(url=DATABASE_URL, echo=bool(settings.DEBUG))


def init_db() -> None:
    SQLModel.metadata.create_all(engine)


def get_session() -> Generator[Session, Any, None]:
    with Session(engine) as session:
        yield session
