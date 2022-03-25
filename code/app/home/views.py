from flask import render_template, Response, redirect, session, request, url_for
from app.auth.forms import LoginForm
from app.auth.permission_required import permission_required
from app.models import login_required


#Import blueprint
from app.home import home

@home.route('/')
def index():
    return render_template('index.html')

@home.route("/admin")
@login_required
@permission_required('admin')
def admin():
    return render_template("admin.html")

@home.route("/testpage")
@login_required
def testpage():
    return render_template("testpage.html")

@home.route("/account_confirmed")
@login_required
def account_confirmed():
    return render_template("security/account_confirmed.html")

@home.route("/permission_denied")
def lacking_permission():
    return render_template("permission_denied.html")

@home.errorhandler(403)
def page_not_found(e):
    session['redirected_from'] = request.url
    return redirect(url_for("home.lacking_permission"))
