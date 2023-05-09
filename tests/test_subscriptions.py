from typing import Any, Generator

from fastapi import FastAPI
from fastapi.testclient import TestClient
from sqlmodel import Session, create_engine

from app.routers import subscriptions

TEST_DB_URL = "sqlite:///./test.db"

app = FastAPI()
app.include_router(subscriptions.router)

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


def test_create_subscription():
    subscription_data = {
        "user_id": 1,
        "plan": "basic",
        "start_date": "2023-05-01",
        "is_active": True
    }

    response = client.post("/api/subscriptions/", json=subscription_data)
    assert response.status_code == 201
    subscription = response.json()
    for key, value in subscription_data.items():
        assert subscription[key] == value


def test_get_subscription():
    response = client.get("/api/subscriptions/1")
    assert response.status_code == 200
    subscription = response.json()
    assert subscription["user_id"] == 1
    assert subscription["plan"] == "basic"
    assert subscription["start_date"] == "2023-05-01"
    assert subscription["is_active"] is True


def test_update_subscription():
    subscription_data = {"user_id": 1, "plan": "premium",
                         "start_date": "2023-05-01", "is_active": False}
    response = client.put("/api/subscriptions/1", json=subscription_data)
    assert response.status_code == 200
    subscription = response.json()
    assert subscription["plan"] == "premium"
    assert subscription["is_active"] is False


def test_delete_subscription():
    response = client.delete("/api/subscriptions/1")
    assert response.status_code == 204


def test_get_non_existent_subscription():
    response = client.get("/api/subscriptions/100")
    assert response.status_code == 404
