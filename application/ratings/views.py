from application import app, db
from application.auth.models import User
from application.movies.models import Movie
from application.ratings.models import Rating
from application.ratings.forms import RatingForm
from flask import render_template, redirect, url_for, request
from flask_login import login_required, current_user


@app.route("/ratings/<movie_id>/")
@login_required
def ratings_form(movie_id):
    rating = Rating.query.filter_by(movie_id=movie_id, user_id=current_user.id).first()
    return render_template("ratings/rating_form.html", form=RatingForm(obj=rating),
                           movie=Movie.query.get(movie_id))


@app.route("/ratings/<movie_id>/", methods=["POST"])
@login_required
def add_rating(movie_id):
    form = RatingForm(request.form)
    if not form.validate():
        return render_template("ratings/rating_form.html", form=form, movie=Movie.query.get(movie_id))

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

    rating.rating = form.rating.data
    rating.want_to_watch = form.want_to_watch.data

    db.session().commit()

    return redirect(url_for("movies_index"))
