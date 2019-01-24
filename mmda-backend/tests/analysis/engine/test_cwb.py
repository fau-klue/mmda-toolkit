import pytest
import sys
import logging
from pandas.util.testing import assert_frame_equal
from subprocess import TimeoutExpired
import pandas
import unittest.mock as mock
from abc import ABC

from backend.analysis.engines.cwb import *

TEST_REGISTRY_PATH = '/usr/local/cwb-3.4.13/share/cwb/registry'


@pytest.fixture
def corpus_settings():

    corpus_set = {
        'sentence_boundary': 's',
        'association_measures': ['Dice', 'Log']
    }

    return corpus_set


def test_cwb_engine_inheritance():

    assert issubclass(CWBEngine, Engine)


def test_cwb_engine_instance(corpus_settings):

    actual = CWBEngine('foo_corpus', corpus_settings)

    assert isinstance(actual, CWBEngine)


def test_cwb_create_cqp_query_simple():

    actual = create_cqp_query('fooquery')
    expected = '[word = "fooquery" %c]'

    assert actual == expected


def test_cwb_create_cqp_query_complex():

    actual = create_cqp_query('[complexfooquery]')
    expected = '[complexfooquery]'

    assert actual == expected


def test_cwb_create_discourse_query():

    actual = create_discourse_query('fooquery', 's', ['collo1', 'collo2'])
    expected = 'MU (meet [lemma = "collo1" | lemma = "collo2"] [word = "fooquery" %c] s)'

    assert actual == expected


def test_cwb_start_cqp_command():

    actual = start_cqp_command('foocorpus')
    expected = [
        'cqp',
        '-c',
        '-r',
        TEST_REGISTRY_PATH,
        '-D',
        'FOOCORPUS'
    ]

    assert actual == expected


def test_cwb_make_ucs_command_nocoll():

    actual = make_ucs_command('foocorpus', 'fooquery', '5', 's')
    expected = ['ucs-tool', 'surface-from-cwb-query', '-q', '-S', 's', '-w',
                '5',
                '-nh',
                '-r',
                TEST_REGISTRY_PATH,
                '-ca',
                'lemma',
                '-M', '/tmp/mmda_marginals_foocorpus_lemma.gz',
                '-f',
                '1',
                'foocorpus',
                '-',
                '[word = "fooquery" %c]',
                'NODE']

    assert actual == expected


def test_cwb_make_ucs_command_coll():

    actual = make_ucs_command('foocorpus', 'fooquery', '5', 's', ['collo1'])
    expected = ['ucs-tool', 'surface-from-cwb-query', '-q', '-S', 's',
                '-w',
                '5', '-nh',
                '-r',
                TEST_REGISTRY_PATH,
                '-ca', 'lemma',
                '-M', '/tmp/mmda_marginals_foocorpus_lemma.gz',
                '-f', '1',
                'foocorpus',
                '-',
                'MU (meet [lemma = "collo1"] [word = "fooquery" %c] s)', 'NODE']

    assert actual == expected


def test_cwb_make_ucs_command_typeerror():

    with pytest.raises(TypeError):
        fail = make_ucs_command('foocorpus', 'fooquery', '5', 's', 'collo1')


def test_cwb_format_cqp_concordances():

    from_cqp = ['   323122:  Deutschland/Deutschland will/wollen aussteigen/aussteigen aus/aus der/die Nuklearenergie/Nuklearenergie ,/, Frankreich/Frankreich und/und Großbritannien/Großbritannien weiter/weiter Geld/Geld damit/damit verdienen/verdienen ./.']

    expected = [{'s_pos': 323122, 'tokens': ['Deutschland', 'will', 'aussteigen', 'aus', 'der', 'Nuklearenergie', ',', 'Frankreich', 'und', 'Großbritannien', 'weiter', 'Geld', 'damit', 'verdienen', '.'], 'emphas': ['coll', None, None, None, None, 'node', None, None, None, None, None, None, None, None, None], 'lemmas': ['Deutschland', 'wollen', 'aussteigen', 'aus', 'die', 'Nuklearenergie', ',', 'Frankreich', 'und', 'Großbritannien', 'weiter', 'Geld', 'damit', 'verdienen', '.']}]

    actual = format_cqp_concordances(from_cqp, 'Nuklearenergie', 'Deutschland')

    assert actual == expected


def test_cwb_format_cqp_concordances_nocollocate():

    from_cqp = ['   323122:  Deutschland/Deutschland will/wollen aussteigen/aussteigen aus/aus der/die Nuklearenergie/Nuklearenergie ,/, Frankreich/Frankreich und/und Großbritannien/Großbritannien weiter/weiter Geld/Geld damit/damit verdienen/verdienen ./.']

    expected = [{'s_pos': 323122, 'tokens': ['Deutschland', 'will', 'aussteigen', 'aus', 'der', 'Nuklearenergie', ',', 'Frankreich', 'und', 'Großbritannien', 'weiter', 'Geld', 'damit', 'verdienen', '.'], 'lemmas': ['Deutschland', 'wollen', 'aussteigen', 'aus', 'die', 'Nuklearenergie', ',', 'Frankreich', 'und', 'Großbritannien', 'weiter', 'Geld', 'damit', 'verdienen', '.'], 'emphas': [None, None, None, None, None, 'node', None, None, None, None, None, None, None, None, None]}]

    actual = format_cqp_concordances(from_cqp, 'Nuklearenergie')

    assert actual == expected


def test_cwb_format_cqp_concordances_error():

    from_cqp = ['   123:  Deutschland ./.']

    expected = [{'s_pos': 123, 'emphas': [None, None], 'lemmas': ['ERR', '.'], 'tokens': ['ERR', '.']}]

    actual = format_cqp_concordances(from_cqp, 'Nuklearenergie', 'Deutschland')

    assert actual == expected


def test_cwb_format_cqp_concordances_error2():

    from_cqp = ['   123:  Deutschland ///']

    expected = [{'s_pos': 123, 'emphas': [None, None], 'lemmas': ['ERR', '/'], 'tokens': ['ERR', '/']}]

    actual = format_cqp_concordances(from_cqp, 'Nuklearenergie', 'Deutschland')

    assert actual == expected


def test_cwb_format_cqp_concordances_multi():

    from_cqp = ['   323122:  Deutschland/Deutschland will/wollen aussteigen/aussteigen aus/aus der/die Nuklearenergie/Nuklearenergie ,/, Frankreich/Frankreich und/und Großbritannien/Großbritannien weiter/weiter Geld/Geld damit/damit verdienen/verdienen ./.',
        '   1337:  Deutschland/Deutschland will/wollen aussteigen/aussteigen aus/aus der/die Nuklearenergie/Nuklearenergie ,/, Frankreich/Frankreich und/und Großbritannien/Großbritannien weiter/weiter Geld/Geld damit/damit verdienen/verdienen ./.']

    expected = [{'s_pos': 323122, 'tokens': ['Deutschland', 'will', 'aussteigen', 'aus', 'der', 'Nuklearenergie', ',', 'Frankreich', 'und', 'Großbritannien', 'weiter', 'Geld', 'damit', 'verdienen', '.'], 'emphas': ['coll', None, None, None, None, 'node', None, None, None, None, None, None, None, None, None], 'lemmas': ['Deutschland', 'wollen', 'aussteigen', 'aus', 'die', 'Nuklearenergie', ',', 'Frankreich', 'und', 'Großbritannien', 'weiter', 'Geld', 'damit', 'verdienen', '.']},
                {'s_pos': 1337, 'tokens': ['Deutschland', 'will', 'aussteigen', 'aus', 'der', 'Nuklearenergie', ',', 'Frankreich', 'und', 'Großbritannien', 'weiter', 'Geld', 'damit', 'verdienen', '.'], 'emphas': ['coll', None, None, None, None, 'node', None, None, None, None, None, None, None, None, None], 'lemmas': ['Deutschland', 'wollen', 'aussteigen', 'aus', 'die', 'Nuklearenergie', ',', 'Frankreich', 'und', 'Großbritannien', 'weiter', 'Geld', 'damit', 'verdienen', '.']},
    ]

    actual = format_cqp_concordances(from_cqp, 'Nuklearenergie', 'Deutschland')

    assert actual == expected


def test_cwb_merge_concordances():

    input_a = {'s_pos': 323122, 'tokens': ['Deutschland', 'will', 'aussteigen', 'aus', 'der', 'Nuklearenergie', ',', 'Frankreich', 'und', 'Großbritannien', 'weiter', 'Geld', 'damit', 'verdienen', '.'], 'emphas': ['coll', None, None, None, None, 'node', None, None, None, None, None, None, None, None, None], 'lemmas': ['Deutschland', 'wollen', 'aussteigen', 'aus', 'die', 'Nuklearenergie', ',', 'Frankreich', 'und', 'Großbritannien', 'weiter', 'Geld', 'damit', 'verdienen', '.']}

    input_b = {'s_pos': 323122, 'tokens': ['Deutschland', 'will', 'aussteigen', 'aus', 'der', 'Nuklearenergie', ',', 'Frankreich', 'und', 'Großbritannien', 'weiter', 'Geld', 'damit', 'verdienen', '.'], 'emphas': ['coll', None, None, None, None, 'node', None, None, None, None, None, None, None, None, None], 'lemmas': ['Deutschland', 'wollen', 'aussteigen', 'aus', 'die', 'Nuklearenergie', ',', 'Frankreich', 'und', 'Großbritannien', 'weiter', 'Geld', 'damit', 'verdienen', '.']}

    expected = {'s_pos': 323122, 'tokens': ['Deutschland', 'will', 'aussteigen', 'aus', 'der', 'Nuklearenergie', ',', 'Frankreich', 'und', 'Großbritannien', 'weiter', 'Geld', 'damit', 'verdienen', '.'], 'emphas': ['coll', None, None, None, None, 'node', None, None, None, None, None, None, None, None, None], 'lemmas': ['Deutschland', 'wollen', 'aussteigen', 'aus', 'die', 'Nuklearenergie', ',', 'Frankreich', 'und', 'Großbritannien', 'weiter', 'Geld', 'damit', 'verdienen', '.']}

    actual = merge_concordances(input_a, input_b)

    assert actual == expected


def test_cwb_merge_concordances_none():

    input_a = {'s_pos': 323122, 'tokens': ['Deutschland', 'ist', 'groß', '.'], 'emphas': ['node', None, 'coll', None], 'lemmas': ['Deutschland']}
    input_b = {'s_pos': 323122, 'tokens': ['Deutschland', 'ist', 'groß', '.'], 'emphas': ['node', 'coll', None, None], 'lemmas': ['Deutschland']}

    expected = {'s_pos': 323122, 'tokens': ['Deutschland', 'ist', 'groß', '.'], 'emphas': ['node', 'coll', 'coll', None], 'lemmas': ['Deutschland']}

    actual = merge_concordances(input_a, input_b)

    assert actual == expected


def test_cwb_merge_concordances_valueerror():

    input_a = {'s_pos': 123}

    input_b = {'s_pos': 312}

    with pytest.raises(ValueError):
        actual = merge_concordances(input_a, input_b)


@mock.patch('backend.analysis.engines.cwb.Popen')
def test_cwb_sentence_positions_of_cqp_query(mock_popen):

    from_cqp = (b'CQP version 3.4.14\n    85144: olitischen Stillstand <p> <Donald Trump konnte nicht an sich halten .> Als sich ein Sieg von Ba\n', b'')

    mock_popen.return_value.communicate.return_value = from_cqp

    actual = sentence_positions_of_cqp_query('foocorpus', 'fooquery')
    expected = [85144]

    assert actual == expected
    assert mock_popen.call_count == 1


@mock.patch('backend.analysis.engines.cwb.Popen')
def test_cwb_sentence_positions_of_cqp_query_oserror(mock_popen):

    mock_popen.return_value.communicate.side_effect = Exception('foo')

    with pytest.raises(OSError):
        fail = sentence_positions_of_cqp_query('foocorpus', 'fooquery')


@mock.patch('backend.analysis.engines.cwb.Popen')
def test_cwb_sentence_positions_of_cqp_query_error(mock_popen):

    from_cqp = (b'CQP version 3.4.14\n    85144: olitischen Stillstand <p> <Donald Trump konnte nicht an sich halten .> Als sich ein Sieg von Ba\n', b'')

    mock_popen.return_value.communicate.return_value = from_cqp

    actual = sentence_positions_of_cqp_query('foocorpus', 'fooquery')
    expected = [85144]

    assert actual == expected
    assert mock_popen.call_count == 1


@mock.patch('backend.analysis.engines.cwb.Popen')
def test_cwb_cqp_concordances_of_topic(mock_popen):

    from_cqp = (b'CQP version 3.4.14\n    85145:  Donald/Donald Trump/Trump konnte/k\xc3\xb6nnen nicht/nicht an/an sich/sich halten/halten ./.\n', b'')

    mock_popen.return_value.communicate.return_value = from_cqp

    expected = [{'emphas': [None, 'node', None, None, None, None, None, None], 'tokens': ['Donald', 'Trump', 'konnte', 'nicht', 'an', 'sich', 'halten', '.'], 'lemmas': ['Donald', 'Trump', 'können', 'nicht', 'an', 'sich', 'halten', '.'], 's_pos': 85145}]

    actual = cqp_concordances_of_topic('foocorpus', 'Trump')

    assert actual == expected
    assert mock_popen.call_count == 1


@mock.patch('backend.analysis.engines.cwb.Popen')
def test_cwb_cqp_concordances_of_topic_oserror(mock_popen):

    mock_popen.return_value.communicate.side_effect = Exception('foo')

    with pytest.raises(OSError):
        fail = cqp_concordances_of_topic('foocorpus', 'Trump')


@mock.patch('backend.analysis.engines.cwb.Popen')
def test_cwb_cqp_concordances_of_collocate_oserror(mock_popen):

    mock_popen.return_value.communicate.side_effect = Exception('foo')

    with pytest.raises(OSError):
        fail = cqp_concordances_of_collocate('foocorpus', 'Atomkraft', 'Merkel', 5, 's')


@mock.patch('backend.analysis.engines.cwb.Popen')
def test_cwb_cqp_concordances_of_collocate(mock_popen):

    from_cqp = (b'CQP version 3.4.14\n  2233795:  Mein/mein achtj\xc3\xa4hriger/achtj\xc3\xa4hrig Sohn/Sohn Felix/Felix malte/malen kurz/kurz nach/nach den/die ersten/erst Nachrichten/Nachricht aus/aus Fukushima/Fukushima Bilder/Bild des/die Protestes/Protest gegen/gegen Atomkraft/Atomkraft und/und schrieb/schreiben an/an Bundeskanzlerin/Bundeskanzlerin Merkel/Merkel ./.\n', b'')

    mock_popen.return_value.communicate.return_value = from_cqp

    expected = [{'tokens': ['Mein', 'achtjähriger', 'Sohn', 'Felix', 'malte', 'kurz', 'nach', 'den', 'ersten', 'Nachrichten', 'aus', 'Fukushima', 'Bilder', 'des', 'Protestes', 'gegen', 'Atomkraft', 'und', 'schrieb', 'an', 'Bundeskanzlerin', 'Merkel', '.'], 's_pos': 2233795, 'emphas': [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 'node', None, None, None, None, 'coll', None], 'lemmas': ['mein', 'achtjährig', 'Sohn', 'Felix', 'malen', 'kurz', 'nach', 'die', 'erst', 'Nachricht', 'aus', 'Fukushima', 'Bild', 'die', 'Protest', 'gegen', 'Atomkraft', 'und', 'schreiben', 'an', 'Bundeskanzlerin', 'Merkel', '.']}]

    actual = cqp_concordances_of_collocate('foocorpus', 'Atomkraft', 'Merkel', 5, 's')

    assert actual == expected
    assert mock_popen.call_count == 1


@mock.patch('backend.analysis.engines.cwb.Popen')
def test_cwb_cqp_concordances_of_discourse_mergeit(mock_popen):

    from_cqp = (b'CQP version 3.4.14\n  123: Atomkraft/Atomkraft und/und schrieb/schreiben an/an Bundeskanzlerin/Bundeskanzlerin Merkel/Merkel ./.\n 123: Atomkraft/Atomkraft und/und schrieb/schreiben an/an Bundeskanzlerin/Bundeskanzlerin Merkel/Merkel ./.\n', b'')

    mock_popen.return_value.communicate.return_value = from_cqp

    expected = [{'s_pos': 123, 'tokens': ['Atomkraft', 'und', 'schrieb', 'an', 'Bundeskanzlerin', 'Merkel', '.'], 'lemmas': ['Atomkraft', 'und', 'schreiben', 'an', 'Bundeskanzlerin', 'Merkel', '.'], 'emphas': ['node', None, None, None, None, 'coll', None]}]

    actual = cqp_concordances_of_discourse('foocorpus', 'Atomkraft', 5, 's', ['Merkel'])

    assert actual == expected


@mock.patch('backend.analysis.engines.cwb.Popen')
def test_cwb_cqp_concordances_of_discourse(mock_popen):

    from_cqp = (b'CQP version 3.4.14\n  2233795:  Mein/mein achtj\xc3\xa4hriger/achtj\xc3\xa4hrig Sohn/Sohn Felix/Felix malte/malen kurz/kurz nach/nach den/die ersten/erst Nachrichten/Nachricht aus/aus Fukushima/Fukushima Bilder/Bild des/die Protestes/Protest gegen/gegen Atomkraft/Atomkraft und/und schrieb/schreiben an/an Bundeskanzlerin/Bundeskanzlerin Merkel/Merkel ./.\n', b'')

    mock_popen.return_value.communicate.return_value = from_cqp

    expected = [{'emphas': [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 'node', None, None, None, None, 'coll', None], 'lemmas': ['mein', 'achtjährig', 'Sohn', 'Felix', 'malen', 'kurz', 'nach', 'die', 'erst', 'Nachricht', 'aus', 'Fukushima', 'Bild', 'die', 'Protest', 'gegen', 'Atomkraft', 'und', 'schreiben', 'an', 'Bundeskanzlerin', 'Merkel', '.'], 'tokens': ['Mein', 'achtjähriger', 'Sohn', 'Felix', 'malte', 'kurz', 'nach', 'den', 'ersten', 'Nachrichten', 'aus', 'Fukushima', 'Bilder', 'des', 'Protestes', 'gegen', 'Atomkraft', 'und', 'schrieb', 'an', 'Bundeskanzlerin', 'Merkel', '.'], 's_pos': 2233795}]

    actual = cqp_concordances_of_discourse('foocorpus', 'Atomkraft', 5, 's', ['Merkel'])

    assert actual == expected
    assert mock_popen.call_count == 1


@mock.patch('backend.analysis.engines.cwb.shuffle')
def test_cwb_sort_concordances(mock_shuffle):

    actual = sort_concordances([1, 2, 3], 'random')

    mock_shuffle.assert_called_with([1, 2, 3])


def test_cwb_sort_concordances_error():

    with pytest.raises(NotImplementedError):
        fail = sort_concordances([1,2,3], 'fooorder')


def test_cwb_format_ucs_data():

    expected_df = pandas.DataFrame(data=[['17013', '1', '4', '1'],['1404', '1', '9', '2'],['16711','1', '4', '3']],
                                    columns=['f2', 'O11', 'am.simple.ll', 'am.log.likelihood'],
                                    index=['nicht', 'halten', 'sich'])
    expected_df.index.name = 'item'

    ams = ['am.simple.ll', 'am.log.likelihood']

    data = pandas.DataFrame(data=[
        ['1', 'NODE', 'nicht', '1', '7', '17013', '2693270', '4', '1'],
        ['2', 'NODE', 'halten', '1', '7', '1404', '2693270', '9', '2'],
        ['3', 'NODE', 'sich', '1', '7', '16711', '2693270', '4', '3']],
        columns=['id', 'l1', 'l2', 'f', 'f1', 'f2', 'N', 'am.simple.ll', 'am.log.likelihood'])

    actual_df, actual_f1, actual_N = format_ucs_data(data, ams)

    assert actual_f1 == 7
    assert actual_N == 2693270
    assert_frame_equal(actual_df, expected_df)


@mock.patch('backend.analysis.engines.cwb.Popen')
@mock.patch('backend.analysis.engines.cwb.run')
def test_cwb_ucs_tool_collocates(mock_run, mock_popen):

    from_ucs = b'id\tl1\tl2\tf\tf1\tf2\tN\tam.simple.ll\n1\tNODE\tnicht\t1\t7\t17013\t2693270\t4.32568287237778\n2\tNODE\thalten\t1\t7\t1404\t2693270\t9.23384997753814\n3\tNODE\tsich\t1\t7\t16711\t2693270\t4.35993417844056\n4\tNODE\tk\xc3\xb6nnen\t1\t7\t8945\t2693270\t5.56951034391385\n5\tNODE\tDonald\t1\t7\t16\t2693270\t18.1756186810848\n6\tNODE\t.\t1\t7\t117967\t2693270\t0.977601770158918\n7\tNODE\tan\t1\t7\t16604\t2693270\t4.37222508730367\n'

    mock_run.stdout.return_value = from_ucs

    process_mock = mock.Mock()
    attrs = {'stdout': from_ucs}
    process_mock.configure_mock(**attrs)
    mock_run.return_value = process_mock

    actual = ucs_tool_collocates('sz_small', 'Trump', '7', ['am.simple.ll'], 's')

    expected = pandas.DataFrame(data=[
        ['1', 'NODE', 'nicht', '1', '7', '17013', '2693270', '4.32568287237778'],
        ['2', 'NODE', 'halten', '1', '7', '1404', '2693270', '9.23384997753814'],
        ['3', 'NODE', 'sich', '1', '7', '16711', '2693270', '4.35993417844056'],
        ['4', 'NODE', 'können', '1', '7', '8945', '2693270', '5.56951034391385'],
        ['5', 'NODE', 'Donald', '1', '7', '16', '2693270', '18.1756186810848'],
        ['6', 'NODE', '.', '1', '7', '117967', '2693270', '0.977601770158918'],
        ['7', 'NODE', 'an', '1', '7', '16604', '2693270', '4.37222508730367']],
        columns=['id', 'l1', 'l2', 'f', 'f1', 'f2', 'N', 'am.simple.ll'])

    assert_frame_equal(actual, expected)


@mock.patch('backend.analysis.engines.cwb.Popen')
@mock.patch('backend.analysis.engines.cwb.run')
def test_cwb_ucs_tool_collocates_timeout(mock_run, mock_popen):

    mock_run.side_effect = TimeoutExpired('foo', 1)

    fail = ucs_tool_collocates('sz_small', 'Trump', '7', ['am.simple.ll'], 's')

    assert fail.empty == True


@mock.patch('backend.analysis.engines.cwb.Popen')
@mock.patch('backend.analysis.engines.cwb.run')
def test_cwb_ucs_tool_collocates_error(mock_run, mock_popen):

    mock_run.side_effect = Exception('foo')

    fail = ucs_tool_collocates('sz_small', 'Trump', '7', ['am.simple.ll'], 's')

    assert fail.empty == True


@mock.patch('backend.analysis.engines.cwb.ucs_tool_collocates')
def test_cwb_engine_extract_collocates_error(mock_collo, corpus_settings):

    eng = CWBEngine('foo_corpus', corpus_settings)

    with pytest.raises(ValueError):
        fail = eng.extract_collocates('fooquery', 5)


@mock.patch('backend.analysis.engines.cwb.ucs_tool_collocates')
def test_cwb_engine_extract_collocates(mock_collo, corpus_settings):

    expected_df = pandas.DataFrame(data=[['17013', '1', '4', '1'],['1404', '1', '9', '2'],['16711','1', '4', '3']],
                                    columns=['f2', 'O11', 'Dice', 'Log'],
                                    index=['nicht', 'halten', 'sich'])
    expected_df.index.name = 'item'

    mock_data = pandas.DataFrame(data=[
        ['1', 'NODE', 'nicht', '1', '7', '17013', '2693270', '4', '1'],
        ['2', 'NODE', 'halten', '1', '7', '1404', '2693270', '9', '2'],
        ['3', 'NODE', 'sich', '1', '7', '16711', '2693270', '4', '3']],
        columns=['id', 'l1', 'l2', 'f', 'f1', 'f2', 'N', 'Dice', 'Log'])

    mock_collo.return_value = mock_data

    eng = CWBEngine('foo_corpus', corpus_settings)

    actual_df, actual_f1, actual_N = eng.extract_collocates('fooquery', 5)

    assert actual_f1 == 7
    assert actual_N == 2693270
    assert_frame_equal(actual_df, expected_df)
    assert mock_collo.call_count == 1


@mock.patch('backend.analysis.engines.cwb.sort_concordances')
@mock.patch('backend.analysis.engines.cwb.cqp_concordances_of_discourse')
@mock.patch('backend.analysis.engines.cwb.cqp_concordances_of_topic')
def test_cwb_engine_extract_concordances_topic(mock_topic, mock_discourse, mock_sort, corpus_settings):

    mock_topic.return_value = [1, 2, 3]
    eng = CWBEngine('foo_corpus', corpus_settings)

    actual = eng.extract_concordances('fooquery', 5)

    mock_topic.assert_called_with('foo_corpus', 'fooquery')
    mock_sort.assert_called_with([1, 2, 3], 'random')


@mock.patch('backend.analysis.engines.cwb.cqp_concordances_of_discourse', return_value=None)
def test_cwb_engine_extract_concordances_discourse_error(mock_discourse, corpus_settings):

    eng = CWBEngine('foo_corpus', corpus_settings)

    with pytest.raises(ValueError):
        fail = eng.extract_concordances('fooquery', 5, ['item1'])


@mock.patch('backend.analysis.engines.cwb.sort_concordances')
@mock.patch('backend.analysis.engines.cwb.cqp_concordances_of_discourse')
@mock.patch('backend.analysis.engines.cwb.cqp_concordances_of_topic')
def test_cwb_engine_extract_concordances_discourse(mock_topic, mock_discourse, mock_sort, corpus_settings):

    mock_discourse.return_value = [1, 2, 3]
    eng = CWBEngine('foo_corpus', corpus_settings)

    actual = eng.extract_concordances('fooquery', 5, ['item1'])

    mock_discourse.assert_called_with('foo_corpus', 'fooquery', 5, 's', ['item1'])
    mock_sort.assert_called_with([1, 2, 3], 'random')
