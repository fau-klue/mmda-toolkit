"""Coordinates Models

Relationships:

=== one to one ===
# collocation/keyword - coordinates
- a collocation/keyword analysis (parent) has exactly one coordinates table (child)
- a coordinates table belongs to exactly one collocation/keyword analysis

"""


from pandas import read_json

from backend import db


class Coordinates(db.Model):
    """Coordinates

    """

    __tablename__ = 'coordinates'

    id = db.Column(db.Integer(), primary_key=True)

    # data is stored as JSON <str>, will be returned as <pd.DataFrame>
    # NB: not all databases support JSON
    _data = db.Column(db.Unicode(255*255), nullable=True)

    # analysis
    collocation_id = db.Column(db.Integer(),
                               db.ForeignKey('collocation.id', ondelete='CASCADE'))

    # keyword analysis
    keyword_id = db.Column(db.Integer(),
                           db.ForeignKey('keyword.id', ondelete='CASCADE'))

    @property
    def data(self):
        """Read JSON String and create DataFrame

        :return: Pandas DataFrame from JSON
        :rtype: DataFrame

        """

        return read_json(self._data)

    @data.setter
    def data(self, dataframe):
        """Turn DataFrame into JSON String

        :return: JSON from DataFrame
        :rtype: str

        """

        self._data = dataframe.to_json()
