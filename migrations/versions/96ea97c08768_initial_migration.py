"""Initial Migration

Revision ID: 96ea97c08768
Revises:
Create Date: 2022-11-08 11:38:13.445663

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '96ea97c08768'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    genders = op.create_table('genders',
                              sa.Column('id', sa.Integer(),
                                        autoincrement=True, nullable=False),
                              sa.Column('biology', sa.String(
                                  length=6), nullable=False),
                              sa.PrimaryKeyConstraint('id')
                              )
    op.create_table('users',
                    sa.Column('id', sa.Integer(),
                              autoincrement=True, nullable=False),
                    sa.Column('name', sa.String(length=100), nullable=False),
                    sa.Column('email', sa.String(length=40), nullable=False),
                    sa.Column('password', sa.String(
                        length=200), nullable=False),
                    sa.Column('created_on', sa.DateTime(), nullable=False),
                    sa.Column('gender_id', sa.Integer(), nullable=False),
                    sa.Column('birthday', sa.Date(), nullable=False),
                    sa.ForeignKeyConstraint(['gender_id'], ['genders.id'], ),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('email')
                    )
    op.create_table('measurements',
                    sa.Column('id', sa.Integer(),
                              autoincrement=True, nullable=False),
                    sa.Column('user_id', sa.Integer(), nullable=False),
                    sa.Column('timestamp', sa.DateTime(), nullable=True),
                    sa.Column('bmi', sa.Float(), nullable=False),
                    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
                    sa.PrimaryKeyConstraint('id')
                    )
    op.create_index(op.f('ix_measurements_timestamp'),
                    'measurements', ['timestamp'], unique=False)

    op.bulk_insert(genders, [
        {'id': 1, 'biology': 'MALE'},
        {'id': 2, 'biology': 'FEMALE'},
    ])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_measurements_timestamp'), table_name='measurements')
    op.drop_table('measurements')
    op.drop_table('users')
    op.drop_table('genders')
    # ### end Alembic commands ###
