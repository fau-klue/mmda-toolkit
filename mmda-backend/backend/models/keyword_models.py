"""
Keyword Models:

"""


# from pandas import read_json
from backend import db


keyword_discoursemes = db.Table(
    # many to many mapping:
    # - a keyword analysis has several associated discoursemes
    # - a discourseme can belong to several analyses
    'KeywordDiscoursemes',
    db.Column('keyword_id', db.Integer, db.ForeignKey('keyword.id')),
    db.Column('discourseme_id', db.Integer, db.ForeignKey('discourseme.id'))
)


class Keyword(db.Model):
    """
    Keyword Analysis data model
    """

    __tablename__ = 'keyword'
    _separator = ','

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.Unicode(255))
    corpus = db.Column(db.Unicode(255), nullable=False)
    corpus_reference = db.Column(db.Unicode(255), nullable=False)
    p = db.Column(db.Unicode(255), nullable=False)
    p_reference = db.Column(db.Unicode(255), nullable=False)
    s_break = db.Column(db.Unicode(255), nullable=False)
    flags = db.Column(db.Unicode(255), nullable=True)
    flags_reference = db.Column(db.Unicode(255), nullable=True)
    # association_measures are stored as <str>, will be returned as <list>
    _association_measures = db.Column(db.Unicode(), nullable=True)

    # FOREIGN KEYS FOR PARENTS
    user_id = db.Column(db.Integer(),
                        db.ForeignKey('users.id', ondelete='CASCADE'))

    # RELATIONSHIP DEFINITIONS FOR CHILDREN
    coordinates = db.relationship("Coordinates",
                                  backref='keyword',
                                  cascade='all, delete',
                                  lazy=True)
    # associated discoursemes
    discoursemes = db.relationship("Discourseme",
                                   secondary=keyword_discoursemes,
                                   backref=db.backref('keyword_associated', lazy=True))

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
            'user_id': self.user_id,
            'name': self.name,
            'corpus': self.corpus,
            'corpus_reference': self.corpus_reference,
            'p': self.p,
            'p_reference': self.p_reference,
            'flags': self.flags,
            'flags_reference': self.flags_reference
        }
