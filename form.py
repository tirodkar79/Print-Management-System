from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, PasswordField, SelectField, SubmitField
from wtforms.validators import DataRequired, Length, EqualTo, NumberRange


class Registration(FlaskForm):
    s1name = StringField('STUDENT NAME', validators=[
                         DataRequired(), Length(min=2, max=35)])
    s2name = StringField('STUDENT NAME', validators=[
                         DataRequired(), Length(min=2, max=35)])
    s3name = StringField('STUDENT NAME', validators=[
                         DataRequired(), Length(min=2, max=35)])
    roll_no1 = IntegerField('ROLL NO.', validators=[DataRequired()])
    roll_no2 = IntegerField('ROLL NO.', validators=[DataRequired()])
    roll_no3 = IntegerField('ROLL NO.', validators=[DataRequired()])
    year = SelectField(
        'Year', choices=[('SE', 'SECOND YEAR'), ('TE', 'THIRD YEAR'), ('FE', 'FOURTH YEAR')], default="")
    sem = IntegerField('SEMESTER', validators=[
                       DataRequired(), NumberRange(min=1, max=8)])
    batch = IntegerField('BATCH', validators=[
                         DataRequired(), NumberRange(min=1, max=4)])
    password = PasswordField('Password', validators=[
        DataRequired(), Length(min=5, max=12)])
    cpwd = PasswordField('Confirm Password', validators=[
                         DataRequired(), EqualTo('password')])

    style = {'style': 'width:160px'}
    submit = SubmitField('Submit', render_kw=style)
