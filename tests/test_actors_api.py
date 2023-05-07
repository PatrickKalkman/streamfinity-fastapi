from typing import Any, Generator
from fastapi.testclient import TestClient
from fastapi import FastAPI
from sqlmodel import Session, create_engine

from routers import actors

TEST_DB_URL = "sqlite:///./test.db"

app = FastAPI()
app.include_router(actors.router)

engine = create_engine(
    TEST_DB_URL,
    echo=True,
    connect_args={"check_same_thread": False}
)


# Dependency for session injection
def get_session() -> Generator[Session, Any, None]:
    with Session(engine) as session:
        yield session


client = TestClient(app)


def test_create_actor():
    actor_data = {
        "first_name": "John",
        "last_name": "Doe",
        "date_of_birth": "1990-01-01",
        "nationality": "American"
    }

    response = client.post("/api/actors/", json=actor_data)
    assert response.status_code == 201
    actor = response.json()
    for key, value in actor_data.items():
        assert actor[key] == value


def test_get_actor():
    response = client.get("/api/actors/1")
    assert response.status_code == 200
    actor = response.json()
    assert actor["first_name"] == "John"
    assert actor["last_name"] == "Doe"
    assert actor["date_of_birth"] == "1990-01-01"
    assert actor["nationality"] == "American"


def test_update_actor():
    actor_data = {"first_name": "Johnny", "last_name": "Doe",
                  "date_of_birth": "1990-02-01", "nationality": "English"}
    response = client.put("/api/actors/1", json=actor_data)
    assert response.status_code == 200
    actor = response.json()
    assert actor["first_name"] == "Johnny"


def test_delete_actor():
    response = client.delete("/api/actors/1")
    assert response.status_code == 204


def test_get_non_existent_actor():
    response = client.get("/api/actors/100")
    assert response.status_code == 404
