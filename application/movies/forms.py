from flask_wtf import FlaskForm
from wtforms import SelectField, StringField, IntegerField, validators

from application.genres.models import Genre


class MovieForm(FlaskForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.genre_id.choices = [(g.id, g.name) for g in Genre.query.order_by(Genre.name).all()]

    name = StringField("Movie title:", [validators.Length(min=2, max=144)])
    year = IntegerField("Year:", [validators.NumberRange(min=1800, max=99999)])
    runtime = IntegerField("Runtime (min):", [validators.NumberRange(min=0, max=99999)])
    genre_id = SelectField("Genre:", coerce=int)

    class Meta:
        csrf = False
