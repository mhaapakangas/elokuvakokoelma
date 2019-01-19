from application import app, db
from flask import render_template, request, redirect, url_for
from application.movies.models import Movie


@app.route("/movies", methods=["GET"])
def movies_index():
    return render_template("movies/list.html", movies=Movie.query.all())


@app.route("/movies/new/")
def movies_form():
    return render_template("movies/new.html")


@app.route("/movies/", methods=["POST"])
def movies_create():
    movie = Movie(request.form.get("name"),
                  request.form.get("year"),
                  request.form.get("genre"),
                  request.form.get("runtime"))

    db.session().add(movie)
    db.session().commit()

    return redirect(url_for("movies_index"))
