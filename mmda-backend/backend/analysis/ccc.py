#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Concordance and Collocation Computation
"""

from ccc import Corpora, Corpus
from ccc.discoursemes import get_concordance, get_collocates
from anycache import anycache

import logging

logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO)
log = logging.getLogger('mmda-logger')

CACHE_PATH = '/tmp/mmda-anycache/'


def ccc_corpora(cqp_bin, registry_path):
    corpora = Corpora(cqp_bin, registry_path).show()
    return corpora


def ccc_corpus(corpus_name, cqp_bin, registry_path, data_path):
    corpus = Corpus(corpus_name,
                    cqp_bin=cqp_bin,
                    registry_path=registry_path,
                    data_path=data_path)
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


@anycache(CACHE_PATH)
# TODO take care of caching for random order
def ccc_concordance(corpus_name, cqp_bin, registry_path, data_path, lib_path,
                    topic_items, topic_name, s_context,
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
        lib_path, cqp_bin, registry_path, data_path
    )

    return conc


@anycache(CACHE_PATH)
def ccc_collocates(corpus_name, cqp_bin, registry_path, data_path, lib_path,
                   topic_items, s_context, window_sizes,
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
        lib_path, cqp_bin, registry_path, data_path
    )

    return coll


@anycache(CACHE_PATH)
def ccc_breakdown(corpus_name, cqp_bin, registry_path, data_path, lib_path,
                  topic_items, p_query='lemma',
                  p_show=['word'], s_query=None):

    return {'msg': 'received'}
