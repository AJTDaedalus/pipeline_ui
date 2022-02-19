from flask import render_template, redirect, url_for, flash, request
from app.models import db
from app.auth.forms import RegistrationForm
from app.auth.forms import LoginForm
from app.models import User
from app.auth import auth
from flask_login import (login_user, login_required, current_user, logout_user)

#registration route
@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        if User.query.filter_by(username=form.username.data.lower()).first():
            flash('User already exists.', category='error')
            return redirect(url_for('home.index'))
        else:
            user = User(username=form.username.data.lower(),
                        email=form.email.data)
            user.set_password(form.password.data)
            db.session.add(user)
            db.session.commit()
            flash('Congratulations, you are now a registered user!',
                  category='success')
            return redirect(url_for('home.index'))
    return render_template('registration.html', title='Register', form=form)

#login route
@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data.lower()).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('home.index'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('home.index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)
    
#logout route
@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('home.index'))