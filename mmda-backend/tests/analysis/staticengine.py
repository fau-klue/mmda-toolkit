from collections import Counter
from os import path
from pandas import read_csv, DataFrame


THIS_DIR, THIS_FILENAME = path.split(__file__)
DATA_PATH = path.join(THIS_DIR, 'mock-data.csv.gz')


class StaticEngine():

    def __init__(self, corpus_settings):
        self.df = read_csv(DATA_PATH, index_col=0)
        # TODO: Is N missing?

    def get_marginals(self, items, p_att):

        counts = Counter(self.df[p_att])
        rel_counts = list()

        for k in items:
            if k in counts.keys():
                rel_counts.append(counts[k])
            else:
                rel_counts.append(0)

        f2 = DataFrame(index=items)
        f2['f2'] = rel_counts

        return f2, len(self.df)

    def prepare_df_node(self, p_query, s_break, items):

        rel_lines = self.df.copy()
        rel_lines = rel_lines[rel_lines[p_query].isin(items)]
        rel_lines['matchend'] = rel_lines.index
        rel_lines = rel_lines[['matchend', 's_start', 's_end']]

        # DF_Node
        return rel_lines

    def lexicalize_positions(self, positions, p_att='word'):

        rel_lines = self.df.loc[positions]

        return list(rel_lines[p_att])
