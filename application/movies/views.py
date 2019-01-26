from application import app, db
from flask import render_template, request, redirect, url_for
from application.movies.models import Movie
from application.movies.forms import MovieForm


@app.route("/movies", methods=["GET"])
def movies_index():
    return render_template("movies/list.html", movies=Movie.query.all())


@app.route("/movies/new/")
def movies_add_form():
    return render_template("movies/new.html", form=MovieForm())


@app.route("/movies/update/<movie_id>/")
def movies_update_form(movie_id):
    return render_template("movies/update.html", form=MovieForm(obj=Movie.query.get(movie_id)))


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


@app.route("/movies/update/", methods=["POST"])
def movies_update():
    form = MovieForm(request.form)

    if not form.validate():
        return render_template("movies/update.html", form=form)

    movie = Movie.query.get(form.id.data)
    movie.name = form.name.data
    movie.year = form.year.data
    movie.runtime = form.runtime.data
    movie.genre = form.genre.data

    db.session().commit()

    return redirect(url_for("movies_index"))
