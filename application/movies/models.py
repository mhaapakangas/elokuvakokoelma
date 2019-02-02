from application import db
from application.models import Base


class Movie(Base):
    __tablename__ = "movie"

    name = db.Column(db.String(144), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    genre = db.Column(db.String(144), nullable=False)
    runtime = db.Column(db.Integer, nullable=False)

    users = db.relationship('Rating', backref='movie', lazy=True)

    def __init__(self, name, year, genre, runtime):
        self.name = name
        self.year = year
        self.genre = genre
        self.runtime = runtime
