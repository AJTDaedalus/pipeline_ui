'''
1Feb22 BIOT670 Group 6
Initialization file for the home page of the interface
'''

from flask import Blueprint

home = Blueprint('home', __name__)

#import views
from app.home import views
