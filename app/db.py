from typing import Any, Generator

from sqlmodel import Session, create_engine
import os

is_testing = os.environ.get("TESTING")

if is_testing:
    database_url = "sqlite:///../db/streamfinity_test.db"
else:
    database_url = "sqlite:///../db/streamfinity.db"


def get_engine():
    engine = create_engine(
        database_url,
        echo=True,
        connect_args={"check_same_thread": False})
    return engine


engine = get_engine()


def get_session() -> Generator[Session, Any, None]:
    with Session(engine) as session:
        yield session
