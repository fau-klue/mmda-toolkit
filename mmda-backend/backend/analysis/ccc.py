#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Concordance and Collocation Computation
"""

from ccc import Corpora, Corpus
from ccc.discoursemes import create_constellation
from ccc.utils import format_cqp_query
from ccc.counts import score_counts

from pandas import DataFrame, concat

from anycache import anycache
from backend.settings import ANYCACHE_PATH as CACHE_PATH

import logging

logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO)
log = logging.getLogger('mmda-logger')


#############
# UTILITIES #
#############
def format_meta(lines, s_show):

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


def format_counts(df, add=None):

    ams_dict = {
        # asymptotic hypothesis tests
        'log_likelihood': 'log likelihood',
        'z_score': 'z-score',
        't_score': 't-score',
        'simple_ll': 'simple LL',
        # point estimates of association strength
        'dice_1000': 'Dice-1000',
        'log_ratio': 'log ratio',
        # information theory
        'mutual_information': 'mutual information',
        'local_mutual_information': 'local MI',
        # conservative estimates
        'conservative_log_ratio': 'Conservative LR',
        # frequencies
        'ipm': 'IPM (obs.)',
        'ipm_expected': 'IPM (exp.)',
    }

    # scale Dice coefficient
    df['dice_1000'] = df['dice'] * 10**3

    # select and rename
    df = df[list(ams_dict.keys())]
    df = df.rename(ams_dict, axis=1)

    # add additional items
    if add is not None and len(add) > 0:
        add = add[['freq']].copy()
        for c in df.columns:
            add[[c]] = add[['freq']]
        df = concat([df, add])

    return df


def sort_p(p_atts, order=['lemma_pos', 'lemma', 'word']):
    """sort p-attributes

    :param list p_atts: p-attributes

    """
    ordered = [p for p in order if p in p_atts] + [p for p in p_atts if p not in order]
    return ordered


def sort_s(s_atts, order=['tweet', 's', 'p', 'text']):
    """sort s-attributes

    :param list s_atts: s-attributes

    """
    ordered = [s for s in order if s in s_atts] + [s for s in s_atts if s not in order]
    return ordered


#################
# CCC INTERFACE #
#################
def ccc_corpora(cqp_bin, registry_path):
    """get available corpora

    :param str cqp_bin: path to CQP binary
    :param str registry_path: path to CWB registry

    """
    corpora = Corpora(cqp_bin, registry_path).show()
    return corpora


def ccc_corpus(corpus_name, cqp_bin, registry_path, data_path):
    """get available corpus attributes

    :param str corpus_name: name of corpus in CWB registry
    :param str cqp_bin: path to CQP binary
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


@anycache(CACHE_PATH)
def ccc_collocates(corpus_name, cqp_bin, registry_path, data_path,
                   lib_path, topic_items, s_context, windows,
                   context=20, filter_discoursemes={},
                   additional_discoursemes={}, p_query='lemma',
                   flags_query='%c', s_query=None, p_show=['lemma'],
                   flags_show='', ams=None, cut_off=500, min_freq=2,
                   order='log_likelihood', escape=True,
                   frequencies=True, topic_name='topic'):
    """get collocates for topic (+ additional discoursemes).

    :param str corpus_name: name of corpus in CWB registry
    :param str cqp_bin: path to CQP binary
    :param str registry_path: path to CWB registry
    :param str data_path: path to data directory
    :param str lib_path: path to library (with macros and wordlists)

    :param list topic_items: list of lexical items
    :param str s_context: s-att to use for delimiting contexts
    :param list windows: windows (int) to use for collocation analyses around nodes
    :param int context: context around the nodes used to identify relevant matches

    :param dict additional_discoursemes: {name: items}

    :param str p_query: p-att layer to query
    :param str flags_query: flags to use for querying
    :param str s_query: s-att to use for delimiting queries
    :param list p_show: p-atts to use for collocation analysis
    :param str flags_show: post-hoc folding ('%cd') with cwb-ccc-algorithm
    :param list ams: association measures to calculate (None = all)

    :param int cut_off: number of collocates to retrieve
    :param int min_freq: rare item treshold
    :param str order: collocation order (column in scored table)

    :param bool escape: whether to cqp-escape the query items
    :param bool frequencies: whether to retrieve frequencies

    :return: dict of collocation tables (key=window)
    :rtype: dict

    """

    # preprocess parameters
    s_query = s_context if s_query is None else s_query
    match_strategy = 'longest'
    escape_query = True
    topic_discourseme = {'topic': topic_items}

    # create constellation
    try:
        const = create_constellation(corpus_name,
                                     # discoursemes
                                     topic_discourseme,
                                     filter_discoursemes,
                                     additional_discoursemes,
                                     # context settings
                                     s_context,
                                     context,
                                     # query settings
                                     p_query,
                                     s_query,
                                     flags_query,
                                     escape_query,
                                     match_strategy,
                                     # CWB settings
                                     lib_path,
                                     cqp_bin,
                                     registry_path,
                                     data_path)
    except KeyError:            # no matches
        return
    collocates = const.collocates(
        windows=windows,
        p_show=p_show, flags=flags_show,
        ams=ams, frequencies=frequencies, min_freq=min_freq,
        order=order, cut_off=cut_off
    )

    # append items in freq breakdown p_att = p_query with high size
    breakdowns = list()
    breakdown = None
    for idx, dump in const.discoursemes.items():
        if idx != 'topic':
            breakdowns.append(dump.breakdown(p_atts=[p_query]))
    if len(breakdowns) > 0:
        breakdown = concat(breakdowns)

    # formatting
    for window in collocates.keys():
        collocates[window] = format_counts(collocates[window], breakdown)

    return collocates


# @anycache(CACHE_PATH)
def ccc_breakdown(corpus_name, cqp_bin, registry_path, data_path, lib_path,
                  topic_items, p_query='lemma', s_query=None, p_show=['lemma'],
                  flags_query='%c', escape=True, flags_show='%c'):
    """get breakdown of topic.
    :param str corpus_name: name of corpus in CWB registry
    :param str lib_path:
    :param str cqp_bin:
    :param str registry_path:
    :param str data_path:

    :param list topic_items: list of lexical items
    :param str p_query: p-att layer to query
    :param str s_query: s-att to use for delimiting queries
    :param list p_show: p-atts to base breakdown on
    :param str flags_query: flags to use for querying
    :param bool escape: whether to cqp-escape the query items
    :param str flags_show: post-hoc folding ('%cd') with cwb-ccc-algorithm TODO

    :return: breakdown
    :rtype: dict

    """

    # init corpus
    corpus = Corpus(corpus_name, lib_path, cqp_bin, registry_path, data_path)

    # init discourseme constellation
    topic_query = format_cqp_query(topic_items,
                                   p_query=p_query, s_query=s_query,
                                   flags=flags_query, escape=escape)
    dump = corpus.query(topic_query, context=None)
    breakdown = dump.breakdown(p_show, flags_show)

    # formatting
    out = list()
    for row in breakdown.iterrows():
        out.append({
            'item': row[0],
            'freq': int(row[1]['freq'])
        })

    return out


@anycache(CACHE_PATH)
def ccc_meta(corpus_name, cqp_bin, registry_path, data_path, lib_path,
             topic_items, p_query='lemma', s_query=None,
             flags_query='%c', s_show=['text_id'], order='first',
             cut_off=None, escape=True):
    """get meta data of topic.

    :param str corpus_name: name of corpus in CWB registry
    :param str cqp_bin: path to CQP binary
    :param str registry_path: path to CWB registry
    :param str data_path: path to data directory
    :param str lib_path: path to library (with macros and wordlists)

    :param list topic_items: list of lexical items
    :param str p_query: p-att layer to query
    :param str s_query: s-att to use for delimiting queries
    :param str flags_query: flags to use for querying
    :param list s_show: s-attributes to show
    :param str order: concordance order (first / last / random)
    :param int cut_off: number of lines to retrieve
    :param bool escape: whether to cqp-escape the query items

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

    # get meta data
    meta = dump.concordance(
        s_show=s_show, form='simple', order=order, cut_off=cut_off
    )

    # tabulate
    output = list()
    for s in s_show:

        # tabulate number of tokens
        # TODO: no need to calculate for each text_x, text_y, etc.
        lengths = corpus.query_s_att(s)
        lengths = lengths.df.reset_index()
        lengths['nr_tokens'] = lengths['matchend'] - lengths['match'] + 1

        # absolute frequency in each subcorpus
        m = meta[s].value_counts()

        if len(m) < 100:
            m = m.to_frame()
            m.columns = ['frequency']
            ell = lengths.groupby(s)[['nr_tokens']].agg(sum)
            ell = ell.join(m, how='outer')
            ell = ell.fillna(0, downcast='infer')
            ell['IPM'] = round(ell['frequency'] / ell['nr_tokens'] * 10**6, 2)
            ell.index.name = s
            ell = ell.reset_index()
            output.append(ell.to_html(index=False, bold_rows=False))

    return output


@anycache(CACHE_PATH)
def ccc_constellation_association(corpus_name, cqp_bin, registry_path,
                                  data_path, lib_path, discoursemes,
                                  p_query='lemma', s_query=None,
                                  flags_query='%c',
                                  escape_query=True, s_context=None,
                                  context=None):
    """Pairwise association scores for discoursemes.

    :param str corpus_name: name corpus in CWB registry
    :param str cqp_bin:
    :param str registry_path:
    :param str data_path:
    :param str lib_path:

    :param dict discoursemes: {name: items}
    :param str p_query: p-att layer to query
    :param str s_query: s-att to use for delimiting queries
    :param str flags_query: flags to use for querying
    :param bool escape_query: whether to cqp-escape the query items

    :param str s_context: s-att to use for delimiting contexts
    :param int context: context around the nodes used to identify relevant matches

    :return: associations between all pairs of discoursemes in the constellation
    :rtype: DataFrame

    """

    # pre-process parameters
    s_context = s_query if not s_context else s_context
    match_strategy = 'longest'

    # create constellation
    const = create_constellation(corpus_name,
                                 # discoursemes
                                 {},
                                 discoursemes,
                                 {},
                                 # context settings
                                 s_context,
                                 context,
                                 # query settings
                                 p_query,
                                 s_query,
                                 flags_query,
                                 escape_query,
                                 match_strategy,
                                 # CWB settings
                                 lib_path,
                                 cqp_bin,
                                 registry_path,
                                 data_path)

    tables = const.associations()

    # formatting
    out = list()
    for row in tables.iterrows():
        v = dict(row[1])
        out.append(v)

    return out


@anycache(CACHE_PATH)
def ccc_keywords(corpus, corpus_reference,
                 cqp_bin, registry_path, data_path, lib_path,
                 p=['lemma'], p_reference=['lemma'],
                 flags=None, flags_reference=None,
                 ams=None, cut_off=500, min_freq=2, order='log_likelihood'):

    # TODO mv to CWB
    corpus = Corpus(corpus)
    corpus_reference = Corpus(corpus_reference)
    left = corpus.marginals(p_atts=p)[['freq']]
    right = corpus_reference.marginals(p_atts=p_reference)[['freq']]
    left.columns = ['f1']
    right.columns = ['f2']
    df = left.join(right, how='outer')
    df['N1'] = corpus.corpus_size
    df['N2'] = corpus_reference.corpus_size
    keywords = score_counts(df, order=order, cut_off=cut_off,
                            ams=ams, digits=4)

    # formatting
    keywords = format_counts(keywords)

    return keywords


@anycache(CACHE_PATH)
def ccc_concordance(corpus_name, cqp_bin, registry_path, data_path,
                    lib_path, topic_discourseme, filter_discoursemes,
                    additional_discoursemes, s_context,
                    window_size, context=20, p_query='lemma',
                    p_show=['word', 'lemma'], s_show=['text_id'],
                    s_query=None, order='random', cut_off=100,
                    flags_query='%c', escape_query=True, random_seed=42):
    """get concordance lines for topic (+ additional discoursemes).

    :param str corpus_name: name of corpus in CWB registry
    :param str cqp_bin: path to CQP binary
    :param str registry_path: path to CWB registry
    :param str data_path: path to data directory
    :param str lib_path: path to library (with macros and wordlists)

    :param list topic_items: list of lexical items
    :param str topic_name: name of the topic ('node') discourseme
    :param str s_context: s-att to use for delimiting contexts
    :param int window_size: mark tokens further away from topic as 'out_of_window'
    :param int context: context around the nodes used to identify relevant matches

    :param dict additional_discoursemes: {name: items}

    :param str p_query: p-att layer to query
    :param list p_show: p-attributes to show
    :param list s_show: s-attributes to show
    :param str s_query: s-att to use for delimiting queries
    :param str order: concordance order (first / last / random)
    :param int cut_off: number of lines to retrieve
    :param str flags_query: flags to use for querying
    :param bool escape_query: whether to cqp-escape the query items

    :return: dict of concordance lines (each one a dict, keys=1:N)
    :rtype: dict

    """

    # preprocess parameters
    s_query = s_context if s_query is None else s_query
    window = context if window_size is None else window_size
    match_strategy = 'longest'

    # create constellation
    const = create_constellation(corpus_name,
                                 # discoursemes
                                 topic_discourseme,
                                 filter_discoursemes,
                                 additional_discoursemes,
                                 # context settings
                                 s_context,
                                 context,
                                 # query settings
                                 p_query,
                                 s_query,
                                 flags_query,
                                 escape_query,
                                 match_strategy,
                                 # CWB settings
                                 lib_path,
                                 cqp_bin,
                                 registry_path,
                                 data_path,
                                 window=window_size)

    # retrieve lines
    lines = const.concordance(window,
                              p_show,
                              s_show,
                              order=order,
                              cut_off=cut_off,
                              random_seed=random_seed)

    # format meta data as HTML tables
    lines = format_meta(lines, s_show)

    return lines
