from fastapi.testclient import TestClient

from streamfinity import app


client = TestClient(app)


def test_get_movies():
    response = client.get("/api/movies/")
    assert response.status_code == 200
    movies = response.json()
    assert all(["title" in m for m in movies])
