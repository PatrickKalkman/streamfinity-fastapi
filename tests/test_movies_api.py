from streamfinity_fastapi.schemas.movie_actor_schema import MovieInput
from streamfinity_fastapi.streamfinity import app
from fastapi import status
from fastapi.testclient import TestClient

client = TestClient(app)

# Test data
test_movie = MovieInput(
    title="Test Movie",
    length=120,
    synopsis="A test movie",
    release_year=2022,
    director="John Doe",
    genre="Action",
    rating=8,
)


def create_movie():
    response = client.post("/api/movies/", json=test_movie.dict())
    assert response.status_code == status.HTTP_201_CREATED
    return response.json()["id"]


def test_create_movie():
    response = client.post("/api/movies/", json=test_movie.dict())
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json()["title"] == test_movie.title
    assert response.json()["director"] == test_movie.director


def test_get_movie():
    movie_id = create_movie()
    response = client.get(f"/api/movies/{movie_id}")
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["title"] == test_movie.title
    assert response.json()["director"] == test_movie.director


def test_get_movies():
    response = client.get("/api/movies/")
    assert response.status_code == status.HTTP_200_OK
    assert isinstance(response.json(), list)


def test_update_movie():
    movie_id = create_movie()
    updated_movie = test_movie.copy(update={"title": "Updated Test Movie"}).dict()
    response = client.put(f"/api/movies/{movie_id}", json=updated_movie)
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["title"] == "Updated Test Movie"


def test_delete_movie():
    movie_id = create_movie()
    response = client.delete(f"/api/movies/{movie_id}")
    assert response.status_code == status.HTTP_204_NO_CONTENT
