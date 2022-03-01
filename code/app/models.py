'''
BIOT670 Initial database module for pipeline UI
taken from https://flask-roles.readthedocs.io/en/latest/usage.html

'''

from flask import Flask, flash, redirect, url_for, request, render_template, Response
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from flask_login import LoginManager, current_user, login_required, login_user
from passlib.hash import pbkdf2_sha512


db = SQLAlchemy()



class User(db.Model, UserMixin):
    """
    User class. Your Typical user class.
    """
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password = db.Column(db.String(128))
    role = db.Column(db.String(40))
    
    def set_password(self, password):
        self.password = pbkdf2_sha512.using(salt_size=8).hash(password)
        
    def check_password(self, password):
        return pbkdf2_sha512.verify(password, self.password)
        
    def is_active(self):
        return True
        
    def __repr__(self):
        return "<User %r>" % self.email        
        
from app.auth.role_required import ROLE_required, not_ROLE
LoginManager.not_ROLE = not_ROLE
login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.not_ROLE_view = 'auth.not_ROLE'


@login_manager.user_loader
def load_user(user_id):
    user = db.session.query(User).get(int(user_id))
    return user

@login_manager.unauthorized_handler
def unauthorized():
    return(
    Response("You must be logged in to view that page."),
    401,
    )