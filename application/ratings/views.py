from application import app, db
from application.movies.models import Movie
from application.ratings.models import Rating
from application.ratings.forms import RatingForm
from flask import render_template, redirect, url_for, request
from flask_login import login_required, current_user


@app.route("/ratings/<movie_id>/", methods=["POST"])
@login_required
def add_rating(movie_id):
    rating = Rating.query.filter_by(movie_id=movie_id, user_id=current_user.id).first()

    form = RatingForm(request.form)
    if not form.validate():
        return render_template("movies/view.html",
                               movie=Movie.query.get(movie_id),
                               form=form,
                               rating=rating)

    if not rating:
        rating = Rating()
        rating.movie_id = movie_id
        rating.user_id = current_user.id
        rating.want_to_watch = False
        db.session().add(rating)

    rating.rating = form.rating.data

    db.session().commit()

    return redirect(url_for("movies_view", movie_id=movie_id))


@app.route("/ratings/wishlist/<movie_id>/", methods=["POST"])
@login_required
def update_wishlist(movie_id):
    rating = Rating.query.filter_by(movie_id=movie_id, user_id=current_user.id).first()

    if not rating:
        rating = Rating()
        rating.movie_id = movie_id
        rating.user_id = current_user.id
        db.session().add(rating)

    if request.form.get("wishlist"):
        rating.want_to_watch = True
    else:
        rating.want_to_watch = False

    db.session().commit()

    return redirect(url_for("movies_view", movie_id=movie_id))
