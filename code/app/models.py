'''
10Feb22 BIOT670 Initial database module for pipeline UI
'''

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    """Data model for user accounts."""
    __tablename__ = 'User'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))

    
    def set_password(self, password):
        self.password_hash = password
        
    def check_password(self, password):
        return self.password_hash

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

    def __repr__(self):
        return '<User {}>'.format(self.username)
