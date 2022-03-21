from flask import render_template, redirect, url_for, flash, request, Flask, current_app, session
from app.auth.forms import RegistrationForm, LoginForm
from flask_login import login_user, login_required, current_user, logout_user
from unittest import TextTestResult
from app.models import db
from app.auth.forms import LoginForm
from app.auth import auth
from app.auth.permission_required import permission_required
from app.models import db
from app.models import User, Role, Serializer
from app.email import send_email


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
            flash('A confirmation link has been sent to {}!'.format(user.email), 'warning')
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

@auth.route('/confirm-account/<token>')
#@login_required
def confirm(token):
    """Confirm new user's account with provided token."""
    print(token)
    try:
        s = Serializer(app.config['SECRET_KEY'])
        email = s.loads(token, salt='email-confirm')
    except:
        flash('The confirmation link is invalid or expired', 'error')
        return redirect(url_for('auth.login'))
    user= User.query.filter_by(email=email).first_or_404()
    if user.confirmed:
        return redirect(url_for('home.index'))    
    else:
        user.confirmed = True
        db.session.add(user)
        db.session.commit()
        flash('You have confirmed your account. Thanks!', 'success')
    return redirect(url_for('home.index'))

@auth.route('/confirm-account')
@login_required
def confirm_request():
    """Respond to new user's request to confirm their account."""
    token = current_user.generate_confirmation_token()
    confirm_link = url_for('auth.confirm', token=token, _external=True)
    send_email(
        recipient=current_user.email,
        subject='Confirm Your Account',
        template='email/confirm',
        # current_user is a LocalProxy, we want the underlying user object
        user=current_user._get_current_object(),
        confirm_link=confirm_link)
    flash('A new confirmation link has been sent to {}.'.format(
        current_user.email), 'warning')
    return redirect(url_for('home.index'))
    
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