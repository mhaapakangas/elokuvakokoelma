from application import app, db
from flask import render_template, request, redirect, url_for
from application.movies.models import Movie, Cast
from application.movies.forms import MovieForm
from application.actors.models import Actor
from sqlalchemy.sql import text


@app.route("/movies", methods=["GET"])
def movies_index():
    return render_template("movies/list.html", movies=Movie.query.all())


@app.route("/movies/new/")
def movies_add_form():
    return render_template("movies/new.html", form=MovieForm())


@app.route("/movies/update/<movie_id>/")
def movies_update_form(movie_id):
    return render_template("movies/update.html", form=MovieForm(obj=Movie.query.get(movie_id)), movie_id=movie_id)


@app.route("/movies/cast/<movie_id>/")
def movies_cast_form(movie_id):
    stmt = text("SELECT actor_id FROM cast"
                " WHERE movie_id = :movie_id").params(movie_id=movie_id)
    res = db.engine.execute(stmt)
    cast = [actor[0] for actor in res]
    return render_template("movies/cast.html", actors=Actor.query.all(), movie_id=movie_id,
                           cast=cast)


@app.route("/movies/", methods=["POST"])
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
def movies_delete(movie_id):
    movie = Movie.query.get(movie_id)
    db.session().delete(movie)
    db.session().commit()

    return redirect(url_for("movies_index"))


@app.route("/movies/update/<movie_id>/", methods=["POST"])
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
def movies_cast(movie_id):
    form = request.form

    movie = Movie.query.get(movie_id)
    movie.actors.clear()

    for actor_id in form:
        movie.actors.append(Actor.query.get(actor_id))

    db.session().commit()

    return redirect(url_for("movies_index"))
