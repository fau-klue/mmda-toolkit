"""
Corpus Workbench Engine
"""


from copy import deepcopy
from subprocess import Popen, PIPE, run, TimeoutExpired
from logging import getLogger
from os import getenv
from re import sub, search, escape
from random import shuffle
from pandas import DataFrame
from .engine import Engine
from .engine import Collocates


LOGGER = getLogger('mmda-logger')
# TODO: How can we set this in the settings.py?
REGISTRY_PATH = getenv('MMDA_CQP_REGISTRY', default='/usr/local/cwb-3.4.13/share/cwb/registry')


def create_cqp_query(query):
    """
    Return original query (if input starts with '[', assuming it is a correct CQP query)
    or transforms simple input query (i.e. single word) into a CQP query.

    :param str query: user input in interface.
    :return: CQP query as string.
    :rtype: str
    """

    # If the query starts with [ we assume it's a correct CQP query
    if query.startswith("["):
        return query

    return '[word = "{}" %c]'.format(query)


def create_discourse_query(topic_query, s_break, collocates):
    """
    Creates CQP query for a discourse.

    :param str topic_query: original topic query.
    :param str s_break: s-attribute where to break (typically 's' or 'tweet').
    :param list collocates: list of lemmas (discourseme).
    :return: discourse CQP query as string.
    :rtype: str
    """

    topic_query = create_cqp_query(topic_query)

    # Create CQP command from list of collocates
    collocate_group = list()
    for coll in collocates:
        collocate_group.append('lemma = "{coll}"'.format(coll=coll))

    collocate_group = " | ".join(collocate_group)

    # Create full CQP query
    query = 'MU (meet [{collocate_group}] {topic_query} {br})'.format(
        topic_query=topic_query,
        collocate_group=collocate_group,
        br=s_break)

    return query


def start_cqp_command(corpus_name):
    """
    Creates a CQP command to be executed by Popen.

    :param str corpus_name: Corpus to be queried.
    :return: CQP command as list.
    :rtype: list
    """

    return [
        'cqp',
        '-c',
        '-r',
        REGISTRY_PATH,
        '-D',
        corpus_name.upper()
    ]


def make_ucs_command(corpus_name,
                     topic_query,
                     window_size,
                     s_break,
                     collocates=None):
    """
    Compiles a ucs-tool command to be executed by Popen. Either with or without discourse collocates.

    :param str corpus_name: Corpus to be queried.
    :param str window_size: window size for collocate retrieval.
    :param str topic_query: Query to be extracted.
    :param str s_break: s-attribute where to break (typically 's' or 'tweet').
    :param list collocates: (Optional) collocate group for discourse collocates.
    :return: ucs-tool command as list.
    :rtype: list
    """

    # Retrieve only topic collocates of no discourse collocates are provided
    if collocates is None:
        query = create_cqp_query(topic_query)

    # Retrieve discourse collocates
    elif isinstance(collocates, list):
        if window_size:
            LOGGER.warning('Window size provided, but are retrieving discourse collocates. window size will be ignored')
        query = create_discourse_query(topic_query, s_break, collocates)
    else:
        raise TypeError('Collocate group is not a list')

    return [
        "ucs-tool",
        "surface-from-cwb-query",
        "-q",
        "-S",
        str(s_break),
        "-w",
        str(window_size),
        "-nh",
        "-r",
        REGISTRY_PATH,
        "-ca",
        "lemma",
        "-M",
        # cache marginal frequencies
        "/tmp/mmda_marginals_{corpus}_lemma.gz".format(corpus=corpus_name),
        # drop hapax co-occurrences for improved performance
        "-f", "1",
        str(corpus_name),
        "-",
        query,
        # so queries matching multiple words or phrases are treated
        # as a single node type (requires UCS revision >= r41)
        'NODE'
    ]


def format_cqp_concordances(concordances, topic_query, collocate=None):
    """
    Formats the return of a CQP query into a list of dictionaries.

    :param list concordances: List of concordances extracted from a CQP command.
    :param str topic_query: Topic query that was used for extraction.
    :param str collocate: (Optional) collocate that was used for extraction.
    :return: List of dictionaries containing concordances.
    :rtype: list
    """

    concs_f = list()

    for conc in concordances:
        # init formatted concordance
        conc_f = dict()
        # get sentence position
        conc_f['s_pos'] = int(search(r"\s*(\d{1,}):\s+", conc).group(1))

        # pre-format concordance
        conc_p = sub(r"^\s*\d{1,}:\s+", "", conc).split(" ")
        conc_f['tokens'] = list()
        conc_f['lemmas'] = list()
        conc_f['emphas'] = list()
        for elem in conc_p:
            # tokens and lemmas are separated by "/"
            # problem if token or lemma contains character "/"
            if elem == "///":
                token = lemma = "/"  # catch the most common and annoying case
            elif elem.count("/") != 1:
                token = lemma = "ERR"  # need better solution here
            else:
                token, lemma = elem.split("/")
            if search(escape(lemma), topic_query):
                empha = "node"
            elif collocate:
                if lemma == collocate:
                    empha = "coll"
                else:
                    empha = None
            else:
                empha = None

            conc_f['tokens'].append(token)
            conc_f['lemmas'].append(lemma)
            conc_f['emphas'].append(empha)

        concs_f.append(conc_f)

    return concs_f


def sentence_positions_of_cqp_query(corpus_name, cqp_query):
    """
    Returns positions of sentences containing a given lemma.

    :param str corpus_name: Corpus to be queried.
    :param str cqp_query: CQP query to get sentences for.
    :return: list of sentence positions in corpus.
    :rtype: list
    """

    cqp_query = create_cqp_query(cqp_query)
    cqp_exec = 'A = {cqp_query}; A = A expand to s; cat A;'
    cqp_exec = cqp_exec.format(cqp_query=cqp_query)

    cqp_cmd = start_cqp_command(corpus_name)
    cqp_process = Popen(cqp_cmd,
                        stdin=PIPE,
                        stdout=PIPE,
                        stderr=PIPE)

    try:
        sentences = cqp_process.communicate(cqp_exec.encode())
        sentences = sentences[0].decode().split("\n")[1:-1]
        positions = [int(sentence.lstrip().split(": ")[0]) for sentence in sentences]
    except Exception:
        LOGGER.error('Error during cqp command')
        raise OSError('Error during cqp command')

    return positions


def cqp_concordances_of_topic(corpus_name, topic_query):
    """
    Uses cqp to get concordances for a given query

    :param str corpus_name: corpus to be queried
    :param str cqp_query: cqp query to extract concordances for
    :return: list containing concordances
    :rtype: list
    """

    cqp_cmd = start_cqp_command(corpus_name)
    cqp_process = Popen(cqp_cmd,
                        stdin=PIPE,
                        stdout=PIPE,
                        stderr=PIPE)

    topic_query = create_cqp_query(topic_query)

    cqp_exec = 'set LD ""; set RD ""; set Context 1 s; show +lemma;' +\
               'query={topic_query}; cat query;'.format(topic_query=topic_query)

    try:
        concordances = cqp_process.communicate(cqp_exec.encode())
        concordances = concordances[0].decode().split("\n")[1:-1]
    except Exception:
        LOGGER.error('Error during cqp command')
        raise OSError('Error during cqp command')

    return format_cqp_concordances(concordances=concordances, topic_query=topic_query)


def cqp_concordances_of_collocate(corpus_name,
                                  topic_query,
                                  collocate,
                                  window_size,
                                  s_break):
    """
    Uses CQP to get concordances for a given topic query and one of its collocates.

    :param str corpus_name: Corpus to be queried.
    :param str topic_query: Topic query which was used for the collocation analysis.
    :param str collocate: One of the topic collocates.
    :param int window_size: Window size used in extraction.
    :param str s_break: s-attribute where to break (typically 's' or 'tweet').
    :return: list of dictionaries containing concordances.
    :rtype: list
    """

    topic_query = create_cqp_query(topic_query)
    # TODO: Sentence boundary s should not be hardcoded
    cqp_exec = 'set LD ""; set RD ""; set Context 1 s; show +lemma;' +\
               'A = ({topic_query} []{{,{ws}}} [lemma = "{coll}"])' +\
               '| ([lemma = "{coll}"] []{{,{ws}}} {topic_query})' +\
               'within {br};' +\
               'A = A expand to {br}; cat A;'

    cqp_exec = cqp_exec.format(
        topic_query=topic_query,
        coll=collocate,
        ws=window_size,
        br=s_break
    )

    cqp_cmd = start_cqp_command(corpus_name)
    cqp_process = Popen(cqp_cmd,
                        stdin=PIPE,
                        stdout=PIPE,
                        stderr=PIPE)

    try:
        raw_concordances = cqp_process.communicate(cqp_exec.encode())
        raw_concordances = raw_concordances[0].decode().split("\n")[1:-1]
    except Exception:
        LOGGER.error('Error during cqp command')
        raise OSError('Error during cqp command')

    # TODO: Probably bad for error handling
    return format_cqp_concordances(concordances=raw_concordances, topic_query=topic_query, collocate=collocate)


def merge_concordances(concordances_a, concordances_b):
    """
    Combines two concordances with the same sentence id.

    :param str concordances_a: Formatted concordance to merge.
    :param str concordances_b: Formatted concordance to merge.
    :raises RunTimeError: If concordances are not equal.
    :return: Merged concordance dictionary.
    :rtype: dict
    """

    if concordances_a['s_pos'] != concordances_b['s_pos']:
        LOGGER.warning('Concordance ids are not equal')
        raise ValueError('Concordance ids are not equal')

    concordances = deepcopy(concordances_a)
    concordances['emphas'] = list()

    for elem_a, elem_b in zip(concordances_a['emphas'], concordances_b['emphas']):
        if elem_a is not None:
            concordances['emphas'].append(elem_a)
        else:
            concordances['emphas'].append(elem_b)

    return concordances


def cqp_concordances_of_discourse(corpus_name,
                                  topic_query,
                                  window_size,
                                  s_break,
                                  collocates):
    """
    Uses CQP to get concordances for a discourse (topic + group of collocates).

    :param str corpus_name: Corpus to be queried.
    :param str topic_query: topic query which was used for the collocation analysis.
    :param list collocates: Collocates that make up the discourse.
    :param int window_size: Window size used in extraction.
    :param str s_break: s-attribute where to break (typically 's' or 'tweet').
    :return: dictionary of dictionaries containing concordances (key: s_pos).
    :rtype: dict
    """

    concordances_all = dict()

    for collocate in collocates:
        concordances = cqp_concordances_of_collocate(corpus_name,
                                                     topic_query,
                                                     collocate,
                                                     window_size=window_size,
                                                     s_break=s_break)

        for conc in concordances:
            if conc['s_pos'] not in concordances_all.keys():
                concordances_all[conc['s_pos']] = conc
            else:
                # Concordance already exsists, merging the two
                existing_conc = concordances_all[conc['s_pos']]
                concordances_all[conc['s_pos']] = merge_concordances(conc, existing_conc)

    return list(concordances_all.values())


def sort_concordances(concordances, order):
    """
    Sort concordances according to order passed. Hint: Currently only Random.

    :return: List of concordances in specified order.
    :rtype: list
    """

    # TODO: Implement further methods
    if order == 'random':
        shuffle(concordances)
    else:
        LOGGER.error('Sampling method not implemented')
        LOGGER.debug(order)
        raise NotImplementedError('Sampling method not implemented')

    return concordances


def format_ucs_data(data, association_measures):
    """
    Adds association measures to data from ucs_tool_collocates.

    :param pandas.DataFrame data: DataFrame to transform (contains f1, N, l2, O11)
    :param list association_measures: Association measures to use.
    :return: Tuple of DataFrame with added association measures, f1 and N
    :rtype: tuple
    """

    f1_score = int(data['f1'][0])
    n_value = int(data['N'][0])

    data.index = data['l2']
    data.index.name = 'item'

    data = data[['f2', 'f'] + association_measures]
    data.columns = ['f2', 'O11'] + association_measures

    return Collocates(data=data, f1=f1_score, N=n_value)


def ucs_tool_collocates(corpus_name,
                        topic_query,
                        window_size,
                        assoc_measures,
                        s_break,
                        collocates=None):
    """
    Runs ucs-tool surface-from-cwb-query and ucs-add with the measures provided.

    **Example**
    This is how you call the ucs-tool in the shell:
       ucs-tool surface-from-cwb-query -q -S s -w 5 -nh -r /opt/registry/ sz_small - '"Atomkraft"'

    **Python**
    This is how you call this function::
        collocates_from_cwb_query(corpus='SZ_SMALL', registry='/opt/cwb/registry', query='Atom', windowsize=4, measures=['am.simple.ll'], boundary='s')

    :param str corpus_name: Corpus to be queried.
    :param str topic_query: Query to extract.
    :param str window_size: Window size to be used in command.
    :param list association_measures: Association measures to be used.
    :param str s_break: s-attribute where to break (typically 's' or 'tweet').
    :param str collocates: (Optional) collocate group for discourse collocates.
    :return: DataFrame containing collocates extraced by ucs-toolkit.
    :rtype: pandas.DataFrame
    """

    add_cmd = ["ucs-add"] + assoc_measures
    ucs_cmd = make_ucs_command(corpus_name,
                               topic_query,
                               window_size,
                               s_break,
                               collocates)

    LOGGER.debug("UCS pipe:  " + " ".join(ucs_cmd) + " | " + " ".join(add_cmd))

    try:
        ucs_process = Popen(ucs_cmd, stdout=PIPE)
        add_process = run(add_cmd, stdin=ucs_process.stdout, stdout=PIPE, stderr=PIPE, timeout=300)
    except TimeoutExpired:
        LOGGER.error('Error during ucs-add. Timeout during query.')
        return DataFrame()
    except Exception: # pylint: disable=broad-except
        LOGGER.error('Error during ucs-add.')
        return DataFrame()

    raw_stdout = add_process.stdout
    data = raw_stdout.decode().split('\n')
    # Last element is None because return string ends with \n
    data = [row.split('\t') for row in data[:-1]]
    collocate_df = DataFrame(data=data[1:], columns=data[0])

    # Return only 200 most relevant items
    # TODO: Sort by want?
    collocate_df.sort_values(by='f2', ascending=False)
    collocate_df = collocate_df.head(200)

    return collocate_df


class CWBEngine(Engine):
    """
    Corpus Workbench Engine Class.
    """

    def extract_collocates(self, topic_query, window_size, collocates=None):
        """
        Extract collocates from a CWB corpus. See BaseClass for parameters.
        """

        association_measures = self.corpus_settings['association_measures']
        s_break = self.corpus_settings['sentence_boundary']

        data = ucs_tool_collocates(corpus_name=self.corpus_name,
                                   assoc_measures=association_measures,
                                   s_break=s_break,
                                   topic_query=topic_query,
                                   window_size=window_size,
                                   collocates=collocates)

        if data.empty:
            LOGGER.error('Collocation extraction failed. Empty return for CWB UCS query')
            LOGGER.debug(topic_query)
            raise ValueError('Collocation extraction failed. Empty return for CWB UCS query')

        return format_ucs_data(data, association_measures)

    def extract_concordances(self, topic_query, window_size, collocates=None, order='random'):
        """
        Extract concordances from a CWB corpus. See BaseClass for parameters.
        """

        s_break = self.corpus_settings['sentence_boundary']

        if collocates is None:
            concordances = cqp_concordances_of_topic(self.corpus_name, topic_query)
            return sort_concordances(concordances, order)

        concordances = cqp_concordances_of_discourse(self.corpus_name,
                                                     topic_query,
                                                     window_size,
                                                     s_break,
                                                     collocates)
        if not concordances:
            LOGGER.error('Concordance extraction failed. Empty return for CWB query')
            LOGGER.debug(topic_query)
            raise ValueError('concordance extraction failed. Empty return for CWB query')

        return sort_concordances(concordances, order)
