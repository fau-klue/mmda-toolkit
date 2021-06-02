"""
Central entrypoint for Flask
"""


import os
import logging
from functools import wraps
from logging.handlers import SMTPHandler
from sys import stdout
from flask import Flask, jsonify, request
from flask_caching import Cache
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from flask_migrate import Migrate
from flask_user import UserManager
from flask_wtf.csrf import CSRFProtect
from flask_jwt_extended import JWTManager, get_jwt_identity, verify_jwt_in_request
from wtforms.fields import HiddenField


# Instantiate Flask extensions
cache = Cache(config={'CACHE_TYPE': 'simple'})
csrf_protect = CSRFProtect()
db = SQLAlchemy()
mail = Mail()
migrate = Migrate()
jwt = JWTManager()


def create_logger(name,
                  log_format='%(asctime)s [%(levelname)s]: %(message)s',
                  log_file=None, is_debug=False):
    """
    Creates a Logger with the config provided.
    Logs are printed to stdout and optionally into a file.

   :param str name: Name of the Logger
   :param str log_format: Logformat for Output Handlers
   :param str log_file: Optional Logfile to use
   :param bool is_debug: Optional Logfile to use
   :return: Configured Logger
   :rtype: logging.Logger
    """

    logger = logging.getLogger(name)
    formatter = logging.Formatter(log_format)

    stdout_handler = logging.StreamHandler(stdout)
    stdout_handler.setFormatter(formatter)
    logger.addHandler(stdout_handler)

    if log_file:
        file_handler = logging.FileHandler(log_file)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    if is_debug:
        logger.setLevel(logging.DEBUG)

    return logger


def preflight_check_vectors_passed(app):
    """
    Preflight: Check if the vector files are available.
    """

    for corpus_settings in app.config['CORPORA'].values():
        if not os.path.exists(corpus_settings['embeddings']):
            print('INFO: Wordvectors {path} not available'.format(
                path=corpus_settings['embeddings'])
            )


def preflight_check_config_passed(app):
    """
    Preflight: Check if config files are available to start the application.
    """

    local_settings_file = 'backend/local_settings_{ENV}.py'.format(
        ENV=app.config['APP_ENV']
    )
    corpora_settings_file = 'backend/corpora_settings_{ENV}.py'.format(
        ENV=app.config['APP_ENV']
    )

    config_available = False
    if os.path.exists(local_settings_file) and os.path.exists(corpora_settings_file):
        config_available = True

    return config_available


def admin_required(fn):
    """
    Decorator: JWT Wrapper to allow admins only
    """

    @wraps(fn)
    def wrapper(*args, **kwargs):  # pylint: disable=missing-docstring
        verify_jwt_in_request()
        identity = get_jwt_identity()

        # For regular tokens without roles
        if not isinstance(identity, dict):
            return jsonify(msg='Unauthorized'), 403

        if 'admin' not in identity['roles']:
            return jsonify(msg='Unauthorized'), 403
        else:
            return fn(*args, **kwargs)

    return wrapper


def user_required(fn):
    """
    Decorator: JWT Wrapper to validate user
    """

    @wraps(fn)
    def wrapper(*args, **kwargs):  # pylint: disable=missing-docstring
        verify_jwt_in_request()
        identity = get_jwt_identity()
        username = request.view_args['username']

        # For regular tokens without roles
        if isinstance(identity, dict):
            identity = identity['username']

        if username != identity:
            return jsonify(msg='Unauthorized'), 403
        else:
            return fn(*args, **kwargs)

    return wrapper


# Initialize Flask Application
def create_app(extra_config_settings={}):
    """
    Create a Flask application.
    """

    # Instantiate Flask
    app = Flask(__name__)

    # Setup CORS
    cors = CORS(app, supports_credentials=True)

    # Load common settings
    app.config.from_object('backend.settings')

    # Load extra settings from extra_config_settings param
    app.config.update(extra_config_settings)

    # Load environment settings
    print('Loading Environment: {ENV}'.format(ENV=app.config['APP_ENV']))
    app.config.from_object('backend.local_settings_{ENV}'.format(
        ENV=app.config['APP_ENV']
    ))
    app.config.from_object('backend.corpora_settings_{ENV}'.format(
        ENV=app.config['APP_ENV']
    ))
    app.config.update(ENV=app.config['APP_ENV'])

    # Preflight: Check if config is available
    if not preflight_check_config_passed(app):
        print('Error: Config files not initialized')
        exit(1)

    # Create central logging instance
    app.logger = create_logger('mmda-logger',
                               log_file=app.config['APP_LOG_FILE'],
                               is_debug=app.config['DEBUG'])

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path, exist_ok=True)
    except OSError:
        app.logger.error("could not create instance folder")
        raise OSError

    # Preflight: Check if wordvectors are available
    preflight_check_vectors_passed(app)

    # Setup Flask-SQLAlchemy
    db.init_app(app)

    # Setup Flask-Migrate
    migrate.init_app(app, db)

    # Setup Flask JWT
    jwt.init_app(app)

    # Setup Flask-Mail
    mail.init_app(app)

    # Setup Flask Caching
    cache.init_app(app)

    # Setup WTForms CSRFProtect
    csrf_protect.init_app(app)

    # Register blueprints
    from .views import register_blueprints
    register_blueprints(app)

    # Define bootstrap_is_hidden_field for flask-bootstrap's bootstrap_wtf.html
    def is_hidden_field_filter(field):
        return isinstance(field, HiddenField)

    app.jinja_env.globals['bootstrap_is_hidden_field'] = is_hidden_field_filter

    # Setup an error-logger to send emails to app.config.ADMINS
    init_email_error_handler(app)

    # Setup Flask-User to handle user account related forms
    from .models.user_models import User
    user_manager = UserManager(app, db, User)

    @app.context_processor
    def context_processor():
        return dict(user_manager=user_manager)

    return app


def init_email_error_handler(app):
    """
    Initialize a logger to send emails on error-level messages.
    Unhandled exceptions will now send an email message to app.config.ADMINS.
    """

    # Do not send error emails while developing
    if app.debug:
        return

    # Retrieve email settings from app.config
    host = app.config['MAIL_SERVER']
    port = app.config['MAIL_PORT']
    from_addr = app.config['USER_EMAIL_SENDER_NAME']
    username = app.config['MAIL_USERNAME']
    password = app.config['MAIL_PASSWORD']
    secure = () if app.config.get('MAIL_USE_TLS') else None

    # Retrieve app settings from app.config
    to_addr_list = app.config['ADMINS']
    subject = app.config.get('APP_SYSTEM_ERROR_SUBJECT_LINE', 'System Error')

    # Setup an SMTP mail handler for error-level messages
    mail_handler = SMTPHandler(
        mailhost=(host, port),            # Mail host and port
        fromaddr=from_addr,               # From address
        toaddrs=to_addr_list,             # To address
        subject=subject,                  # Subject line
        credentials=(username, password),  # Credentials
        secure=secure,
    )
    # Log errors using: app.logger.error('Some error message')
    mail_handler.setLevel(logging.ERROR)
    app.logger.addHandler(mail_handler)
