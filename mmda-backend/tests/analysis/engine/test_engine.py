import pytest
import sys
import logging
import unittest.mock as mock
from abc import ABC

from backend.analysis.engines import Engine


@pytest.fixture
def corpus_settings():

    corpus_set = {
        'sentence_boundary': 's',
        'association_measures': ['Dice', 'Log']
    }

    return corpus_set


def test_abstract_engine(corpus_settings):

    actual = Engine('foo_corpus', corpus_settings)

    assert isinstance(actual, ABC)
    assert actual.corpus_name == 'foo_corpus'
    assert actual.corpus_settings == corpus_settings

def test_abstract_extract_collocates(corpus_settings):

    eng = Engine('foo_corpus', corpus_settings)

    with pytest.raises(NotImplementedError):
         eng.extract_collocates('query', 5, ['testnode'])


def test_abstract_extract_concordances(corpus_settings):

    eng = Engine('foo_corpus', corpus_settings)

    with pytest.raises(NotImplementedError):
         eng.extract_concordances('query', 5, ['testnode'])
