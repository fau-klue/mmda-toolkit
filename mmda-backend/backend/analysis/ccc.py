#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Concordance and Collocation Computation
"""

from ccc import Corpus
from ccc.discoursemes import Disc, DiscCon
from collections import defaultdict

import logging

logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO)
log = logging.getLogger('mmda-logger')


def get_concordance(corpus_name, topic_items, topic_name, s_context,
                    window_size, context=20,
                    additional_discoursemes=[], p_query='lemma',
                    p_show=['word', 'lemma'], s_show=['text_id'],
                    s_query=None, order='random', cut_off=100,
                    form='dataframes'):

    if s_query is None:
        s_query = s_context

    # init corpus
    corpus = Corpus(corpus_name)

    # init topic discourseme
    topic_disc = Disc(
        corpus,
        items=topic_items,
        p_query=p_query,
        s_query=s_query,
        s_context=s_context,
        context=context
    )

    # init discourseme constellation
    dp = DiscCon(topic_disc)

    # id2name: mapper from ccc cache names to discourseme names
    id2name = {
        topic_disc.idx: topic_name
    }

    # add discoursemes to discourseme constellation
    for key in additional_discoursemes.keys():
        idx = dp.add_items(additional_discoursemes[key])
        id2name[idx] = key

    # extract concordance
    concordance = dp.concordance(
        window=window_size,
        matches=None,
        p_show=p_show,
        s_show=s_show,
        order=order,
        cut_off=cut_off,
        form=form
    )

    if concordance.empty:
        return None

    # convert each concordance line to dictionary, create roles
    # TODO: implement as form='json' in cwb-ccc
    concordance = concordance.reset_index()
    ret = dict()
    for idx, df in zip(concordance['match'], concordance['df']):

        # rename columns according to given names for discoursemes
        df = df.rename(columns=id2name)

        # get roles as dict
        roles = defaultdict(list)
        for cpos, row in df.iterrows():
            for col_name in id2name.values():
                if row[col_name]:
                    # TODO: propagate proper info about discourseme names
                    if col_name == topic_name:
                        roles[cpos].append('topic')
                    else:
                        roles[cpos].append('collocate')
                else:
                    roles[cpos].append(None)

        ret[idx] = {
            'word': list(df['word']),    # list of words
            p_query: list(df[p_query]),  # secondary p-att
            'role': list(roles.values())  # roles
        }

    return ret


def get_collocates(corpus_name, topic_items, s_context, window_size,
                   context=20, additional_discoursemes=[],
                   p_query='lemma', s_query=None, ams=None,
                   cut_off=200, order='log_likelihood'):

    if s_query is None:
        s_query = s_context

    corpus = Corpus(corpus_name)

    topic_disc = Disc(
        corpus,
        items=topic_items,
        p_query=p_query,
        s_query=s_query,
        s_context=s_context,
        context=context
    )

    if not additional_discoursemes:
        # single discourseme
        collocates = topic_disc.collocates(
            window=window_size,
            order=order,
            cut_off=cut_off,
            p_query=p_query,
            ams=ams,
            min_freq=2,
            frequencies=False,
            flags=None
        )
    else:
        # discursive position
        dp = DiscCon(topic_disc)
        for key in additional_discoursemes.keys():
            dp.add_items(additional_discoursemes[key])

        collocates = dp.collocates(
            window=window_size,
            order=order,
            cut_off=cut_off,
            p_query=p_query,
            ams=ams,
            min_freq=2,
            frequencies=False,
            flags=None
        )

    # drop superfluous columns and sort
    collocates = collocates[[
        'f',
        'f2',
        'log_likelihood',
        'log_ratio',
        'mutual_information',
        'z_score',
        't_score'
    ]]

    # rename AMs
    am_dict = {
        'log_likelihood': 'log-likelihood',
        'f': 'co-oc. freq.',
        'mutual_information': 'mutual information',
        'log_ratio': 'log-ratio',
        'f2': 'marginal freq.',
        't_score': 't-score',
        'z_score': 'z-score'
    }
    collocates = collocates.rename(am_dict, axis=1)
    print(collocates)

    return collocates
