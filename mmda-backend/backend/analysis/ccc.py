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


def sort_p(p_atts):
    order = ['lemma_pos', 'lemma', 'word']
    ordered = [p for p in order if p in p_atts] + [p for p in p_atts if p not in order]
    return ordered


def sort_s(s_atts):
    order = ['s', 'p', 'tweet', 'text']
    ordered = [s for s in order if s in s_atts] + [s for s in s_atts if s not in order]
    return ordered


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

    # provide reasonable sort order
    crps = {
        'p-atts': sort_p(p_atts),
        's-atts': sort_s(s_atts)
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
def ccc_collocates(corpus_name, cqp_bin, registry_path, data_path,
                   lib_path, topic_items, s_context, windows,
                   context=20, additional_discoursemes={},
                   p_query='lemma', flags_query='%cd', s_query=None,
                   p_show=['lemma'], flags_show="", ams=None,
                   cut_off=200, min_freq=2, order='log_likelihood',
                   escape=True):

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


# @anycache(CACHE_PATH)
def ccc_breakdown(corpus_name, cqp_bin, registry_path, data_path, lib_path,
                  topic_items, p_query='lemma', s_query=None, p_show=['word']):

    flags_query = "%cd"
    flags_show = ""
    escape = True

    breakdown = get_breakdown(
        corpus_name,
        topic_items,
        p_query,
        s_query,
        flags_query,
        escape,
        p_show,
        flags_show,
        lib_path, cqp_bin, registry_path, data_path
    )

    return breakdown


# @anycache(ANYCACHE_PATH)
def get_breakdown(corpus_name,
                  topic_items,
                  p_query='lemma',
                  s_query=None,
                  flags_query="%cd",
                  escape_items=True,
                  p_show=['word', 'lemma'],
                  flags_show="",
                  lib_path=None, cqp_bin='cqp',
                  registry_path='/usr/local/share/cwb/registry/',
                  data_path='/tmp/ccc-data/'):
    """
    :param str corpus_name: name corpus in CWB registry

    :param list topic_items: list of lexical items
    :param str p_query: p-att layer to query
    :param str s_query: s-att to use for delimiting queries
    :param str flags_query: flags to use for querying
    :param bool escape_items: whether to cqp-escape the query items

    :param list p_show: p-atts to use for collocation analysis
    :param str flags_show: post-hoc folding ("%cd") with cwb-ccc-algorithm

    :param str lib_path:
    :param str cqp_bin:
    :param str registry_path:
    :param str data_path:

    :return: dict of breakdown
    :rtype: dict

    """
    from ccc import Corpus
    from ccc.utils import format_cqp_query

    # init corpus
    corpus = Corpus(corpus_name, lib_path, cqp_bin, registry_path, data_path)

    # init discourseme constellation
    topic_query = format_cqp_query(topic_items,
                                   p_query=p_query, s_query=s_query,
                                   flags=flags_query, escape=escape_items)
    dump = corpus.query(topic_query, context=None)

    # convert to dictionary
    out = list()
    for row in dump.breakdown().iterrows():
        out.append({
            'item': row[0][0],
            'freq': int(row[1]['freq'])
        })

    return out
