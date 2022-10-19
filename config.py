import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    """ Set Flask config variables """

    # General Config
    FLASK_APP = 'wsgi.py'
    FLASK_ENV = 'development'
    STATIC_FOLDER = 'static'
    TEMPLATES_FOLDER = 'templates'
    TEMPLATES_AUTO_RELOAD = True

    # Database
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + \
        os.path.join(basedir, 'bmi.db')
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Session
    SESSION_PERMANENT = False
    SESSION_TYPE = "filesystem"
