from typing import Optional
from pydantic import BaseModel
from sqlalchemy import Date, select
from sqlalchemy.orm import Session
from .core import DBMovie, NotFoundError, DBActor


class Movie(BaseModel):
    id: int
    title: str
    release_date: str
    actors: list[int] = []


def read_db_movies(session: Session) -> list[DBMovie]:
    stmt_select_all_movies = select(DBMovie).order_by(DBMovie.id)
    movies = session.scalars(stmt_select_all_movies).all()
    if len(movies) == 0:
        raise NotFoundError(f"No (zero) movies were found.")
    return movies


def read_db_movie(movie_id: int, session: Session) -> DBMovie:
    stmt_movie_by_id = select(DBMovie).where(DBMovie.id == movie_id)
    selected_movie = session.scalars(stmt_movie_by_id).one_or_none()
    if selected_movie is None:
        raise NotFoundError(f"Movie id={movie_id} was not found!")
    return selected_movie
