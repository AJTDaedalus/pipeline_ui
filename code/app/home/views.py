from flask import render_template, Response, redirect, session, request, flash, url_for, current_app
from app.auth.forms import LoginForm
from app.auth.permission_required import permission_required
from app.models import login_required
from app.models import Job
import csv
import os


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
@login_required
@permission_required('admin')
def admin():
    return render_template("admin.html")

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

@login_required
@home.route("/job")
def jobpage():
    joblist=Job.query.all()
    current_app.logger.error('Job list is ' + str(len(joblist)))
    return render_template("jobpage.html", joblist=joblist)

@home.route("/upload")
def uploadpage():
    UPLOAD_FOLDER = 'c:/user/19786/desktop/piplineui/code/app/static'
    ALLOWED_EXTENSIONS = {'txt', 'csv'}
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return render_template(upload.html)
        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            return render_template(upload.html)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('download_file', name=filename))
    return render_template('upload.html')
 