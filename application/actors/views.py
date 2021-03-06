from flask import render_template, request, redirect, url_for

from application import app, db, login_required
from application.actors.forms import ActorForm
from application.actors.models import Actor


@app.route("/actors/", methods=["GET"])
@login_required("ADMIN")
def actors_index():
    return render_template("actors/list.html", actors=Actor.query.order_by(Actor.name).all())


@app.route("/actors/new/")
@login_required("ADMIN")
def actors_add_form():
    return render_template("actors/new.html", form=ActorForm())


@app.route("/actors/update/<actor_id>/")
@login_required("ADMIN")
def actors_update_form(actor_id):
    return render_template("actors/update.html", form=ActorForm(obj=Actor.query.get(actor_id)), actor_id=actor_id)


@app.route("/actors/", methods=["POST"])
@login_required("ADMIN")
def actors_create():
    form = ActorForm(request.form)

    if not form.validate():
        return render_template("actors/new.html", form=form)

    actor = Actor(form.name.data)

    db.session().add(actor)
    db.session().commit()

    return redirect(url_for("actors_index"))


@app.route("/actors/delete/<actor_id>/", methods=["POST"])
@login_required("ADMIN")
def actors_delete(actor_id):
    actor = Actor.query.get(actor_id)
    db.session().delete(actor)
    db.session().commit()

    return redirect(url_for("actors_index"))


@app.route("/actors/update/<actor_id>/", methods=["POST"])
@login_required("ADMIN")
def actors_update(actor_id):
    form = ActorForm(request.form)

    if not form.validate():
        return render_template("actors/update.html", form=form, actor_id=actor_id)

    actor = Actor.query.get(actor_id)
    actor.name = form.name.data

    db.session().commit()

    return redirect(url_for("actors_index"))
