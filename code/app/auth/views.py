from flask import render_template, redirect, url_for, flash, request, Flask, current_app, session
from app.auth.forms import RegistrationForm, LoginForm
from flask_login import login_user, login_required, current_user, logout_user
from app.auth import auth
from app.auth.role_required import ROLE_required, not_ROLE
from app.models import db
from app.models import User


#registration route
@auth.route('/register', methods=['GET','POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        if User.query.filter_by(email=form.email.data.lower()).first():
            flash('User already exists.', category='error')
            return redirect(url_for('home.index'))
        else:
            user = User(email=form.email.data)
            user.set_password(form.password.data)
            db.session.add(user)
            db.session.commit()
            flash('Congratulations, you are now a registered user!',
                  category='success')
            return redirect(url_for('home.index'))
    return render_template('security/register_user.html', title='Register', form=form)

#login route
@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data.lower()).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid email or password')
            return redirect(url_for('home.index'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('home.index')
        return redirect(next_page)
    return render_template('security/login_user.html', title='Sign In', form=form)
    
#logout route
@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('home.index'))

@auth.route('/user-page/')
@login_required
def user_page():
    return 'Any logged-in users can visit this page.'
    
@auth.route('/not-ROLE/')
@login_required
def not_ROLE():
    return "Authorized users without ROLE privileges are redirected here.<br>\
            Notice that this view can be @login_required, because only users\
            who are authorized but who don't have ROLE privileges will be\
            redirected here.<br>\
            Unauthorized users accessing an @ROLE_required view are redirected\
            to the login_view, so a @login_required decorator is not\
            additionally needed on a @ROLL_required view."


@auth.route('/ROLE-page/')
@ROLE_required
def ROLE_page():
    return 'Only logged-in ROLE users can visit this page.'
    
