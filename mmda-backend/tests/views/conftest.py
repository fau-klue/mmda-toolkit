# This file contains pytest 'fixtures'.
# If a test functions specifies the name of a fixture function as a parameter,
# the fixture function is called and its result is passed to the test function.

import pytest
from flask_jwt_extended import create_access_token
from backend import create_app, db as the_db


# Init test vectors
test_vectors = open('/tmp/foo.pymagnitude', 'w')
test_vectors.write('nothing to see here')
test_vectors.close()

# Initialize the Flask-App with test-specific settings
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
from backend.commands.init_db import init_db
init_db()
# Run twice to ensure the function runs idempotently
init_db()


@pytest.fixture(scope='session')
def app():
    """ Makes the 'app' parameter available to test functions. """
    return the_app


@pytest.fixture(scope='session')
def db():
    """ Makes the 'db' parameter available to test functions. """
    return the_db


@pytest.fixture(scope='function')
def session(db, request):
    """Creates a new database session for a test."""
    connection = db.engine.connect()
    transaction = connection.begin()

    options = dict(bind=connection, binds={})
    session = db.create_scoped_session(options=options)

    db.session = session

    def teardown():
        transaction.rollback()
        connection.close()
        session.remove()

    request.addfinalizer(teardown)
    return session


@pytest.fixture(scope='session')
def client(app):
    return app.test_client()


@pytest.fixture
def header():
    access_token = create_access_token('student1')

    headers = {
        'Authorization': 'Bearer {}'.format(access_token)
    }

    return headers


@pytest.fixture
def admin_header():
    access_token = create_access_token(identity={'username': 'admin', 'roles': ['admin']})

    headers = {
        'Authorization': 'Bearer {}'.format(access_token)
    }

    return headers
