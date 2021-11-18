#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Concordance and Collocation Computation
"""

from ccc import Corpora, Corpus
from ccc.discoursemes import create_constellation, role_formatter
from ccc.utils import format_cqp_query
from ccc.concordances import Concordance

from pandas import DataFrame, isna

# from anycache import anycache
# from backend.settings import ANYCACHE_PATH as CACHE_PATH

import logging

logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO)
log = logging.getLogger('mmda-logger')


def sort_p(p_atts, order=['lemma_pos', 'lemma', 'word']):
    """sort p-attributes

    :param list p_atts: p-attributes

    """
    ordered = [p for p in order if p in p_atts] + [p for p in p_atts if p not in order]
    return ordered


def sort_s(s_atts, order=['s', 'p', 'tweet', 'text']):
    """sort s-attributes

    :param list s_atts: s-attributes

    """
    ordered = [s for s in order if s in s_atts] + [s for s in s_atts if s not in order]
    return ordered


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


# @anycache(CACHE_PATH)
# TODO take care of caching for random order
def ccc_concordance(corpus_name, cqp_bin, registry_path, data_path,
                    lib_path, topic_items, topic_name, s_context,
                    window_size, context=20,
                    additional_discoursemes={}, p_query='lemma',
                    p_show=['word', 'lemma'], s_show=['text_id'],
                    s_query=None, order='random', cut_off=100,
                    flags_query='%cd', escape_query=True):
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


# @anycache(CACHE_PATH)
def ccc_collocates(corpus_name, cqp_bin, registry_path, data_path,
                   lib_path, topic_items, s_context, windows,
                   context=20, additional_discoursemes={},
                   p_query='lemma', flags_query='%cd', s_query=None,
                   p_show=['lemma'], flags_show='', ams=None,
                   cut_off=500, min_freq=2, order='log_likelihood',
                   escape=True, frequencies=True, topic_name='topic'):
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

    # choose and name columns
    am_dict = {
        # 'O11': 'cooc. freq. (obs.)',
        # 'O12', 'O21', 'O22',
        # 'E11': 'cooc. freq. (exp.)',
        # 'E12', 'E21', 'E22'
        # 'in_nodes'
        # 'marginal'
        # 'ipm_reference': 'IPM (obs.)',
        # 'ipm_reference_expected': 'IPM (exp.)',
        'log_likelihood': 'log likelihood',
        'dice': 'Dice',
        'log_ratio': 'log ratio',
        'mutual_information': 'mutual information',
        'z_score': 'z-score',
        't_score': 't-score',
        'simple_ll': 'simple LL',
        'local_mutual_information': 'local MI',
        'conservative_log_ratio': 'Conservative LR',
        'ipm': 'IPM (obs.)',
        'ipm_expected': 'IPM (exp.)',
    }

    # preprocess parameters
    s_query = s_context if s_query is None else s_query

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

        collocates[window] = collocates[window][list(am_dict.keys())]
        collocates[window] = collocates[window].rename(am_dict, axis=1)
        collocates[window]['Dice-1000'] = collocates[window]['Dice'] * 10**3
        collocates[window] = collocates[window].drop('Dice', axis=1)

    return collocates


# @anycache(CACHE_PATH)
def ccc_breakdown(corpus_name, cqp_bin, registry_path, data_path, lib_path,
                  topic_items, p_query='lemma', s_query=None, p_show=['lemma'],
                  flags_query='%cd', escape=True, flags_show=''):
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
    breakdown = dump.breakdown(p_show)

    # convert to dictionary
    out = list()
    for row in breakdown.iterrows():
        out.append({
            'item': row[0],
            'freq': int(row[1]['freq'])
        })

    return out


# @anycache(CACHE_PATH)
def ccc_meta(corpus_name, cqp_bin, registry_path, data_path, lib_path,
             topic_items, p_query='lemma', s_query=None,
             flags_query='%cd', s_show=['text_id'], order='first',
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


# @anycache(CACHE_PATH)
# TODO take care of caching for random order
def ccc_constellation_concordance(corpus_name, cqp_bin, registry_path,
                                  data_path, lib_path, discoursemes,
                                  p_query='lemma', s_query=None,
                                  flags_query='%cd', escape_query=True,
                                  s_context=None, context=None,
                                  p_show=['word', 'lemma'], s_show=['text_id'],
                                  order='random', cut_off=100):
    """get concordance lines for constellation.

    :param str corpus_name: name of corpus in CWB registry
    :param str cqp_bin: path to CQP binary
    :param str registry_path: path to CWB registry
    :param str data_path: path to data directory
    :param str lib_path: path to library (with macros and wordlists)

    :param dict discoursemes: {name: items}
    :param str p_query: p-att layer to query
    :param str s_query: s-att to use for delimiting queries
    :param str flags_query: flags to use for querying
    :param bool escape_query: whether to cqp-escape the query items

    :param str s_context: s-att to use for delimiting contexts
    :param int context: context around the nodes used to identify relevant matches

    :param list p_show: p-attributes to show
    :param list s_show: s-attributes to show
    :param str order: concordance order (first / last / random)
    :param int cut_off: number of lines to retrieve

    :return: dict of concordance lines (each one a dict, keys=1:N)
    :rtype: dict

    """

    corpus = Corpus(
        corpus_name=corpus_name,
        lib_path=lib_path,
        cqp_bin=cqp_bin,
        registry_path=registry_path,
        data_path=data_path
    )
    names = list(discoursemes.keys())
    topic = names[0]
    s_context = s_query if not s_context else s_context

    topic_name = topic
    topic_items = discoursemes.pop(topic_name)
    additional_discoursemes = discoursemes
    flags = flags_query
    escape = escape_query

    df = create_constellation(corpus_name, topic_name, topic_items,
                              p_query, s_query, flags, escape,
                              s_context, context,
                              additional_discoursemes,
                              lib_path, cqp_bin, registry_path, data_path,
                              match_strategy='longest',
                              dataframe=True, drop=False)

    # get relevant columns from constellation dataframe
    # NB: duplicate context-ids
    df = df.set_index('contextid')
    df_reduced = df[~df.index.duplicated(keep='first')][
        ['context', 'contextend']
    ]
    for name in ([topic] + list(discoursemes.keys())):
        columns = [m + '_' + name for m in ['offset', 'match', 'matchend']]
        df[name] = df[columns].values.tolist()
        df[name] = df[name].apply(tuple)
        df = df.drop(columns, axis=1)
        df_reduced[name] = df.groupby(['contextid'])[name].apply(
            lambda x: set([y for y in x if not isna(y[0])])
        )

    # repair context..contextend and use as match..matchend proxy
    df_reduced = df_reduced.drop(['context', 'contextend'], axis=1)
    context_spans = corpus.attributes.attribute(s_context, 's')
    tmp = DataFrame(df_reduced.index.map(lambda x: context_spans[x]).to_list())
    df_reduced['match'] = tmp[0].values
    df_reduced['matchend'] = tmp[1].values
    df_reduced = df_reduced.set_index(['match', 'matchend'])

    # retrieve concordance lines
    conc = Concordance(corpus.copy(), df_reduced)
    lines = conc.lines(form='dict', p_show=p_show, s_show=s_show,
                       order=order, cut_off=cut_off)
    names_bool = list()
    for name in ([topic] + list(discoursemes.keys())):
        name_bool = '_'.join(['BOOL', name])
        lines[name_bool] = lines[name].apply(lambda x: len(x) > 0)
        names_bool.append(name_bool)
    lines = list(lines.apply(
        lambda row: role_formatter(
            row, [topic] + list(discoursemes.keys()), s_show=names_bool+s_show, window=0
        ), axis=1
    ))

    # convert to HTML table
    # TODO: speed up!
    output = list()
    c = 0                       # random key (for sorting)
    for line in lines:
        c += 1
        meta = dict()
        for s in ['match'] + s_show:
            meta[s] = line.pop(s)
        line['word'] = ' '.join(line['word'])
        line['meta'] = DataFrame.from_dict(
            meta, orient='index'
        ).to_html(bold_rows=False, header=False)
        line['id'] = c
        output.append(line)

    return output


# @anycache(CACHE_PATH)
def ccc_constellation_association(corpus_name, cqp_bin, registry_path,
                                  data_path, lib_path, discoursemes,
                                  p_query='lemma', s_query=None,
                                  flags_query='%cd',
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

    # get names of topic and further discoursemes
    names = list(discoursemes.keys())
    topic = names[0]

    topic_name = topic
    topic_items = discoursemes.pop(topic_name)
    additional_discoursemes = discoursemes
    flags = flags_query
    escape = escape_query

    constellation = create_constellation(corpus_name, topic_name, topic_items,
                                         p_query, s_query, flags, escape,
                                         s_context, context,
                                         additional_discoursemes,
                                         lib_path, cqp_bin, registry_path, data_path,
                                         match_strategy='longest',
                                         text=True)

    tables = constellation.associations()

    out = list()
    for row in tables.iterrows():
        v = dict(row[1])
        out.append(v)

    return out
