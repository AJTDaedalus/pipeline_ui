'''
1Feb22 BIOT670 Group 6
App initialization file
'''

from flask import Flask
from settings import DevelopmentSettings
from .db import db

def create_app(settings=DevelopmentSettings):
    app = Flask(__name__)
    app.config.from_object(settings)

    db.init_app(app)

    from app.home import home as home_bp
    app.register_blueprint(home_bp)

    with app.app_context():
        db.create_all()

        return app
