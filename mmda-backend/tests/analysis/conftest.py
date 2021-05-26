# This file contains pytest 'fixtures'.
# If a test functions specifies the name of a fixture function as a parameter,
# the fixture function is called and its result is passed to the test function.

import pytest
from backend import create_app
from backend.commands.init_db import init_db
import os


here = os.path.dirname(os.path.realpath(__file__))


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
    """ settings for GERMAPARL1318 """

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
        'disc2': ["Ausstieg", "Laufzeit"],
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

    collocates_atomkraft = set(open(os.path.join(here, "collocates-atomkraft-germaparl1318.txt")).read().split("\n"))

    return {
        'corpus_name': corpus_name,
        'query': query,
        'parameters': parameters,
        'discoursemes': discoursemes,
        'discoursemes2': discoursemes2,
        'collocates_atomkraft': collocates_atomkraft
    }
