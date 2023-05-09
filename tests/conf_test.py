import pytest
from sqlmodel import SQLModel, create_engine
from app.db import get_session


@pytest.fixture(scope="session", autouse=True)
def create_test_database():
    engine = create_engine(
        "sqlite:///./db/streamfinity_test.db",
        echo=True,
        connect_args={"check_same_thread": False}
    )

    SQLModel.metadata.create_all(engine)

    yield

    SQLModel.metadata.drop_all(engine)


@pytest.fixture(scope="function", autouse=True)
def db_session():
    with get_session() as session:
        yield session
