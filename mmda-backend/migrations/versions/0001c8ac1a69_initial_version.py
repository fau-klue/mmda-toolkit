"""Initial version

Revision ID: 0001c8ac1a69
Revises: None
Create Date: 2019-01-01 17:46:32.620018

"""


# revision identifiers, used by Alembic.
revision = '0001c8ac1a69'
down_revision = None

from alembic import op
import sqlalchemy as sa


def upgrade():

    # Table role
    op.create_table('role',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=64), nullable=True),
    sa.Column('description', sa.String(length=255), server_default='', nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )

    # Table user
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=64), nullable=False),
    sa.Column('password', sa.String(length=255), server_default='', nullable=False),
    sa.Column('reset_password_token', sa.String(length=128), server_default='', nullable=False),
    sa.Column('email', sa.String(length=128), nullable=False),
    sa.Column('email_confirmed_at', sa.DateTime(), nullable=True),
    sa.Column('is_active', sa.Boolean(), server_default='0', nullable=False),
    sa.Column('first_name', sa.String(length=64), server_default='', nullable=False),
    sa.Column('last_name', sa.String(length=64), server_default='', nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('username')
    )

    # Table user_roles
    op.create_table('user_roles',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('role_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['role_id'], ['role.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )

    # Table analysis
    op.create_table('analysis',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=255), nullable=True),
    sa.Column('corpus', sa.String(length=255), nullable=True),
    sa.Column('topic_id', sa.Integer(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['topic_id'], ['discourseme.id'], ondelete='SET NULL'),
    sa.PrimaryKeyConstraint('id')
    )

    # Table analysis_discourseme_junction
    op.create_table('analysis_discourseme',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('analysis_id', sa.Integer(), nullable=True),
    sa.Column('discourseme_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['analysis_id'], ['analysis.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['discourseme_id'], ['discourseme.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )

    # Table discourseme
    # Means it's a topic discourseme, associated with an analysis
    op.create_table('discourseme',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=255), nullable=True),
    sa.Column('topic', sa.Boolean(), server_default='0', nullable=True),
    sa.Column('items', sa.String(length=255), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )

    # Table coordinates
    op.create_table('coordinate',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('data', sa.String(length=255*255), nullable=False),
    sa.Column('analysis_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['analysis_id'], ['analysis.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )

    # Table discursive_position_discourseme_junction
    op.create_table('discursive_position_discourseme',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('discursive_position_id', sa.Integer(), nullable=True),
    sa.Column('discourseme_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['discursive_position_id'], ['discursive_position.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['discourseme_id'], ['discourseme.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )

    # Table discursive_position
    op.create_table('discursive_position',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=255), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )

def downgrade():

    op.drop_table('user_roles')
    op.drop_table('user')
    op.drop_table('role')
    op.drop_table('coordinate')
    op.drop_table('analysis')
    op.drop_table('analysis_discourseme_junction')
    op.drop_table('discourseme')
