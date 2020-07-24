import pytest


@pytest.fixture
def brexit():
    """ settings for BREXIT_V20190522_DEDUP """

    corpus = {
        'name': "BREXIT_V20190522_DEDUP",
        'registry_path': "/home/ausgerechnet/corpora/cwb/registry/",
        'lib_path': (
            "/home/ausgerechnet/"
            "repositories/spheroscope/library/BREXIT_V20190522_DEDUP/"
        ),
        'meta_path': (
            "/home/ausgerechnet/corpora/cwb/upload/"
            "brexit/brexit-preref-rant/brexit_v20190522_dedup.tsv.gz"
        ),
        'meta_s': 'tweet_id',
        'max_window_size': 20
    }

    parameters = {
        'context': 20,
        's_context': 'tweet',
        's_query': 'tweet',
        'p_query': 'lemma'
    }

    query = '[lemma="test"]'
    query_lib = (
        '<np>[pos_simple!="P"] []*</np> [lemma = $verbs_cause] [pos_simple="R"]? '
        '<np>[]*</np> (<np>[]*</np> | <vp>[]*</vp> | <pp>[]*</pp>)+'
    )

    discoursemes = {
        'topic': '',
        'disc1': '',
        'disc2': ''
    }

    return {
        'corpus': corpus,
        'query': query,
        'query_lib': query_lib,
        'parameters': parameters,
        'discoursemes': discoursemes
    }


@pytest.fixture
def germaparl():
    """ settings for GERMAPARL_1114 """

    corpus = {
        'name': "GERMAPARL_1114",
        'registry_path': "/home/ausgerechnet/corpora/cwb/registry/",
        'meta_s': 'text_id'
    }

    parameters = {
        'context': 20,
        's_context': 's',
        's_query': 's',
        'p_query': 'lemma'
    }

    query = '[lemma="Test"]'

    discoursemes = {
        'topic': ["Merkel", "Seehofer", "Steinmeier"],
        'disc1': ["Angela", "Streit", "Verhandlung", "Regierung"],
        'disc2': ['die']
    }

    return {
        'corpus': corpus,
        'query': query,
        'parameters': parameters,
        'discoursemes': discoursemes
    }
