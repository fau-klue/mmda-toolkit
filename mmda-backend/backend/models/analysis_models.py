"""
Analysis Models
"""


from pandas import read_json
from backend import db


class Analysis(db.Model):
    """
    Define the Analysis data model.
    """

    __tablename__ = 'analysis'

    id = db.Column(db.Integer, primary_key=True)
    # Maximum window size
    window_size = db.Column(db.Integer, nullable=True)
    name = db.Column(db.Unicode(255), nullable=False)
    corpus = db.Column(db.Unicode(255), nullable=False)
    user_id = db.Column(db.Integer(), db.ForeignKey('users.id', ondelete='CASCADE'))
    topic_id = db.Column(db.Integer(),  db.ForeignKey('discourseme.id', ondelete='SET NULL'))

    # Relationship
    user = db.relationship('User', back_populates='analysis')
    discourseme = db.relationship('Discourseme', secondary='analysis_discoursemes', backref=db.backref('analysis', lazy='dynamic'))

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
           'window_size': self.window_size
       }


class Discourseme(db.Model):
    """
    Define the Discourseme data model
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
           'items': self._items.split(self._separator)
       }


class AnalysisDiscoursemes(db.Model):
    """
    Define the Analysis Discourseme association model
    """

    __tablename__ = 'analysis_discoursemes'

    id = db.Column(db.Integer(), primary_key=True)
    analysis_id = db.Column(db.Integer(), db.ForeignKey('analysis.id', ondelete='CASCADE'))
    discourseme_id = db.Column(db.Integer(), db.ForeignKey('discourseme.id', ondelete='CASCADE'))


class DiscursivePositionDiscoursemes(db.Model):
    """
    Define the Discursive Position Discourseme association model
    """

    __tablename__ = 'discursive_position_discoursemes'

    id = db.Column(db.Integer(), primary_key=True)
    discursive_position_id = db.Column(db.Integer(), db.ForeignKey('discursive_position.id', ondelete='CASCADE'))
    discourseme_id = db.Column(db.Integer(), db.ForeignKey('discourseme.id', ondelete='CASCADE'))


class DiscursivePosition(db.Model):
    """
    Define the discursive position data model
    """

    __tablename__ = 'discursive_position'

    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.Unicode(255), nullable=True)
    user_id = db.Column(db.Integer(), db.ForeignKey('users.id', ondelete='CASCADE'))

    # Relationship
    user = db.relationship('User', back_populates='discursive_position')
    discourseme = db.relationship('Discourseme', secondary='discursive_position_discoursemes', backref=db.backref('discursive_position', lazy='dynamic'))

    @property
    def serialize(self):
       """
       Return object data in easily serializeable format
       :return: Dictionary containing the discursive position values
       :rtype: dict
       """

       return {
           'id': self.id,
           'name': self.name
       }


class Coordinates(db.Model):
    """
    Define the Coordinates data model
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
