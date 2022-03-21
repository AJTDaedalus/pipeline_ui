from flask import render_template, Response, redirect, session, request, url_for
from app.auth.forms import LoginForm, AssignRoleForm
from app.auth.permission_required import permission_required
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

@home.route("/admin", methods=['GET', 'POST'])
@login_required
@permission_required('admin')
def admin():
    form = AssignRoleForm()
    return render_template("admin.html", form=form)

@home.route("/testpage")
@login_required
def testpage():
    return render_template("testpage.html")

@home.route("/permission_denied")
def lacking_permission():
    return render_template("permission_denied.html")

@home.errorhandler(403)
def page_not_found(e):
    session['redirected_from'] = request.url
    return redirect(url_for("home.lacking_permission"))
