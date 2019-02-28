from flask import render_template, request, redirect, url_for
from flask_login import current_user
from sqlalchemy.sql import text

from application import app, db, login_required
from application.actors.models import Actor
from application.genres.models import Genre
from application.movies.forms import MovieForm
from application.movies.models import Movie
from application.ratings.forms import RatingForm
from application.ratings.models import Rating

page_size = 10  # Number of entries on one page


@app.route("/movies/", methods=["GET", "POST"])
def movies_index():
    page = request.args.get('p') or 0
    page = int(page)

    filter_type = None
    if request.form:
        filter_type = request.form.get("filter_type")

    if not filter_type:
        filter_type = "title"

    movie_count = Movie.query.count()
    last_page = movie_count <= page_size * (page + 1)

    # fetch movies for the current page
    movies = Movie.query\
        .order_by(Movie.name)\
        .offset(page_size * page)\
        .limit(page_size)\
        .all()

    return render_template("movies/list.html", movies=movies, genres=Genre.query.order_by(Genre.name).all(),
                           filter1="", filter2="", filter_type=filter_type, page=page, last_page=last_page)


@app.route("/movies/top", methods=["GET"])
def movies_top_list():
    movies = Movie.get_best_rated_movies()
    return render_template("movies/toplist.html", movies=movies)


@app.route("/movies/new/")
@login_required("ADMIN")
def movies_add_form():
    return render_template("movies/new.html", form=MovieForm())


@app.route("/movies/update/<movie_id>/")
@login_required("ADMIN")
def movies_update_form(movie_id):
    form = MovieForm(obj=Movie.query.get(movie_id))
    return render_template("movies/update.html", form=form, movie_id=movie_id)


@app.route("/movies/view/<movie_id>/")
def movies_view(movie_id):
    # Count the number of ratings for each category
    res = Rating.count_ratings_per_category(movie_id)

    # Assign the number of ratings to the correct category. Set the value to zero if there're no ratings.
    ratings = [0] * 10
    for result in res:
        ratings[result.get("rating") - 1] = result.get("count")
    # Find the category with the most ratings
    max_rating = max(max(ratings), 1)
    # Weight each category based on the highest number of ratings
    weighted_ratings = [r/max_rating for r in ratings]

    if current_user.is_authenticated:
        rating = Rating.query.filter_by(movie_id=movie_id, user_id=current_user.id).first()
    else:
        rating = None
    return render_template("movies/view.html", movie=Movie.query.get(movie_id), form=RatingForm(obj=rating),
                           rating=rating, ratings=weighted_ratings)


@app.route("/movies/cast/<movie_id>/")
@login_required("ADMIN")
def movies_cast_form(movie_id):
    stmt = text("SELECT actor_id FROM movie_cast"
                " WHERE movie_id = :movie_id").params(movie_id=movie_id)
    res = db.engine.execute(stmt)
    cast = [actor[0] for actor in res]
    return render_template("movies/cast.html", actors=Actor.query.order_by(Actor.name).all(),
                           movie=Movie.query.get(movie_id), cast=cast)


@app.route("/movies/add/", methods=["POST"])
@login_required("ADMIN")
def movies_create():
    form = MovieForm(request.form)

    if not form.validate():
        return render_template("movies/new.html", form=form)

    movie = Movie(form.name.data,
                  form.year.data,
                  form.genre_id.data,
                  form.runtime.data)

    db.session().add(movie)
    db.session().commit()

    return redirect(url_for("movies_index"))


@app.route("/movies/delete/<movie_id>/", methods=["POST"])
@login_required("ADMIN")
def movies_delete(movie_id):
    ratings = Rating.query.filter_by(movie_id=movie_id).all()
    for rating in ratings:
        db.session().delete(rating)

    movie = Movie.query.get(movie_id)
    db.session().delete(movie)

    db.session().commit()

    return redirect(url_for("movies_index"))


@app.route("/movies/update/<movie_id>/", methods=["POST"])
@login_required("ADMIN")
def movies_update(movie_id):
    form = MovieForm(request.form)

    if not form.validate():
        return render_template("movies/update.html", form=form, movie_id=movie_id)

    movie = Movie.query.get(movie_id)
    movie.name = form.name.data
    movie.year = form.year.data
    movie.runtime = form.runtime.data
    movie.genre_id = form.genre_id.data

    db.session().commit()

    return redirect(url_for("movies_index"))


@app.route("/movies/cast/<movie_id>/", methods=["POST"])
@login_required("ADMIN")
def movies_cast(movie_id):
    form = request.form

    movie = Movie.query.get(movie_id)
    movie.actors.clear()

    for actor_id in form:
        movie.actors.append(Actor.query.get(actor_id))

    db.session().commit()

    return redirect(url_for("movies_index"))


@app.route("/movies/filter/<filter_type>/", methods=["POST"])
def movies_filter(filter_type):
    form = request.form
    filter1 = form.get('filter1') or request.args.get('filter1')
    filter2 = form.get('filter2') or request.args.get('filter2')

    all_movies = []
    if filter_type == "title":
        all_movies = Movie.get_movies_by_title(filter1)
    elif filter_type == "actor":
        all_movies = Movie.get_movies_by_actor(filter1)
    elif filter_type == "year":
        all_movies = Movie.get_movies_by_year(filter1, filter2)
    elif filter_type == "rating":
        all_movies = Movie.get_movies_by_rating(filter1, filter2)
    elif filter_type == "genre":
        all_movies = Movie.get_movies_by_genre(filter1)

    page = request.args.get('p')
    if not page:
        page = 0
    page = int(page)

    # in a real app filtering movies for the current page should be done in the database query.
    page_start = page_size * page
    page_end = page_size * (page + 1)
    movies = all_movies[page_start:page_end]

    movie_count = len(all_movies)
    last_page = movie_count <= page_end

    return render_template("movies/list.html", movies=movies, genres=Genre.query.order_by(Genre.name).all(),
                           filter1=filter1, filter2=filter2, filter_type=filter_type, page=page, last_page=last_page)

