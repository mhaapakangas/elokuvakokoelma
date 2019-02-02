from application import db
from application.models import Base
from application.movies.models import Movie
from application.auth.models import User


class Rating(Base):
    __tablename__ = "rating"

    movie_id = db.Column(db.Integer, db.ForeignKey('movie.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('account.id'))
    want_to_watch = db.Column(db.Boolean)
    rating = db.Column(db.Integer)

    movie = db.relationship(Movie, backref='ratings', lazy=True)
    user = db.relationship(User, backref='ratings', lazy=True)
