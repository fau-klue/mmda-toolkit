#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Central entrypoint for Flask
"""


import logging
import os
from functools import wraps
from sys import stdout

from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_jwt_extended import (JWTManager, get_jwt_identity,
                                verify_jwt_in_request)
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
from wtforms.fields import HiddenField

# Instantiate Flask extensions
csrf_protect = CSRFProtect()
db = SQLAlchemy()
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

    # add stdout handler
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
    CORS(app, supports_credentials=True)

    # Load common settings
    app.config.from_object('settings')

    # Load extra settings from extra_config_settings param
    app.config.update(extra_config_settings)

    # Load corpora settings
    print('Loading Corpora: {PATH}'.format(PATH=app.config['CORPORA_SETTINGS']))
    app.config.from_pyfile(app.config['CORPORA_SETTINGS'])

    # Preflight: Check if wordvectors are available
    preflight_check_vectors_passed(app)

    # Create central logging instance
    app.logger = create_logger('mmda-logger',
                               log_file=app.config['APP_LOG_FILE'],
                               is_debug=app.config['DEBUG'])

    # initialise database
    from . import database
    app.register_blueprint(database.bp)
    db.init_app(app)

    # Setup Flask JWT
    jwt.init_app(app)

    # Setup WTForms CSRFProtect
    csrf_protect.init_app(app)

    # Register blueprints
    from .views import register_blueprints
    register_blueprints(app)

    # Define bootstrap_is_hidden_field for flask-bootstrap's bootstrap_wtf.html
    def is_hidden_field_filter(field):
        return isinstance(field, HiddenField)

    app.jinja_env.globals['bootstrap_is_hidden_field'] = is_hidden_field_filter

    return app
