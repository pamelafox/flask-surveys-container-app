"""empty message
Revision ID: 23d454425300
Revises:
Create Date: 2023-01-23 19:56:22.037011
"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "23d454425300"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "survey",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("topic", sa.String(length=50), nullable=True),
        sa.Column("question", sa.String(length=150), nullable=True),
        sa.Column("options", sa.String(length=500), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "answer",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("survey", sa.Integer(), nullable=True),
        sa.Column("selected_option", sa.String(length=500), nullable=True),
        sa.ForeignKeyConstraint(["survey"], ["survey.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("answer")
    op.drop_table("survey")
    # ### end Alembic commands ###
