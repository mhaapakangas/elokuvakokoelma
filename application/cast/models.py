from application import db
from application.movies.models import Movie


class Cast(db.Model):
    __tablename__ = "cast"

    movie_id = db.Column(db.Integer, db.ForeignKey('movie.id'), primary_key=True)
    actor_id = db.Column(db.Integer, db.ForeignKey('actor.id'), primary_key=True)

    movie = db.relationship(Movie, backref='cast', lazy=True)

    def __init__(self, movie_id, actor_id):
        self.movie_id = movie_id
        self.actor_id = actor_id
