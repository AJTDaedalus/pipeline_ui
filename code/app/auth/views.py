from flask import render_template, redirect, url_for, flash, request, Flask, current_app, session
from app.models import db
from app.auth.forms import RegistrationForm
from app.auth.forms import LoginForm
from app.models import *
from app.auth import auth
from flask_login import (login_user, login_required, current_user, logout_user)
from werkzeug.wrappers import Request, Response
from werkzeug.exceptions import HTTPException, NotFound, Forbidden
from flask_security import Security, SQLAlchemyUserDatastore, UserMixin, RoleMixin, login_required
from flask_principal import Principal, Permission, RoleNeed, Identity, AnonymousIdentity, identity_changed, identity_loaded

admin_permission = Permission(RoleNeed('admin'))
#wasn't sure what to name these other two levels of permission
low_permission = Permission(RoleNeed('low'))
medium_permission = Permission(RoleNeed('medium'))

 
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
    return render_template('security/register_user.html', title='Register', form=form)

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
        identity_changed.send(
            current_app._get_current_object(), identity=Identity(user.id),
        )
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
    #Remove session keys set by Flask-Principal
    for key in ('identity.name', 'identity.auth_type'):
        session.pop(key,None)
    #Tell Flask-Principal the user is anonymous
    identity_changed.send(current_app._get_current_object(), identity=AnonymousIdentity())
    return redirect(url_for('home.index'))
    
#@auth.errorhandler(werkzeug.exceptions.Forbidden)
#def handle_bad_request(e):
#    return(
#        Response("Forbidden"),
#        403,
#    )



#@auth.route("/protected/view")
#@login_required
#@view_permission.require(403)
#def protected_view():
#    return Response("view protected")    