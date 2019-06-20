"""
Custom interface to CWB (CQP and Corpus Positions)
"""


from subprocess import Popen, PIPE
from pandas import DataFrame, read_csv
from CWB.CL import Corpus
from io import StringIO
from os import getenv

from .engine import Engine

REGISTRY_PATH = getenv('CQP_REGISTRY_PATH',
                       default='/usr/local/cwb-3.4.13/share/cwb/registry')


def _formulate_discourseme_query(corpus_name,
                                 p_att,
                                 s_att,
                                 items):
    """Formulates a CQP query that extracts corpus positions of all
    regions defined by s_att (keyword and target) that contain at
    least one p_att=item (potential mwu, match and matchend). The
    resulting quadruples of corpus positions are dumped (match,
    match_end, s_start, s_end).

    :param str corpus_name: corpus name (in CWB registry)
    :param str p_att: p-attribute to use for querying
    :param str s_att: s-attribute that defines the regions to extract
    :param list items: list of items that each region has to contain

    :return: valid CQP query
    :rtype: str

    """

    # set corpus for CQP query
    cqp_exec = corpus_name + "; "

    # split MWUs and build query
    mwu_queries = list()
    for item in items:
        tokens = item.split(" ")
        mwu_query = ""
        for token in tokens:
            mwu_query += '[{p_att}="{token}"]'.format(p_att=p_att, token=token)
        mwu_queries.append("(" + mwu_query + ")")
    query = '|'.join(mwu_queries)

    # dump results
    cqp_exec += '{query};'.format(query=query)
    cqp_exec += 'set Last target nearest [lbound({s_att})] within left {s_att} from match inclusive;'.format(s_att=s_att)
    cqp_exec += 'set Last keyword nearest [rbound({s_att})] within right {s_att} from matchend inclusive;'.format(s_att=s_att)
    cqp_exec += 'dump Last;'
    return cqp_exec


def _execute_cqp_query(registry_path,
                       query):
    """Lets CQP evaluate a query via Popen. Raises RuntimeError if
    something goes wrong communicating with CQP.

    :param str registry_path: path to CQP registry
    :param str query: valid CQP query

    :return: decoded return value of CQP
    :rtype: str

    """

    start_cqp = [
        'cqp',
        '-c',
        '-r',
        registry_path
    ]

    try:
        cqp_process = Popen(start_cqp,
                            stdin=PIPE,
                            stdout=PIPE,
                            stderr=PIPE)
        cqp_return = cqp_process.communicate(query.encode())

    except Exception:
        raise RuntimeError('Error during CQP command')

    return cqp_return[0].decode()


def _dump_corpus_positions(registry_path,
                           corpus_name,
                           p_att,
                           s_att,
                           items):
    """Extracts corpus positions of all regions defined by s_att that
    contain at least one p_att=item. Returns CQP dump.

    :param str registry_path: path to CQP registry
    :param str corpus_name: corpus name (in CWB registry)
    :param str p_att: p-attribute to use for querying
    :param str s_att: s-attribute that defines the regions to extract
    :param list items: list of items that each region has to contain

    :return: corpus positions (list of quadruples)
    :rtype: list

    """

    query = _formulate_discourseme_query(corpus_name,
                                         p_att,
                                         s_att,
                                         items)

    cqp_dump = _execute_cqp_query(registry_path, query)

    return cqp_dump.split("\n")[1:-1]


def _dump_to_df_node(dump):
    df = read_csv(StringIO("\n".join(dump)),
                  sep="\t", index_col=0, header=None,
                  names=["match", "matchend", "s_start", "s_end"])
    return df


class CWBEngine(Engine):
    """ interface to CWB, convenience wrapper """

    def __init__(self, corpus_settings):
        """Establishes connection to the indexed corpus. Raises KeyError if
        corpus not in registry.
        """

        self.corpus_name = corpus_settings['name_api']
        self.registry_path = corpus_settings['registry_path']
        self.corpus = Corpus(self.corpus_name, registry_dir=self.registry_path)
        self._N = len(self.corpus.attribute('word', 'p'))

    def _run_query(self, query):
        """Runs a query an returns CWB Output as list of lines"""
        cqp_dump = _execute_cqp_query(self.registry_path, query)
        return cqp_dump.split("\n")[1:-1]

    def lexicalize_positions(self, positions, p_att='word'):
        """Fills corpus positions. Raises IndexError if out-of-bounds.

        :param list positions: corpus positions to fill
        :param str p_att: p-attribute to fill positions with

        :return: lexicalizations of the positions
        :rtype: list

        """
        tokens_all = self.corpus.attribute(p_att, 'p')
        tokens_requested = list()
        for position in positions:
            tokens_requested.append(
                tokens_all[position]
            )
        return tokens_requested

    def get_marginals(self, items, p_att='word'):
        """Extracts marginal frequencies for given items (0 if not in corpus).

        :param list items: items to get marginals for
        :param str p_att: p-attribute to get counts for

        :return: counts for each item (indexed by items, column "f2")
        :rtype: DataFrame

        """

        tokens_all = self.corpus.attribute(p_att, 'p')
        N = len(tokens_all)
        counts = list()
        for item in items:
            try:
                counts.append(tokens_all.frequency(item))
            except KeyError:
                counts.append(0)
        f2 = DataFrame(index=items)
        f2['f2'] = counts
        return f2, N

    def prepare_df_node(self,
                        p_query,
                        s_break,
                        items):
        """
        Executes query to get corpus positions of query matches.
        match, matchend, target=left_s_break, keyword=right_s_break.
        """

        # test if requested p-attribute exists
        try:
            self.corpus.attribute(p_query, 'p')
        except KeyError:
            # raise KeyError('requested p-attribute not in corpus')
            return None

        # test if requested s-attribute exists
        try:
            self.corpus.attribute(s_break, 's')
        except KeyError:
            # raise KeyError('requested s-attribute not in corpus')
            return None

        dump = _dump_corpus_positions(
            self.registry_path,
            self.corpus_name,
            p_query,
            s_break,
            items
        )
        df_node = _dump_to_df_node(dump)
        return df_node
