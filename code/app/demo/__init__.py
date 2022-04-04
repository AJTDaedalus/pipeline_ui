'''
1Feb22 BIOT670 Group 6
Initialization file for the the demo blueprint
'''
from flask import Blueprint

demo = Blueprint('demo', __name__)

from app.demo import views
