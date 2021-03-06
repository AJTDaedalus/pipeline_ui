import datetime
from flask import render_template, Response, redirect, session, request, \
                  flash, url_for, current_app, send_file
from app.auth.forms import LoginForm
from app.static.permission_required import permission_required
from app.models import login_required
from app.models import Job
import csv
import os
from flask_wtf import FlaskForm
from flask_wtf.file import FileField
from werkzeug.utils import secure_filename
from csv import DictWriter
from flask import send_file, send_from_directory, safe_join, abort
import pandas


#Import blueprint
from app.home import home

ALLOWED_EXTENSIONS = {'csv'}


@home.route('/')
def index():
    return render_template('index.html')

@home.route("/login")
def login():
    form = LoginForm()
    return render_template('security/login_user.html', form=form)

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

@home.route("/job")
@login_required
def jobpage():
    joblist=Job.query.all()
    current_app.logger.error('Job list is ' + str(len(joblist)))
    return render_template("jobpage.html", joblist=joblist)


class UploadForm(FlaskForm):
    file = FileField()


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS



@home.route('/download')
def download():
    todayDate = str(datetime.datetime.now().date())
    newFileName = 'job_' + todayDate + '.csv'
    return send_file('../test.csv', attachment_filename=newFileName,
                     as_attachment=True)

@home.route('/fail')
def fail():
   return render_template("fail.html")


## Use Get and POST method to get user input and send the result
@home.route("/gccontent", methods=["GET", "POST"])
def gccontent():
    ### store the user input in variables to calculate GC content
    if request.method == "POST":
        data = request.form.get("data").upper()
        G = data.count("G")
        C = data.count("C")
        GC = G + C
        A = data.count("A")
        T = data.count("T")
        total = G + C + A + T
        result = round((GC / total * 100), 2)

        ### create session to store the result
        session["final_result"] = result

        print(result)


        return redirect("/gccontent")
    else:
        ## create session to store the result
        finalResult = session.get("final_result")
        print(finalResult,'sarfraz')
        ## Release session and clear session data
        session.pop("final_result", None)
        return render_template("gccontent.html", final_Result=finalResult)


@home.route('/upload', methods=['GET', 'POST'])
def upload():
    form = UploadForm()
    if request.method == 'POST':
        file = request.files['file']
        if 'file' not in request.files:
            return render_template('fail.html')
        if file.filename == '':
            return render_template('fail.html')
        if file and allowed_file(file.filename):
            filename = secure_filename('test.csv')
            form.file.data.save(filename)
            row = ['Result1', 'Result2','Result3','Result4','Result5','Result6']
            with open (filename,'a') as csvFile:
                writer = csv.writer(csvFile)
                csvFile.write("\n")
                writer.writerow(row)
            csvFile.close()
            data = pandas.read_csv(filename, header=0, on_bad_lines='skip')
            return redirect(url_for('home.download'))

        if not allowed_file(file.name):
            return redirect(url_for('home.fail'))

    return render_template('upload.html', form=form)
