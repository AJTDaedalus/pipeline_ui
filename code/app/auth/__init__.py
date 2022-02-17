'''
1Feb22 BIOT670 Group 6
Initialization file for the authentication pages of the interface
'''
from flask import Blueprint

auth = Blueprint('auth', __name__)

from app.auth import views
