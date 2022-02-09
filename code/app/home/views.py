from flask import render_template

#Import blueprint
from app.home import home

@home.route('/')
def index():
    return render_template('home.html')
@home.route('/login')
def index():
    return render_template('home.html')

@home.route('/home')
def index():
    return render_template('home.html')

@home.route('/admin')
def index():
    return render_template('home.html')

