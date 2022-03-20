from flask import render_template, current_app
from app.auth.forms import LoginForm
from app.models import Job
#Import blueprint
from app.home import home

@home.route('/')
def index():
    return render_template('index.html')
@home.route("/login")
def login():
    form = LoginForm()
    return render_template('login.html', form=form)
@home.route("/admin")
def admin():
    return render_template("admin.html")
@home.route("/testpage")
def testpage():
    return render_template("testpage.html")
@home.route("/job")
def jobpage():
    joblist=Job.query.all()
    current_app.logger.error('Job list is ' + str(len(joblist)))
    return render_template("jobpage.html", joblist=joblist)
