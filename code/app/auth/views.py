from flask import render_template, redirect, url_for, flash, request, Flask, current_app, session
from app.auth.forms import RegistrationForm, LoginForm
from flask_login import login_user, login_required, current_user, logout_user
from unittest import TextTestResult
from app.models import db
from app.auth.forms import LoginForm
from app.models import User
from app.auth import auth
from app.auth.permission_required import permission_required
from app.models import db
from app.models import User, Role


#registration route
@auth.route('/register', methods=['GET','POST'])
def register():
    form = RegistrationForm()
    Role.insert_roles()
    if form.validate_on_submit():
        if User.query.filter_by(email=form.email.data.lower()).first():
            flash('User already exists.', category='error')
            return redirect(url_for('home.index'))
        password=form.password.data
        SpecialSym="*?!'^+%&/()=}][{$#"
        if len(password) < 8:
            flash('Password too short. Must be 8 characters','error')
            return redirect(url_for('auth.register'))
        if not any (char.isupper() for char in password):
            flash('Password must include at least one upper case letter','error')
            return redirect(url_for('auth.register'))
        if not any (char.isdigit() for char in password):
            flash('Password must include at least one digit.','error')
            return redirect(url_for('auth.register'))
        if not any(char in SpecialSym for char in password):
            flash('Password must include at least one special character.','error')
            return redirect(url_for('auth.register'))

        else:
            user = User(
                first_name=form.first_name.data,
                last_name=form.last_name.data,
                email=form.email.data,
                password=form.password.data)
            db.session.add(user)
            db.session.commit()
            flash('Congratulations, you are now a registered user!', 'success')
            return redirect(url_for('home.index'))
    return render_template('security/register_user.html', title='Register', form=form)





#login route
@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():

        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.password_hash is not None and \
                user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
            flash('You are now logged in. Welcome back!', 'success')
            return redirect(request.args.get('next') or url_for('home.index'))
        else:
            flash('Invalid email or password.', 'error')
    return render_template('security/login_user.html', form=form)

#logout route
@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('home.index'))
