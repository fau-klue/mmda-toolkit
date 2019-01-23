# Random Engine for Development and Testing

from random import choices, randint, random
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

    return choices(WORDS, k=num)


class RandomEngine(Engine):
    """
    RandomEngine Class for testing purposes. Returns random values in the correct format.
    """

    # pylint: disable=unused-argument, no-self-use
    def extract_collocates(self, items, window_size, collocates=None):
        """
        See Base Engine for details.
        """

        num = randint(5,15)
        columns=['011', 'f2', 'Dice', 'MI', 'simple.ll', 't.score']
        index = random_words(num=num)
        data = []

        for idx in range(0, num):
            random_data = [idx,
                           randint(1,100),
                           random(),
                           random()*10,
                           random()*100,
                           random()]
            data.append(random_data)

        ret_collocates = DataFrame(data=data, columns=columns, index=index)

        return (ret_collocates, 15, 1000)

    # pylint: disable=unused-argument, no-self-use
    def extract_concordances(self, items, window_size=None, collocates=None, order='random'):
        """
        See Base Engine for details.
        """

        ret_concordances = []

        for idx in range(0, randint(1, 10)):
            sentence_length = randint(5,15)
            sentence = random_words(num=sentence_length)
            random_concordance = {'s_pos': 323122,
                                  'tokens': sentence,
                                  'emphas': [None] * sentence_length,
                                  'lemmas': sentence}
            ret_concordances.append(random_concordance)

        return ret_concordances
