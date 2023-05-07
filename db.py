from typing import Any, Generator

from sqlmodel import Session, create_engine

engine = create_engine(
    "sqlite:///./db/streamfinity.db",
    echo=True,
    connect_args={"check_same_thread": False}
)


def get_session() -> Generator[Session, Any, None]:
    with Session(engine) as session:
        yield session
