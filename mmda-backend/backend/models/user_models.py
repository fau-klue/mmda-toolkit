"""
User Models
"""


from flask_user import UserMixin
from backend import db


users_roles = db.Table(
    # many to many mapping:
    # - a user can have several roles
    # - a role can be token by several users
    'UsersRoles',
    db.Column('user_id', db.Integer, db.ForeignKey('users.id')),
    db.Column('role_id', db.Integer, db.ForeignKey('roles.id'))
)


class User(db.Model, UserMixin):
    """
    User data model
    """

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.Unicode(255), nullable=False, server_default=u'', unique=True)
    email = db.Column(db.Unicode(255), nullable=False, server_default=u'', unique=True)
    email_confirmed_at = db.Column(db.DateTime())
    password = db.Column(db.String(255), nullable=False, server_default='')
    reset_password_token = db.Column(db.Unicode(255), nullable=False, server_default=u'')
    # active = db.Column(db.Boolean(), nullable=False, server_default='0')
    active = db.Column('is_active', db.Boolean(), nullable=False, server_default='0')
    first_name = db.Column(db.Unicode(255), nullable=False, server_default=u'')
    last_name = db.Column(db.Unicode(255), nullable=False, server_default=u'')

    # FOREIGN KEYS #
    # roles
    roles = db.relationship('Role',
                            secondary=users_roles,
                            backref=db.backref('users', lazy='dynamic'))
    # analyses
    collocation_analyses = db.relationship('Collocation', backref='users', lazy=True)
    keyword_analyses = db.relationship('Keyword', backref='users', lazy=True)
    # discoursemes
    discoursemes = db.relationship('Discourseme', backref='users', lazy=True)
    # constellations
    constellations = db.relationship('Constellation', backref='users', lazy=True)

    @property
    def serialize(self):
        """
        Return object data in easily serializeable format
        :return: Dictionary containing the user values
        :rtype: dict
        """

        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'email_confirmed_at': self.email,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'active': self.active,
        }


class Role(db.Model):
    """
    Role data model
    """

    __tablename__ = 'roles'

    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(255), nullable=False, server_default=u'', unique=True)  # for @roles_accepted()
    description = db.Column(db.Unicode(255), server_default=u'')
