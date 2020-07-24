#!/usr/bin/python3 -*- coding: utf-8 -*-
"""
Concordance and Collocation Calculation
"""

from ccc import Corpus
from ccc.discoursemes import Disc, DiscPos

import logging

logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO)
log = logging.getLogger('mmda-logger')


def get_concordance(corpus_name, topic_items, topic_name, s_context,
                    window_size, context=20,
                    additional_discoursemes=[], p_query='lemma',
                    p_show=['word', 'lemma'], s_show=['text_id'],
                    s_query=None, order='random', cut_off=100,
                    form='dataframes'):
    id2name = dict()

    if s_query is None:
        s_query = s_context

    corpus = Corpus(
        corpus_name
    )
    topic_disc = Disc(
        corpus,
        items=topic_items,
        p_query=p_query,
        s_query=s_query,
        s_context=s_context,
        context=context
    )
    id2name[topic_disc.idx] = topic_name
    if not additional_discoursemes:
        # single discourseme
        concordance = topic_disc.show_concordance(
            context,
            p_show=p_show,
            s_show=s_show,
            order=order,
            cut_off=cut_off,
            form=form
        )
    else:
        # discursive position
        dp = DiscPos(topic_disc)
        for key in additional_discoursemes.keys():
            idx = dp.add_items(additional_discoursemes[key])
            id2name[idx] = key

        concordance = dp.show_concordance(
            window=window_size,
            matches=None,
            p_show=p_show,
            s_show=s_show,
            order=order,
            cut_off=cut_off,
            form=form
        )

    # TODO: rename columns according to given names
    print(id2name)

    return concordance


def get_collocates(corpus_name, topic_items, s_context, window_size,
                   context=20, additional_discoursemes=[],
                   p_query='lemma', s_query=None, ams=None,
                   cut_off=200, order='log_likelihood'):

    if s_query is None:
        s_query = s_context

    corpus = Corpus(
        corpus_name
    )

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
        collocates = topic_disc.show_collocates(
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
        dp = DiscPos(topic_disc)
        for key in additional_discoursemes.keys():
            dp.add_items(additional_discoursemes[key])

        collocates = dp.show_collocates(
            window=window_size,
            order=order,
            cut_off=cut_off,
            p_query=p_query,
            ams=ams,
            min_freq=2,
            frequencies=False,
            flags=None
        )

    # drop superfluous columns
    collocates = collocates.drop(['in_nodes', 'marginal', 'N'], axis=1)

    return collocates
