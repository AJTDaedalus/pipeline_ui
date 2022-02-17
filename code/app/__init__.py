'''
1Feb22 BIOT670 Group 6
App initialization file
'''

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from settings import DevelopmentSettings


def create_app(settings=DevelopmentSettings):
    app = Flask(__name__)
    app.config.from_object(settings)

    db = SQLAlchemy(app)
    db.init_app(app)

    from app.home import home as home_bp
    app.register_blueprint(home_bp)

    with app.app_context():
        db.create_all()

        return app
