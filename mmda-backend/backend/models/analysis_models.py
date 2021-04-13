"""
Analysis Models
"""


from pandas import read_json
from backend import db


class Analysis(db.Model):
    """
    Analysis data model
    """

    __tablename__ = 'analysis'
    _separator = ','

    id = db.Column(db.Integer, primary_key=True)
    # Maximum window size
    max_window_size = db.Column(db.Integer, nullable=True)
    # p_query: p-attribute for the query (e.g. lemma, pos)
    p_query = db.Column(db.Unicode(255), nullable=False)
    # s_break: s-attribute for sentence break (e.g. <s>, <tweet>)
    s_break = db.Column(db.Unicode(255), nullable=False)
    # association_measures
    _association_measures = db.Column(db.Unicode(), nullable=True)

    name = db.Column(db.Unicode(255), nullable=False)
    corpus = db.Column(db.Unicode(255), nullable=False)
    user_id = db.Column(db.Integer(),
                        db.ForeignKey('users.id', ondelete='CASCADE'))
    topic_id = db.Column(db.Integer(),
                         db.ForeignKey('discourseme.id', ondelete='SET NULL'))

    # Relationship
    user = db.relationship('User', back_populates='analysis')
    discourseme = db.relationship('Discourseme',
                                  secondary='analysis_discoursemes',
                                  backref=db.backref('analysis', lazy='dynamic'))

    @property
    def association_measures(self):
        """
        Read string and turn into list
        :return: Association_Measures as list
        :rtype: list
        """
        return self._association_measures.split(self._separator)

    @association_measures.setter
    def association_measures(self, association_measures):
        """
        Turn list into String
        :return: Association_Measures as str
        :rtype: str
        """
        self._association_measures = self._separator.join(association_measures)

    @property
    def serialize(self):
        """
        Return object data in easily serializeable format
        :return: Dictionary containing the analysis values
        :rtype: dict
        """

        return {
            'id': self.id,
            'name': self.name,
            'corpus': self.corpus,
            'user_id': self.user_id,
            'topic_id': self.topic_id,
            'p_query': self.p_query,
            's_break': self.s_break,
            'max_window_size': self.max_window_size
        }


class Discourseme(db.Model):
    """
    Discourseme data model
    """

    __tablename__ = 'discourseme'
    _separator = ','

    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.Unicode(255), nullable=True)
    # topic means it's a topic discourseme, associated with an analysis
    topic = db.Column(db.Boolean(), nullable=True, server_default='0')
    # Items are a string containing the lexical items, will be returned as a list.
    _items = db.Column(db.Unicode(), nullable=True)
    user_id = db.Column(db.Integer(), db.ForeignKey('users.id', ondelete='CASCADE'))

    # Relationship
    user = db.relationship('User', back_populates='discourseme')

    @property
    def items(self):
        """
        Read string and turn into list
        :return: Items as list
        :rtype: list
        """
        return self._items.split(self._separator)

    @items.setter
    def items(self, items):
        """
        Turn list into String
        :return: Items as str
        :rtype: str
        """
        self._items = self._separator.join(items)

    @property
    def serialize(self):
        """
        Return object data in easily serializeable format
        :return: Dictionary containing the discourseme values
        :rtype: dict
        """

        return {
            'id': self.id,
            'name': self.name,
            'is_topic': self.topic,
            'user_id': self.user_id,
            'items': self._items.split(self._separator)
        }


class AnalysisDiscoursemes(db.Model):
    """
    Analysis Discourseme association model
    """

    __tablename__ = 'analysis_discoursemes'

    id = db.Column(db.Integer(), primary_key=True)
    analysis_id = db.Column(db.Integer(), db.ForeignKey('analysis.id', ondelete='CASCADE'))
    discourseme_id = db.Column(db.Integer(), db.ForeignKey('discourseme.id', ondelete='CASCADE'))


class ConstellationDiscoursemes(db.Model):
    """
    Constellation Discourseme association model
    """

    __tablename__ = 'constellation_discoursemes'

    id = db.Column(db.Integer(), primary_key=True)
    constellation_id = db.Column(db.Integer(), db.ForeignKey('constellation.id', ondelete='CASCADE'))
    discourseme_id = db.Column(db.Integer(), db.ForeignKey('discourseme.id', ondelete='CASCADE'))


class Constellation(db.Model):
    """
    Constellatoin data model
    """

    __tablename__ = 'constellation'

    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.Unicode(255), nullable=True)
    user_id = db.Column(db.Integer(), db.ForeignKey('users.id', ondelete='CASCADE'))

    # Relationship
    user = db.relationship('User', back_populates='constellation')
    discourseme = db.relationship('Discourseme', secondary='constellation_discoursemes', backref=db.backref('constellation', lazy='dynamic'))

    @property
    def serialize(self):
        """
        Return object data in easily serializeable format
        :return: Dictionary containing the constellation values
        :rtype: dict
        """

        return {
            'id': self.id,
            'user_id': self.user_id,
            'name': self.name
        }


class Coordinates(db.Model):
    """
    Coordinates data model
    """

    __tablename__ = 'coordinate'

    id = db.Column(db.Integer(), primary_key=True)
    # This will store a pandas DataFrame as JSON String (not all databases support JSON)
    _data = db.Column(db.Unicode(255*255), nullable=True)
    analysis_id = db.Column(db.Integer(), db.ForeignKey('analysis.id', ondelete='CASCADE'))

    @property
    def data(self):
        """
        Read JSON String an create DataFrame
        :return: Pandas DataFrame from JSON
        :rtype: DataFrame
        """

        return read_json(self._data)

    @data.setter
    def data(self, dataframe):
        """
        Turn DataFrame into JSON String
        :return: JSON from DataFrame
        :rtype: str
        """

        self._data = dataframe.to_json()
