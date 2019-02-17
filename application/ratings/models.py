from sqlalchemy.ext.declarative.base import declared_attr

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
