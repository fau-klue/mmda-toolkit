import pytest
import sys
import logging
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


def test_dummy_engine_inheritance():

    assert issubclass(DummyEngine, Engine)


def test_dummy_engine(corpus_settings):

    actual = DummyEngine('foo_corpus', corpus_settings)

    assert isinstance(actual, DummyEngine)


def test_dummy_collocates(corpus_settings):

    eng = DummyEngine('foo_corpus', corpus_settings)

    actual  = eng.extract_collocates('fooquery', 5)

    assert isinstance(actual, tuple)


def test_dummy_concordances(corpus_settings):

    eng = DummyEngine('foo_corpus', corpus_settings)

    actual  = eng.extract_concordances('fooquery', 5)

    assert isinstance(actual, list)
