# This file contains pytest 'fixtures'.
# If a test functions specifies the name of a fixture function as a parameter,
# the fixture function is called and its result is passed to the test function.

import pytest
from flask_jwt_extended import create_access_token
from backend import create_app, db as the_db
from backend.commands.init_db import init_db

the_app = create_app(dict(
    TESTING=True,  # Propagate exceptions
    DEBUG=False,
    APP_ENV='testing',
    LOGIN_DISABLED=False,  # Enable @register_required
    MAIL_SUPPRESS_SEND=True,  # Disable Flask-Mail send
    SERVER_NAME='localhost',  # Enable url_for() without request context
    SQLALCHEMY_DATABASE_URI='sqlite:///:memory:',  # In-memory SQLite DB
    WTF_CSRF_ENABLED=False,  # Disable CSRF form validation
))

# Setup an application context (since the tests run outside of the webserver context)
the_app.app_context().push()

# Create and populate roles and users tables
init_db()


@pytest.fixture(scope='session')
def app():
    """ Makes the 'app' parameter available to test functions. """
    return the_app


@pytest.fixture
def test_corpus():
    """ settings for GERMAPARL_1114 """

    corpus_name = "GERMAPARL1318"

    query = '[lemma="Atomkraft"]'

    parameters = {
        'context': 20,
        's_context': 's',
        's_query': 's',
        'p_query': 'lemma',
        'window_sizes': [3, 5, 7],
        's_show': ['text_id']
    }

    discoursemes = {
        'topic': ['Atomkraft', 'Atomenergie', 'Kernkraft'],
        'disc1': ["CDU", "CSU"],
        'disc2': ["Ausstieg", "Laufzeit"]
    }

    return {
        'corpus_name': corpus_name,
        'query': query,
        'parameters': parameters,
        'discoursemes': discoursemes,
    }
