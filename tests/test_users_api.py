from fastapi.testclient import TestClient
from streamfinity_fastapi.streamfinity import app
from streamfinity_fastapi.schemas.user_schema import UserInput


client = TestClient(app)

# Test data
test_user = UserInput(
    email="pkalkie2@gmail.com",
    password="test_password",
    first_name="Test",
    last_name="User",
    is_active=True
)


def create_user() -> dict:
    response = client.post("/api/users/", json=test_user.dict())
    return response.json()


def test_add_user():
    response = client.post("/api/users/", json=test_user.dict())
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == test_user.email


def test_get_user():
    user = create_user()
    user_id = user["id"]

    response = client.get(f"/api/users/{user_id}")
    assert response.status_code == 200
    assert response.json()["email"] == test_user.email


def test_get_users():
    create_user()

    response = client.get("/api/users/")
    assert response.status_code == 200
    users = response.json()
    assert len(users) > 0
    assert users[0]["email"] == test_user.email


def test_update_user():
    user = create_user()
    user_id = user["id"]

    updated_user = test_user.copy(update={"email": "updated@example.com"})
    response = client.put(f"/api/users/{user_id}", json=updated_user.dict())
    assert response.status_code == 200
    assert response.json()["email"] == "updated@example.com"


def test_delete_user():
    user = create_user()
    user_id = user["id"]

    response = client.delete(f"/api/users/{user_id}")
    assert response.status_code == 204

    response = client.get(f"/api/users/{user_id}")
    assert response.status_code == 404
