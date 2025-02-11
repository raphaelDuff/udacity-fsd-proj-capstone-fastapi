from fastapi import APIRouter, HTTPException, Request
from fastapi.params import Depends
from sqlalchemy import select
from sqlalchemy.orm import Session
from db.core import NotFoundError, get_db, Movie


router = APIRouter(
    prefix="/movies",
)


@router.get("/")
def create_item(session: Session = Depends(get_db)):
    stmt_select_all_movies = select(Movie).order_by(Movie.id)
    movies = session.scalars(stmt_select_all_movies).all()
    # if len(list_movies) == 0:
    #     abort(404)
    return [{"id": movie.id, "title": movie.title} for movie in movies]
