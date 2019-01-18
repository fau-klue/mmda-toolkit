"""
Environment specific settings
"""


# DO NOT use "DEBUG = True" in production environments
DEBUG = True

# DO NOT use an Unsecure Secrets in production environments
SECRET_KEY = 'DO NOT use an Unsecure Secrets in production environments'

# JWT Settings
JWT_ACCESS_TOKEN_EXPIRES = False
JWT_REFRESH_TOKEN_EXPIRES = False

# SQLAlchemy settings
SQLALCHEMY_DATABASE_URI = 'sqlite:///../backend.sqlite'
# Avoids a SQLAlchemy deprecation warning
SQLALCHEMY_TRACK_MODIFICATIONS = False

# TLS settings
APP_TLS_KEYFILE = '/privkey.pem'
APP_TLS_CERTFILE = '/cert.pem'

# Flask-Mail settings
MAIL_SERVER = 'localhost'
MAIL_PORT = 1025
MAIL_USE_SSL = False
MAIL_USE_TLS = False
MAIL_USERNAME = 'yourname@gmail.com'
MAIL_PASSWORD = 'password'

# Flask-User settings
USER_APP_NAME = 'MMDA Backend'
USER_EMAIL_SENDER_NAME = 'FAU'
USER_EMAIL_SENDER_EMAIL = 'mmda@fau.de'

ADMINS = [
    '"Admin" <admin@fau.de>',
    ]
