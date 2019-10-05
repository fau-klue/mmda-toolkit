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


@pytest.mark.engine
def test_abstract_engine(corpus_settings):

    actual = Engine(corpus_settings)
    assert isinstance(actual, ABC)


@pytest.mark.engine
def test_abstract_engine_N(corpus_settings):

    actual = Engine(corpus_settings)
    assert actual.N == 0


@pytest.mark.engine
def test_abstract_engine_lexicalize(corpus_settings):

    actual = Engine(corpus_settings)
    with pytest.raises(NotImplementedError):
        actual.lexicalize_positions([1], 'word')


@pytest.mark.engine
def test_abstract_engine_marginal(corpus_settings):

    actual = Engine(corpus_settings)
    with pytest.raises(NotImplementedError):
        actual.get_marginals([1], 'word')


@pytest.mark.engine
def test_abstract_engine_df_node(corpus_settings):

    actual = Engine(corpus_settings)
    with pytest.raises(NotImplementedError):
        actual.prepare_df_node('query', 's', [1])
