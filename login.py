from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, PasswordField, SelectField, SubmitField
from wtforms.validators import DataRequired, Length, EqualTo, NumberRange


class Login(FlaskForm):
    username = StringField('Group ID', validators=[
        DataRequired()])

    password = PasswordField('Password', validators=[
        DataRequired()])

    style = {'style': 'width:160px'}
    submit = SubmitField('Login', render_kw=style)
