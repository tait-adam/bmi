# TODO: Move secret key to dotenv
# NOTE: Secret key generation:
# python -c 'import secrets; print(secrets.token_hex())'

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
    SECRET_KEY = 'b45c99a40877a33a7bfbdabdd696dff2eb9805e06562773dbb21253cd96ad4a0'  # NOQA
