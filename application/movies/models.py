from application import db, sql_like_key
from application.models import Base
from application.genres.models import Genre

from sqlalchemy.sql import text
import sys

Cast = db.Table('movie_cast',
                db.Column('actor_id', db.Integer, db.ForeignKey('actor.id'), primary_key=True),
                db.Column('movie_id', db.Integer, db.ForeignKey('movie.id'), primary_key=True))


class Movie(Base):
    __tablename__ = "movie"

    name = db.Column(db.String(144), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    genre_id = db.Column(db.Integer, db.ForeignKey('genre.id'), nullable=False)
    runtime = db.Column(db.Integer, nullable=False)

    ratings = db.relationship('Rating', backref='movie', lazy=True)
    actors = db.relationship('Actor', secondary=Cast, backref='movies', lazy=True)

    def __init__(self, name, year, genre_id, runtime):
        self.name = name
        self.year = year
        self.genre_id = genre_id
        self.runtime = runtime

    def get_genre(self):
        return Genre.query.get(self.genre_id)

    @staticmethod
    def apply_filter(stmt):
        res = db.engine.execute(stmt)

        movies = []
        for row in res:
            m = Movie(row[1], row[2], row[3], row[4])
            m.id = row[0]
            movies.append(m)

        return movies

    @staticmethod
    def get_movies_by_title(title_filter):
        filter_value = title_filter or ""
        filter_value = filter_value.strip()

        stmt = text("SELECT DISTINCT movie.id, movie.name, movie.year, movie.genre_id, movie.runtime FROM movie"
                    " WHERE movie.name " + sql_like_key + " :filter_value"
                    " ORDER BY movie.name"
                    ).params(filter_value='%' + filter_value + '%')

        return Movie.apply_filter(stmt)

    @staticmethod
    def get_movies_by_genre(genre_id):
        stmt = text("SELECT DISTINCT movie.id, movie.name, movie.year, movie.genre_id, movie.runtime FROM movie"
                    " WHERE movie.genre_id = :filter_value"
                    " ORDER BY movie.name"
                    ).params(filter_value=genre_id)

        return Movie.apply_filter(stmt)

    @staticmethod
    def get_movies_by_actor(actor_filter):
        filter_value = actor_filter or ""
        filter_value = filter_value.strip()

        stmt = text("SELECT DISTINCT movie.id, movie.name, movie.year, movie.genre_id, movie.runtime FROM movie"
                    " JOIN movie_cast ON movie_id=movie.id"
                    " JOIN actor ON actor_id=actor.id"
                    " WHERE actor.name " + sql_like_key + " :filter_value"
                    " ORDER BY movie.name"
                    ).params(filter_value='%' + filter_value + '%')

        return Movie.apply_filter(stmt)

    @staticmethod
    def get_movies_by_year(min_year, max_year):
        filter_min = min_year or 0
        filter_max = max_year or sys.maxsize

        stmt = text("SELECT DISTINCT movie.id, movie.name, movie.year, movie.genre_id, movie.runtime FROM movie"
                    " WHERE movie.year BETWEEN :filter_min AND :filter_max"
                    " ORDER BY movie.name"
                    ).params(filter_min=filter_min, filter_max=filter_max)

        return Movie.apply_filter(stmt)

    @staticmethod
    def get_movies_by_rating(min_rating, max_rating):
        filter_min = min_rating or 0
        filter_max = max_rating or 10

        stmt = text("SELECT m.id, m.name, m.year, m.genre_id, m.runtime,"
                    " ROUND(m.average, 1) as average FROM "
                    "(SELECT movie.id, movie.name, movie.year, movie.genre_id, movie.runtime,"
                    "AVG(rating.rating) as average FROM movie"
                    " JOIN rating ON rating.movie_id = movie.id"
                    " WHERE rating.rating IS NOT NULL"
                    " GROUP BY movie.id) as m"
                    " WHERE m.average BETWEEN :filter_min AND :filter_max"
                    " ORDER BY m.name").params(filter_min=int(filter_min), filter_max=int(filter_max))

        return Movie.apply_filter(stmt)
