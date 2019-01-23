"""
Testing specific settings
"""

DEBUG = False

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

ADMINS = ['"Admin" <admin@fau.de>']
