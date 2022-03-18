'''
10Feb22 BIOT670 Initial database module for pipeline UI
'''

from flask import Flask, flash, redirect, url_for, request, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from flask_login import LoginManager
from werkzeug.security import generate_password_hash, check_password_hash

login_manager = LoginManager()
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@login_manager.unauthorized_handler
def unauthorized():
    flash("You must be logged in to view that page.")
    return redirect(url_for("auth.login"))

db = SQLAlchemy()

class User(db.Model, UserMixin):
    """Data model for user accounts."""
    __tablename__ = 'User'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))


    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    def __repr__(self):
        return '<User {}>'.format(self.username)


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

class Display(db.Model):
    JobID = db.Column(db.Integer, primary_key=True)
    JobName = db.Column(db.String(255), unique=True, nullable=False)
    DateSubmit = db.Column(db.DateTime, unique=False, nullable=False)
    DataStart = db.Column(db.DateTime, unique=False, nullable=True)
    DataEnd = db.Column(db.DateTime, unique=False, nullable=True)
    Status = db.Column(db.String(255), unique=False, nullable=False)
    UserID = db.Column(db.Integer, ForeignKey("User.id", ondelete="CASCADE"))
