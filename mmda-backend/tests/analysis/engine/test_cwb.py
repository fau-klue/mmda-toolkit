#!/usr/bin/python3 -*- coding: utf-8 -*-
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


test_settings = {

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
        ]  # all_ams = "am.%"
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
def test_evaluate_cqp_query(mock_popen, cqp_simple_file):
    mock_popen.return_value.communicate.return_value = (cqp_simple_file,)
    actual = evaluate_cqp_query(
        test_settings['corpus_name'],
        test_settings['cqp_query']
    )
    assert actual == cqp_simple_file.decode()


def test_create_cqp_query_from_items():
    actual = create_cqp_query_from_items(
        test_settings['items1'],
        test_settings['association_settings']['p_att']
    )
    expected = '[tt_lemma="Hessen|Bayern"]'
    assert actual == expected


def test_create_topic_discourseme_query():
    actual = create_topic_discourseme_query(
        test_settings['items1'],
        test_settings['items2'],
        test_settings['association_settings']['p_att'],
        test_settings['association_settings']['s_att']
    )
    expected = 'MU (meet [tt_lemma="Angela|Merkel"] [tt_lemma="Hessen|Bayern"] tweet)'
    assert actual == expected


def test_create_topic_discourseme_query_window():
    actual = create_topic_discourseme_query_window(
        test_settings['items1'],
        test_settings['items2'],
        test_settings['association_settings']['p_att'],
        test_settings['association_settings']['s_att'],
        test_settings['association_settings']['window_size']
    )
    expected = '(([tt_lemma="Hessen|Bayern"] []{,5} @[tt_lemma="Angela|Merkel"]) | (@[tt_lemma="Angela|Merkel"] []{,5} [tt_lemma="Hessen|Bayern"])) within tweet'
    assert actual == expected


@mock.patch("backend.analysis.engines.cwb.Popen")
def test_cqp_concordances_simple(mock_popen, conc_simple_file, conc_simple_p_att_file):
    mock_popen.return_value.communicate.side_effect = [
        (conc_simple_file,),
        (conc_simple_p_att_file,)
    ]
    actual = cqp_concordances(
        test_settings['corpus_name'],
        test_settings['association_settings']['s_att'],
        test_settings['association_settings']['p_att'],
        test_settings['items2'],
        test_settings['association_settings']['window_size']
    )
    assert mock_popen.call_count == 2


def test_cqp_concordances_complex():
    actual = cqp_concordances(
        test_settings['corpus_name'],
        test_settings['association_settings']['s_att'],
        test_settings['association_settings']['p_att'],
        test_settings['items1'],
        test_settings['association_settings']['window_size'],
        test_settings['items2'],
    )
    expected = ("<concordanceInfo>", "<concordanceInfo>")
    assert((actual[0].split("\n")[1], actual[1].split("\n")[1]) == expected)


def test_format_cqp_concordances_simple():
    cqp_return = cqp_concordances(
        test_settings['corpus_name'],
        test_settings['association_settings']['s_att'],
        test_settings['association_settings']['p_att'],
        test_settings['items1'],
        test_settings['association_settings']['window_size']
    )
    actual = format_cqp_concordances(
        cqp_return[0],
        test_settings['cut_off_concordances'],
        'first',
        True
    )
    # print(actual)
    actual = format_cqp_concordances(
        cqp_return[1],
        test_settings['cut_off_concordances'],
        'first',
        True
    )
    # print(actual)


def test_format_cqp_concordances_complex():
    cqp_return = cqp_concordances(
        test_settings['corpus_name'],
        test_settings['association_settings']['s_att'],
        test_settings['association_settings']['p_att'],
        test_settings['items1'],
        test_settings['association_settings']['window_size'],
        test_settings['items2']
    )
    actual = format_cqp_concordances(
        cqp_return[0],
        test_settings['cut_off_concordances'],
        'first',
        False
    )
    # print(actual)
    actual = format_cqp_concordances(
        cqp_return[1],
        1,
        'first',
        False
    )
    # print(actual)


def test_merge_concordances():
    c1, c2 = cqp_concordances(
        test_settings['corpus_name'],
        test_settings['association_settings']['s_att'],
        test_settings['association_settings']['p_att'],
        test_settings['items1'],
        test_settings['association_settings']['window_size'],
        test_settings['items2']
    )
    actual = merge_concordances(
        format_cqp_concordances(c1,
                                test_settings['cut_off_concordances'],
                                'first'),
        format_cqp_concordances(c2,
                                test_settings['cut_off_concordances'],
                                'first'),
    )
    # print(actual)


def test_sort_concordances():
    c1, c2 = cqp_concordances(
        test_settings['corpus_name'],
        test_settings['association_settings']['s_att'],
        test_settings['association_settings']['p_att'],
        test_settings['items1'],
        test_settings['association_settings']['window_size'],
        test_settings['items2']
    )
    concordances = merge_concordances(
        format_cqp_concordances(c1,
                                test_settings['cut_off_concordances'],
                                'first'),
        format_cqp_concordances(c2,
                                test_settings['cut_off_concordances'],
                                'first')
    )
    actual = sort_concordances(concordances)
    # print(actual)


def test_extract_concordances_simple():

    engine = CWBEngine(
        test_settings['corpus_name'],
        test_settings['association_settings']
    )

    actual = engine.extract_concordances(
        test_settings['items1'],
        test_settings['association_settings']['window_size'],
        cut_off=test_settings['cut_off_concordances']
    )

    # print(actual)


def test_extract_concordances_complex():

    engine = CWBEngine(
        test_settings['corpus_name'],
        test_settings['association_settings']
    )

    actual = engine.extract_concordances(
        test_settings['items1'],
        test_settings['association_settings']['window_size'],
        test_settings['items2'],
        cut_off=test_settings['cut_off_concordances']
    )

    # print(actual)


def test_create_ucs_query():

    actual = create_ucs_query(test_settings['corpus_name'],
                              test_settings['items1'],
                              test_settings['association_settings']['p_att'],
                              test_settings['association_settings']['window_size'],
                              test_settings['association_settings']['s_att'],
                              test_settings['association_settings']['association_measures'],
                              test_settings['items2'])

    # print(actual)


def test_evaluate_ucs_query():
    ucs_cmd, ucs_add = create_ucs_query(test_settings['corpus_name'],
                                        test_settings['items1'],
                                        test_settings['association_settings'][
                                            'p_att'
                                        ],
                                        test_settings['association_settings'][
                                            'window_size'
                                        ],
                                        test_settings['association_settings'][
                                            's_att'
                                        ],
                                        test_settings['association_settings'][
                                            'association_measures'
                                        ])

    actual = evaluate_ucs_query(
        test_settings['corpus_name'],
        ucs_cmd,
        ucs_add
    )
    # print(actual)


def test_format_ucs_collocates():
    ucs_cmd, ucs_add = create_ucs_query(test_settings['corpus_name'],
                                        test_settings['items1'],
                                        test_settings['association_settings'][
                                            'p_att'
                                        ],
                                        test_settings['association_settings'][
                                            'window_size'
                                        ],
                                        test_settings['association_settings'][
                                            's_att'
                                        ],
                                        test_settings['association_settings'][
                                            'association_measures'
                                        ])

    ucs_return = evaluate_ucs_query(
        test_settings['corpus_name'],
        ucs_cmd,
        ucs_add
    )

    actual = format_ucs_collocates(
        ucs_return,
        test_settings['association_settings'][
            'association_measures'
        ]
    )
    # print(actual)


def test_ucs_collocates():
    collocates = ucs_collocates(
        test_settings['corpus_name'],
        test_settings['association_settings']['s_att'],
        test_settings['association_settings']['p_att'],
        test_settings['items1'],
        test_settings['association_settings']['window_size'],
        test_settings['association_settings']['association_measures'],
        test_settings['items2']
    )

    # print(collocates)


def test_extract_collocates_simple():

    engine = CWBEngine(
        test_settings['corpus_name'],
        test_settings['association_settings']
    )

    actual = engine.extract_collocates(
        test_settings['items1'],
        test_settings['association_settings']['window_size'],
        cut_off=test_settings['cut_off_collocates'],
        order='am.Dice'
    )

    # print(actual)


def test_extract_collocates_complex():

    engine = CWBEngine(
        test_settings['corpus_name'],
        test_settings['association_settings']
    )

    actual = engine.extract_collocates(
        test_settings['items1'],
        test_settings['association_settings']['window_size'],
        test_settings['items2'],
        cut_off=test_settings['cut_off_collocates'],
        order='am.Dice'
    )

    # print(actual)
