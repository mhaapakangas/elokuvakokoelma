from flask import Flask
app = Flask(__name__)

from flask_sqlalchemy import SQLAlchemy

import os

global sql_like_key

if os.environ.get("HEROKU"):
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL")
    sql_like_key = "ILIKE"
else:
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///movies.db"
    app.config["SQLALCHEMY_ECHO"] = True
    sql_like_key = "LIKE"

db = SQLAlchemy(app)


from os import urandom
app.config["SECRET_KEY"] = urandom(32)

from flask_login import LoginManager, current_user
login_manager = LoginManager()
login_manager.init_app(app)

login_manager.login_view = "auth_login"
login_manager.login_message = "Please login to use this functionality."


# roles in login_required
from functools import wraps


def login_required(role="ANY"):
    def wrapper(fn):
        @wraps(fn)
        def decorated_view(*args, **kwargs):
            if not current_user:
                return login_manager.unauthorized()

            if not current_user.is_authenticated:
                return login_manager.unauthorized()

            unauthorized = False

            if role != "ANY":
                unauthorized = True

                for user_role in current_user.roles():
                    if user_role == role:
                        unauthorized = False
                        break

            if unauthorized:
                return login_manager.unauthorized()

            return fn(*args, **kwargs)

        return decorated_view

    return wrapper


from application import views

from application.genres import models
from application.genres import views

from application.movies import models
from application.movies import views

from application.auth import models
from application.auth import views

from application.ratings import models
from application.ratings import views

from application.actors import models
from application.actors import views

from application.auth.models import User

from sqlalchemy import text


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


def get_average_rating(movie_id):
    stmt = text("SELECT ROUND(AVG(rating.rating), 1) FROM movie"
                " JOIN rating ON rating.movie_id = movie.id"
                " WHERE rating.rating IS NOT NULL AND movie.id = :id").params(id=movie_id)
    res = db.engine.execute(stmt)
    for row in res:
        return row[0]
    return None


def get_genre_name(genre_id):
    genre = genres.models.Genre.query.get(genre_id)
    if genre:
        return genre.name
    return None


app.jinja_env.globals.update(get_average_rating=get_average_rating)
app.jinja_env.globals.update(get_genre_name=get_genre_name)

try:
    db.create_all()
    if not User.query.filter_by(username="admin").first():
        user = User("admin", "admin", "password")
        db.session().add(user)
        db.session().commit()
except:
    pass
