from application import app, db
from flask import render_template, request, redirect, url_for
from application.movies.models import Movie
from application.movies.forms import MovieForm
from application.actors.models import Actor
from application.cast.models import Cast
from sqlalchemy.sql import text


@app.route("/movies", methods=["GET"])
def movies_index():
    return render_template("movies/list.html", movies=Movie.query.all(), filter="")


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
    Cast.query.filter_by(movie_id=movie_id).delete()

    for actor_id in form:
        cast = Cast(movie_id, actor_id)
        db.session().add(cast)

    db.session().commit()

    return redirect(url_for("movies_index"))


@app.route("/movies/filter/", methods=["POST"])
def movies_filter():
    actorfilter = request.form.get("filter")

    stmt = text("SELECT DISTINCT movie.id, movie.name, movie.year, movie.genre, movie.runtime FROM movie"
                " JOIN cast ON movie_id=movie.id"
                " JOIN actor ON actor_id=actor.id"
                " WHERE actor.name LIKE :actorfilter"
                ).params(actorfilter='%' + actorfilter + '%')
    res = db.engine.execute(stmt)
    cast = []
    for movie in res:
        m = Movie(movie[1], movie[2], movie[3], movie[4])
        m.id = movie[0]
        cast.append(m)

    return render_template("movies/list.html", movies=cast, filter=actorfilter)
