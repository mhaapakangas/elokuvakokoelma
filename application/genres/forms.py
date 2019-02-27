from flask_wtf import FlaskForm
from wtforms import StringField, validators


class GenreForm(FlaskForm):
    name = StringField("Name:", [validators.Length(min=2, max=144)])

    class Meta:
        csrf = False
