from fastapi.testclient import TestClient
from .main import app
from .dependencies import get_movies_db

client = TestClient(app)

def override_dependency():
    return [
        {
            "id": 1,
            "film":"(500) Days of Summer",
            "genre": "Comedy",
            "studio": "Fox",
            "score": 81,
            "year": 2009
        },
        {
            "id": 2,
            "film":"27 Dresses",
            "genre": "Comedy",
            "studio": "Fox",
            "score": 71,
            "year": 2008
        },
        {
            "id": 3,
            "film":"A Dangerous Method",
            "genre": "Drama",
            "studio": "Independent",
            "score": 89,
            "year": 2011
        },
    ]

app.dependency_overrides[get_movies_db] = override_dependency

def test_health():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["message"] == "ok"

def test_get_movie_by_id():
    response = client.get("/movie?id=1")
    assert response.status_code == 200
    assert response.json()["id"] == 1

    response = client.get("/movie?id=0")
    assert response.status_code == 404

def test_add_movie():
    new_movie = {
        "id": 4,
        "film": "The Accidental Superhero: Cape Not Included",
        "genre": "Drama",
        "studio": "Independent",
        "score": 99,
        "year": 1892,
    }

    response = client.post("/movie", json=new_movie)
    assert response.status_code == 200
    assert response.json()["message"] == "La película fue creada con éxito"

    new_movie["id"] = 1
    response = client.post("/movie", json=new_movie)
    assert response.status_code == 409

def test_get_movies():
    response = client.get("/movies?total=2&order=asc")
    data = response.json()
    assert response.status_code == 200
    assert len(data) == 2
    assert data[0]["id"] == 3 and data[1]["id"] == 2

    response = client.get("/movies?total=2&order=desc")
    data = response.json()
    assert response.status_code == 200
    assert len(data) == 2
    assert data[0]["id"] == 1 and data[1]["id"] == 2

    response = client.get("/movies?total=0&order=desc")
    data = response.json()
    assert response.status_code == 200
    assert len(data) == 0

    response = client.get("/movies?total=100&order=asc")
    data = response.json()
    assert response.status_code == 200
    assert len(data) == 3
    assert data[0]["id"] == 3

    response = client.get("/movies?total=100&order=desc")
    data = response.json()
    assert response.status_code == 200
    assert len(data) == 3
    assert data[0]["id"] == 1