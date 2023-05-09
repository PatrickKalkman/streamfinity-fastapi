from fastapi.testclient import TestClient
from fastapi import status
from app.streamfinity import app
from app.schemas.movie_actor_schema import ActorInput
from datetime import date

client = TestClient(app)

# Test data
test_actor = ActorInput(first_name="John",
                        last_name="Doe",
                        date_of_birth=date(1990, 1, 1),
                        nationality="American")

# A valid JWT token for testing generated by using a dummy secret key
access_token = (
    "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9."
    "eyJzdWIiOiJwa2Fsa2llMkBnbWFpbC5jb20iLCJleHAiOjE4NjM1NjkzMDZ9."
    "7_92eJtzh3v0VNBoUJZknyoQI1zxSWIEy_AG12RGmuc"
)


def create_actor():
    actor_data = test_actor.dict()
    actor_data["date_of_birth"] = test_actor.date_of_birth.isoformat()
    add_actor_response = client.post(
        "/api/actors/", json=actor_data,
        headers={"Authorization": f"Bearer {access_token}"})
    assert add_actor_response.status_code == status.HTTP_201_CREATED
    return add_actor_response.json()["id"]


def test_add_actor():
    actor_data = test_actor.dict()
    actor_data["date_of_birth"] = test_actor.date_of_birth.isoformat()
    response = client.post("/api/actors/", json=actor_data,
                           headers={"Authorization": f"Bearer {access_token}"})
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json()["first_name"] == test_actor.first_name
    assert response.json()["last_name"] == test_actor.last_name


def test_get_actor():
    # First, create an actor in the database and get its ID
    created_actor_id = create_actor()

    # Now, fetch the actor using the ID
    response = client.get(f"/api/actors/{created_actor_id}")
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["first_name"] == test_actor.first_name
    assert response.json()["last_name"] == test_actor.last_name


def test_get_actors():
    response = client.get("/api/actors/")
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) > 0


def test_update_actor():
    created_actor_id = create_actor()
    updated_actor = test_actor.copy(update={"first_name": "Jane"}).dict()
    updated_actor["date_of_birth"] = date(1990, 1, 1).isoformat()
    response = client.put(f"/api/actors/{created_actor_id}", json=updated_actor)
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["first_name"] == "Jane"


def test_delete_actor():
    created_actor_id = create_actor()
    response = client.delete(f"/api/actors/{created_actor_id}")
    assert response.status_code == status.HTTP_204_NO_CONTENT
