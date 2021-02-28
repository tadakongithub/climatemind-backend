"""change pk for sessions and signup table

Revision ID: b53b3fb50a6e
Revises: c643d0b48ade
Create Date: 2021-02-28 21:02:00.402787

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mssql

# revision identifiers, used by Alembic.
revision = "b53b3fb50a6e"
down_revision = "c643d0b48ade"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.execute("ALTER TABLE sessions DROP CONSTRAINT pk__sessions__69B13FDCF2832A7B")
    op.alter_column(
        "sessions",
        "session_id",
        existing_type=sa.VARCHAR(length=256, collation="SQL_Latin1_General_CP1_CI_AS"),
        nullable=True,
    )
    op.alter_column(
        "sessions", "session_uuid", existing_type=mssql.UNIQUEIDENTIFIER, nullable=False
    )
    op.create_primary_key("pk_sessions", "sessions", ["session_uuid"])
    op.execute("ALTER TABLE signup DROP CONSTRAINT pk__signup__AB6E6165A0BA3B52")
    op.alter_column(
        "signup",
        "email",
        existing_type=sa.VARCHAR(length=254, collation="SQL_Latin1_General_CP1_CI_AS"),
        nullable=True,
    )
    op.alter_column("signup", "signup_id", existing_type=sa.Integer, nullable=False)
    op.create_primary_key("pk_signup", "signup", ["signup_id"])
    op.execute("ALTER TABLE users DROP CONSTRAINT pk__users__B9BE370FCD96ECEF")
    op.alter_column(
        "users",
        "user_id",
        existing_type=sa.VARCHAR(length=256, collation="SQL_Latin1_General_CP1_CI_AS"),
        nullable=True,
    )
    op.alter_column(
        "users", "user_uuid", existing_type=mssql.UNIQUEIDENTIFIER, nullable=False
    )
    op.create_primary_key("pk_users", "users", ["user_uuid"])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column(
        "users",
        "user_id",
        existing_type=sa.VARCHAR(length=256, collation="SQL_Latin1_General_CP1_CI_AS"),
        nullable=False,
    )
    op.alter_column(
        "signup",
        "email",
        existing_type=sa.VARCHAR(length=254, collation="SQL_Latin1_General_CP1_CI_AS"),
        nullable=False,
    )
    op.alter_column(
        "sessions",
        "session_id",
        existing_type=sa.VARCHAR(length=256, collation="SQL_Latin1_General_CP1_CI_AS"),
        nullable=False,
    )
    # ### end Alembic commands ###
