'''
BIOT670 Initial database module for pipeline UI
taken from https://github.com/hack4impact/flask-base/blob/master/app/models/user.py

'''

from flask import Flask, flash, redirect, url_for, request, render_template, Response, current_app
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, AnonymousUserMixin
from flask_login import LoginManager, current_user, login_required, login_user
#from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
#from itsdangerous import BadSignature, SignatureExpired
from werkzeug.security import check_password_hash, generate_password_hash
from sqlalchemy import Table, ForeignKey, Column, Integer
from sqlalchemy.orm import relationship



db = SQLAlchemy()


user_role = db.Table('user_role', db.Model.metadata,
    db.Column('user_id', db.Integer, ForeignKey('users.id')),
    db.Column('role_id', db.Integer, ForeignKey('roles.id')),
)

class User(UserMixin, db.Model):
    """
    User class. Your Typical user class.
    """
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    confirmed = db.Column(db.Boolean, default=False)
    first_name = db.Column(db.String(64), index=True)
    last_name = db.Column(db.String(64), index=True)
    email = db.Column(db.String(64), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    roles = db.relationship(
        "Role",
        secondary=user_role,
        )

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)


    def full_name(self):
        return '%s %s' % (self.first_name, self.last_name)

    def can(self, permission):
        if any(r for r in current_user.roles if r.name==permission):
           return True
           
    @property
    def password(self):
        raise AttributeError('`password` is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    #def generate_confirmation_token(self, expiration=604800):
    #    """Generate a confirmation token to email a new user."""

    #    s = Serializer(current_app.config['SECRET_KEY'], expiration)
    #    return s.dumps({'confirm': self.id})


    #def generate_password_reset_token(self, expiration=3600):
    #    """
    #    Generate a password reset change token to email to an existing user.
    #    """
    #    s = Serializer(current_app.config['SECRET_KEY'], expiration)
    #    return s.dumps({'reset': self.id})


    #def reset_password(self, token, new_password):
    #    """Verify the new password for this user."""
    #    s = Serializer(current_app.config['SECRET_KEY'])
    #    try:
    #        data = s.loads(token)
    #    except (BadSignature, SignatureExpired):
    #        return False
    #    if data.get('reset') != self.id:
    #        return False
    #    self.password = new_password
    #    db.session.add(self)
    #    db.session.commit()
    #    return True

    def __repr__(self):
        return '<User \'%s\'>' % self.full_name()

class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    index = db.Column(db.String(64))
    default = db.Column(db.Boolean, default=False, index=True)

    @staticmethod
    def insert_roles():
        roles = {
            'Placeholder1': ('placeholder1', False),
            'Placeholder2': ('placeholder2', False),
            'Administrator': (
                'admin',
                False
            )
        }
        for r in roles:
            role = Role.query.filter_by(name=r).first()
            if role is None:
                role = Role(name=r)
            role.index = roles[r][0]
            role.default = roles[r][1]
            db.session.add(role)
        db.session.commit()

    def __repr__(self):
        return '<Role \'%s\'>' % self.name


login_manager = LoginManager()
login_manager.login_view = 'login'

class AnonymousUser(AnonymousUserMixin):
    def can(self, _):
        return False


login_manager.anonymous_user = AnonymousUser

@login_manager.user_loader
def load_user(user_id):
    user = User.query.get(int(user_id))
    return user

@login_manager.unauthorized_handler
def unauthorized():
    return(
    Response("You must be logged in to view that page."),
    401,
    )