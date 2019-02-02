from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, validators


class MovieForm(FlaskForm):
    name = StringField("Movie title", [validators.Length(min=2)])
    year = IntegerField("Year", [validators.NumberRange(min=1800)])
    runtime = IntegerField("Runtime", [validators.NumberRange(min=0)])
    genre = StringField("Genre", [validators.Length(min=2)])

    class Meta:
        csrf = False
