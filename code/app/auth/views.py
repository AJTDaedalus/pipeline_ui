from flask import render_template, redirect, url_for, flash, request
from app.models import db
from app.auth.forms import RegistrationForm
from app.models import User
from app.auth import auth

@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for(index))
    return render_template('registration.html', title='Register', form=form)
