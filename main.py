from fastapi import FastAPI
from contextlib import asynccontextmanager
from .utils import extract_csv_data
from .routers import movie, movies
from .dependencies import movies_db

@asynccontextmanager
async def lifespan(app: FastAPI):
    extract_csv_data("./static/movies.csv", movies_db)
    yield
    movies_db.clear()

app = FastAPI(lifespan=lifespan)
app.include_router(movie.router)
app.include_router(movies.router)

@app.get("/")
async def root():
    return {"message": "ok"}