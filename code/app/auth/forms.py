from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, \
                    EmailField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, \
                               InputRequired, Length, Regexp
from app.models import User
from flask import url_for



class RegistrationForm(FlaskForm):
    first_name = StringField(
        'First name', validators=[InputRequired(),
                                  Length(1, 64)])
    last_name = StringField(
        'Last name', validators=[InputRequired(),
                                 Length(1, 64)])
    email = EmailField(
        'Email', validators=[InputRequired(),
                             Length(1, 64),
                             Email()])
                             #Regexp('.+@viracor-eurofins.com$', flags=0,
                             #       message='Use company email')])
    password = PasswordField(
        'Password',
        validators=[
            InputRequired(),
            EqualTo('password2', 'Passwords must match')
        ])
    password2 = PasswordField('Confirm password', validators=[InputRequired()])
    submit = SubmitField('Register')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Email already registered. Did you mean to '
                                  'log in instead?')

class LoginForm(FlaskForm):
    email = EmailField(
        'Email', validators=[InputRequired(),
                             Length(1, 64),
                             Email()])
    password = PasswordField('Password', validators=[InputRequired()])
    remember_me = BooleanField('Keep me logged in')
    submit = SubmitField('Log in')
