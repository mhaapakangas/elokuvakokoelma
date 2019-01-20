from application import app, db
from flask import render_template, request, redirect, url_for
from application.movies.models import Movie


@app.route("/movies", methods=["GET"])
def movies_index():
    return render_template("movies/list.html", movies=Movie.query.all())


@app.route("/movies/new/")
def movies_add_form():
    return render_template("movies/new.html")


@app.route("/movies/update/<movie_id>/")
def movies_update_form(movie_id):
    return render_template("movies/update.html", movie=Movie.query.get(movie_id))


@app.route("/movies/", methods=["POST"])
def movies_create():
    movie = Movie(request.form.get("name"),
                  request.form.get("year"),
                  request.form.get("genre"),
                  request.form.get("runtime"))

    db.session().add(movie)
    db.session().commit()

    return redirect(url_for("movies_index"))


@app.route("/movies/<movie_id>/", methods=["POST"])
def movies_update(movie_id):
    movie = Movie.query.get(movie_id)
    movie.name = request.form.get("name")
    movie.year = request.form.get("year")
    movie.runtime = request.form.get("runtime")
    movie.genre = request.form.get("genre")

    db.session().commit()

    return redirect(url_for("movies_index"))
