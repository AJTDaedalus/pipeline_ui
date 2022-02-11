from flask import render_template

#Import blueprint
from app.home import home

@home.route('/')
def index():
    return render_template('index.html')
@home.route("/login")
def login():
    return render_template("login.html")
@home.route("/admin")
def admin():
    return render_template("admin.html")
@home.route("/mypage1")
def mypage1():
    return render_template("index.html")
@home.route("/testpage")
def testpage():
    return render_template("testpage.html")
@home.route("/registration")
def registration():
    return render_template("registration.html")

