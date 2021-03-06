"""Add tables

Revision ID: 73f412cfc2c0
Revises: 
Create Date: 2021-09-19 19:05:50.196136

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '73f412cfc2c0'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        'laboratory',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=100), nullable=True),
        sa.Column('address', sa.String(length=100), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('name'),
    )
    op.create_table(
        'parameter',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=100), nullable=True),
        sa.Column('description', sa.String(length=300), nullable=True),
        sa.Column('type', sa.Enum('int', 'int_bool', name='parametertype'), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('name'),
    )
    op.create_table(
        'user',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('username', sa.String(length=50), nullable=True),
        sa.Column('email', sa.String(length=50), nullable=True),
        sa.Column('first_name', sa.String(length=50), nullable=True),
        sa.Column('last_name', sa.String(length=50), nullable=True),
        sa.Column('type', sa.Enum('patient', 'doctor', 'laboratory', name='usertype'), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('email'),
        sa.UniqueConstraint('username'),
    )
    op.create_table(
        'analysis',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=True),
        sa.Column('laboratory_id', sa.Integer(), nullable=True),
        sa.Column('timestamp', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(('laboratory_id',), ('laboratory.id',)),
        sa.ForeignKeyConstraint(('user_id',), ('user.id',)),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_table(
        'sharing',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('owner_id', sa.Integer(), nullable=True),
        sa.Column('viewer_id', sa.Integer(), nullable=True),
        sa.Column('analysis_id', sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(('analysis_id',), ('analysis.id',)),
        sa.ForeignKeyConstraint(('owner_id',), ('user.id',)),
        sa.ForeignKeyConstraint(('viewer_id',), ('user.id',)),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_table(
        'test',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('analysis_id', sa.Integer(), nullable=True),
        sa.Column('value', sa.Float(), nullable=True),
        sa.Column('result', sa.Boolean(), nullable=True),
        sa.Column('status', sa.Enum('created', 'processing', 'done', name='teststatus'), nullable=True),
        sa.ForeignKeyConstraint(('analysis_id',), ('analysis.id',)),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_table(
        'test_parameter',
        sa.Column('test_id', sa.Integer(), nullable=False),
        sa.Column('parameter_id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(('parameter_id',), ('parameter.id',)),
        sa.ForeignKeyConstraint(('test_id',), ('test.id',)),
        sa.PrimaryKeyConstraint('test_id', 'parameter_id'),
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('test_parameter')
    op.drop_table('test')
    op.drop_table('sharing')
    op.drop_table('analysis')
    op.drop_table('user')
    op.drop_table('parameter')
    op.drop_table('laboratory')
    # ### end Alembic commands ###
