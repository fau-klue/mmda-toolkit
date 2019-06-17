# Dummy Engine for Development and Testing

from pandas import DataFrame
from .engine import Engine


class DummyEngine(Engine):
    """
    DummyEngine Class for testing purposes. Returns fixed values in the correct format.
    """

    # pylint: disable=unused-argument, no-self-use
    def lexicalize_positions(self, positions, p_att):
        return ['Lorem', 'ipsum', 'dolor', 'sit', 'amet', 'consectetur', 'adipiscing', 'elit', '.', 'Nulla', 'ac', '.']

    # pylint: disable=unused-argument, no-self-use
    def get_marginals(self, items, p_att):
        N = 1234
        marginals = {'f2':
                     {
                         'Lorem': 12,
                         'ipsum': 123,
                         'dolor': 13,
                         'sit': 121,
                         'amet': 124,
                         'consectetur': 12,
                         'adipiscing': 19,
                         'elit': 20,
                         '.': 21,
                         'Nulla': 123,
                         'ac': 123,
                     }}

        return DataFrame.from_dict(marginals), N

    # pylint: disable=unused-argument, no-self-use
    def prepare_df_node(self, p_query, s_break, items):

        data_node = {
            'match': [319, 345, 1469],
            'matchend': [319, 345, 1469],
            's_start': [315, 337, 1467],
            's_end': [336, 346, 1471],
        }

        df_node = DataFrame(data_node)

        return df_node
