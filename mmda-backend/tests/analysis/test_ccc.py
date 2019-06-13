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


REGISTRY_PATH = os.getenv(
    'MMDA_CQP_REGISTRY',
    default='/usr/local/cwb-3.4.16/share/cwb/registry/'
)


logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO)
LOGGER = logging.getLogger('mmda-logger')


def timeit(func):
    """This decorator prints the execution time for the decorated function."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = timer()
        result = func(*args, **kwargs)
        end = timer()
        LOGGER.info("{} ran in {}s".format(func.__name__, round(end - start, 2)))
        return result
    return wrapper


t = {
    'items1': ['Angela Merkel', 'Seehofer', 'Merkel'],
    'items2': ['eine', 'die'],
    'items3': ['die'],
    'items_fail': ['dsgf32421', 'fadgoöp'],

    'corpus_settings': {
        'name': 'MMDA_DE_TWEETS',
        # 'name': 'LTWBY2018_TWEETS',
        'registry_path': REGISTRY_PATH
    },

    'corpus_settings_fail': {
        'name': 'MMDA_DE_TWEETS2',
        'registry_path': REGISTRY_PATH
    },

    'analysis_settings': {
        'idx': 1,
        'p_query': 'lemma',
        # 'p_query': 'tt_lemma',
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


class Discourseme():

    def __init__(self, idx, items):
        self.id = idx
        self.items = items


ENGINE = StaticEngine(t['corpus_settings'])


@timeit
def test_slice_discourseme_topic():

    topic_df_node = ENGINE.prepare_df_node(
        t['analysis_settings']['p_query'],
        t['analysis_settings']['s_break'],
        t['items1']
    )

    disc_df_node = ENGINE.prepare_df_node(
        t['analysis_settings']['p_query'],
        t['analysis_settings']['s_break'],
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
def test_combine_df_nodes_single():

    topic_df_node = ENGINE.prepare_df_node(
        t['analysis_settings']['p_query'],
        t['analysis_settings']['s_break'],
        t['items1']
    )

    disc1_df_node = ENGINE.prepare_df_node(
        t['analysis_settings']['p_query'],
        t['analysis_settings']['s_break'],
        t['items2']
    )

    df_nodes_single1 = slice_discourseme_topic(topic_df_node, disc1_df_node, 10)

    disc2_df_node = ENGINE.prepare_df_node(
        t['analysis_settings']['p_query'],
        t['analysis_settings']['s_break'],
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
    assert len(df_nodes) > 1


@pytest.mark.ccc
@timeit
def test_CCC_retrieve_discourseme_dfs():

    ccc = CCC(t['analysis_settings'], ENGINE)
    df_node, df_cooc, f1 = ccc._retrieve_discourseme_dfs(t['items1'])
    assert len(df_node) > 10


@pytest.mark.ccc
@timeit
def test_slice_discoursemes_topic():

    ccc = CCC(t['analysis_settings'], ENGINE)
    topic_df_node, topic_df_cooc, topic_match_pos = ccc._retrieve_discourseme_dfs(
        t['items1']
    )

    disc1_df_node = ENGINE.prepare_df_node(
        t['analysis_settings']['p_query'],
        t['analysis_settings']['s_break'],
        t['items2']
    )

    disc2_df_node = ENGINE.prepare_df_node(
        t['analysis_settings']['p_query'],
        t['analysis_settings']['s_break'],
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

    assert len(match_pos_set) > 100


@pytest.mark.ccc
@timeit
def test_df_dp_nodes_to_cooc():

    ccc = CCC(t['analysis_settings'], ENGINE)
    topic_df_node, topic_df_cooc, topic_match_pos = ccc._retrieve_discourseme_dfs(
        t['items1']
    )

    disc1_df_node = ENGINE.prepare_df_node(
        t['analysis_settings']['p_query'],
        t['analysis_settings']['s_break'],
        t['items2'],
    )

    disc2_df_node = ENGINE.prepare_df_node(
        t['analysis_settings']['p_query'],
        t['analysis_settings']['s_break'],
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
    assert len(df_cooc_glob) > 10


@pytest.mark.ccc
@timeit
def test_CCC_extract_concordances():

    ccc = CCC(t['analysis_settings'], ENGINE)
    topic_discourseme = Discourseme(1, t['items1'])
    concordances = ccc.extract_concordances(
        topic_discourseme
    )
    assert len(concordances) > 1


@pytest.mark.ccc
@timeit
def test_CCC_extract_concordances_dp():

    ccc = CCC(t['analysis_settings'], ENGINE)
    topic_discourseme = Discourseme(1, t['items1'])
    disc2 = Discourseme(2, t['items2'])
    disc3 = Discourseme(3, t['items3'])
    concordances = ccc.extract_concordances(
        topic_discourseme,
        [disc2, disc3]
    )
    assert len(concordances) > 1


@pytest.mark.ccc
@timeit
def test_CCC_extract_collocates():

    ccc = CCC(t['analysis_settings'], ENGINE)
    topic_discourseme = Discourseme(1, t['items1'])
    collocates = ccc.extract_collocates(
        topic_discourseme
    )
    assert len(collocates) == 10


@pytest.mark.ccc
@timeit
def test_CCC_extract_collocates_dp():

    ccc = CCC(t['analysis_settings'], ENGINE)
    topic_discourseme = Discourseme(1, t['items1'])
    disc2 = Discourseme(2, t['items2'])
    disc3 = Discourseme(3, t['items3'])
    collocates = ccc.extract_collocates(
        topic_discourseme,
        [disc2, disc3]
    )
    assert len(collocates) == 10
