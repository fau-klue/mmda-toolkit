# Random Engine for Development and Testing

from random import sample, randint, random
from pandas import DataFrame
from .engine import Engine


WORD_FILE = '/usr/share/dict/words'
WORDS = ['than', 'then', 'now', 'look', 'only', 'come' ,'its' ,'over' ,'also' ,'your' ,'good' ,'some' ,'could' ,'them', 'see', 'other']
try:
    WORDS = open(WORD_FILE).read().splitlines()
except FileNotFoundError:
    pass


def random_words(num):
    """
    Get some random words
    """

    return sample(WORDS, k=num)


class RandomEngine(Engine):
    """
    RandomEngine Class for testing purposes. Returns random values in the correct format.
    """

    # pylint: disable=unused-argument, no-self-use
    def lexicalize_positions(self, positions, p_att):
        return ['Weitblick', 'RT', '@neos_eu', ':', '.', '@BMeinl', ':', 'Nie', 'war', 'es', 'so', 'wichtig', ',', 'in', 'Europa', 'Haltung', 'zu', 'zeigen', ',', 'wie', 'jetzt', '.', 'Da', 'gehört', 'die', 'Unterstützung', 'unserer', 'europäischen', 'Freu', '…']

    # pylint: disable=unused-argument, no-self-use
    def get_marginals(self, items, p_att):
        return pandas.DataFrame.from_dict({"f2":{"wählt":181,"morgen":38}})

    # pylint: disable=unused-argument, no-self-use
    def prepare_discourseme(self, p_att, s_att, items, max_window_size):
        data_cooc = {
            'node_id': [1,1,1,1,2,2,2,2,2,3,3,3,3],
            'offset': [-2, -1, 1, 2, -2, -1, 1, 2, -2, -1, 1, 2,],
            'collocate':  ['Weitblick', 'RT', '@neos_eu', ':', '.', '@BMeinl', ':', 'Nie', 'war', 'es', 'so', 'wichtig', ',']}

        data_node = {
            'node_id': [1,2,3],
            'node_start': [319, 345, 1469],
            'node_end': [319, 345, 1469],
            'node': ['Weitblick', 'RT', 'Nie'],
            's_start': [315, 337, 1467],
            's_end': [336, 346, 1471],
        }

        df_cooc = pandas.Dataframe(data_cooc)
        df_node = pandas.Dataframe(data_node)

        return df_cooc, df_node
