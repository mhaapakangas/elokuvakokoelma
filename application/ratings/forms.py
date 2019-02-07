from flask_wtf import FlaskForm
from wtforms import IntegerField, validators


class RatingForm(FlaskForm):
    rating = IntegerField("My rating", [validators.Optional(), validators.NumberRange(min=1, max=10)])

    class Meta:
        csrf = False
