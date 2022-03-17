'''
1Feb22 BIOT670 Group 6
App initialization file
'''

import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from settings import DevelopmentSettings, ProductionSettings
from app.models import db
from app.models import login_manager

if os.environ.get("FLASK_ENV") == 'production':
    settings = ProductionSettings
else:
    settings = DevelopmentSettings

def create_app(settings=settings):
    app = Flask(__name__)
    app.config.from_object(settings)

    db.init_app(app)
    login_manager.init_app(app)

    from app.home import home as home_bp
    from app.auth import auth as auth_bp
    app.register_blueprint(home_bp)
    app.register_blueprint(auth_bp)

    with app.app_context():
        db.create_all()

        return app
