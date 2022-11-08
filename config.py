# NOTE: Secret key generation:
# python -c 'import secrets; print(secrets.token_hex())'

from os import environ, path
from dotenv import load_dotenv

basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, ".env"))


class Config:
    """ Set Flask config variales """

    # Flask
    FLASK_APP = environ.get('FLASK_APP')
    FLASK_ENV = 'development'
    FLASK_DEBUG = True

    # Session
    SESSION_TYPE = "filesystem"
    SESSION_PERMANENT = False
    SECRET_KEY = environ.get('SECRET_KEY')

    # SQLAlchemy
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + path.join(basedir, 'bmi.db')
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Static Assets
    STATIC_FOLDER = 'static'
    TEMPLATES_FOLDER = 'templates'
    TEMPLATES_AUTO_RELOAD = True
