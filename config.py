from logging import DEBUG
import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'i-did-not-created-it-yet'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or\
         os.environ.get('URI_POSTGRES') or \
             'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    LOG_TO_STDOUT = os.environ.get('LOG_TO_STDOUT')

    