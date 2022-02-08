from flask import render_template

#Import blueprint
from app.home import home

@home.route('/')
def index():
    return render_template('index.html')
@app.route("/login")
def login():
    return render_template("index.html")
@app.route("/admin")
def admin():
    return render_template("index.html")
@app.route("/mypage1")
def mypage1():
    return render_template("index.html")
@app.route("/testnew")
def testnew():
    return render_template("new.html")
