from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, \
                    EmailField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, \
                               InputRequired, Length, Regexp
from wtforms_sqlalchemy.fields import QuerySelectField, QuerySelectMultipleField
from app.models import User, Role
from flask import url_for



class RegistrationForm(FlaskForm):
    """
    Form for registering new users.
    """
    first_name = StringField(
        'First name', validators=[InputRequired(),
                                  Length(1, 64)])
    last_name = StringField(
        'Last name', validators=[InputRequired(),
                                 Length(1, 64)])
    email = EmailField(
        'Email', validators=[InputRequired(),
                             Length(1, 64),
                             Email(),
                             Regexp('.+@eurofins-viracor.com$', flags=0,
                                    message='Use company email')])
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
    """
    Form for logging in users.
    """
    email = EmailField(
        'Email', validators=[InputRequired(),
                             Length(1, 64),
                             Email()])
    password = PasswordField('Password', validators=[InputRequired()])
    remember_me = BooleanField('Keep me logged in')
    submit = SubmitField('Log in')

class NewRoleForm(FlaskForm):
    """
    Form for creating new roles.
    """
    name = StringField('Role name', validators=[InputRequired(), Length(1,64)])
    submit = SubmitField('Create new role')

class AssignRoleForm(FlaskForm):
    """
    Form for assigning roles to users.
    """
    user = QuerySelectField('User',
                            query_factory=lambda: User.query,
                            get_label = 'email')
    roles = QuerySelectMultipleField('Roles',
                                     query_factory=lambda: Role.query,
                                     get_label = 'name')
    submit = SubmitField('Assign role to user')
