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
    if len(movies) == 0:
        raise HTTPException(status_code=404, detail=f"No movies were found!")
    return {"success": True, "movies": [movie.short() for movie in movies]}


@router.get("/details/{movie_id}")
def get_movie_detail(movie_id: int, session: Session = Depends(get_db)):
    stmt_movie_by_id = select(Movie).where(Movie.id == movie_id)
    selected_movie = session.scalars(stmt_movie_by_id).one_or_none()
    if selected_movie is None:
        raise HTTPException(
            status_code=404, detail=f"Movie id={movie_id} was not found!"
        )
    return {"success": True, "movies": selected_movie.long()}
