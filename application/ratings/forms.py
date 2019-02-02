from flask_wtf import FlaskForm
from wtforms import BooleanField, IntegerField, validators


class RatingForm(FlaskForm):
    rating = IntegerField("Rating", [validators.Optional(), validators.NumberRange(min=1, max=10)])
    want_to_watch = BooleanField("In wishlist")

    class Meta:
        csrf = False
