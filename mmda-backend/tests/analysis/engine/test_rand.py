import pytest
import unittest.mock as mock
from abc import ABC

from backend.analysis.engines import *


@pytest.fixture
def corpus_settings():

    corpus_set = {
        'sentence_boundary': 's',
        'association_measures': ['Dice', 'Log']
    }

    return corpus_set


def test_random_engine_inheritance():

    assert issubclass(RandomEngine, Engine)


def test_random_engine(corpus_settings):

    actual = RandomEngine('foo_corpus', corpus_settings)

    assert isinstance(actual, RandomEngine)


def test_random_collocates(corpus_settings):

    eng = RandomEngine('foo_corpus', corpus_settings)

    actual  = eng.extract_collocates('fooquery', 5)

    print(actual)

    assert isinstance(actual, tuple)


def test_random_concordances(corpus_settings):

    eng = RandomEngine('foo_corpus', corpus_settings)

    actual  = eng.extract_concordances('fooquery', 5)

    assert isinstance(actual, list)
