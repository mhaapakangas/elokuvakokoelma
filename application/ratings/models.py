from sqlalchemy.ext.declarative.base import declared_attr
from sqlalchemy.sql import text

from application import db
from application.models import Base


class Rating(Base):
    __tablename__ = "rating"

    movie_id = db.Column(db.Integer, db.ForeignKey('movie.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('account.id'))
    want_to_watch = db.Column(db.Boolean)
    rating = db.Column(db.Integer)

    @declared_attr
    def __table_args__(cls):
        return (db.Index("rating_index_%s" % cls.__tablename__, "rating"),)

    @staticmethod
    def count_ratings_per_category(movie_id):
        stmt = text("SELECT rating.rating, COUNT(rating.id) FROM rating"
                    " WHERE rating.rating IS NOT NULL AND rating.movie_id = :movie_id"
                    " GROUP BY rating.rating"
                    " ORDER BY rating.rating").params(movie_id=movie_id)
        res = db.engine.execute(stmt)
        response = []
        for row in res:
            response.append({"rating": row[0], "count": row[1]})

        return response
