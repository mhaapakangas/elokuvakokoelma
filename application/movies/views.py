from flask import render_template, request, redirect, url_for
from flask_login import current_user
from sqlalchemy.sql import text

from application import app, db, sql_like_key, login_required
from application.actors.models import Actor
from application.movies.forms import MovieForm
from application.movies.models import Movie
from application.ratings.models import Rating
from application.ratings.forms import RatingForm

import sys

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

    return render_template("movies/list.html", movies=movies, filter1="", filter2="", filter_type=filter_type,
                           page=page, last_page=last_page)


@app.route("/movies/top", methods=["GET"])
def movies_top_list():
    stmt = text("SELECT movie.id, movie.name, movie.year, movie.genre, movie.runtime,"
                " ROUND(AVG(rating.rating), 1) as average FROM movie"
                " JOIN rating ON rating.movie_id = movie.id"
                " WHERE rating.rating IS NOT NULL"
                " GROUP BY movie.id"
                " ORDER BY average DESC"
                " LIMIT 10")
    res = db.engine.execute(stmt)
    return render_template("movies/toplist.html", movies=res)


@app.route("/movies/new/")
@login_required("ADMIN")
def movies_add_form():
    return render_template("movies/new.html", form=MovieForm())


@app.route("/movies/update/<movie_id>/")
@login_required("ADMIN")
def movies_update_form(movie_id):
    return render_template("movies/update.html", form=MovieForm(obj=Movie.query.get(movie_id)), movie_id=movie_id)


@app.route("/movies/view/<movie_id>/")
def movies_view(movie_id):
    # Count the number of ratings for each category
    stmt = text("SELECT rating.rating, COUNT(rating.id) FROM rating"
                " WHERE rating.rating IS NOT NULL AND rating.movie_id = :movie_id"
                " GROUP BY rating.rating"
                " ORDER BY rating.rating").params(movie_id=movie_id)
    res = db.engine.execute(stmt)

    # Assign the number of ratings to the correct category. Set the value to zero if there're no ratings.
    ratings = [0] * 10
    for row in res:
        ratings[row[0] - 1] = row[1]
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
                  form.genre.data,
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
    movie.genre = form.genre.data

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


@app.route("/movies/filter/title/", methods=["POST"])
def movies_filter_title():
    filter_value = request.form.get('filter1') or request.args.get('filter1') or ""
    filter_value = filter_value.strip()

    stmt = text("SELECT DISTINCT movie.id, movie.name, movie.year, movie.genre, movie.runtime FROM movie"
                " WHERE movie.name " + sql_like_key + " :filter_value"
                " ORDER BY movie.name"
                ).params(filter_value='%' + filter_value + '%')

    return apply_filter(stmt, filter_value, "", "title", request.args.get('p'))


@app.route("/movies/filter/actor/", methods=["POST"])
def movies_filter_actor():
    filter_value = request.form.get('filter1') or request.args.get('filter1') or ""
    filter_value = filter_value.strip()

    stmt = text("SELECT DISTINCT movie.id, movie.name, movie.year, movie.genre, movie.runtime FROM movie"
                " JOIN movie_cast ON movie_id=movie.id"
                " JOIN actor ON actor_id=actor.id"
                " WHERE actor.name " + sql_like_key + " :filter_value"
                " ORDER BY movie.name"
                ).params(filter_value='%' + filter_value + '%')

    return apply_filter(stmt, filter_value, "", "actor", request.args.get('p'))


@app.route("/movies/filter/year/", methods=["POST"])
def movies_filter_year():
    form = request.form
    filter1 = form.get('filter1') or request.args.get('filter1')
    filter_min = filter1 or 0
    filter2 = form.get('filter2') or request.args.get('filter2')
    filter_max = filter2 or sys.maxsize

    stmt = text("SELECT DISTINCT movie.id, movie.name, movie.year, movie.genre, movie.runtime FROM movie"
                " WHERE movie.year BETWEEN :filter_min AND :filter_max"
                " ORDER BY movie.name"
                ).params(filter_min=filter_min, filter_max=filter_max)

    return apply_filter(stmt, filter1, filter2, "year", request.args.get('p'))


@app.route("/movies/filter/rating/", methods=["POST"])
def movies_filter_rating():
    form = request.form
    filter1 = form.get('filter1') or request.args.get('filter1')
    filter_min = filter1 or 0
    filter2 = form.get('filter2') or request.args.get('filter2')
    filter_max = filter2 or 10

    stmt = text("SELECT m.id, m.name, m.year, m.genre, m.runtime,"
                " ROUND(m.average, 1) as average FROM "
                "(SELECT movie.id, movie.name, movie.year, movie.genre, movie.runtime,"
                "AVG(rating.rating) as average FROM movie"
                " JOIN rating ON rating.movie_id = movie.id"
                " WHERE rating.rating IS NOT NULL"
                " GROUP BY movie.id) as m"
                " WHERE m.average BETWEEN :filter_min AND :filter_max"
                " ORDER BY m.name").params(filter_min=int(filter_min), filter_max=int(filter_max))

    return apply_filter(stmt, filter1, filter2, "rating", request.args.get('p'))


def apply_filter(stmt, filter1, filter2, filter_type, page):
    if not page:
        page = 0
    page = int(page)

    res = db.engine.execute(stmt)

    all_movies = []
    for row in res:
        m = Movie(row[1], row[2], row[3], row[4])
        m.id = row[0]
        all_movies.append(m)

    # in a real app filtering movies for the current page should be done in the database query.
    page_start = page_size * page
    page_end = page_size * (page + 1)
    movies = all_movies[page_start:page_end]

    movie_count = len(all_movies)
    last_page = movie_count <= page_end

    return render_template("movies/list.html", movies=movies,
                           filter1=filter1, filter2=filter2, filter_type=filter_type, page=page, last_page=last_page)

