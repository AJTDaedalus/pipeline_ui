'''
1Feb22 BIOT670 Group 6
settings file for bioinformatics pipeline
structure derived from github.com/corpsgeek/social-app-structure
'''

import os
import secrets

#Set the base directory
basedir = os.path.abspath(os.path.dirname(__name__))

#Create superclass
class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False

#Create development settings
class DevelopmentSettings(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///'+os.path.join(basedir, 'dev-data.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SECRET_KEY = 'Thisismykeyitisverysecret'
    SECURITY_PASSWORD_SALT = 'TEMPORARYSALTYSALT'
    #SERVER_NAME =

class ProductionSettings(Config):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = 'mariadb+mysqlconnector://pipeline:pipeline123@db/pipeline_ui'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = 'Thisismykeyitisverysecret'
