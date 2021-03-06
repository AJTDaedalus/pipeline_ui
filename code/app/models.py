'''
<<<<<<< HEAD
10Feb22 BIOT670 Initial database module for pipeline UI
some code adapted from hack4impact/flask-base/blob/master/app/models/user.py
'''

from flask import Flask, flash, redirect, url_for, request, render_template, \
                  Response, current_app
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
    roles = db.relationship("Role", secondary=user_role,
                            back_populates="users")

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)

    def full_name(self):
        return '%s %s' % (self.first_name, self.last_name)

    def can(self, permission):
        if any(r for r in current_user.roles if r.name==permission):
           return True

    def assign_role(self, role):
        if self not in User.query.filter(User.roles.any(name=role)).all():
            assignment = Role.query.filter(Role.name == role).first()
            self.roles.append(assignment)
            db.session.add(self)
            db.session.commit()
            flash('Role {} granted successfully.'.format(role),'success')
        else:
            flash('Role {} already granted.'.format(role), 'error')

    def remove_role(self, role):
        if self not in User.query.filter(User.roles.any(name=role)).all():
            flash('User does not have role {}.'.format(role),'error')
        else:
            removal = Role.query.filter(Role.name == role).first()
            self.roles.remove(removal)
            db.session.add(self)
            db.session.commit()
            flash('Role {} removed.'.format(role), 'success')

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
            email = s.loads(token, salt='email-confirm', max_age=600)
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
    """
    Role class defining access roles.
    """
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    users = relationship("User", secondary=user_role, back_populates="roles")

    def __repr__(self):
        return '<Role \'%s\'>' % self.name

    def create_role(role):
        db_role = Role.query.filter_by(name=role).first()
        if db_role:
            flash('Role already exists','error')
        else:
            new_role = Role(name=role)
            db.session.add(new_role)
            db.session.commit()


class AnonymousUser(AnonymousUserMixin):
    def can(self, _):
        return False
    def confirmed(self):
        return False

login_manager = LoginManager()
login_manager.login_view = 'login'
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

class RequestDetails(db.Model):
    """
    RequestDetails table for information regarding requests.
    """
    Id = db.Column(db.Integer, primary_key=True)
    requestData = db.Column(db.CHAR(None), unique=False, nullable=True)
    status = db.Column(db.String(20), unique=False, nullable=True)
    createDate = db.Column(db.DateTime, unique=False, nullable=False)
    userId = db.Column(db.Integer, unique=False, nullable=False)
    Output = db.Column(db.Text, unique=False, nullable=False)
    errorMessage = db.Column(db.String(100), unique=False, nullable=False)
    priority = db.Column(db.Integer)

    def __init__(self, requestData, status, createDate, userId, Output, errorMessage):
        self.requestData = requestData
        self.status = status
        self.createDate = createDate
        self.userId = userId
        self.Output = Output
        self.errorMessage = errorMessage

class Job(db.Model):
    JobID = db.Column(db.Integer, primary_key=True)
    JobName = db.Column(db.String(255), unique=True, nullable=False)
    DateSubmit = db.Column(db.DateTime, unique=False, nullable=False)
    DateStart = db.Column(db.DateTime, unique=False, nullable=True)
    DateEnd = db.Column(db.DateTime, unique=False, nullable=True)
    Status = db.Column(db.String(255), unique=False, nullable=False)
    UserID = db.Column(db.Integer, ForeignKey("users.id", ondelete="CASCADE"))

    user = relationship('User', foreign_keys='Job.UserID')
