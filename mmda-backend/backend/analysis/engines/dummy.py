# Dummy Engine for Development and Testing

from pandas import DataFrame
from .engine import Engine
from .engine import Collocates


class DummyEngine(Engine):
    """
    DummyEngine Class for testing purposes. Returns fixed values in the correct format.
    """

    # pylint: disable=unused-argument, no-self-use
    def extract_collocates(self, items, window_size, collocates=None):
        """
        Return a fixed tuple with a collocate format you would expect from a real engine.
        See Base Engine for details.
        """

        dataframe = DataFrame(data=[['1', '13', '1.70', '154.591', '269.3270', '0.974522461783836'],
                                    ['2', '1', '1.70', '32.90', '269.3270', '1.55898224042095'],
                                    ['3', '1', '1.70', '27.887', '269.3270', '-0.389575957724699'],
                                    ['4', '1', '17.0', '16.43', '269.3270', '2.73979143636172'],
                                    ['5', '1', '1.70', '3.8', '269.3270', '10.0705612023562'],
                                    ['6', '1', '1.70', '1.13', '269.3270', '7.90042592880611'],
                                    ['7', '2', '1.70', '17.361', '269.3270', '0.598198042642508'],
                                    ['8', '4', '1.70', '22.712', '2693.270', '3.07608715306093'],
                                    ['9', '1', '1.70', '25.246', '269.3270', '-0.25516035965878'],
                                    ['10', '1', '1.70', '65.59', '269.3270', '0.591761561552103']],
                              columns=['011', 'f2', 'Dice', 'MI', 'simple.ll', 't.score'],
                              index=['der', 'die', 'das', 'wer', 'wie', 'was', 'wieso', 'weshalb', 'warum', 'wo'])

        collocates = Collocates(data=dataframe, f1=15, N=1000)

        return collocates

    # pylint: disable=unused-argument, no-self-use
    def extract_concordances(self, items, window_size=None, collocates=None, order='random'):
        """
        Return a fixed list you would expect from a real engine.
        See Base Engine for details.
        """

        ret_concordances = [
            {'word': ['RT', '@AndreaSchlegel3', ':', 'Die', 'Grünen', 'werden', 'von', 'der', 'Presse', 'nur', 'hochgepuscht', ',', 'weil', 'Schwarz', 'Grün', 'das', 'ist', ',', 'was', 'sie', 'in', 'Bayern', 'wollen', '.', 'Auch', 'Merkel', '…'],
             'role': ['token', 'token', 'token', 'token', 'token', 'token', 'token', 'token', 'token', 'token', 'token', 'token', 'token', 'token', 'token', 'token', 'token', 'token', 'token', 'token', 'token', 'topic', 'token', 'token', 'token', 'collocate', 'token'],
             'tt_lemma': ['RT', '@AndreaSchlegel3', ':', 'die', 'Grüne', 'werden', 'von', 'die', 'Presse', 'nur', 'hochgepuscht', ',', 'weil', 'Schwarz', 'grün', 'die', 'sein', ',', 'was', 'sie', 'in', 'Bayern', 'wollen', '.', 'auch', 'Merkel', '…'],
             's_pos': '466849'},
            {'word': ['Bouffier', '43', '%', 'Bravo', '!', 'CDU', '27', '%', 'Was', 'sagt', 'uns', 'das', '?', 'Vielleicht', 'wäre', 'Merkel', 'besser', 'nicht', 'in', 'Hessen', 'aufgetreten', '?', '@CDU', '@cducsubt', '@CSU', '@BILD', 'Umfrage', 'und', 'Prognose', 'zur', 'Landtagswahl', 'Hessen', ':', 'So', 'sieht', 'es', 'für', 'CDU', ',', 'SPD', ',', 'Grüne', ',', 'AfD', 'und', 'Co.', 'aus', '|', 'Landtagswahl', 'Hessen', 'https://t.co/W2RfELUnvC'],
             'role': ['token', 'token', 'token', 'token', 'token', 'token', 'token', 'token', 'token', 'token', 'token', 'token', 'token', 'token', 'token', 'collocate', 'token', 'token', 'token', 'topic', 'token', 'token', 'token', 'token', 'token', 'token', 'token', 'token', 'token', 'token', 'token', 'token', 'token', 'token', 'token', 'token', 'token', 'token', 'token', 'token', 'token', 'token', 'token', 'token', 'token', 'token', 'token', 'token', 'token', 'token', 'token'],
             'tt_lemma': ['Bouffier', '43', '%', 'Bravo', '!', 'CDU', '27', '%', 'was', 'sagen', 'wir', 'die', '?', 'vielleicht', 'sein', 'Merkel', 'gut', 'nicht', 'in', 'Hessen', 'auftreten', '?', '@CDU', '@cducsubt', '@CSU', '@BILD', 'Umfrage', 'und', 'Prognose', 'zu', 'Landtagswahl', 'Hessen', ':', 'so', 'sehen', 'es', 'für', 'CDU', ',', 'SPD', ',', 'Grüne', ',', 'AfD', 'und', 'Co.', 'aus', '|', 'Landtagswahl', 'Hessen', 'https://t.co/W2RfELUnvC'],
             's_pos': '381844'}
        ]

        return ret_concordances
