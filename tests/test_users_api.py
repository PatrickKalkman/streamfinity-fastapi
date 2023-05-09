from fastapi.testclient import TestClient
from sqlmodel import Session
from app.streamfinity import app
from app.db import engine
from app.schemas.user_schema import User, UserInput

client = TestClient(app)


def create_user(session: Session):
    user_input = UserInput(email="testuser@example.com",
                           password="testpassword", first_name="Test",
                           last_name="User")

    new_user = User.from_orm(user_input)
    session.add(new_user)
    session.commit()
    session.refresh(new_user)
    return new_user


def test_get_user():
    with Session(engine) as session:
        test_user = create_user(session)
        response = client.get(f"/api/users/{test_user.id}")
    assert response.status_code == 200
    assert response.json()["email"] == "testuser@example.com"


def test_get_users():
    with Session(engine) as session:
        create_user(session)
        response = client.get("/api/users", params={"email": "testuser@example.com"})
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["email"] == "testuser@example.com"


def test_add_user():
    user_data = {"email": "newuser@example.com", "password": "newpassword"}
    response = client.post("/api/users", json=user_data)
    assert response.status_code == 201
    assert response.json()["email"] == "newuser@example.com"


def test_delete_user():
    with Session(engine) as session:
        test_user = create_user(session)
        response = client.delete(f"/api/users/{test_user.id}")
    assert response.status_code == 204


def test_update_user():
    with Session(engine) as session:
        test_user = create_user(session)
        updated_user_data = {"email": "updateduser@example.com",
                             "password": "updatedpassword"}
        response = client.put(f"/api/users/{test_user.id}", json=updated_user_data)
    assert response.status_code == 200
    assert response.json()["email"] == "updateduser@example.com"
