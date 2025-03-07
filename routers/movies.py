from fastapi import APIRouter, HTTPException, Request
from fastapi.params import Depends
from sqlalchemy import select
from sqlalchemy.orm import Session
from db.core import NotFoundError, get_db, DBMovie
from db.movies import read_db_movies, read_db_movie, Movie


router = APIRouter(
    prefix="/movies",
)


@router.get("/")
def get_movies(session: Session = Depends(get_db)):
    try:
        movies = read_db_movies(session)
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=f"No (zero) movies were found!")
    return {"success": True, "movies": [movie.short() for movie in movies]}


# @router.post("/")
# def post_movies(session: Session = Depends(get_db)):
#     try:
#             data_json = request.get_json()
#             if not data_json:
#                 abort(400)

#             data_json_movie_title = data_json.get("title", None)
#             data_json_release_date = data_json.get("release_date", None)
#             data_json_actors = data_json.get("actors", None)

#             if (
#                 data_json_movie_title is None
#                 or data_json_release_date is None
#                 or data_json_actors is None
#             ):
#                 abort(400)

#             release_date_datetime = datetime.strptime(
#                 str(data_json_release_date), "%d-%m-%Y"
#             )

#             actors = []

#             if len(data_json_actors) > 0:
#                 stmt_select_actors_by_ids = select(Actor).where(
#                     Actor.id.in_(data_json_actors)
#                 )
#                 actors = session.scalars(stmt_select_actors_by_ids).all()

#             new_movie = Movie(
#                 title=data_json_movie_title,
#                 release_date=release_date_datetime,
#                 actors=actors,
#             )
#             session.add(new_movie)
#             session.commit()

#             return (
#                 jsonify({"success": True, "movie": new_movie.long()}),
#                 200,
#             )
#         except SQLAlchemyError as e:
#             db.session.rollback()
#             abort(500)
#         finally:
#             db.session.close()


@router.get("/details/{movie_id}")
def get_movie_details(movie_id: int, session: Session = Depends(get_db)):
    try:
        movie = read_db_movie(movie_id, session)
    except NotFoundError as e:
        raise HTTPException(
            status_code=404, detail=f"Movie id={movie_id} was not found!"
        )
    return {"success": True, "movies": movie.long()}
