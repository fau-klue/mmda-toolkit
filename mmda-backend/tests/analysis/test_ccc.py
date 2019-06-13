import os
import pytest
from timeit import default_timer as timer
from functools import wraps
import logging

from staticengine import StaticEngine
from backend.analysis.ccc import slice_discourseme_topic
from backend.analysis.ccc import combine_df_nodes_single
from backend.analysis.ccc import slice_discoursemes_topic
from backend.analysis.ccc import _df_dp_nodes_to_cooc
from backend.analysis.ccc import ConcordanceCollocationCalculator as CCC


logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO)
LOGGER = logging.getLogger('mmda-logger')


def timeit(func):
    """This decorator prints the execution time for the decorated function."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = timer()
        result = func(*args, **kwargs)
        end = timer()
        # LOGGER.info("{} ran in {}s".format(func.__name__, round(end - start, 2)))
        return result
    return wrapper


t = {
    'items1': ['Angela Merkel', 'Seehofer', 'Merkel'],
    'items2': ['eine', 'die'],
    'items3': ['die'],
    'items_fail': ['dsgf32421', 'fadgoöp'],

    'corpus_settings': {
        'name': 'MMDA_DE_TWEETS',
        'registry_path': '/usr/local/cwb-3.4.16/share/cwb/registry/'
    },

    'corpus_settings_fail': {
        'name': 'MMDA_DE_TWEETS2',
        'registry_path': '/usr/local/cwb-3.4.16/share/cwb/registry/'
    },

    'analysis_settings': {
        'idx': 1,
        'p_query': 'lemma',
        's_break': 'tweet',
        'max_window_size': 10
    },

    'concordance_settings': {
        'order': 'random',
        'cut_off': 10
    },

    'collocate_settings': {
        'order': 'random',
        'cut_off': 10
    }
}

class Analysis():
    def __init__(self, p_query='lemma', s_break='tweet', window_size=10):
        self.idx = 1
        self.p_query = p_query
        self.s_break = s_break
        self.window_size = window_size

@pytest.fixture
def analysis():
    return Analysis()

class Discourseme():

    def __init__(self, idx, items):
        self.id = idx
        self.items = items


ENGINE = StaticEngine(t['corpus_settings'])


@timeit
def test_slice_discourseme_topic(analysis):

    topic_df_node = ENGINE.prepare_df_node(
        analysis.p_query,
        analysis.s_break,
        t['items1']
    )

    disc_df_node = ENGINE.prepare_df_node(
        analysis.p_query,
        analysis.s_break,
        t['items2']
    )

    df_nodes_single = slice_discourseme_topic(
        topic_df_node,
        disc_df_node,
        t['analysis_settings']['max_window_size']
    )
    assert len(df_nodes_single) > 1


@pytest.mark.ccc
@timeit
def test_combine_df_nodes_single(analysis):

    topic_df_node = ENGINE.prepare_df_node(
        analysis.p_query,
        analysis.s_break,
        t['items1']
    )

    disc1_df_node = ENGINE.prepare_df_node(
        analysis.p_query,
        analysis.s_break,
        t['items2']
    )

    df_nodes_single1 = slice_discourseme_topic(topic_df_node, disc1_df_node, 10)

    disc2_df_node = ENGINE.prepare_df_node(
        analysis.p_query,
        analysis.s_break,
        t['items3']
    )

    df_nodes_single2 = slice_discourseme_topic(
        topic_df_node, disc2_df_node, 10
    )
    df_nodes = combine_df_nodes_single(
        {
            '1': df_nodes_single1,
            '2': df_nodes_single2
        }
    )

    assert df_nodes.shape == (52, 5)
    # TODO: Extend
    assert 'topic_match' in df_nodes.columns
    assert len(df_nodes) > 1


@pytest.mark.ccc
@timeit
def test_CCC_retrieve_discourseme_dfs(analysis):

    ccc = CCC(analysis, ENGINE)
    df_node, df_cooc, match_pos = ccc._retrieve_discourseme_dfs(t['items1'])

    assert 'matchend' in df_node.columns
    assert df_node.shape == (34, 3)

    assert 'offset' in df_cooc.columns
    assert df_cooc.shape == (566, 3)

    assert isinstance(match_pos, set)
    assert len(match_pos) == 34

@pytest.mark.ccc
@timeit
def test_slice_discoursemes_topic(analysis):

    ccc = CCC(analysis, ENGINE)
    topic_df_node, topic_df_cooc, topic_match_pos = ccc._retrieve_discourseme_dfs(
        t['items1']
    )

    disc1_df_node = ENGINE.prepare_df_node(
        analysis.p_query,
        analysis.s_break,
        t['items2']
    )

    disc2_df_node = ENGINE.prepare_df_node(
        analysis.p_query,
        analysis.s_break,
        t['items3']
    )

    df_dp_nodes, match_pos_set = slice_discoursemes_topic(
        topic_df_node,
        topic_match_pos,
        {
            '1': disc1_df_node,
            '2': disc2_df_node
        },
        t['analysis_settings']['max_window_size']
    )


    assert isinstance(match_pos_set, set)
    assert len(match_pos_set) == 1260


@pytest.mark.ccc
@timeit
def test_df_dp_nodes_to_cooc(analysis):

    ccc = CCC(analysis, ENGINE)
    topic_df_node, topic_df_cooc, topic_match_pos = ccc._retrieve_discourseme_dfs(
        t['items1']
    )

    disc1_df_node = ENGINE.prepare_df_node(
        analysis.p_query,
        analysis.s_break,
        t['items2'],
    )

    disc2_df_node = ENGINE.prepare_df_node(
        analysis.p_query,
        analysis.s_break,
        t['items3'],
    )

    df_dp_nodes, match_pos_set = slice_discoursemes_topic(
        topic_df_node,
        topic_match_pos,
        {
            '1': disc1_df_node,
            '2': disc2_df_node
        },
        t['analysis_settings']['max_window_size']
    )

    df_cooc_glob = _df_dp_nodes_to_cooc(topic_df_cooc, df_dp_nodes)

    assert df_cooc_glob.shape == (248, 3)
    assert 'match' in df_cooc_glob.columns


@pytest.mark.ccc
@timeit
def test_CCC_extract_concordances(analysis):

    ccc = CCC(analysis, ENGINE)
    topic_discourseme = Discourseme(1, t['items1'])

    concordances = ccc.extract_concordances(
        topic_discourseme
    )

    assert isinstance(concordances, dict)
    assert len(concordances.keys()) == 10

    for concordance in concordances.values():
        assert 'word' in concordance.columns
        assert 'role' in concordance.columns
        assert 'offset' in concordance.columns
        assert len(concordance) > 1


@pytest.mark.ccc
@timeit
def test_CCC_extract_concordances_dp(analysis):

    ccc = CCC(analysis, ENGINE)
    topic_discourseme = Discourseme(1, t['items1'])
    disc2 = Discourseme(2, t['items2'])
    disc3 = Discourseme(3, t['items3'])

    concordances = ccc.extract_concordances(
        topic_discourseme,
        [disc2, disc3]
    )

    assert isinstance(concordances, dict)
    assert len(concordances.keys()) == 10

    for concordance in concordances.values():
        assert 'word' in concordance.columns
        assert 'role' in concordance.columns
        assert 'offset' in concordance.columns
        assert len(concordance) > 1


@pytest.mark.ccc
@timeit
def test_CCC_extract_collocates(analysis):

    ccc = CCC(analysis, ENGINE)
    topic_discourseme = Discourseme(1, t['items1'])

    collocates = ccc.extract_collocates(
        topic_discourseme
    )


    assert isinstance(collocates, dict)
    assert len(collocates.keys()) == 10

    for collocate in collocates.values():
        assert 'O11' in collocate.columns
        assert 'f2' in collocate.columns
        assert 'N' in collocate.columns
        assert len(collocate) > 1


@pytest.mark.ccc
@timeit
def test_CCC_extract_collocates_dp(analysis):

    ccc = CCC(analysis, ENGINE)
    topic_discourseme = Discourseme(1, t['items1'])
    disc2 = Discourseme(2, t['items2'])
    disc3 = Discourseme(3, t['items3'])

    collocates = ccc.extract_collocates(
        topic_discourseme,
        [disc2, disc3]
    )

    assert isinstance(collocates, dict)
    assert len(collocates.keys()) == 10

    for collocate in collocates.values():
        assert 'O11' in collocate.columns
        assert 'f2' in collocate.columns
        assert 'N' in collocate.columns
        assert len(collocate) > 1
