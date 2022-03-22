from flask import render_template, redirect, url_for, flash, request, Flask, \
                  current_app, session
from app.auth.forms import RegistrationForm, LoginForm
from flask_login import login_user, login_required, current_user, logout_user
from unittest import TextTestResult
from app.models import db
from app.auth.forms import LoginForm, NewRoleForm, AssignRoleForm, \
                           RemoveRoleForm
from app.models import User
from app.auth import auth
from app.auth.permission_required import permission_required
from app.models import db
from app.models import User, Role


#registration route
@auth.route('/register', methods=['GET','POST'])
def register():
    form = RegistrationForm()
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
            flash('Password must include at least one upper case letter',
                  'error')
            return redirect(url_for('auth.register'))
        if not any (char.isdigit() for char in password):
            flash('Password must include at least one digit.','error')
            return redirect(url_for('auth.register'))
        if not any(char in SpecialSym for char in password):
            flash('Password must include at least one special character.',
                  'error')
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
    return render_template('security/register_user.html', title='Register',
                           form=form)

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

#Admin route
@auth.route('/admin', methods=['GET', 'POST'])
@login_required
@permission_required('admin')
def admin():
    nrole = NewRoleForm()
    if nrole.create.data and nrole.validate():
        if not Role.query.filter_by(name=nrole.name.data).first():
            print(nrole.name.data)
            new_role = Role(name=nrole.name.data)
            db.session.add(new_role)
            db.session.commit()
            flash("Role created.",'success')
        else:
            flash("Role already exists.",'error')

    #Deal with requests to assign roles to users
    assign = AssignRoleForm()
    if assign.assign.data and assign.validate():
        for u in assign.user.iter_choices():
            if u[2] == True:
                user = User.query.get(u[0])
                for r in assign.new_roles.iter_choices():
                    if r[2] == True:
                        user.assign_role(r[1])

    #Deal with requests to remove roles from users
    remove = RemoveRoleForm()
    if remove.remove.data and remove.validate():
        for u in remove.user.iter_choices():
            if u[2] == True:
                user = User.query.get(u[0])
                for r in remove.rem_roles.iter_choices():
                    if r[2] == True:
                        print(r[1])
                        user.remove_role(r[1])

    return render_template('security/admin.html', nrole=NewRoleForm(),
                           assign=AssignRoleForm(), remove=RemoveRoleForm())

#logout route
@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('home.index'))
