from flask_wtf import FlaskForm
from wtforms import IntegerField, BooleanField, SubmitField
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
    student_id = IntegerField('student ID', validators=[DataRequired()])
    pin = IntegerField('PIN', validators=[DataRequired()])
    remember_me = BooleanField('Remember ME')
    submit = SubmitField('Sign in')