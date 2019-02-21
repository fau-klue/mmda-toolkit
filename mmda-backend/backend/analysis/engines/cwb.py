"""
Corpus Workbench Engine
"""

from subprocess import Popen, PIPE, run, TimeoutExpired
from logging import getLogger
from os import getenv
from re import search
import xml.etree.ElementTree as ET
from random import shuffle
from pandas import DataFrame
from .engine import Engine
from .engine import Collocates


LOGGER = getLogger('mmda-logger')
# TODO: How can we set this in the settings.py?
REGISTRY_PATH = getenv(
    'MMDA_CQP_REGISTRY',
    default='/usr/local/cwb-3.4.13/share/cwb/registry'
)


def evaluate_cqp_query(corpus_name, cmd):
    """
    Lets CQP evaluate a command via Popen.

    :param str corpus_name: corpus to be queried
    :param str cmd: CQP command
    :return: decoded return value of CQP
    :rtype: str
    """

    start_cqp = [
        'cqp',
        '-c',
        '-r',
        REGISTRY_PATH,
        '-D',
        corpus_name.upper()
    ]

    cqp_process = Popen(start_cqp,
                        stdin=PIPE,
                        stdout=PIPE,
                        stderr=PIPE)

    try:
        cqp_return = cqp_process.communicate(cmd.encode())[0]
    except Exception:
        LOGGER.error('Error during execution of CQP command')
        return ''

    return cqp_return.decode()


def evaluate_ucs_query(corpus_name, ucs_cmd, add_cmd):
    """
    Lets UCS evalutate a command via Popen.

    :param str corpus_name: corpus to be queried
    :param str cmd: query to be used
    """

    try:
        ucs_process = Popen(ucs_cmd, stdout=PIPE)
        add_process = run(add_cmd,
                          stdin=ucs_process.stdout,
                          stdout=PIPE,
                          stderr=PIPE,
                          timeout=300)

    except TimeoutExpired:
        LOGGER.error('Error during ucs-add. Timeout during query.')
        return ''
    except Exception:  # pylint: disable=broad-except
        LOGGER.error('Error during ucs-add.')
        return ''

    ucs_return = add_process.stdout

    # error handling for UCS toolkit
    if len(ucs_return) == 0:
        LOGGER.error('Collocation extraction failed. Empty return for UCS query.')
        return ''

    return ucs_return.decode()


###############
# CQP QUERIES #
###############

def create_cqp_query_from_items(items, p_att):
    """
    Creates CQP query from item-list

    :param list items: user input in interface (list of tokens)
    :parm p_att str: p-attribute to query
    :return: CQP query as string
    :rtype: str
    """

    query = '[{p_att}="{items}"]'.format(p_att=p_att, items='|'.join(items))

    return query


def create_topic_discourseme_query(topic_items,
                                   discourseme_items,
                                   p_att,
                                   s_att):
    """
    Creates CQP query for a discourseme given a topic.
    Uses MU to determine s_att-areas that contain both.

    :param str topic_items: topic items
    :param str discourseme_items: discourseme items
    :param str p_att: p-attribute to query (typically 'lemma')
    :param str s_att: s-attribute where to break (typically 's' or 'tweet')
    :return: topic-discourseme CQP query as string
    :rtype: str
    """

    query = 'MU (meet {discourseme_query} {topic_query} {s_att})'

    query = query.format(
        discourseme_query=create_cqp_query_from_items(discourseme_items, p_att),
        topic_query=create_cqp_query_from_items(topic_items, p_att),
        s_att=s_att
    )

    return query


def create_topic_discourseme_query_window(topic_items,
                                          discourseme_items,
                                          p_att,
                                          s_att,
                                          window_size):
    """
    Creates CQP query for a discourseme given a topic.
    Includes window_size breaks.

    :param str topic_items: topic items
    :param str discourseme_items: discourseme items
    :param str p_att: p-attribute to query (typically 'lemma')
    :param str s_att: s-attribute where to break (typically 's' or 'tweet')
    :return: topic-discourseme CQP query as string
    :rtype: str
    """
    query = '(({topic_query} []{{,{ws}}} @{discourseme_query}) ' +\
            '| (@{discourseme_query} []{{,{ws}}} {topic_query})) ' +\
            'within {s_att}'
    query = query.format(
        discourseme_query=create_cqp_query_from_items(discourseme_items, p_att),
        topic_query=create_cqp_query_from_items(topic_items, p_att),
        s_att=s_att,
        ws=window_size
    )

    return query


################
# CONCORDANCES #
################

def cqp_concordances(corpus_name,
                     s_att,
                     p_att,
                     topic_items,
                     window_size,
                     discourseme_items=None):
    """
    Uses CQP to get concordances for a given list of topic items.
    Optional discourseme items.

    :param str corpus_name: corpus to be queried
    :param str s_att: s-attribute where to break (typically 's' or 'tweet')
    :param str p_att: p-attribute to be queried (typically 'lemma')
    :param list topic_items: list of topic items
    :param int window_size: window size used in extraction
    :param list discourseme_items: optional list of discourseme items
    :return: tuple of raw concordance strings (words + queried p-attribute)
    :rtype: tuple
    """

    # cqp settings
    cqp_settings = 'set PrintOptions hdr;' +\
                   'set ShowTagAttributes on;' +\
                   'set PrintMode sgml;' +\
                   'set Context 1 {s_att};'
    cqp_settings = cqp_settings.format(
        s_att=s_att
    )

    if p_att != "word":
        cqp_settings_p_att = 'set PrintOptions hdr;' +\
                   'set ShowTagAttributes on;' +\
                   'set PrintMode sgml;' +\
                   'set Context 1 {s_att};' +\
                   'show -word +{p_att};'
        cqp_settings_p_att = cqp_settings_p_att.format(
            p_att=p_att,
            s_att=s_att
        )

    # retrieve topic concordances if no discourseme items are provided
    if discourseme_items is None:
        cqp_exec = 'A = {query}; cat A;'
        cqp_exec = cqp_exec.format(
            query=create_cqp_query_from_items(topic_items, p_att)
        )

    # retrieve topic-discourseme concordances
    elif isinstance(discourseme_items, list):
        cqp_exec = 'A = {query}; cat A;'
        cqp_exec = cqp_exec.format(
            query=create_topic_discourseme_query_window(
                topic_items,
                discourseme_items,
                p_att,
                s_att,
                window_size
            )
        )

    # raise an Error if discourseme items are not a list
    else:
        LOGGER.error('discourseme items are not a list')
        raise TypeError('discourseme items are not a list')

    # get raw concordances
    concordances_raw = evaluate_cqp_query(
        corpus_name,
        cqp_settings + cqp_exec
    )
    # get concordances of queried p-attribute
    if p_att != "word":
        concordances_p_att = evaluate_cqp_query(
            corpus_name,
            cqp_settings_p_att + cqp_exec
        )
    else:
        concordances_p_att = concordances_raw

    # give back the raw concordances
    return concordances_raw, concordances_p_att


##################
# CQP formatting #
##################

def _process_simple_match(match):
    # matches have the tokens as children
    match_tokens = list()
    match_roles = list()
    for match_child in match.getchildren():
        match_tokens.append(match_child.text)
        match_roles.append('topic')
    return match_tokens, match_roles


def _process_complex_match(match):
    # matches consist of tokens and collocates
    match_tokens = list()
    match_roles = list()
    for match_child in match.getchildren():
        # tokens only have a text element
        if match_child.tag == 'TOKEN':
            match_roles.append('token')
            match_tokens.append(match_child.text)
        # collocates have the tokens as children
        elif match_child.tag == 'COLLOCATE':
            for token in match_child.getchildren():
                match_roles.append('collocate')
                match_tokens.append(token.text)

    # either the first or last element of the match is the topic
    # TODO: doesn't work for multiple topic hits
    if match_roles[0] == 'token':
        match_roles[0] = 'topic'
    elif match_roles[-1] == 'token':
        match_roles[-1] = 'topic'

    return match_tokens, match_roles


def _process_match(match, simple):
    # TODO solve case differentiation
    if simple:
        return _process_simple_match(match)
    else:
        return _process_complex_match(match)


def format_cqp_concordances(cqp_return, cut_off, order, simple=True):
    # TODO: Add docstring

    if order != 'first':
        raise NotImplementedError('can only format first "cut_off" concordances from CWB')

    # init output
    lines = dict()

    # loop through CQP return value
    for line in str(cqp_return).split("\n"):

        # get p_attribute
        t = search('<attribute type=positional name="(\w+)" anr=0>', line)
        if t:
            p_att = t.group(1)

        # get number of concordances
        t = search("<subcorpusInfo size=(\d+)>", line)
        if t:
            size = t.group(1)
            if int(size) > cut_off:
                LOGGER.warning('only %d values will be retrieved' % cut_off)

        # process concordances lines
        if line.startswith("<LINE>"):

            # rows contain MATCHNUM[0] and CONTENT[1]
            row = ET.fromstring(line)
            matchnum = row[0].text
            tokens = list()
            roles = list()

            # CONTENT contains TOKENs and MATCHes
            for child in row[1].getchildren():

                # TOKENs only have one text element
                if child.tag == 'TOKEN':
                    roles.append('token')
                    tokens.append(child.text)

                elif child.tag == 'MATCH':
                    # TODO get rid of case-folding for MATCH
                    match_tokens, match_roles = _process_match(child, simple)
                    # append tokens and roles of match
                    tokens += match_tokens
                    roles += match_roles

            # save concordance line
            lines[matchnum] = {
                p_att: tokens,
                'role': roles
            }

            # TODO
            if len(lines) >= cut_off:
                break

    return lines


def merge_concordances(conc1, conc2):
    # TODO: Add docstring
    for s_pos in conc1.keys():
        if s_pos in conc1.keys():
            for key in (set(conc2[s_pos].keys()) - set(conc1[s_pos].keys())):
                conc1[s_pos][key] = conc2[s_pos][key]
        else:
            LOGGER.warning("concordances don't overlap")

    return conc1


def sort_concordances(concordances, order='random'):
    """
    Shuffles concordance dictionary
    Returns shuffled list
    """

    if order != 'random':
        raise NotImplementedError('can only shuffle formatted concordances')

    shuffled_concordances = list()
    shuffled_keys = list(concordances.keys())
    shuffle(shuffled_keys)

    for key in shuffled_keys:
        conc = concordances[key]
        conc['s_pos'] = key
        shuffled_concordances.append(conc)

    return shuffled_concordances


##############
# COLLOCATES #
##############

def ucs_collocates(corpus_name,
                   s_att,
                   p_att,
                   topic_items,
                   window_size,
                   assoc_measures,
                   discourseme_items=None):

    # create the UCS commands
    ucs_cmd, ucs_add = create_ucs_query(corpus_name,
                                        topic_items,
                                        p_att,
                                        window_size,
                                        s_att,
                                        assoc_measures,
                                        discourseme_items)

    # get collocates
    collocates_raw = evaluate_ucs_query(corpus_name, ucs_cmd, ucs_add)

    return collocates_raw


def create_ucs_query(corpus_name,
                     topic_items,
                     p_att,
                     window_size,
                     s_att,
                     assoc_measures,
                     discourseme_items=None):
    """
    Compiles a UCS query to be executed by Popen.
    Either with or without discourseme collocates.

    :param str corpus_name: corpus to be queried
    :param list topic_items: topic items
    :param str p_att: p-attribute to query
    :param str window_size: window size for collocate retrieval
    :param str s_att: s-attribute where to break (typically 's' or 'tweet')
    :param list discourseme_items: (optional) collocate group for discourseme collocates
    :return: UCS command as list
    :rtype: list
    """

    if isinstance(discourseme_items, list) and len(discourseme_items) > 1:
        if window_size:
            LOGGER.info('Window size will be ignored while retrieving discourse collocates.')
        # Retrieve topic-discourseme collocates
        query = create_topic_discourseme_query(topic_items, discourseme_items, p_att, s_att)
    else:
        # Retrieve topic collocates if no discourseme items are provided
        query = create_cqp_query_from_items(topic_items, p_att)

    # Create UCS command as list for system call
    ucs_cmd = [
        "ucs-tool",
        "surface-from-cwb-query",
        "-q",
        "-S",
        str(s_att),
        "-w",
        str(window_size),
        "-nh",
        "-r",
        REGISTRY_PATH,
        "-ca",
        str(p_att),
        "-M",
        # cache marginal frequencies
        "/tmp/mmda_marginals_{corpus}_lemma.gz".format(corpus=corpus_name),
        # drop hapax co-occurrences for improved performance
        "-f", "1",
        str(corpus_name),
        "-",
        "{query}".format(query=query),
        # so queries matching multiple words or phrases are treated
        # as a single node type (requires UCS revision >= r41)
        'NODE'
    ]

    # Create query
    add_cmd = ["ucs-add"] + assoc_measures

    LOGGER.debug("UCS pipe:  " + " ".join(ucs_cmd) + " | " + " ".join(add_cmd))

    return ucs_cmd, add_cmd


def format_ucs_collocates(ucs_return, assoc_measures, cut_off, order):
    """
    Adds association measures to data from ucs_tool_collocates.

    :param pandas.DataFrame data: DataFrame to transform (contains f1, N, l2, O11)
    :param list association_measures: association measures to use
    :return: tuple of DataFrame with added association measures, f1, and N
    :rtype: tuple
    """

    data = ucs_return.split('\n')
    if len(data) < 3:
        return DataFrame(), 0, 0

    # Last element is None because return string ends with \n
    data = [row.split('\t') for row in data[:-1]]
    collocates = DataFrame(data=data[1:], columns=data[0])

    f1 = int(collocates['f1'][0])
    N = int(collocates['N'][0])

    collocates.index = collocates['l2']
    collocates.index.name = 'item'

    collocates = collocates[['f2', 'f'] + assoc_measures]
    collocates.columns = ['f2', 'O11'] + assoc_measures

    collocates.sort_values(by=order, ascending=False)
    collocates = collocates.head(cut_off)

    return collocates, f1, N


##########
# ENGINE #
##########

class CWBEngine(Engine):
    """
    Corpus Workbench Engine Class.
    """

    def extract_collocates(self,
                           items,
                           window_size,
                           collocates=None,
                           cut_off=100,
                           order='f2'):
        """
        Extract collocates from a CWB corpus.
        See BaseClass for parameters.
        """

        # extract collocates with UCS toolkit
        collocates_raw = ucs_collocates(
            corpus_name=self.corpus_name,
            assoc_measures=self.corpus_settings['association_measures'],
            s_att=self.corpus_settings['s_att'],
            p_att=self.corpus_settings['p_att'],
            topic_items=items,
            window_size=window_size,
            discourseme_items=collocates
        )

        # format collocates
        collocates, f1, N = format_ucs_collocates(
            ucs_return=collocates_raw,
            assoc_measures=self.corpus_settings['association_measures'],
            cut_off=cut_off,
            order=order
        )

        return Collocates(data=collocates, f1=f1, N=N)

    def extract_concordances(self,
                             items,
                             window_size,
                             collocates=None,
                             cut_off=100,
                             order='random'):
        """
        Extract concordances from a CWB indexed corpus.
        See BaseClass for parameters.
        """

        # extract concordances with CWB CQP
        concordances_raw, concordances_p = cqp_concordances(
            corpus_name=self.corpus_name,
            s_att=self.corpus_settings['s_att'],
            p_att=self.corpus_settings['p_att'],
            topic_items=items,
            window_size=window_size,
            discourseme_items=collocates
        )

        # error handling for CWB
        if not concordances_raw or not concordances_p:
            LOGGER.error(
                'Concordance extraction failed. Empty return for CQP query.'
            )
            LOGGER.debug(items)
            raise ValueError(
                'Concordance extraction failed. Empty return for CQP query.'
            )

        if collocates:
            concordances_raw = format_cqp_concordances(
                cqp_return=concordances_raw,
                cut_off=cut_off,
                order='first',
                simple=False
            )
            concordances_p = format_cqp_concordances(
                cqp_return=concordances_p,
                cut_off=cut_off,
                order='first',
                simple=False
            )
        else:
            concordances_raw = format_cqp_concordances(
                cqp_return=concordances_raw,
                cut_off=cut_off,
                order='first',
                simple=True
            )
            concordances_p = format_cqp_concordances(
                cqp_return=concordances_p,
                cut_off=cut_off,
                order='first',
                simple=True
            )

        concordances = merge_concordances(
            concordances_raw,
            concordances_p
        )

        # sort concordances
        concordances = sort_concordances(concordances, order)
        return concordances
