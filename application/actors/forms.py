from flask_wtf import FlaskForm
from wtforms import StringField, validators


class ActorForm(FlaskForm):
    name = StringField("Name", [validators.Length(min=2)])

    class Meta:
        csrf = False
