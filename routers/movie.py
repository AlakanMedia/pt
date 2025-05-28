from fastapi import APIRouter, Depends, HTTPException
from ..dependencies import get_movies_db
from pydantic import BaseModel

router = APIRouter(
    prefix="/movie",
    tags=["movie"],
)

class Movie(BaseModel):
    id: int
    film: str
    genre: str
    studio: str
    score: int
    year: int

@router.get("")
def get_movie_by_id(id: int, db : list = Depends(get_movies_db)):
    for movie in db:
        if movie["id"] == id:
            return movie

    raise HTTPException(status_code=404, detail=f"Película con id igual a '{id}' no fue encontrada.")

@router.post("")
def add_movie(new_movie: Movie, db : list = Depends(get_movies_db)):
    for movie in db:
        if movie["id"] == new_movie.id:
            raise HTTPException(status_code=409, detail=f"Película con id igual a '{new_movie.id}' ya existe.")

    db.append(new_movie.model_dump())
    return {"message": "La película fue creada con éxito"}