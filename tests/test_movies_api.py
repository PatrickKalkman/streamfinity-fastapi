from typing import Any, Generator
from fastapi import FastAPI
import pytest
from fastapi.testclient import TestClient
from sqlmodel import create_engine, Session

from schemas.movie_actor_schema import MovieInput, Movie

from routers import movies

TEST_DB_URL = "sqlite:///./test.db"

app = FastAPI()
app.include_router(movies.router)

engine = create_engine(
    TEST_DB_URL,
    echo=True,
    connect_args={"check_same_thread": False}
)


# Dependency for session injection
def get_session() -> Generator[Session, Any, None]:
    with Session(engine) as session:
        yield session


@pytest.fixture
def client():
    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture
def movie_input() -> MovieInput:
    return MovieInput(title="Test Movie", release_year=2022, length=120,
                      synopsis="Test Synopsis", director="Test Director",
                      genre="Test Genre", rating=5)


def test_create_movie(client: TestClient, movie_input: MovieInput):
    response = client.post("/api/movies/", json=movie_input.dict())
    assert response.status_code == 200
    movie = Movie.parse_obj(response.json())
    assert movie.id is not None
    assert movie.title == movie_input.title
    assert movie.release_year == movie_input.release_year


def test_get_movie(client: TestClient, movie_input: MovieInput):
    new_movie = client.post("/api/movies/", json=movie_input.dict()).json()
    movie_id = new_movie["id"]
    response = client.get(f"/api/movies/{movie_id}")
    assert response.status_code == 200
    movie = Movie.parse_obj(response.json())
    assert movie.id == movie_id
    assert movie.title == movie_input.title
    assert movie.release_year == movie_input.release_year


def test_get_movies(client: TestClient, movie_input: MovieInput):
    response = client.get("/api/movies/")
    assert response.status_code == 200
    movies = [Movie.parse_obj(movie) for movie in response.json()]
    assert len(movies) > 0


def test_update_movie(client: TestClient, movie_input: MovieInput):
    new_movie = client.post("/api/movies/", json=movie_input.dict()).json()
    movie_id = new_movie["id"]
    updated_title = "Updated Test Movie"
    response = client.put(f"/api/movies/{movie_id}",
                          json={"title": updated_title,
                                "release_year": movie_input.release_year,
                                "length": movie_input.length,
                                "synopsis": movie_input.synopsis,
                                "director": movie_input.director,
                                "genre": movie_input.genre,
                                "rating": movie_input.rating})
    assert response.status_code == 200
    movie = Movie.parse_obj(response.json())
    assert movie.id == movie_id
    assert movie.title == updated_title
    assert movie.release_year == movie_input.release_year


def test_delete_movie(client: TestClient, movie_input: MovieInput):
    new_movie = client.post("/api/movies/", json=movie_input.dict()).json()
    movie_id = new_movie["id"]
    response = client.delete(f"/api/movies/{movie_id}")
    assert response.status_code == 204
    response = client.get(f"/api/movies/{movie_id}")
    assert response.status_code == 404
