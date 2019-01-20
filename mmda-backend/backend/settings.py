"""
Settings common to all environments (development|staging|production)
Place environment specific settings in env_settings.py
An example file (env_settings_example.py) can be used as a starting point
"""


# Application settings
APP_NAME = "MMDA Backend"
APP_SYSTEM_ERROR_SUBJECT_LINE = APP_NAME + " system error"

# Flask settings
# Since we use JWT
WTF_CSRF_ENABLED = False

# Avoids a SQLAlchemy deprecation warning
SQLALCHEMY_TRACK_MODIFICATIONS = False

# TLS settings
APP_TLS_ENABLE = False
APP_TLS_KEYFILE = 'private_key.pem'
APP_TLS_CERTFILE = 'certificate.pem'

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
