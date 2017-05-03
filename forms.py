from flask_wtf import FlaskForm,Form
from wtforms import StringField, TextAreaField
from wtforms.validators import DataRequired


class CommentForm(FlaskForm):
    title = StringField(
        'Name',
        validators=[DataRequired()]
    )
    text = TextAreaField(
        u'Comment',
        validators=[DataRequired()]
    )
