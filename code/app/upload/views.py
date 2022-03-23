from flask import render_template, Response, redirect, session, request, flash, url_for, current_app
from app.auth.forms import LoginForm
from app.auth.permission_required import permission_required
from app.models import login_required
from app.models import Job
import csv
import os
from flask import * 

@upload.route('/upload')
def upload():
    return render_template("fileform.html")

@upload.route('/success',methods=['POST'])
def success():
    if request.method == 'POST':
        f=request.files['file']
        f.save(f.filename)
        return render_template("success.html")
    
if __name__ == 'main':
    app.run(debug=True)