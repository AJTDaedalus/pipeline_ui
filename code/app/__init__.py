'''
1Feb22 BIOT670 Group 6
App initialization file
'''

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from settings import DevelopmentSettings
from app.models import db
from app.models import login_manager
from flask_roles import Roles
from flask_security import SQLAlchemyUserDatastore, Security, UserMixin, RoleMixin
from app.auth.views import admin_permission, security, user_datastore
from flask_principal import Principal, identity_loaded
from flask_login import current_user

roles=Roles()
principals = Principal()

    
def create_app(settings=DevelopmentSettings):
    app = Flask(__name__)
    app.config.from_object(settings)

    #@identity_loaded.connect_via(app)
    #def on_identity_loaded(sender, identity):
    #    identity.user = current_user
    #    #Add the UserNeed to the identity
    #    if hasattr(current_user, 'user.id'):
    #        identity.provides.add(UserNeed(current_user.id))
    #    #Add any roles for the user via group membership
    #    if hasattr(current_user, 'group.id'):
    #       the_user = db.query.filter_by(id=current_user).first()
      #      for g in the_user.group_id:
     #           identity.provides.add(RoleNeed('{}'.format(g.group_name)))
    
    
    from app.home import home as home_bp
    from app.auth import auth as auth_bp
    app.register_blueprint(home_bp)
    app.register_blueprint(auth_bp)
    
                
    db.init_app(app)
    login_manager.init_app(app)
    roles.init_app(app)
    principals.init_app(app)
    security.init_app(app,user_datastore)
    
    
                
    with app.app_context():
        db.create_all()

        return app

