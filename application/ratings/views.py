from application import app, db, login_required
from application.movies.models import Movie
from application.ratings.models import Rating
from application.ratings.forms import RatingForm
from flask import render_template, redirect, url_for, request
from flask_login import current_user


@app.route("/ratings/collection/")
@login_required("USER")
def get_collection():
    collection = Rating.query.filter_by(user_id=current_user.id).all()
    ratings = [r for r in collection if r.rating]
    wishlist = [r for r in collection if r.want_to_watch]

    return render_template("movies/collection.html",
                           ratings=ratings, wishlist=wishlist)


@app.route("/ratings/<movie_id>/", methods=["POST"])
@login_required("USER")
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
@login_required("USER")
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
