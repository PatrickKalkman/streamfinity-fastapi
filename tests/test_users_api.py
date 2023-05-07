from typing import Any, Generator

from fastapi import FastAPI
from fastapi.testclient import TestClient
from sqlmodel import Session, create_engine

from routers import users

TEST_DB_URL = "sqlite:///./test.db"

app = FastAPI()
app.include_router(users.router)

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


def test_create_user():
    user_data = {
        "email": "johndoe@example.com",
        "first_name": "John",
        "last_name": "Doe",
        "password": "supersecretpassword",
        "is_active": True
    }

    response = client.post("/api/users/", json=user_data)
    assert response.status_code == 201
    user = response.json()
    for key, value in user_data.items():
        if key != "password":  # Do not compare the password directly
            assert user[key] == value


def test_get_user():
    response = client.get("/api/users/1")
    assert response.status_code == 200
    user = response.json()
    assert user["email"] == "johndoe@example.com"
    assert user["first_name"] == "John"
    assert user["last_name"] == "Doe"
    assert user["is_active"]


def test_update_user():
    user_data = {"first_name": "Johnny", "last_name": "Doe",
                 "email": "johnnydoe@example.com", "is_active": False,
                 "password": "newpassword"}
    response = client.put("/api/users/1", json=user_data)
    assert response.status_code == 200
    user = response.json()
    assert user["first_name"] == "Johnny"


def test_delete_user():
    response = client.delete("/api/users/1")
    assert response.status_code == 204


def test_get_non_existent_user():
    response = client.get("/api/users/100")
    assert response.status_code == 404
