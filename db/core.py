from dotenv import load_dotenv
from enum import Enum as PyEnum
import json
import os
from sqlalchemy import create_engine, Column, Date, Enum, ForeignKey, Integer, Table
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column,
    relationship,
    sessionmaker,
)


class NotFoundError(Exception):
    pass


class Base(DeclarativeBase):
    pass


actor_movie_association = Table(
    "actors_movies",
    Base.metadata,
    Column("actor_id", Integer, ForeignKey("actors.id"), primary_key=True),
    Column("movie_id", Integer, ForeignKey("movies.id"), primary_key=True),
)


class DBMovie(Base):
    __tablename__ = "movies"

    id: Mapped[int] = mapped_column(primary_key=True, index=True, autoincrement=True)
    title: Mapped[str] = mapped_column(nullable=False)
    release_date: Mapped[str] = mapped_column(Date, nullable=False)
    actors: Mapped[list["DBActor"]] = relationship(
        "DBActor", secondary=actor_movie_association, back_populates="movies"
    )

    def short(self):
        return {"id": self.id, "title": self.title, "release_date": self.release_date}

    def long(self):
        actors = []
        if len(self.actors) > 0:
            actors = [actor.id for actor in self.actors]
        return {
            "id": self.id,
            "title": self.title,
            "release_date": self.release_date,
            "actors": actors,
        }

    def __repr__(self):
        return json.dumps(self.short())


class Gender(PyEnum):
    MALE = "Male"
    FEMALE = "Female"


class DBActor(Base):
    __tablename__ = "actors"

    id: Mapped[int] = mapped_column(primary_key=True, index=True, autoincrement=True)
    name: Mapped[str] = mapped_column(nullable=False)
    age: Mapped[int] = mapped_column(nullable=False)
    gender: Mapped[Gender] = mapped_column(
        Enum(Gender, name="gender_enum"), nullable=False
    )
    movies: Mapped[list[DBMovie]] = relationship(
        "DBMovie", secondary=actor_movie_association, back_populates="actors"
    )

    def short(self):
        return {
            "id": self.id,
            "name": self.name,
            "age": self.age,
            "gender": self.gender.value,
        }

    def long(self):
        movies = []
        if len(self.movies) > 0:
            movies = [movie.id for movie in self.movies]
        return {
            "id": self.id,
            "name": self.name,
            "age": self.age,
            "gender": self.gender.value,
            "actors": movies,
        }

    def __repr__(self):
        return json.dumps(self.short())


load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL)
session_local = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)


# Dependency to get the database session
def get_db():
    database = session_local()
    try:
        yield database
    finally:
        database.close()
