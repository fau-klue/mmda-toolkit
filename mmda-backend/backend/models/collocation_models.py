"""
Collocation Models:

- Collocation

- Discourseme
- Constellation
- Coordinates

Relationships:

=== one to many ===
# (topic) discourseme - collocation
- a discourseme (parent) can have several analyses (children)
- an collocation has exactly one topic discourseme

# user - [collocation, discourseme, constellation]
- a user can have several analyses
- an collocation belongs to exactly one user

=== one to one ===
# collocation - coordinates
- an collocation (parent) has exactly one coordinates table (child)
- a coordinates table belongs to exactly one collocation

=== many to many ===
# collocation - discoursemes
- an collocation has several associated discoursemes
- a discourseme can belong to several analyses

# constellation - discoursemes
- a constellation has several associated discoursemes
- a discourseme can belong to several constellations

"""


from pandas import read_json
from backend import db


collocation_discoursemes = db.Table(
    # many to many mapping:
    # - an analysis has several associated discoursemes
    # - a discourseme can belong to several collocation analyses
    'CollocationDiscoursemes',
    db.Column('collocation_id', db.Integer, db.ForeignKey('collocation.id')),
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


class Collocation(db.Model):
    """
    Collocation Analysis data model
    """

    __tablename__ = 'collocation'
    _separator = ','

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.Unicode(255))
    corpus = db.Column(db.Unicode(255), nullable=False)
    p_query = db.Column(db.Unicode(255), nullable=False)
    p_collocation = db.Column(db.Unicode(255), nullable=False)
    s_break = db.Column(db.Unicode(255), nullable=False)
    context = db.Column(db.Integer, nullable=True)
    # association_measures are stored as <str>, will be returned as <list>
    _association_measures = db.Column(db.Unicode(), nullable=True)
    # items are stored as <str>, will be returned as <list>
    _items = db.Column(db.Unicode(), nullable=False)

    # FOREIGN KEYS FOR PARENTS
    topic_id = db.Column(db.Integer(),
                         db.ForeignKey('discourseme.id', ondelete='CASCADE'),
                         nullable=False)
    user_id = db.Column(db.Integer(),
                        db.ForeignKey('users.id', ondelete='CASCADE'))

    # RELATIONSHIP DEFINITIONS FOR CHILDREN
    coordinates = db.relationship("Coordinates",
                                  backref='collocation',
                                  cascade='all, delete',
                                  lazy=True)
    # associated discoursemes
    discoursemes = db.relationship("Discourseme",
                                   secondary=collocation_discoursemes,
                                   backref=db.backref('collocation_associated', lazy=True))

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
        :return: Dictionary containing the collocation analysis values
        :rtype: dict
        """
        return {
            'id': self.id,
            'name': self.name,
            'corpus': self.corpus,
            'user_id': self.user_id,
            'topic_id': self.topic_id,
            'p_query': self.p_query,
            'p_collocation': self.p_collocation,
            's_break': self.s_break,
            'context': self.context,
            'items': self.items,
            'topic_discourseme': Discourseme.query.filter_by(id=self.topic_id).first().serialize
        }

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

    # linked analyses as a topic (discourseme is parent of collocation analysis)
    collocation_analyses = db.relationship('Collocation', backref='topic',
                                           cascade='all, delete')

    # users
    user_id = db.Column(db.Integer(),
                        db.ForeignKey('users.id', ondelete='CASCADE'))

    # topic = is there an associated collocation analysis?
    @property
    def topic(self):
        return len(self.collocation_analyses) > 0

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
            'items': self._items.split(self._separator),
            'collocation_analyses': [
                collocation.id for collocation in self.collocation_analyses
            ]
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
            'discoursemes': [discourseme.id for discourseme in self.discoursemes],
            'discoursemes_names': [discourseme.name for discourseme in self.discoursemes]
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
    collocation_id = db.Column(db.Integer(),
                               db.ForeignKey('collocation.id', ondelete='CASCADE'))

    # keyword analysis
    keyword_id = db.Column(db.Integer(),
                           db.ForeignKey('keyword.id', ondelete='CASCADE'))

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