'''
1Feb22 BIOT670 Group 6
App initialization file
'''

import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from settings import DevelopmentSettings, ProductionSettings
from app.models import db
from app.models import login_manager, User, Role
from flask_login import current_user, login_required
from flask_wtf.csrf import CSRFProtect
from flask_mail import Mail

csrf = CSRFProtect()
mail = Mail()

if os.environ.get("FLASK_ENV") == 'production':
    settings = ProductionSettings
else:
    settings = DevelopmentSettings

def create_app(settings=settings):
    app = Flask(__name__)
    app.config.from_object(settings)

    from app.home import home as home_bp
    from app.auth import auth as auth_bp
    app.register_blueprint(home_bp)
    app.register_blueprint(auth_bp)

    #Email
        
    app.config['MAIL_SERVER'] = 'smtp.gmail.com'
    app.config['MAIL_PORT'] = 587
    app.config['MAIL_USE_TLS'] = True
    app.config['MAIL_USE_SSL'] = False
    app.config['MAIL_USERNAME'] = 'biot670testing@gmail.com'
    app.config['MAIL_PASSWORD'] = 'zwrfwpdmcobjlsdj'
    app.config['MAIL_DEFAULT_SENDER'] = 'biot670testing@gmail.com'            
    
    mail.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)
    csrf.init_app(app)

    with app.app_context():
        db.create_all()
        #Test code below, please remove before production launch
        if not db.session.query(User).first():
            test_user = User(email='me123@gmail.com',
                             first_name='Me', last_name='MEME',
                             password="12345678",
                             confirmed=True)
            #test_role = Role(name='test')
            test_user.roles.append(Role(name='admin'))
            test_user.roles.append(Role(name='Placeholder1'))
            print (test_user.roles)
            db.session.add(test_user)
            db.session.commit()
        #Test code above, please remove before production launch
        return app

