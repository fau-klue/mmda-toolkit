"""
Abstract base class for corpus Engines.
These are classes that serve as backend to extract collocates/concordances from different corpora,
since corpora may differ in extraction methods.
"""


from abc import ABC
from collections import namedtuple


class Engine(ABC):
    """
    Abstract base class for all Corpus Engines
    """

    # Return value for extract collocates
    # data=pandas.DataFrame
    # f1=Number of query in corpus
    # N=Total number of tokens in corpus
    Collocates = namedtuple('Collocates', ['data', 'f1', 'N'])

    def __init__(self, corpus_name, corpus_settings):
        """
        :param str corpus_name: Name of corpus for which this engine acts
        :param dict corpus_settings: Corpus settings for this corpus
        """

        self.corpus_name = corpus_name
        self.corpus_settings = corpus_settings

    def extract_collocates(self, topic_query, window_size, collocates=None):
        """
        Extract collocates from a corpus.

        :param str topic_query: Query for collocate extraction.
        :param int window_size: Window Size for collocate extraction.
        :param list collocates: (Optional) collocate group for extracting discourse collocates.
        :return: Tuple with collocates in DataFrame, f1 and N (see below)
        DataFrame
            index: lexical items
            columns: O11, f2, am.[...]
        f1 (number of occurrences of topic_query)
        N (number of all tokens in corpus)
        :rtype: tuple(DataFrame, int, int)
        """

        raise NotImplementedError

    def extract_concordances(self, topic_query, window_size, collocates=None, order='random'):
        """
        Extract concordances from a corpus.

        :param str topic_query: Query for concordance extraction.
        :param int window_size: Window Size for concordance extraction.
        :param list collocates: (Optional) collocate group for extracting discourse concordances
        :param str order: How to sort the concordances. Options: (random)
        :return: list of dictionaries containing the concordances, keys:
            s_pos
            sentiment
            tokens
            emphas
            lemmas
        :rtype: list
        """

        raise NotImplementedError
