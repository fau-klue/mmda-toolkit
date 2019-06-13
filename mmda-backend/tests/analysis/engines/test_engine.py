import pytest
from abc import ABC

from backend.analysis.engines import Engine


@pytest.fixture
def corpus_settings():

    corpus_set = {
        'name': 'foocorpus',
        'sentence_boundary': 's',
        'association_measures': ['Dice', 'Log']
    }

    return corpus_set


def test_abstract_engine(corpus_settings):

    actual = Engine(corpus_settings)
    assert isinstance(actual, ABC)
