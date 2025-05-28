from fastapi import APIRouter, Depends
from ..dependencies import get_movies_db
from enum import Enum

router = APIRouter(
    prefix="/movies",
    tags=["movies"],
)

class Order(str, Enum):
    asc = "asc"
    desc = "desc"

@router.get("")
def get_movies(total: int, order: Order, db : list = Depends(get_movies_db)):
    if total <= 0:
        return []
    elif total > len(db):
        total = len(db)

    if order is Order.desc:
        return db[:total]
    else:
        db_len = len(db)
        return [db[db_len - i] for i in range(1, total + 1)]

    # movies = db if total > len(db) else db[:total]
    # return sorted(movies, key=lambda x: x["film"], reverse=True if order is Order.desc else False)