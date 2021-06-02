"""
Settings common to all environments (development|staging|production)
Place environment specific settings in env_settings.py
An example file (env_settings_example.py) can be used as a starting point
"""


from os import getenv

################################
# SET VIA ENVIRONMENT VARIABLES
################################
# CWB-CCC PATHS
CCC_REGISTRY_PATH = getenv('CWB_REGISTRY_PATH', default='/usr/local/share/cwb/registry')
CCC_DATA_PATH = getenv('CCC_DATA_PATH', default='/tmp/mmda-ccc/')
CCC_CQP_BIN = getenv('CQP_BIN', default='cqp')
CCC_LIB_PATH = getenv('CCC_LIB_PATH', None)

# SEPARATE MMDA CACHE
ANYCACHE_PATH = getenv('ANYCACHE_PATH', '/tmp/mmda-anycache/')

# DATABASE URI
SQLALCHEMY_DATABASE_URI = getenv('SQL_DATABASE_URI', 'sqlite:////tmp/mmda.sqlite')

# SECRECT KEY (MO: change in production!)
SECRET_KEY = str(getenv('SECRET_KEY', default='Please Change me in production. Stay Save!'))

# ENVIRONMENT
APP_ENV = str(getenv('ENVIRONMENT', default='development'))

# HOST AND PORT (MO: get from environment to make Docker life easier)
MMDA_APP_HOST = str(getenv('HOST', default='0.0.0.0'))
MMDA_APP_PORT = int(getenv('PORT', default='5000'))

# TLS SETTINGS
APP_TLS_ENABLE = bool(getenv('TLS_ENABLE', default=''))
APP_TLS_KEYFILE = str(getenv('TLS_KEYFILE', default='key.pem'))
APP_TLS_CERTFILE = str(getenv('TLS_CERTFILE', default='certificate.pem'))


#####################
# CONSTANT VARIABLES
#####################
# Application settings
APP_NAME = "MMDA Backend"
APP_SYSTEM_ERROR_SUBJECT_LINE = APP_NAME + " system error"
APP_LOG_FILE = None

# Flask settings - False, since we're using JWT
WTF_CSRF_ENABLED = False

# Avoids SQLAlchemy deprecation warning
SQLALCHEMY_TRACK_MODIFICATIONS = False

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
