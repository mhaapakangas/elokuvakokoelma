from application import db


class Rating(db.Model):
    __tablename__ = "rating"

    id = db.Column(db.Integer, primary_key=True)
    movie_id = db.Column(db.Integer, db.ForeignKey('movie.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('account.id'))
    want_to_watch = db.Column(db.Boolean)
    rating = db.Column(db.Integer)
