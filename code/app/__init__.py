'''
1Feb22 BIOT670 Group 6
App initialization file
'''

from flask import Flask
from settings import DevelopmentSettings

def create_app(settings=DevelopmentSettings):
    app = Flask(__name__)
    app.config.from_object(settings)

    from app.home import home as home_bp
    app.register_blueprint(home_bp)

    return app
