from flask import render_template, request, redirect, url_for

from application import app, db, login_required
from application.genres.forms import GenreForm
from application.genres.models import Genre


@app.route("/genres/", methods=["GET"])
@login_required("ADMIN")
def genres_index():
    return render_template("genres/list.html", genres=Genre.query.order_by(Genre.name).all())


@app.route("/genres/new/")
@login_required("ADMIN")
def genres_add_form():
    return render_template("genres/new.html", form=GenreForm())


@app.route("/genres/update/<genre_id>/")
@login_required("ADMIN")
def genres_update_form(genre_id):
    return render_template("genres/update.html", form=GenreForm(obj=Genre.query.get(genre_id)), genre_id=genre_id)


@app.route("/genres/", methods=["POST"])
@login_required("ADMIN")
def genres_create():
    form = GenreForm(request.form)

    if not form.validate():
        return render_template("genres/new.html", form=form)

    genre = Genre(form.name.data)

    db.session().add(genre)
    db.session().commit()

    return redirect(url_for("genres_index"))


@app.route("/genres/update/<genre_id>/", methods=["POST"])
@login_required("ADMIN")
def genres_update(genre_id):
    form = GenreForm(request.form)

    if not form.validate():
        return render_template("genres/update.html", form=form, genre_id=genre_id)

    genre = Genre.query.get(genre_id)
    genre.name = form.name.data

    db.session().commit()

    return redirect(url_for("genres_index"))
