import pytest
import os
from backend.analysis.engines.cwb import _formulate_discourseme_query
from backend.analysis.engines.cwb import _execute_cqp_query
from backend.analysis.engines.cwb import _dump_corpus_positions
from backend.analysis.engines.cwb import _dump_to_df_node
from backend.analysis.engines.cwb import CWBEngine
from backend.analysis.engines import Engine


REGISTRY_PATH = os.getenv(
    'MMDA_CQP_REGISTRY',
    default='/usr/local/cwb-3.4.16/share/cwb/registry/'
)


t = {
    'items1': ['Angela', 'Merkel', 'Atomkraft'],
    'items2': ['Streit', 'Verhandlung'],
    'items_fail': ['dsgf32421', 'fadgoöp'],

    'corpus_settings': {
        # 'name': 'MMDA_DE_TWEETS',
        'name': 'LTWBY2018_TWEETS',
        'registry_path': REGISTRY_PATH
    },

    'corpus_settings_fail': {
        'name': 'MMDA_DE_TWEETS2',
        'registry_path': REGISTRY_PATH
    },

    'analysis_settings': {
        # 'p_query': 'lemma',
        'p_query': 'tt_lemma',
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


@pytest.mark.cwb
def test_cwb_engine_inheritance():
    assert issubclass(CWBEngine, Engine)


@pytest.mark.cwb
@pytest.mark.xfail
def test_formulate_discourseme_query():

    cqp_exec = _formulate_discourseme_query(
        t['corpus_settings']['name'],
        t['analysis_settings']['p_query'],
        t['analysis_settings']['s_break'],
        t['items1']
    )

    assert type(cqp_exec) == str


@pytest.mark.cwb
@pytest.mark.xfail
def test_execute_cqp_query():

    query = _formulate_discourseme_query(
        t['corpus_settings']['name'],
        t['analysis_settings']['p_query'],
        t['analysis_settings']['s_break'],
        t['items1']
    )

    cqp_return = _execute_cqp_query(t['corpus_settings']['registry_path'],
                                    query)

    assert type(cqp_return) == str


@pytest.mark.cwb
@pytest.mark.xfail
def test_dump_corpus_positions():

    actual = _dump_corpus_positions(
        t['corpus_settings']['registry_path'],
        t['corpus_settings']['name'],
        t['analysis_settings']['p_query'],
        t['analysis_settings']['s_break'],
        t['items1']
    )
    assert len(actual) > 1 and len(actual[0].split("\t")) == 4


@pytest.mark.cwb
@pytest.mark.xfail
def test_dump_to_df_node():

    dump = _dump_corpus_positions(
        t['corpus_settings']['registry_path'],
        t['corpus_settings']['name'],
        t['analysis_settings']['p_query'],
        t['analysis_settings']['s_break'],
        t['items1']
    )
    actual = _dump_to_df_node(dump)
    assert len(actual) > 1


@pytest.mark.cwb
@pytest.mark.xfail
def test_CWB_df_node():
    engine = CWBEngine(t['corpus_settings'])
    df_node = engine.prepare_df_node(
        t['analysis_settings']['p_query'],
        t['analysis_settings']['s_break'],
        t['items1']
    )
    assert len(df_node) > 1


@pytest.mark.cwb
@pytest.mark.xfail
def test_CWB_lexicalize_positions():

    engine = CWBEngine(t['corpus_settings'])
    tokens = engine.lexicalize_positions(list(range(510, 512)))
    lemmas = engine.lexicalize_positions(list(range(510, 512)),
                                         t['analysis_settings']['p_query'])
    assert tokens == ['wählt', 'die'] and lemmas == ['wählen', 'die']
