"""Discourseme Models

Relationships:

- Discourseme
- Constellation

# constellation - discoursemes
- a constellation has several associated discoursemes
- a discourseme can belong to several constellations

"""


from backend import db

constellation_discoursemes = db.Table(
    'ConstellationDiscoursemes',
    db.Column('constellation_id', db.Integer, db.ForeignKey('constellation.id')),
    db.Column('discourseme_id', db.Integer, db.ForeignKey('discourseme.id'))
)


class Discourseme(db.Model):
    """Discourseme

    """

    __tablename__ = 'discourseme'
    _separator = '\t'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Unicode(255), nullable=True)
    description = db.Column(db.Unicode, nullable=True)

    # items are stored as <str>, will be returned as <list>
    _items = db.Column(db.Unicode, nullable=True)

    # linked analyses as a topic (discourseme is parent of collocation analysis)
    collocation_analyses = db.relationship('Collocation', backref='topic', cascade='all, delete')

    # users
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'))

    # topic = is there an associated collocation analysis?
    @property
    def topic(self):
        return len(self.collocation_analyses) > 0

    @property
    def items(self):
        """Read string and turn into list

        :return: Items as list
        :rtype: list

        """
        return self._items.split(self._separator)

    @items.setter
    def items(self, items):
        """Turn list into String

        :return: Items as str
        :rtype: str

        """
        self._items = self._separator.join(items)

    @property
    def serialize(self):
        """Return object data in easily serializeable format

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
    """Constellation

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
        """Return object data in easily serializeable format

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
