from flask import render_template, Response, redirect, session, request, url_for
from app.auth.forms import LoginForm
from app.auth.role_required import ROLE_required, not_ROLE
from app.models import login_required


#Import blueprint
from app.home import home

@home.route('/')
def index():
    return render_template('index.html')
    
@home.route("/login")
def login():
    form = LoginForm()
    return render_template('security/login_user.html', form=form)
    
@home.route("/admin")
@ROLE_required
def admin():
    return render_template("admin.html")
    
@home.route("/mypage1")
def mypage1():
    return render_template("index.html")

@home.route("/testpage")
def testpage():
    return render_template("testpage.html")

@home.route("/permission_denied")
def lacking_permission():
    return render_template("permission_denied.html")

@home.errorhandler(403)
def page_not_found(e):
    session['redirected_from'] = request.url
    return redirect(url_for("home.lacking_permission"))