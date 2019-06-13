# Dummy Engine for Development and Testing

from pandas import DataFrame
from .engine import Engine


class DummyEngine(Engine):
    """
    DummyEngine Class for testing purposes. Returns fixed values in the correct format.
    """

    # pylint: disable=unused-argument, no-self-use
    def lexicalize_positions(self, positions, p_att):
        return ['Weitblick', 'RT', '@neos_eu', ':', '.', '@BMeinl', ':', 'Nie', 'war', 'es', 'so', 'wichtig', ',', 'in', 'Europa', 'Haltung', 'zu', 'zeigen', ',', 'wie', 'jetzt', '.', 'Da', 'gehört', 'die', 'Unterstützung', 'unserer', 'europäischen', 'Freu', '…']

    # pylint: disable=unused-argument, no-self-use
    def get_marginals(self, items, p_att):
        return DataFrame.from_dict({"f2":{"wählt":181,"morgen":38}})

    # pylint: disable=unused-argument, no-self-use
    def prepare_df_node(self, p_query, s_breaks, items):

        data_node = {
            'match': [319, 345, 1469],
            'matchend': [319, 345, 1469],
            's_start': [315, 337, 1467],
            's_end': [336, 346, 1471],
        }

        df_node = DataFrame(data_node)

        return df_node
