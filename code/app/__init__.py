'''
1Feb22 BIOT670 Group 6
App initialization file
'''

import os
import datetime
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from settings import DevelopmentSettings, ProductionSettings
from app.models import db
from app.models import login_manager, User, Role, Job
from flask_login import current_user, login_required
from flask_wtf.csrf import CSRFProtect

csrf = CSRFProtect()

if os.environ.get("FLASK_ENV") == 'production':
    settings = ProductionSettings
else:
    settings = DevelopmentSettings


def create_app(settings=settings):
    app = Flask(__name__)
    app.config.from_object(settings)

    db.init_app(app)
    login_manager.init_app(app)
    migrate = Migrate(app, db)

    from app.home import home as home_bp
    from app.auth import auth as auth_bp
    app.register_blueprint(home_bp)
    app.register_blueprint(auth_bp)


    db.init_app(app)
    login_manager.init_app(app)
    csrf.init_app(app)


    with app.app_context():
        db.create_all()
        #Test code below, please remove before production launch
        if not db.session.query(User).first():
            test_user = User(email='me123@gmail.com',
                             first_name='Me', last_name='MEME',
                             password="12345678")
            #test_role = Role(name='test')
            test_user.roles.append(Role(name='admin'))
            test_user.roles.append(Role(name='Placeholder1'))
            print (test_user.roles)
            db.session.add(test_user)
            db.session.commit()

        if not db.session.query(Job).first():
            user=User.query.filter_by(email='me123@gmail.com').first()
            test_job1 = Job(JobID=1,
                            JobName="Job 1",
                            DateSubmit=datetime.datetime.now(),
                            DateStart=None,
                            DateEnd=None,
                            Status="Pending",
                            user=user
            )
            test_job2 = Job(JobID=2,
                            JobName="Job 2",
                            DateSubmit=datetime.datetime.now(),
                            DateStart=datetime.datetime.now(),
                            DateEnd=None,
                            Status="Running",
                            user=user
            )
            test_job3 = Job(JobID=3,
                            JobName="Job 3",
                            DateSubmit=datetime.datetime.now(),
                            DateStart=datetime.datetime.now(),
                            DateEnd=datetime.datetime.now(),
                            Status="Complete",
                            user=user
            )
            test_job4 = Job(JobID=4,
                            JobName="Job 4",
                            DateSubmit=datetime.datetime.now(),
                            DateStart=datetime.datetime.now(),
                            DateEnd=datetime.datetime.now(),
                            Status="Fail",
                            user=user
            )
            test_job5 = Job(JobID=5,
                            JobName="Job 5",
                            DateSubmit=datetime.datetime.now(),
                            DateStart=datetime.datetime.now(),
                            DateEnd=datetime.datetime.now(),
                            Status="Unknown",
                            user=user
            )
            db.session.add(test_job1)
            db.session.add(test_job2)
            db.session.add(test_job3)
            db.session.add(test_job4)
            db.session.add(test_job5)
            db.session.commit()

        #Test code above, please remove before production launch
        return app
