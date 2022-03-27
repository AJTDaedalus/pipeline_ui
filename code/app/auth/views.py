from flask import render_template, redirect, url_for, flash, request, Flask, \
                  current_app, session
from flask_login import login_user, login_required, current_user, logout_user
from unittest import TextTestResult
from app.models import db
from app.auth.forms import LoginForm, RegistrationForm, LoginForm, \
                           RequestResetPasswordForm, ResetPasswordForm
from app.models import User
from app.auth import auth
from app.static.permission_required import permission_required
from app.models import User, Role, Serializer, db
from app.email import send_email



@auth.route('/register', methods=['GET','POST'])
def register():
    """ Register new user, log in as unconfirmed, and send confirmation email """
    form = RegistrationForm()
    if form.validate_on_submit():
        if User.query.filter_by(email=form.email.data.lower()).first():
            flash('User already exists.', category='error')
            return redirect(url_for('home.index'))
        password=form.password.data
        SpecialSym="*?!'^+%&/()=}][{$#"
        if len(password) < 8:
            flash('Password too short. Password must be 8 characters, \
                  have at least one upper case letter, one digit, \
                  and one special character','error')
            return redirect(url_for('auth.register'))
        if not any (char.isupper() for char in password):
            flash('No upper case letter found. Password must be 8 characters, \
                  have at least one upper case letter, one digit, \
                  and one special character','error')

            return redirect(url_for('auth.register'))
        if not any (char.isdigit() for char in password):
            flash('No digit found. Password must be 8 characters, \
                  have at least one upper case letter, one digit, \
                  and one special character','error')
            return redirect(url_for('auth.register'))
        if not any(char in SpecialSym for char in password):
            flash('No special character found. Password must be 8 characters, \
                  have at least one upper case letter, one digit, \
                  and one special character','error')
            return redirect(url_for('auth.register'))

        else:
            user = User(
                first_name=form.first_name.data,
                last_name=form.last_name.data,
                email=form.email.data,
                password=form.password.data,
                confirmed=False)
            db.session.add(user)
            db.session.commit()
            token = user.generate_confirmation_token()
            confirm_link = url_for('auth.confirm', token=token, _external=True)
            send_email(
                recipient=user.email,
                subject='Confirm Your Account',
                template='email/confirm',
                user=user,
                confirm_link=confirm_link)
            flash('A confirmation link has been sent to {}!'.format(user.email),
                  'warning')
            login_user(user)
            return redirect(url_for('home.index'))
    return render_template('security/register_user.html', title='Register',
                           form=form)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    """ Log in """
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
    """ Logs user out"""
    logout_user()
    return redirect(url_for('home.index'))


@auth.route('/confirm-account/<token>')
@login_required
def confirm(token):
    """Accepts token and confirms user if valid"""
    if current_user.confirmed:
        return redirect(url_for('home.index'))
    if current_user.confirm_account(token):
        db.session.commit()
        flash ('You have confirmed your account', 'success')
    else:
        flash('The confirmation link is invalid or expired.')
    return redirect(url_for('home.account_confirmed'))


@auth.route('/confirm-account')
@login_required
def confirm_request():
    """Generates token and sends confirmation link to current user's email"""
    token = current_user.generate_confirmation_token()
    confirm_link = url_for('auth.confirm', token=token, _external=True)
    send_email(
        recipient=current_user.email,
        subject='Confirm Your Account',
        template='email/confirm',
        user=current_user._get_current_object(),
        confirm_link=confirm_link)
    flash('A new confirmation link has been sent to {}.'.format(
        current_user.email), 'warning')
    return redirect(url_for('home.index'))

@auth.route('/reset-password', methods=['GET', 'POST'])
def reset_password_request():
    '''User types in email address to send password reset link w/token'''
    form = RequestResetPasswordForm()
    if not current_user.is_anonymous:
        return redirect(url_for('home.index'))
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is None:
            flash('Invalid email address', 'error')
            return redirect(url_for('home.index'))
        if user is not None:
            token = user.generate_password_reset_token()
            reset_link = url_for('auth.reset_password', token=token,
                                 _external=True)
            send_email(
                recipient = user.email,
                subject = 'Reset Your Password',
                template = 'email/reset_password',
                user = user,
                reset_link = reset_link)
            flash('A password reset link has been sent to {}.'.format(form.email.data),
                  'warning')
        return redirect(url_for('auth.login'))
    return render_template('security/request_pass_reset.html', form=form)


@auth.route('/reset-password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    """User can change password for the email the token was
    sent to. If new password doesn't meet password criteria,
    a new token must be sent"""
    if not current_user.is_anonymous:
        return redirect(url_for('home.index'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        #Add Restrictions for New Password
        new_password=form.new_password.data
        SpecialSym="*?!'^+%&/()=}][{$#"
        if len(new_password) < 8:
            flash('Password too short. Password must be 8 characters, \
                  have at least one upper case letter, one digit, \
                  and one special character','error')
            return redirect(url_for('auth.reset_password_request'))
        if not any (char.isupper() for char in new_password):
            flash('No upper case letter found. Password must be 8 characters, \
                  have at least one upper case letter, one digit, \
                  and one special character','error')
            return redirect(url_for('auth.reset_password_request'))
        if not any (char.isdigit() for char in new_password):
            flash('No digit found. Password must be 8 characters, \
                  have at least one upper case letter, one digit, \
                  and one special character','error')
            return redirect(url_for('auth.reset_password_request'))
        if not any(char in SpecialSym for char in new_password):
            flash('No special character found. Password must be 8 characters, \
                  have at least one upper case letter, one digit, \
                  and one special character','error')
            return redirect(url_for('auth.reset_password_request'))

        user = User.query.filter_by(email=form.email.data).first()
        if user is None:
            flash('Invalid email address.', 'error')
            return redirect(url_for('home.index'))
        if user.reset_password(token, form.new_password.data):
            flash('Your password has been updated.', 'success')
            return redirect(url_for('auth.login'))
        else:
            flash('The password reset link is invalid or has expired.',
                  'error')
            return redirect(url_for('home.index'))
    return render_template('security/set_new_pass.html', form=form)

@auth.before_app_request
def before_request():
    """Force user to confirm email before accessing login-required routes."""
    if current_user.is_authenticated \
            and not current_user.confirmed \
            and request.blueprint != 'auth'\
            and request.endpoint != 'static':
        return redirect(url_for('auth.unconfirmed'))


@auth.route('/unconfirmed')
def unconfirmed():
    """Catch users with unconfirmed emails."""
    if current_user.confirmed:
        return redirect(url_for('home.index'))
    return render_template('security/unconfirmed.html')
