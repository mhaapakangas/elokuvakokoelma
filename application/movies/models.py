from application import db


class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(144), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    genre = db.Column(db.String(144), nullable=False)
    runtime = db.Column(db.Integer, nullable=False)

    def __init__(self, name, year, genre, runtime):
        self.name = name
        self.year = year
        self.genre = genre
        self.runtime = runtime
