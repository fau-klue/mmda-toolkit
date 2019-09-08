"""
Settings common to all environments (development|staging|production)
Place environment specific settings in env_settings.py
An example file (env_settings_example.py) can be used as a starting point
"""


from os import getenv


# Get Host and Port from environment, to make Docker life esier
MMDA_TLS_ENABLE = bool(getenv('TLS_ENABLE', default=''))
MMDA_TLS_KEYFILE = str(getenv('TLS_KEYFILE', default='key.pem'))
MMDA_TLS_CERTFILE = str(getenv('TLS_CERTFILE', default='certificate.pem'))
MMDA_SQL_DATABASE_URI = str(getenv('SQL_DATABASE_URI', default='sqlite:////tmp/backend.sqlite'))
MMDA_APP_ENV = str(getenv('ENVIRONMENT', default='development'))
MMDA_APP_HOST = str(getenv('HOST', default='0.0.0.0'))
MMDA_APP_PORT = int(getenv('PORT', default='5000'))
MMDA_SECRET_KEY = str(getenv('SECRET_KEY', default='Please Change me in production. Stay Save!'))

# Path to Corpus Workbench Registry. See also: CWBEngine Class
REGISTRY_PATH = getenv('CWB_REGISTRY_PATH', default='/usr/local/cwb-3.4.16/share/cwb/registry')

# Application settings
APP_NAME = "MMDA Backend"
APP_SYSTEM_ERROR_SUBJECT_LINE = APP_NAME + " system error"
APP_ENV = MMDA_APP_ENV
APP_LOG_FILE = None

# DO NOT use an Unsecure Secrets in production environments
SECRET_KEY = MMDA_SECRET_KEY

# Flask settings - False, since we're using JWT
WTF_CSRF_ENABLED = False

# Database Settings
SQLALCHEMY_DATABASE_URI = MMDA_SQL_DATABASE_URI
# Avoids a SQLAlchemy deprecation warning
SQLALCHEMY_TRACK_MODIFICATIONS = False

# TLS settings
APP_TLS_ENABLE = MMDA_TLS_ENABLE
APP_TLS_KEYFILE = MMDA_TLS_KEYFILE
APP_TLS_CERTFILE = MMDA_TLS_CERTFILE

# Flask-User settings
USER_APP_NAME = APP_NAME
USER_MIN_PASSWORD_LENGTH = 8
USER_ENABLE_CHANGE_PASSWORD = True  # Allow users to change their password
USER_ENABLE_CHANGE_USERNAME = False  # Allow users to change their username
USER_ENABLE_CONFIRM_EMAIL = True  # Force users to confirm their email
USER_ENABLE_FORGOT_PASSWORD = True  # Allow users to reset their passwords
USER_ENABLE_EMAIL = False  # Register with Email
USER_ENABLE_REGISTRATION = True  # Allow new users to register
USER_REQUIRE_RETYPE_PASSWORD = True  # Prompt for `retype password` in:
USER_ENABLE_USERNAME = False  # Register and Login with username
