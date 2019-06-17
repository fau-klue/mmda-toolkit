#!/usr/bin/python3 -*- coding: utf-8 -*-
"""
Concordance and Collocation Calculation
"""

import logging
import shelve
from hashlib import sha256
from pandas import DataFrame, merge
from association_measures import frequencies, measures
from collections import defaultdict, Counter
from random import sample


logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO)
LOGGER = logging.getLogger('mmda-logger')


class Cache:
    def __init__(self):
        self.path = '/tmp/mmda-cache'

    def get(self, key):
        with shelve.open(self.path) as db:
            try:
                return db[key]
            except KeyError:
                return None

    def set(self, key, value):
        with shelve.open(self.path) as db:
            db[key] = value


def create_identifier(*args):
    """
    Generate a hash from a string.

    :param args: arguments to use for identifier
    :return: hash for a given string
    :rtype: str
    """

    string = ' '.join([str(elem) for elem in args])
    return sha256(str(string).encode()).hexdigest()


# concordance ##################################################################
def _get_disc_positions(df_dp_nodes_loc):
    """ converts a local region into a dictionary of discourseme positions """
    disc_matches = defaultdict(list)
    for row in df_dp_nodes_loc.iterrows():
        disc_matches[row[1]['disc_match']].append(row[1]['disc_id'])
    return disc_matches


def _df_node_to_concordance(engine,
                            df_node,
                            window_size,
                            order,
                            cut_off,
                            p_query,
                            df_dp_nodes=None):
    """ retrieves concordances for a df_node and an optional df_dp_nodes """

    # avoid trying to get more concordances than there are
    if df_dp_nodes is not None:
        topic_matches = set(df_dp_nodes['topic_match'])
    else:
        topic_matches = set(df_node.index)
    if not cut_off:
        cut_off = len(topic_matches)
    elif len(topic_matches) < cut_off:
        cut_off = len(topic_matches)

    # take appropriate sub-set
    if order == 'random':
        topic_matches_cut = sample(topic_matches, cut_off)
    elif order == 'first':
        topic_matches_cut = sorted(list(topic_matches))[:cut_off]
    else:
        raise NotImplementedError("concordance order not implemented")

    # fill concordance dictionary
    concordance = dict()
    for topic_match in topic_matches_cut:

        # take values from row
        row = df_node.loc[topic_match]
        topic_matchend = row['matchend']
        s_start = row['s_start']
        s_end = row['s_end']

        # init concordance line variables
        role = list()
        offset = list()
        cpos = list()

        # check additional discourseme positions
        if df_dp_nodes is not None:
            disc_positions = _get_disc_positions(
                df_dp_nodes.loc[df_dp_nodes['topic_match'] == topic_match]
            )

        # fill variables
        for position in range(
                max([s_start, topic_match-window_size]),
                min([topic_matchend+window_size, s_end])+1
        ):
            # cpos
            cpos.append(position)

            # role: basic
            if position >= topic_match and position <= topic_matchend:
                r = ['topic']
            else:
                r = []
            # role: additional discourseme positions
            if df_dp_nodes is not None:
                if position in disc_positions.keys():
                    r = r + disc_positions[position]
            role.append(r)

            # offset
            if position < topic_match:
                offset.append(position - topic_match)
            elif position > topic_matchend:
                offset.append(position - topic_matchend)
            else:
                offset.append(0)

        # lexicalize positions
        word = engine.lexicalize_positions(cpos)
        p_query_items = engine.lexicalize_positions(cpos, p_query)

        # save concordance line
        concordance[topic_match] = DataFrame(
            index=cpos,
            data={
                'word': word,
                'role': role,
                'offset': offset,
                'p_query': p_query_items
            }
        )

    return concordance


def _cut_conc(concordance, window):
    """ input: match-keyed dictionary of concordance-dfs
    output: list of concordances (json) for given window """
    conc_lines = list()
    for match in concordance.keys():
        df_conc = concordance[match]

        # give new roles to positions outside region defined by window
        df_conc.loc[(df_conc['offset'] < -window) | (df_conc['offset'] > +window), 'role'] = 'out_of_window'

        # jsonify
        conc_line = dict()
        conc_line['p_query'] = list(df_conc['p_query'])
        conc_line['word'] = list(df_conc['word'])
        conc_line['role'] = [k if k != 'out_of_window' else [k] for k in df_conc['role']]
        conc_line['match_pos'] = match

        # append
        conc_lines.append(conc_line)

    return conc_lines


# slicing discoursemes #########################################################
def _calculate_offset(row):
    """ calculates appropriate offset of y considering match and matchend of x """
    match_x = row['match_x']
    matchend_x = row['matchend_x']
    match_y = row['match_y']
    if match_x > match_y:
        offset = match_y - match_x
    elif matchend_x < match_y:
        offset = match_y - matchend_x
    else:
        offset = 0
    return offset


def _combine_df_nodes_single(df_nodes_single_dict):
    """ combines a dictionary of single df_nodes into df_dp_nodes """
    # only take relevant topic_matches
    relevant_topic_matches = set.intersection(
        *[set(r['topic_match']) for r in df_nodes_single_dict.values()]
    )

    # init output
    df_dp_nodes = DataFrame()
    for idx in df_nodes_single_dict:
        # get relevant subset of df_node of discourseme
        df_node = df_nodes_single_dict[idx].copy()
        df_node = df_node[df_node['topic_match'].isin(relevant_topic_matches)]
        df_node['disc_id'] = idx
        # add to df_dp_nodes
        df_dp_nodes = df_dp_nodes.append(df_node)
    return df_dp_nodes


def slice_discourseme_topic(topic_df_node, disc_df_node, window_size):
    """ combines df_node of a discourseme with topic df_node """
    df_topic = topic_df_node
    df_topic['match'] = df_topic.index  # move match from index to column
    df_disc = disc_df_node  # positions occupied by discourseme in corpus
    df_disc['match'] = df_disc.index  # move match from index to column
    df_single_nodes = merge(topic_df_node, disc_df_node, on="s_start")
    df_single_nodes = df_single_nodes[['match_x', 'matchend_x', 'match_y']]
    df_single_nodes['disc_offset'] = df_single_nodes.apply(_calculate_offset, axis=1)

    df_single_nodes.columns = ['topic_match',
                               'topic_matchend',
                               'disc_match',
                               'disc_offset']
    df_single_nodes = df_single_nodes[abs(df_single_nodes['disc_offset']) <= window_size]
    return df_single_nodes


def slice_discoursemes_topic(topic_df_node,
                             topic_match_pos_set,
                             disc_df_node_dict,
                             window_size):
    """ combines df_nodes of several discoursemes with topic df_node """
    df_topic = topic_df_node
    df_topic['match'] = df_topic.index  # move match from index to column

    dfs_single_nodes_dict = dict()
    nodes_match_pos = topic_match_pos_set
    for idx in disc_df_node_dict.keys():
        df_disc = disc_df_node_dict[idx]
        disc_match_pos_set = set(df_disc.index)
        dfs_single_nodes_dict[idx] = slice_discourseme_topic(
            df_topic,
            df_disc,
            window_size
        )
        nodes_match_pos = nodes_match_pos.union(disc_match_pos_set)  # book-keeping
    df_dp_nodes = _combine_df_nodes_single(dfs_single_nodes_dict)
    return df_dp_nodes, nodes_match_pos


# nodes to cooc ################################################################
def _df_node_to_df_cooc(df_node,
                        max_window_size):
    """ converts a (topic) df_node to df_cooc """
    # fill cooc lists
    match_list = list()
    cpos_list = list()
    offset_list = list()
    match_pos_set = set()                      # match-positions for book-keeping
    for row in df_node.iterrows():

        # take values from row
        match = row[0]
        matchend = row[1]['matchend']
        s_start = row[1]['s_start']
        s_end = row[1]['s_end']

        # fill variables
        for position in range(
                max([s_start, match-max_window_size]),
                min([matchend+max_window_size, s_end])+1
        ):
            if position < match:
                match_list.append(match)
                cpos_list.append(position)
                offset_list.append(position - match)
            elif position > matchend:
                match_list.append(match)
                cpos_list.append(position)
                offset_list.append(position - matchend)
            else:
                match_pos_set.add(position)

    # concatenate to dataframe
    df_cooc = DataFrame({
        'match': match_list,
        'cpos': cpos_list,
        'offset': offset_list
    })
    # drop node positions
    df_cooc = df_cooc[~df_cooc['cpos'].isin(match_pos_set)]

    return df_cooc, match_pos_set


def _df_dp_nodes_to_cooc(topic_df_cooc, df_dp_nodes):
    """ creates global df cooc from the topic_df_cooc and the df_dp_nodes """

    # drop irrelevant topic matches
    df_cooc_glob = topic_df_cooc[
        topic_df_cooc['match'].isin(set(df_dp_nodes['topic_match']))
    ]
    # drop all discourseme positions
    df_cooc_glob = df_cooc_glob[
        ~df_cooc_glob['cpos'].isin(set(df_dp_nodes['disc_match']))
    ]
    return df_cooc_glob


# cooc to counts ###############################################################
def df_cooc_to_counts(engine,
                      p_query,
                      df_cooc,
                      window,
                      drop_hapaxes=True):
    """ get window counts of a df_cooc for given window size """

    # slice relevant window
    relevant = df_cooc.loc[abs(df_cooc['offset']) <= window]
    relevant = relevant.drop_duplicates('cpos')

    # number of possible occurence positions within window
    f1_inflated = len(relevant)

    # lexicalize positions
    lex_items = engine.lexicalize_positions(
        relevant['cpos'],
        p_query
    )

    # the co-occurrence counts in the window
    counts = Counter(lex_items)
    counts = DataFrame.from_dict(counts, orient='index')
    counts.columns = ["O11"]

    # drop hapax legomena for improved performance
    if drop_hapaxes:
        counts = counts[~counts['O11'] <= 1]

    return counts, f1_inflated


# reference frequencies ########################################################
def get_reference_freq(engine, items, p_query, reference='whole'):
    """ gets the reference frequencies for a list of items """
    if reference == 'whole':
        f2, N = engine.get_marginals(items, p_query)
    else:
        raise NotImplementedError('reference method not implemented')

    return f2, N


# counts to contingencies ######################################################
def counts_to_contingencies(counts, f1, f1_inflated, f2, N):
    """ window counts + marginals to contingency table"""

    # create contingency table
    N_deflated = N - f1
    contingencies = counts
    contingencies = contingencies.join(f2)
    contingencies['N'] = N_deflated
    contingencies['f1'] = f1_inflated
    return contingencies


def add_ams(contingencies):
    """ annotates a contingency table with AM information """
    # rename for convenience
    df = contingencies

    # create the contigency table with the observed frequencies
    df['O11'], df['O12'], df['O21'], df['O22'] = frequencies.observed_frequencies(df)
    # create the indifference table with the expected frequencies
    df['E11'], df['E12'], df['E21'], df['E22'] = frequencies.expected_frequencies(df)

    # calculate all association measures
    collocates = measures.calculate_measures(df)
    collocates = df

    return collocates


# CCC wrapper ##################################################################
class ConcordanceCollocationCalculator():
    """
    Hint: all functions with 'retrieve' call the engine
    """

    def __init__(self, analysis_settings, engine):

        self.analysis = analysis_settings
        self.engine = engine
        self.cache = Cache()

    def _retrieve_discourseme_dfs(self, items):
        """
        calls engine to get df_node, transforms to df_cooc (+f1 positions)
        """

        df_node = self.engine.prepare_df_node(
            self.analysis.p_query,
            self.analysis.s_break,
            items
        )
        df_cooc, match_pos = _df_node_to_df_cooc(
            df_node, self.analysis.window_size
        )
        return df_node, df_cooc, match_pos

    def _retrieve_concordance(self,
                              df_node,
                              df_dp_nodes=None,
                              order='random',
                              cut_off=100):
        """
        retrieves concordance lines from the corpus engine
        """
        concordance = _df_node_to_concordance(
            self.engine,
            df_node,
            self.analysis.window_size,
            order,
            cut_off,
            self.analysis.p_query,
            df_dp_nodes
        )
        return concordance

    def _retrieve_collocates(self, df_cooc, f1):

        # get discourseme contingencies
        collocates = dict()

        # get contingencies
        for window in range(1, self.analysis.window_size + 1):
            counts, f1_inflated = df_cooc_to_counts(
                self.engine,
                self.analysis.p_query,
                df_cooc,
                window
            )
            f2, N = get_reference_freq(self.engine,
                                       counts.index,
                                       self.analysis.p_query,
                                       reference='whole')
            contingencies = counts_to_contingencies(
                counts, f1, f1_inflated, f2, N
            )
            collocates[window] = add_ams(contingencies)

        return collocates

    def _get_df_node(self, items):

        identifier = create_identifier(self.engine, self.analysis, items, 'df_node')
        cached_data = self.cache.get(identifier)
        if cached_data is None:
            df_node = self.engine.prepare_df_node(
                self.analysis.p_query,
                self.analysis.s_break,
                items
            )
            self.cache.set(identifier, df_node)
        else:
            df_node = cached_data
        return df_node

    def _get_discourseme_data(self, identifier, items):
        """
        Extracts data from cache or from engine and then puts it into cache.
        """

        # if cache returns none, it ain't no tuple!
        cached_data = self.cache.get(identifier)
        if isinstance(cached_data, tuple):
            df_node, df_cooc, match_pos = cached_data
        else:
            # TODO: Get Items from discourseme
            df_node, df_cooc, match_pos = self._retrieve_discourseme_dfs(items)
            self.cache.set(identifier, (df_node, df_cooc, match_pos))

        return df_node, df_cooc, match_pos

    def extract_concordances(self,
                             topic_discourseme,
                             discoursemes=None,
                             concordance_settings=None,
                             per_window=False):

        if concordance_settings is None:
            concordance_settings = {
                'order': 'random',
                'cut_off': 10
            }

        # extract data from cache or engine
        identifier = create_identifier(self.engine, self.analysis,
                                       topic_discourseme.items,
                                       'df_node, df_cooc, math_pos')
        df_node, df_cooc, match_pos = self._get_discourseme_data(
            identifier, topic_discourseme.items
        )

        # monkey patch stuff to discourseme
        topic_discourseme.df_cooc = df_cooc
        topic_discourseme.df_node = df_node
        topic_discourseme.match_pos = match_pos

        # concordance of topic_discourseme
        if not discoursemes:
            concordance = _df_node_to_concordance(
                self.engine,
                topic_discourseme.df_node,
                self.analysis.window_size,
                concordance_settings['order'],
                concordance_settings['cut_off'],
                self.analysis.p_query
            )

        # concordance of discursive position
        else:
            disc_df_dict = dict()
            for discourseme in discoursemes:
                disc_df_node = self._get_df_node(
                    discourseme.items
                )
                disc_df_dict[discourseme.id] = disc_df_node

            df_dp_nodes, match_pos_set = slice_discoursemes_topic(
                topic_discourseme.df_node,
                topic_discourseme.match_pos,
                disc_df_dict,
                self.analysis.window_size
            )

            concordance = _df_node_to_concordance(
                self.engine,
                topic_discourseme.df_node,
                self.analysis.window_size,
                concordance_settings['order'],
                concordance_settings['cut_off'],
                self.analysis.p_query,
                df_dp_nodes
            )

        if per_window:
            concordance_dict = dict()
            for window in range(1, self.analysis.window_size + 1):
                concordance_dict[window] = _cut_conc(concordance, window)
            concordance = concordance_dict

        return concordance

    def extract_collocates(self,
                           topic_discourseme,
                           discoursemes=None,
                           collocates_settings=None):

        if collocates_settings is None:
            collocates_settings = {
                'order': 'O11',
                'cut_off': 10
            }

        # extract data from cache or engine
        identifier = create_identifier(self.engine, self.analysis,
                                       topic_discourseme.items,
                                       'df_node, df_cooc, match_pos')
        df_node, df_cooc, match_pos = self._get_discourseme_data(
            identifier, topic_discourseme.items
        )

        # monkey patch stuff to discourseme
        topic_discourseme.df_cooc = df_cooc
        topic_discourseme.df_node = df_node
        topic_discourseme.match_pos = match_pos

        # collocates of topic_discourseme
        if not discoursemes:
            collocates = self._retrieve_collocates(df_cooc, len(match_pos))

        # collocates of discursive position
        else:
            disc_df_dict = dict()
            for discourseme in discoursemes:
                disc_df_node = self._get_df_node(
                    discourseme.items
                )
                disc_df_dict[discourseme.id] = disc_df_node

            df_dp_nodes, match_pos_set = slice_discoursemes_topic(
                topic_discourseme.df_node,
                match_pos,
                disc_df_dict,
                self.analysis.window_size
            )

            df_cooc_glob = _df_dp_nodes_to_cooc(
                topic_discourseme.df_cooc,
                df_dp_nodes
            )

            collocates = self._retrieve_collocates(
                df_cooc_glob, len(match_pos_set)
            )

        # ToDo: give cut_off to engine for better performance
        for window in range(1, self.analysis.window_size + 1):
            # select relevant window
            coll = collocates[window]
            # sort deterministically
            coll.sort_values(
                by=[collocates_settings['order'], 'f2'],
                ascending=[False, True],
                inplace=True
            )
            collocates[window] = coll.head(collocates_settings['cut_off'])

        return collocates
