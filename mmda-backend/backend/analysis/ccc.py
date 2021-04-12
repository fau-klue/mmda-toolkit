#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Concordance and Collocation Computation
"""

from ccc import Corpora, Corpus
from ccc.discoursemes import get_concordance, get_collocates

import logging

logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO)
log = logging.getLogger('mmda-logger')


REGISTRY_PATH = "/usr/local/share/cwb/registry"
DATA_PATH = "/tmp/mmda-ccc-data/"
CQP_BIN = "cqp"
LIB_PATH = None


def ccc_corpora():
    corpora = Corpora(CQP_BIN, REGISTRY_PATH).show()
    return corpora


def ccc_corpus(corpus_name):
    corpus = Corpus(corpus_name,
                    cqp_bin=CQP_BIN,
                    registry_path=REGISTRY_PATH,
                    data_path=DATA_PATH)
    attributes = corpus.attributes_available
    p_atts = list(
        attributes.loc[attributes['type'] == 'p-Att']['attribute'].values
    )
    s_atts = attributes[attributes['type'] == 's-Att']
    s_atts = list(s_atts[~s_atts['annotation']]['attribute'].values)
    crps = {
        'p-atts': p_atts,
        's-atts': s_atts
    }
    return crps


def ccc_concordance(corpus_name, topic_items, topic_name, s_context,
                    window_size, context=20,
                    additional_discoursemes={}, p_query='lemma',
                    p_show=['word', 'lemma'], s_show=['text_id'],
                    s_query=None, order='random', cut_off=100):

    flags_query = "%cd"
    escape_query = True
    window = window_size
    topic_name = 'topic'

    conc = get_concordance(
        corpus_name,
        topic_name, topic_items, p_query, s_query, flags_query, escape_query,
        s_context, context,
        additional_discoursemes,
        p_show, s_show, window, order, cut_off,
        LIB_PATH, CQP_BIN, REGISTRY_PATH, DATA_PATH
    )

    return conc


def ccc_collocates(corpus_name, topic_items, s_context, window_sizes,
                   context=20, additional_discoursemes={},
                   p_query='lemma', s_query=None, ams=None,
                   cut_off=200, order='log_likelihood'):

    flags_query = "%cd"
    flags_show = ""
    escape = True
    p_show = [p_query]
    windows = window_sizes
    min_freq = 2

    coll = get_collocates(
        corpus_name,
        topic_items,
        p_query,
        s_query,
        flags_query,
        escape,
        s_context,
        context,
        additional_discoursemes,
        windows,
        p_show,
        flags_show,
        min_freq,
        order,
        cut_off,
        LIB_PATH, CQP_BIN, REGISTRY_PATH, DATA_PATH
    )

    return coll
