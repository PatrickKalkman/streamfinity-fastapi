import os
import pytest
from sqlmodel import SQLModel

os.environ["TESTING"] = "1"

from streamfinity_fastapi.db import engine


@pytest.fixture(scope="session", autouse=True)
def create_test_database():
    # Create the test database tables
    SQLModel.metadata.create_all(engine)

    # Run the tests
    yield

    # Clean up (e.g., drop the test database tables)
    SQLModel.metadata.drop_all(engine)
