'''
BIOT670 Initial database module for pipeline UI
taken from https://github.com/hack4impact/flask-base/blob/master/app/models/user.py

'''

from flask import Flask, flash, redirect, url_for, request, render_template, Response, current_app
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, AnonymousUserMixin
from flask_login import LoginManager, current_user, login_required, login_user
from itsdangerous import URLSafeTimedSerializer as Serializer
from itsdangerous import BadSignature, SignatureExpired
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
    User class. Access to UI restricted by 'roles' and 'confirmed'.
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
    
    def generate_confirmation_token(self, expiration=30800):
        """Generate a confirmation token to email a new user."""
        s = Serializer(current_app.config['SECRET_KEY'], salt='email-confirm')
        return s.dumps(self.id)

    def confirm_account(self, token):
        """Verify that the provided token is for this user's id."""
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            email = s.loads(token, salt='email-confirm', max_age=60)
        except (BadSignature, SignatureExpired):
            return False
        
        self.confirmed = True
        db.session.add(self)
        db.session.commit()
        return True
        
    def generate_password_reset_token(self, expiration=3600):
        """
        Generate a password reset change token to email to an existing user.
        """
        s = Serializer(current_app.config['SECRET_KEY'], salt='pass-reset')
        return s.dumps({'reset': self.id})
    
    def reset_password(self, token, new_password):
        """Verify the new password for this user."""
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token, salt='pass-reset')
        except (BadSignature, SignatureExpired):
            return False
        if data.get('reset') != self.id:
            return False
        self.password = new_password
        db.session.add(self)
        db.session.commit()
        return True
    
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
    def confirmed(self):
        return False


login_manager.anonymous_user = AnonymousUser

@login_manager.user_loader
def load_user(user_id):
    user = User.query.get(int(user_id))
    return user

@login_manager.unauthorized_handler
def unauthorized():
    return(
    redirect(url_for('auth.login'))
    )

# The home page should have 5 tabs, each capable of performing some type of request handling
# the data for each tab will be stored in the RequestDetails tables

class RequestDetails(db.Model):
    Id = db.Column(db.Integer, primary_key=True)
    requestData = db.Column(db.CHAR(None), unique=False, nullable=True)
    status = db.Column(db.String(20), unique=False, nullable=True)
    createDate = db.Column(db.DateTime, unique=False, nullable=False)
    userId = db.Column(db.Integer, unique=False, nullable=False)
    errorMessage = db.Column(db.String(100), unique=False, nullable=False)

    def __init__(self, requestData, status, createDate, userId, errorMessage):
        self.requestData = requestData
        self.status = status
        self.createDate = createDate
        self.userId = userId
        self.errorMessage = errorMessage
