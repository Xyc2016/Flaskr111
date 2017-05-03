from models import User
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, TextField, PasswordField, BooleanField
from wtforms.validators import DataRequired, EqualTo, URL
from models import db


class CommentForm(FlaskForm):
    title = StringField(
        'Name',
        validators=[DataRequired()]
    )
    text = TextAreaField(
        u'Comment',
        validators=[DataRequired()]
    )


class LoginForm(FlaskForm):
    username = StringField('Username', [DataRequired()])
    password = PasswordField('Password', [DataRequired()])

    def validate(self):
        check_validate = super(LoginForm, self).validate()
        if not check_validate:
            return False
        user = User.query.filter_by(username=self.username.data).first()
        if not user:
            self.username.errors.append('Invalid username or password')
            return False
        if not user.check_password(self.password.data):
            self.username.errors.append('Invalid username or password')
            return False
        return True


class RegisterForm(FlaskForm):
    username = StringField('Username', [DataRequired()])
    password = PasswordField('Password', [DataRequired()])
    confirm = PasswordField('Password', [DataRequired(), EqualTo('password')])

    def validate(self):
        check_validate = super(RegisterForm, self).validate()
        if not check_validate:
            return False
        user = User.query.filter_by(username=self.username.data).first()
        if user:
            self.username.errors.append('Username already exits')
            return False
        return True


class PostForm(FlaskForm):
    title = StringField('title', [DataRequired()])
    text = TextAreaField('Content', [DataRequired()])

