import os

import pytest
from flask_jwt_extended import create_access_token

from backend import create_app
from backend.database import db as the_db
from backend.database import init_db

here = os.path.dirname(os.path.realpath(__file__))


# Init test vectors
test_vectors = open('/tmp/foo.pymagnitude', 'w')
test_vectors.write('nothing to see here')
test_vectors.close()


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


@pytest.fixture
def test_corpus():
    """ settings for GERMAPARL1386 """

    corpus_name = "GERMAPARL1386"

    query = '[lemma="Seehofer"]'

    parameters = {
        'context': 20,
        's_context': 's',
        's_query': 's',
        'p_query': 'lemma',
        'window_sizes': [3, 5, 7],
        's_show': ['text_id']
    }

    discoursemes = {
        'topic': ["CDU", "CSU"],
        'disc1': ["und"],
        'disc2': ["Bundesregierung"],
        # 'disc3': ['Klimawandel'],
        # 'disc4': ['Wirtschaftskrise']
    }

    discoursemes2 = {
        'Klimawandel': ["Klimawandel", "Klimaveränderung", "Klimaänderung", "Klimawechsel", "globale Erwärmung"],
        'Kampf': ["Bekämpfung", "Kampf", "aufhalten"],
        'Ressourcen': ["Armut", "Hunger", "Dürre", "Ressourcenknappheit"],
        'Wetter': ["Sturm", "Wetterereignis", "Naturkatastrophe"],
        'Anpassung': ["Anpassungsmaßnahme", "Maßnahme", "bewältigen", "Anpassung"]
    }

    with open(os.path.join(here, "corpora", "collocates-atomkraft-germaparl1318.txt")) as f:
        collocates_atomkraft = set(f.read().split("\n"))

    return {
        'corpus_name': corpus_name,
        'query': query,
        'parameters': parameters,
        'discoursemes': discoursemes,
        'discoursemes2': discoursemes2,
        'collocates_atomkraft': collocates_atomkraft
    }
