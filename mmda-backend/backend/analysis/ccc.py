#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Concordance and Collocation Computation
"""

from ccc import Corpora, Corpus
from ccc.discoursemes import create_constellation
from ccc.utils import format_cqp_query
from anycache import anycache
from pandas import DataFrame

import logging

logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO)
log = logging.getLogger('mmda-logger')

CACHE_PATH = '/tmp/mmda-anycache/'


def sort_p(p_atts):
    """sort p-attributes

    :param list p_atts: p-attributes
    """
    order = ['lemma_pos', 'lemma', 'word']
    ordered = [p for p in order if p in p_atts] + [p for p in p_atts if p not in order]
    return ordered


def sort_s(s_atts):
    """sort s-attributes

    :param list s_atts: s-attributes
    """
    order = ['s', 'p', 'tweet', 'text']
    ordered = [s for s in order if s in s_atts] + [s for s in s_atts if s not in order]
    return ordered


def ccc_corpora(cqp_bin, registry_path):
    """show available corpora

    :param str cqp_bin: path to CQP binaries
    :param str registry_path: path to CWB registry
    """
    corpora = Corpora(cqp_bin, registry_path).show()
    return corpora


def ccc_corpus(corpus_name, cqp_bin, registry_path, data_path):
    """get available corpus attributes

    :param str corpus_name: name of corpus in CWB
    :param str cqp_bin: path to CQP binaries
    :param str registry_path: path to CWB registry
    :param str data_path: path to data directory

    :return: available corpus attributes
    :rtype: dict
    """
    corpus = Corpus(corpus_name,
                    cqp_bin=cqp_bin,
                    registry_path=registry_path,
                    data_path=data_path)
    attributes = corpus.attributes_available
    p_atts = list(
        attributes.loc[attributes['type'] == 'p-Att']['attribute'].values
    )
    s_atts = attributes[attributes['type'] == 's-Att']
    s_annotations = list(s_atts[s_atts['annotation']]['attribute'].values)
    s_atts = list(s_atts[~s_atts['annotation']]['attribute'].values)

    crps = {
        'p-atts': sort_p(p_atts),  # all p-attributes
        's-atts': sort_s(s_atts),  # s-attributes without annotation
        's-annotations': s_annotations  # s-attributes with annotation
    }

    return crps


# @anycache(CACHE_PATH)
# TODO take care of caching for random order
def ccc_concordance(corpus_name, cqp_bin, registry_path, data_path,
                    lib_path, topic_items, topic_name, s_context,
                    window_size, context=20,
                    additional_discoursemes={}, p_query='lemma',
                    p_show=['word', 'lemma'], s_show=['text_id'],
                    s_query=None, order='random', cut_off=100,
                    flags_query="%cd", escape_query=True):
    """
    :param str corpus_name: name corpus in CWB registry

    :param str topic_name: name of the topic ("node") discourseme
    :param list topic_items: list of lexical items
    :param str p_query: p-att layer to query
    :param str s_query: s-att to use for delimiting queries
    :param str flags_query: flags to use for querying
    :param bool escape_query: whether to cqp-escape the query items

    :param str s_context: s-att to use for delimiting contexts
    :param int context: context around the nodes used to identify relevant matches

    :param dict additional_discoursemes: {name: items}

    :param list p_show: p-attributes to show
    :param list s_show: s-attributes to show
    :param int window: mark tokens further away as 'out_of_window'
    :param str order: concordance order (first / last / random)
    :param int cut_off: number of lines to retrieve

    :param str lib_path:
    :param str cqp_bin:
    :param str registry_path:
    :param str data_path:

    :return: dict of concordance lines (each one a dict, keys=1:N)
    :rtype: dict

    """

    # preprocess parameters
    s_query = s_context if s_query is None else s_query
    window = context if window_size is None else window_size

    # create constellation
    const = create_constellation(corpus_name,
                                 topic_name, topic_items,
                                 p_query, s_query, flags_query, escape_query,
                                 s_context, context,
                                 additional_discoursemes,
                                 lib_path, cqp_bin, registry_path, data_path)

    # retrieve lines
    lines = const.concordance(window=window,
                              p_show=p_show, s_show=s_show,
                              order=order, cut_off=cut_off)

    # convert to HTML table
    # TODO: speed up!
    output = dict()
    c = 0                       # random key (for sorting)
    for line in lines:
        c += 1
        output[c] = line
        meta = dict()
        for s in ['match'] + s_show:
            meta[s] = output[c].pop(s)
        output[c]['meta'] = DataFrame.from_dict(
            meta, orient='index'
        ).to_html(bold_rows=False, header=False)

    return output


@anycache(CACHE_PATH)
def ccc_collocates(corpus_name, cqp_bin, registry_path, data_path,
                   lib_path, topic_items, s_context, windows,
                   context=20, additional_discoursemes={},
                   p_query='lemma', flags_query='%cd', s_query=None,
                   p_show=['lemma'], flags_show="", ams=None,
                   cut_off=200, min_freq=2, order='log_likelihood',
                   escape=True, frequencies=True):
    """
    :param str corpus_name: name corpus in CWB registry

    :param list topic_items: list of lexical items
    :param str p_query: p-att layer to query
    :param str s_query: s-att to use for delimiting queries
    :param str flags_query: flags to use for querying
    :param bool escape_items: whether to cqp-escape the query items

    :param str s_context: s-att to use for delimiting contexts
    :param int context: context around the nodes used to identify relevant matches

    :param dict additional_discoursemes: {name: items}

    :param list windows: windows (int) to use for collocation analyses around nodes
    :param list p_show: p-atts to use for collocation analysis
    :param str flags_show: post-hoc folding ("%cd") with cwb-ccc-algorithm
    :param int min_freq: rare item treshold
    :param str order: collocation order (columns in scored table)
    :param int cut_off: number of collocates to retrieve

    :param str lib_path:
    :param str cqp_bin:
    :param str registry_path:
    :param str data_path:

    :return: dict of collocation tables (key=window)
    :rtype: dict

    """

    # preprocess parameters
    s_query = s_context if s_query is None else s_query
    topic_name = 'topic'

    # create constellation
    const = create_constellation(corpus_name,
                                 topic_name, topic_items,
                                 p_query, s_query, flags_query, escape,
                                 s_context, context,
                                 additional_discoursemes,
                                 lib_path, cqp_bin, registry_path, data_path)

    collocates = const.collocates(windows=windows,
                                  p_show=p_show, flags=flags_show,
                                  ams=ams, frequencies=frequencies, min_freq=min_freq,
                                  order=order, cut_off=cut_off)

    for window in collocates.keys():
        coll_window = collocates[window]
        # drop superfluous columns and sort
        coll_window = coll_window[[
            'log_likelihood',
            'dice',
            'log_ratio',
            'mutual_information',
            'z_score',
            't_score',
            'f',
            'f2'
        ]]

        # rename AMs
        am_dict = {
            'log_likelihood': 'log likelihood',
            'dice': 'Dice',
            'log_ratio': 'log ratio',
            'mutual_information': 'mutual information',
            'z_score': 'z-score',
            't_score': 't-score',
            'f': 'co-oc. freq.',
            'f2': 'marginal freq.'
        }
        collocates[window] = coll_window.rename(am_dict, axis=1)

    return collocates


# @anycache(CACHE_PATH)
def ccc_breakdown(corpus_name, cqp_bin, registry_path, data_path, lib_path,
                  topic_items, p_query='lemma', s_query=None, p_show=['word'],
                  flags_query="%cd", escape=True, flags_show=""):
    """
    :param str corpus_name: name corpus in CWB registry

    :param list topic_items: list of lexical items
    :param str p_query: p-att layer to query
    :param str s_query: s-att to use for delimiting queries
    :param str flags_query: flags to use for querying
    :param bool escape_items: whether to cqp-escape the query items

    :param list p_show: p-atts to use for collocation analysis
    :param str flags_show: post-hoc folding ("%cd") with cwb-ccc-algorithm TODO

    :param str lib_path:
    :param str cqp_bin:
    :param str registry_path:
    :param str data_path:

    :return: dict of breakdown
    :rtype: dict

    """

    # init corpus
    corpus = Corpus(corpus_name, lib_path, cqp_bin, registry_path, data_path)

    # init discourseme constellation
    topic_query = format_cqp_query(topic_items,
                                   p_query=p_query, s_query=s_query,
                                   flags=flags_query, escape=escape)
    dump = corpus.query(topic_query, context=None)
    breakdown = dump.breakdown()

    # convert to dictionary
    out = list()
    for row in breakdown.iterrows():
        out.append({
            'item': row[0][0],
            'freq': int(row[1]['freq'])
        })

    return out


# @anycache(CACHE_PATH)
def ccc_meta(corpus_name, cqp_bin, registry_path, data_path, lib_path,
             topic_items, p_query='lemma', s_query=None,
             flags_query="%cd", s_show=['text_id'], order='first',
             cut_off=None, escape=True):
    """
    :param str corpus_name: name corpus in CWB registry

    :param str topic_name: name of the topic ("node") discourseme
    :param list topic_items: list of lexical items
    :param str p_query: p-att layer to query
    :param str s_query: s-att to use for delimiting queries
    :param str flags_query: flags to use for querying
    :param bool escape_query: whether to cqp-escape the query items

    :param str s_context: s-att to use for delimiting contexts
    :param int context: context around the nodes used to identify relevant matches

    :param dict additional_discoursemes: {name: items}

    :param list p_show: p-attributes to show
    :param list s_show: s-attributes to show
    :param int window: mark tokens further away as 'out_of_window'
    :param str order: concordance order (first / last / random)
    :param int cut_off: number of lines to retrieve

    :param str lib_path:
    :param str cqp_bin:
    :param str registry_path:
    :param str data_path:

    :return: dict of meta data
    :rtype: dict

    """

    # init corpus
    corpus = Corpus(corpus_name, lib_path, cqp_bin, registry_path, data_path)

    # init discourseme constellation
    topic_query = format_cqp_query(topic_items,
                                   p_query=p_query, s_query=s_query,
                                   flags=flags_query, escape=escape)
    dump = corpus.query(topic_query, context=None)

    meta = dump.concordance(
        s_show=s_show, form='simple', order=order, cut_off=cut_off
    )
    output = list()
    for s in s_show:
        m = meta[s].value_counts()
        if len(m) < 100:
            m = m.to_frame().reset_index()
            m.columns = [s, 'frequency']
            m = m.sort_values(by=s)
            output.append(m.to_html(index=False, bold_rows=False))

    return output
