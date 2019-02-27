from flask_wtf import FlaskForm
from wtforms import SelectField, StringField, IntegerField, validators


class MovieForm(FlaskForm):
    name = StringField("Movie title:", [validators.Length(min=2, max=144)])
    year = IntegerField("Year:", [validators.NumberRange(min=1800)])
    runtime = IntegerField("Runtime (min):", [validators.NumberRange(min=0)])
    genre_id = SelectField("Genre:", coerce=int)

    class Meta:
        csrf = False
