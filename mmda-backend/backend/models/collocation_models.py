"""
Collocation Models:

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


from backend import db
from backend.models.discourseme_models import Discourseme


collocation_discoursemes = db.Table(
    # many to many mapping:
    # - a collocation analysis has several associated discoursemes
    # - a discourseme can belong to several collocation analyses
    'CollocationDiscoursemes',
    db.Column('collocation_id', db.Integer, db.ForeignKey('collocation.id')),
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
    flags_query = db.Column(db.Unicode(255), nullable=False)
    escape_query = db.Column(db.Unicode(255), nullable=False)
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
            'flags_query': self.flags_query,
            'escape_query': self.escape_query,
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
