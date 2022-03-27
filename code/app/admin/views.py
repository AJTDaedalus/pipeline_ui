from flask import render_template, redirect, url_for, flash, request, Flask, \
                  current_app, session
from flask_login import login_user, login_required, current_user
from app.models import db
from app.admin.forms import NewRoleForm, AssignRoleForm, RemoveRoleForm
from app.models import User
from app.admin import admin
from app.static.permission_required import permission_required
from app.models import User, Role, db


#Admin route
@admin.route('/admin', methods=['GET', 'POST'])
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
