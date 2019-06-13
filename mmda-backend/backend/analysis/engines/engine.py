"""
Abstract base class for corpus Engines.
These are classes that serve as backend to extract data from different corpora,
since corpora may differ in extraction methods.
"""


from abc import ABC


class Engine(ABC):
    """
    Abstract base class for all Corpus Engines
    """

    def __init__(self, corpus_settings):
        """
        :param dict corpus_settings: Corpus settings for this corpus
        """

        self.corpus_settings = corpus_settings
        self._N = 0

    @property
    def N(self):
        """
        Number of tokens in corpus
        :rtype: int
        """

        return self._N

    def lexicalize_positions(self, positions, p_att):
        """
        Fills corpus positions. Raises IndexError if out-of-bounds.

        :param list positions: corpus positions to fill
        :param str p_att: p-attribute to fill positions with

        :raises: IndexError: If corpus position not in Corpus
        :raises: RuntimeError: If p_att not available in Corpurs annotation

        :return: lexicalizations of the positions
        :rtype: list
        """

        raise NotImplementedError

    def get_marginals(self, items, p_att):
        """
        Extracts marginal frequencies for given items (0 if not in corpus).

        :param list items: items to get marginals for
        :param str p_att: p-attribute to get counts for

        :raises: RuntimeError: If p_att not available in Corpurs annotation

        :return: counts for each item (indexed by items, column "f2"). Will be 0 if item 1not in corpus.
        :rtype: pandas.DataFrame
        """

        raise NotImplementedError

    def prepare_df_node(self, p_query, s_break, items):
        """
        Creates df_cooc and df_node for a given discourseme.

        Example:
        df_node
        match  matchend  s_start s_end
        319     319     315     336
        345     345     337     347

        :param str p_query: p-attribute to use for querying
        :param str s_break: s-attribute that defines the regions to extract
        :param list items: list of items that each region has to contain

        # TODO: Are these ok?
        :raises: RuntimeError: If p_att not available in Corpurs annotation
        :raises: RuntimeError: If s_att not available in Corpurs annotation

        :return: df_node
        :rtype: DataFrame
        """
        raise NotImplementedError
