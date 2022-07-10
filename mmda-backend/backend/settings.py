"""
Settings common to all environments (development|testing|production)
Place environment specific settings in settings_{ENVIRONMENT}.py
"""


from os import getenv

# APPLICATION AND ADMIN SETTINGS
APP_NAME = "MMDA Backend"
USER_EMAIL_SENDER_NAME = 'MMDA'
USER_EMAIL_SENDER_EMAIL = 'mmda@fau.de'
ADMINS = [
    '"Admin" <mmda@fau.de>',
]

################################
# SET VIA ENVIRONMENT VARIABLES
################################

# MMDA CACHE
ANYCACHE_PATH = str(getenv('ANYCACHE_PATH', '/tmp/mmda-anycache/'))

# ENVIRONMENT
APP_ENV = str(getenv('ENVIRONMENT', default='development'))

# SECRECT KEY
SECRET_KEY = str(getenv('SECRET_KEY', default='Please Change me in production. Stay Save!'))

# HOST AND PORT
MMDA_APP_HOST = str(getenv('HOST', default='0.0.0.0'))
MMDA_APP_PORT = int(getenv('PORT', default='5000'))

# TLS SETTINGS
APP_TLS_ENABLE = bool(getenv('TLS_ENABLE', default=''))
APP_TLS_KEYFILE = str(getenv('TLS_KEYFILE', default='key.pem'))
APP_TLS_CERTFILE = str(getenv('TLS_CERTFILE', default='certificate.pem'))

####################
# CONSTANT SETTINGS
####################

# DO NOT use "DEBUG = True" in production environments
DEBUG = True if APP_ENV == 'development' else False

# JWT Settings (seconds)
JWT_ACCESS_TOKEN_EXPIRES = 60*60*12 if APP_ENV == 'production' else False
JWT_REFRESH_TOKEN_EXPIRES = 60*60*12 if APP_ENV == 'production' else False
WTF_CSRF_ENABLED = False        # False since we're using JWT

# Application settings
APP_SYSTEM_ERROR_SUBJECT_LINE = APP_NAME + " system error"
APP_LOG_FILE = None

# Avoid SQLAlchemy deprecation warning
SQLALCHEMY_TRACK_MODIFICATIONS = False

# Flask-Mail settings
MAIL_SERVER = 'localhost'
MAIL_PORT = 1025
MAIL_USE_SSL = False
MAIL_USE_TLS = False
MAIL_USERNAME = 'mmda@fau.de'
MAIL_PASSWORD = 'password'

# Flask-User settings
USER_APP_NAME = APP_NAME
USER_MIN_PASSWORD_LENGTH = 8
USER_ENABLE_CHANGE_PASSWORD = True  # Allow users to change their password
USER_ENABLE_CHANGE_USERNAME = False  # Allow users to change their username
USER_ENABLE_CONFIRM_EMAIL = True  # Force users to confirm their email
USER_ENABLE_FORGOT_PASSWORD = True  # Allow users to reset their passwords
USER_ENABLE_EMAIL = False  # Register with Email
USER_ENABLE_REGISTRATION = True  # Allow new users to register
USER_REQUIRE_RETYPE_PASSWORD = True  # Prompt for `retype password`
USER_ENABLE_USERNAME = False  # Register and Login with username
