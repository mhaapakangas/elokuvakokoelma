from application import app, db
from application.auth.models import User
from application.movies.models import Movie
from application.ratings.models import Rating
from flask import redirect, url_for, request
from flask_login import login_required, current_user


@app.route("/ratings/wishlist/<movie_id>/", methods=["POST"])
@login_required
def add_movie_to_wishlist(movie_id):
    rating = Rating.query.filter_by(movie_id=movie_id, user_id=current_user.id).first()

    if not rating:
        rating = Rating()
        rating.movie_id = movie_id
        rating.user_id = current_user.id

        movie = Movie.query.get(movie_id)
        movie.users.append(rating)
        user = User.query.get(current_user.id)
        user.movies.append(rating)

        db.session().add(rating)

    rating.want_to_watch = True

    db.session().commit()

    return redirect(url_for("movies_index"))


@app.route("/ratings/<movie_id>/", methods=["POST"])
@login_required
def add_rating(movie_id):
    form = request.form
    rating = Rating.query.filter_by(movie_id=movie_id, user_id=current_user.id).first()

    if not rating:
        rating = Rating()
        rating.movie_id = movie_id
        rating.user_id = current_user.id

        movie = Movie.query.get(movie_id)
        movie.users.append(rating)
        user = User.query.get(current_user.id)
        user.movies.append(rating)

        db.session().add(rating)

    rating.rating = form.get("rating")

    db.session().commit()

    return redirect(url_for("movies_index"))
