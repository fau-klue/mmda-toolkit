"""
Keywords Models:

"""


# from pandas import read_json
from backend import db
from backend.models.analysis_models import analyses_discoursemes, Discourseme


class Keywords(db.Model):
    """
    Keywords data model
    """

    __tablename__ = 'keywords'
    _separator = ','

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.Unicode(255))
    corpus = db.Column(db.Unicode(255), nullable=False)
    corpus_reference = db.Column(db.Unicode(255), nullable=False)
    p = db.Column(db.Unicode(255), nullable=True)
    p_reference = db.Column(db.Unicode(255), nullable=True)
    flags = db.Column(db.Unicode(255), nullable=True)
    flags_reference = db.Column(db.Unicode(255), nullable=True)

    # FOREIGN KEYS FOR PARENTS
    user_id = db.Column(db.Integer(),
                        db.ForeignKey('users.id', ondelete='CASCADE'))

    # RELATIONSHIP DEFINITIONS FOR CHILDREN
    coordinates = db.relationship("Coordinates",
                                  backref='keywords',
                                  cascade='all, delete',
                                  lazy=True)
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
            'p_analysis': self.p_analysis,
            's_break': self.s_break,
            'context': self.context,
            'items': self.items,
            'topic_discourseme': Discourseme.query.filter_by(id=self.topic_id).first().serialize
        }
