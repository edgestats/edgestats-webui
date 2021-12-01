from flask_wtf import FlaskForm

from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import (DataRequired, Length)


class SearchAddress(FlaskForm):
    """Search address."""

    addr = StringField(
        "addr",
        validators=[
            DataRequired(message="search address"),
            Length(min=42, message="address required"),
        ],
        render_kw={
            "type": "text",
        },
    )
    submit = SubmitField("Search")


class SearchClusterAddresses(FlaskForm):
    """Search cluster of addresses."""

    addrs = TextAreaField(
        "addrs",
        validators=[
            DataRequired(message="search comma seperated list of addresses"),
            Length(min=42, message="minimum 1 addresses required"),
        ],
        render_kw={
            "type": "text",
        },
    )
    submit = SubmitField("Search")
