import pytest
import unittest.mock as mock

from backend.analysis.engines.cwb import evaluate_cqp_query
from backend.analysis.engines.cwb import create_cqp_query_from_items
from backend.analysis.engines.cwb import create_topic_discourseme_query
from backend.analysis.engines.cwb import create_topic_discourseme_query_window
from backend.analysis.engines.cwb import cqp_concordances
from backend.analysis.engines.cwb import format_cqp_concordances
from backend.analysis.engines.cwb import merge_concordances
from backend.analysis.engines.cwb import sort_concordances
from backend.analysis.engines.cwb import CWBEngine
from backend.analysis.engines.cwb import create_ucs_query
from backend.analysis.engines.cwb import evaluate_ucs_query
from backend.analysis.engines.cwb import format_ucs_collocates
from backend.analysis.engines.cwb import ucs_collocates


@pytest.fixture
def corpus_settings():
    return {
        'corpus_name': 'LTWBY2018',
        'cqp_query': 'show +tt_lemma; A=[tt_lemma="Natur"]; cat A;',
        'items1': ['Hessen', 'Bayern'],
        'items2': ['Angela', 'Merkel'],
        'cut_off_concordances': 10,
        'cut_off_collocates': 100,
        'association_settings': {
            'p_att': 'tt_lemma',
            's_att': 'tweet',
            'window_size': 5,
            'association_measures': [
                'am.Dice',
                'am.log.likelihood'
                # all_ams = "am.%"
            ]
        }
    }


@pytest.fixture
def cqp_simple_file():
    with open("tests/analysis/engine/cqp_output_examples/cqp_simple", "rb") as f:
        return f.read()


@pytest.fixture
def conc_simple_file():
    with open("tests/analysis/engine/cqp_output_examples/concordance_simple", "rb") as f:
        return f.read()


@pytest.fixture
def conc_simple_p_att_file():
    with open("tests/analysis/engine/cqp_output_examples/concordance_simple_p_att", "rb") as f:
        return f.read()


@pytest.fixture
def conc_complex_file():
    with open("tests/analysis/engine/cqp_output_examples/concordance_complex", "rb") as f:
        return f.read()


@pytest.fixture
def conc_complex_p_att_file():
    with open("tests/analysis/engine/cqp_output_examples/concordance_complex_p_att", "rb") as f:
        return f.read()


@mock.patch("backend.analysis.engines.cwb.Popen")
def test_evaluate_cqp_query(mock_popen, cqp_simple_file, corpus_settings):

    mock_popen.return_value.communicate.return_value = (cqp_simple_file,)

    actual = evaluate_cqp_query(
        corpus_settings['corpus_name'],
        corpus_settings['cqp_query']
    )

    assert actual == cqp_simple_file.decode()


def test_create_cqp_query_from_items(corpus_settings):

    actual = create_cqp_query_from_items(
        corpus_settings['items1'],
        corpus_settings['association_settings']['p_att']
    )

    expected = '[tt_lemma="Hessen|Bayern"]'

    assert actual == expected


def test_create_topic_discourseme_query(corpus_settings):

    actual = create_topic_discourseme_query(
        corpus_settings['items1'],
        corpus_settings['items2'],
        corpus_settings['association_settings']['p_att'],
        corpus_settings['association_settings']['s_att']
    )

    expected = 'MU (meet [tt_lemma="Angela|Merkel"] [tt_lemma="Hessen|Bayern"] tweet)'

    assert actual == expected


def test_create_topic_discourseme_query_window(corpus_settings):

    actual = create_topic_discourseme_query_window(
        corpus_settings['items1'],
        corpus_settings['items2'],
        corpus_settings['association_settings']['p_att'],
        corpus_settings['association_settings']['s_att'],
        corpus_settings['association_settings']['window_size']
    )

    expected = '(([tt_lemma="Hessen|Bayern"] []{,5} @[tt_lemma="Angela|Merkel"]) | (@[tt_lemma="Angela|Merkel"] []{,5} [tt_lemma="Hessen|Bayern"])) within tweet'

    assert actual == expected


@mock.patch("backend.analysis.engines.cwb.Popen")
def test_cqp_concordances_simple(mock_popen, conc_simple_file, conc_simple_p_att_file, corpus_settings):

    mock_popen.return_value.communicate.side_effect = [
        (conc_simple_file,),
        (conc_simple_p_att_file,)
    ]

    actual = cqp_concordances(
        corpus_settings['corpus_name'],
        corpus_settings['association_settings']['s_att'],
        corpus_settings['association_settings']['p_att'],
        corpus_settings['items2'],
        corpus_settings['association_settings']['window_size']
    )

    assert mock_popen.call_count == 2


@mock.patch("backend.analysis.engines.cwb.Popen")
def test_cqp_concordances_complex(mock_popen, conc_complex_file, conc_complex_p_att_file, corpus_settings):

    mock_popen.return_value.communicate.side_effect = [
        (conc_complex_file,),
        (conc_complex_p_att_file,)
    ]

    actual = cqp_concordances(
        corpus_settings['corpus_name'],
        corpus_settings['association_settings']['s_att'],
        corpus_settings['association_settings']['p_att'],
        corpus_settings['items1'],
        corpus_settings['association_settings']['window_size'],
        corpus_settings['items2'],
    )

    assert mock_popen.call_count == 2
    assert 'CQP version 3.4.15\n' in actual[0]


def test_format_cqp_concordances_simple(conc_simple_file, corpus_settings):

    actual = format_cqp_concordances(
        cqp_return=conc_simple_file.decode(),
        cut_off=corpus_settings['cut_off_concordances'],
        order='first',
        simple=True
    )

    sentences = list(actual.values())

    # Assert the dict has the correct keys and the sentence lists are equal
    assert len(sentences[0]['word']) == len(sentences[0]['role'])


def test_format_cqp_concordances_complex(conc_complex_file, corpus_settings):

    actual = format_cqp_concordances(
        cqp_return=conc_complex_file.decode(),
        cut_off=corpus_settings['cut_off_concordances'],
        order='first',
        simple=True
    )

    sentences = list(actual.values())

    # Assert the dict has the correct keys and the sentence lists are equal
    assert len(sentences[0]['word']) == len(sentences[0]['role'])


@mock.patch("backend.analysis.engines.cwb.Popen")
def test_extract_concordances_simple(mock_popen, corpus_settings):

    engine = CWBEngine(
        corpus_settings['corpus_name'],
        corpus_settings['association_settings']
    )

    actual = engine.extract_concordances(
        corpus_settings['items1'],
        corpus_settings['association_settings']['window_size'],
        cut_off=corpus_settings['cut_off_concordances']
    )

    # TODO Add proper assert
    assert mock_popen.call_count == 2


def test_create_ucs_query(corpus_settings):

    actual = create_ucs_query(corpus_settings['corpus_name'],
                              corpus_settings['items1'],
                              corpus_settings['association_settings']['p_att'],
                              corpus_settings['association_settings']['window_size'],
                              corpus_settings['association_settings']['s_att'],
                              corpus_settings['association_settings']['association_measures'],
                              corpus_settings['items2'])

    assert 'ucs-tool' in actual[0]


def test_evaluate_ucs_query(corpus_settings):

    ucs_cmd, ucs_add = create_ucs_query(corpus_settings['corpus_name'],
                                        corpus_settings['items1'],
                                        corpus_settings['association_settings']['p_att'],
                                        corpus_settings['association_settings']['window_size'],
                                        corpus_settings['association_settings']['s_att'],
                                        corpus_settings['association_settings']['association_measures'])

    actual = evaluate_ucs_query(
        corpus_settings['corpus_name'],
        ucs_cmd,
        ucs_add
    )

    # TODO: Add proper assert
    assert actual == ''


def test_ucs_collocates(corpus_settings):

    collocates = ucs_collocates(
        corpus_settings['corpus_name'],
        corpus_settings['association_settings']['s_att'],
        corpus_settings['association_settings']['p_att'],
        corpus_settings['items1'],
        corpus_settings['association_settings']['window_size'],
        corpus_settings['association_settings']['association_measures'],
        corpus_settings['items2']
    )

    # TODO: Add proper assert
    assert collocates == ''


@mock.patch('backend.analysis.engines.cwb.ucs_collocates')
@mock.patch('backend.analysis.engines.cwb.format_ucs_collocates')
def test_extract_collocates_simple(mock_ucs, mock_collo, corpus_settings):

    mock_ucs.return_value = ('data', 'f1', 'N')

    engine = CWBEngine(
        corpus_settings['corpus_name'],
        corpus_settings['association_settings']
    )

    actual = engine.extract_collocates(
        corpus_settings['items1'],
        corpus_settings['association_settings']['window_size'],
        cut_off=corpus_settings['cut_off_collocates']
    )


    # TODO: Add proper assert
    assert actual == ('data', 'f1', 'N')
