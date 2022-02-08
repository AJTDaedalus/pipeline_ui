from flask import render_template

#Import blueprint
from app.home import home

@home.route('/')
def index():
    return render_template('index.html')
