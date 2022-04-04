from flask import render_template, redirect, url_for, flash, request, Flask, \
                  current_app, session
from flask_login import login_required
from app.demo.forms import DemoForm
from app.demo import demo
from app.static.permission_required import permission_required
from app.models import User, Role, db


#Demo route
@demo.route('/demo', methods=['GET', 'POST'])
@login_required
def demo():
    demoform = DemoForm()
    if demoform.validate_on_submit():
        flash("Demo message {} received.".format(demoform.name.data),'success')

    return render_template('demo/demo.html', demoform=demoform)
