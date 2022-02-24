'''
BIOT670 Initial database module for pipeline UI
taken from https://flask-roles.readthedocs.io/en/latest/usage.html
'''

from flask import Flask, flash, redirect, url_for, request, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from flask_login import LoginManager, current_user, login_required, login_user
from passlib.hash import pbkdf2_sha512
from flask_principal import Identity, Permission, RoleNeed, identity_loaded, identity_changed, UserNeed
import flask_login
import flask_roles
from flask_security import SQLAlchemyUserDatastore, Security
from flask_security.models import fsqla_v2 as fsqla

login_manager = LoginManager()
login_manager.login_view = 'login'
db = SQLAlchemy()

fsqla.FsModels.set_db_info(db)

@login_manager.user_loader
def load_user(user_id):
    user = db.session.query(User).get(int(user_id))
    return user

@login_manager.unauthorized_handler
def unauthorized():
    return(
    Response("You must be logged in to view that page."),
    401,
    )

 
    


class Role(db.Model, fsqla.FsRoleMixin):
    """
    Role class. A role has the following properties
     - name: A textual representation e.g. accounts.send_money
     - parent: Optional reference to a parent role that owns this role.
    """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    description = db.Column(db.String(140), unique=False, nullable=False)
    parent_id = db.Column(db.Integer, db.ForeignKey("role.id"))
    children = db.relationship(
        "Role",
        lazy="joined",
        join_depth=2,
        order_by=id,
        backref=db.backref("parent", remote_side=[id]),
    )

    def __repr__(self):
        return "<Role %r>" % self.name

class User(db.Model, fsqla.FsUserMixin):
    """
    User class. Your Typical user class.
    You will need to add UserMixin from flask_login and flask_roles
    You may add helper properties roles and groups for your use cases:
     - roles: User has role assigned directly (user_role table stores the relationship)
     - groups: User is assigned to groups which have assigned roles.
    """
    __tablename__ = 'user'
    
    id = db.Column(db.Integer, primary_key=True)
    active = db.Column(db.Boolean, default=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password = db.Column(db.String(128))
    fs_uniquifier = db.Column(db.String(255), unique=True, nullable=False)
    roles = db.relationship(
        "Role",
        secondary="user_role",
        backref=db.backref("roles", lazy="dynamic"),
    )
    groups = db.relationship(
        "Group", secondary="user_group", backref=db.backref("users"),
    )
    
    def set_password(self, password):
        self.password = pbkdf2_sha512.using(salt_size=8).hash(password)
        
    def check_password(self, password):
        return pbkdf2_sha512.verify(password, self.password)
        
    def __repr__(self):
        return "<User %r>" % self.username

        
class UserRole(db.Model):
    """Stores user assigned roles"""
    user_id = db.Column(
        "user_id", db.Integer, db.ForeignKey("user.id"), primary_key=True,
    )
    role_id = db.Column(
        "role_id", db.Integer, db.ForeignKey("role.id"), primary_key=True,
    )

class Group(db.Model, flask_roles.GroupMixin):
    id = db.Column(db.Integer, primary_key=True)
    name= db.Column(db.String(80), unique=True, nullable=False)
    roles = db.relationship(
        "Role",
        secondary="group_role",
        backref=db.backref("groups", lazy="dynamic"),
    )
    def __repr__(self):
        return "<Group %r>" % self.name
    
class GroupRole(db.Model):
    """Stores group assigned roles"""
    group_id = db.Column(
        db.Integer, db.ForeignKey("group.id"), primary_key=True,
    )
    role_id = db.Column(
        db.Integer, db.ForeignKey("role.id"), primary_key=True,
    )

class UserGroup(db.Model):
    """"Stores assignments of users to groups"""
    group_id = db.Column(
        db.Integer, db.ForeignKey("group.id"), primary_key=True,
    )
    user_id = db.Column(
        db.Integer, db.ForeignKey("user.id"), primary_key=True,
    )    

