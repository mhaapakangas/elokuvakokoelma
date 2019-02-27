from application import db
from application.models import Base
from application.genres.models import Genre

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
