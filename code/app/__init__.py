'''
1Feb22 BIOT670 Group 6
App initialization file
'''

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from settings import DevelopmentSettings
from app.models import db
from app.models import login_manager
from flask_login import current_user, login_required



    
def create_app(settings=DevelopmentSettings):
    app = Flask(__name__)
    app.config.from_object(settings)

        
    
    from app.home import home as home_bp
    from app.auth import auth as auth_bp
    app.register_blueprint(home_bp)
    app.register_blueprint(auth_bp)
    
                
    db.init_app(app)
    login_manager.init_app(app)
    
    
    with app.app_context():
        db.create_all()

        return app

