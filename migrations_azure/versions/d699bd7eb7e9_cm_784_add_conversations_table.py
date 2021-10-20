"""CM-784 add conversations table

Revision ID: d699bd7eb7e9
Revises: df2fd4177138
Create Date: 2021-09-25 12:54:39.324392

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mssql

# revision identifiers, used by Alembic.
revision = "d699bd7eb7e9"
down_revision = "df2fd4177138"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "conversations",
        sa.Column("conversation_uuid", mssql.UNIQUEIDENTIFIER(), nullable=False),
        sa.Column("sender_user_uuid", mssql.UNIQUEIDENTIFIER(), nullable=False),
        sa.Column("sender_session_uuid", mssql.UNIQUEIDENTIFIER(), nullable=False),
        sa.Column("receiver_session_uuid", mssql.UNIQUEIDENTIFIER(), nullable=True),
        sa.Column("receiver_name", sa.String(length=50), nullable=False),
        sa.Column("conversation_status", sa.Integer(), nullable=True),
        sa.Column("conversation_created_timestamp", sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(
            ["receiver_session_uuid"],
            ["sessions.session_uuid"],
        ),
        sa.ForeignKeyConstraint(
            ["sender_session_uuid"],
            ["sessions.session_uuid"],
        ),
        sa.ForeignKeyConstraint(
            ["sender_user_uuid"],
            ["users.user_uuid"],
        ),
        sa.PrimaryKeyConstraint("conversation_uuid"),
    )
    op.create_index(
        op.f("ix_conversations_sender_user_uuid"),
        "conversations",
        ["sender_user_uuid"],
        unique=False,
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f("ix_conversations_sender_user_uuid"), table_name="conversations")
    op.drop_table("conversations")
    # ### end Alembic commands ###