"""
Analysis Models:

- Discourseme
- Constellation
- Analysis
- Coordinates

Relationships:

=== one to many ===
# (topic) discourseme - analysis
- a discourseme (parent) can have several analyses (children)
- an analysis has exactly one topic discourseme

# user - [analysis, discourseme, constellation]
- a user can have several analyses
- an analysis belongs to exactly one user

=== one to one ===
# analysis - coordinates
- an analysis (parent) has exactly one coordinates table (child)
- a coordinates table belongs to exactly one analysis

=== many to many ===
# analysis - discoursemes
- an analysis has several associated discoursemes
- a discourseme can belong to several analyses

# constellation - discoursemes
- a constellation has several associated discoursemes
- a discourseme can belong to several constellations

"""


from pandas import read_json
from backend import db


analyses_discoursemes = db.Table(
    # many to many mapping:
    # - an analysis has several associated discoursemes
    # - a discourseme can belong to several analyses
    'AnalysesDiscoursemes',
    db.Column('analysis_id', db.Integer, db.ForeignKey('analysis.id')),
    db.Column('discourseme_id', db.Integer, db.ForeignKey('discourseme.id'))
)

constellation_discoursemes = db.Table(
    # many to many mapping:
    # - a constellation has several associated discoursemes
    # - a discourseme can belong to several constellations
    'ConstellationDiscoursemes',
    db.Column('constellation_id', db.Integer, db.ForeignKey('constellation.id')),
    db.Column('discourseme_id', db.Integer, db.ForeignKey('discourseme.id'))
)


class Analysis(db.Model):
    """
    Analysis data model
    """

    __tablename__ = 'analysis'
    _separator = ','

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.Unicode(255), nullable=False)
    corpus = db.Column(db.Unicode(255), nullable=False)
    p_query = db.Column(db.Unicode(255), nullable=False)
    s_break = db.Column(db.Unicode(255), nullable=False)
    max_window_size = db.Column(db.Integer, nullable=True)
    # association_measures are stored as <str>, will be returned as <list>
    _association_measures = db.Column(db.Unicode(), nullable=True)

    # FOREIGN KEYS ##
    # topic discourseme id
    topic_id = db.Column(db.Integer(),
                         db.ForeignKey('discourseme.id'),
                         nullable=False)
    # coordinates
    coordinates_id = db.Column(db.Integer(),
                               db.ForeignKey('coordinates.id', ondelete='CASCADE'))
    # user
    user_id = db.Column(db.Integer(),
                        db.ForeignKey('users.id', ondelete='CASCADE'))

    # associated discoursemes
    discoursemes = db.relationship("Discourseme",
                                   secondary=analyses_discoursemes,
                                   backref=db.backref('analyses_associated', lazy=True))

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

    # items are stored as <str>, will be returned as <list>
    _items = db.Column(db.Unicode(), nullable=True)

    # linked analyses as a topic
    analyses = db.relationship('Analysis', backref='discourseme', lazy=True)

    # users
    user_id = db.Column(db.Integer(),
                        db.ForeignKey('users.id', ondelete='CASCADE'))

    # topic = is there an associated analysis?
    @property
    def topic(self):
        return len(self.analyses) > 0

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


class Constellation(db.Model):
    """
    Constellation data model
    """

    __tablename__ = 'constellation'

    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.Unicode(255), nullable=True)

    # users
    user_id = db.Column(db.Integer(),
                        db.ForeignKey('users.id', ondelete='CASCADE'))

    # associated discoursemes
    discoursemes = db.relationship("Discourseme",
                                   secondary=constellation_discoursemes,
                                   backref=db.backref('constellations', lazy=True))

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
            'name': self.name,
            'discoursemes': [discourseme.id for discourseme in self.discoursemes]
        }


class Coordinates(db.Model):
    """
    Coordinates data model
    - 1:1-relationship with Analysis
    """

    __tablename__ = 'coordinates'

    id = db.Column(db.Integer(), primary_key=True)

    # data is stored as JSON <str>, will be returned as <pd.DataFrame>
    # NB: not all databases support JSON
    _data = db.Column(db.Unicode(255*255), nullable=True)

    # analysis
    # analysis = db.relationship('Analysis',
    #                            backref='coordinates',
    #                            lazy=True,
    #                            uselist=False)
    analysis_id = db.Column(db.Integer(),
                            db.ForeignKey('analysis.id'))

    @property
    def data(self):
        """
        Read JSON String and create DataFrame
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
