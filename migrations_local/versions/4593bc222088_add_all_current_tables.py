"""add all current tables

Revision ID: 4593bc222088
Revises: 
Create Date: 2021-08-06 10:46:04.395135

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mssql

# revision identifiers, used by Alembic.
revision = '4593bc222088'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('user_uuid', mssql.UNIQUEIDENTIFIER(), nullable=False),
    sa.Column('user_email', sa.String(length=120), nullable=True),
    sa.Column('user_created_timestamp', sa.DateTime(), nullable=True),
    sa.Column('password_hash', sa.String(length=128), nullable=True),
    sa.Column('first_name', sa.String(length=50), nullable=False),
    sa.Column('last_name', sa.String(length=50), nullable=False),
    sa.Column('quiz_uuid', mssql.UNIQUEIDENTIFIER(), nullable=True),
    sa.PrimaryKeyConstraint('user_uuid')
    )
    op.create_index(op.f('ix_users_user_email'), 'users', ['user_email'], unique=True)
    op.create_table('sessions',
    sa.Column('ip_address', sa.String(length=255), nullable=True),
    sa.Column('user_uuid', mssql.UNIQUEIDENTIFIER(), nullable=True),
    sa.Column('session_uuid', mssql.UNIQUEIDENTIFIER(), nullable=False),
    sa.Column('session_created_timestamp', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['user_uuid'], ['users.user_uuid'], ),
    sa.PrimaryKeyConstraint('session_uuid')
    )
    op.create_table('analytics_data',
    sa.Column('analytics_id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('category', sa.String(length=50), nullable=True),
    sa.Column('action', sa.String(length=50), nullable=True),
    sa.Column('label', sa.String(length=50), nullable=True),
    sa.Column('session_uuid', mssql.UNIQUEIDENTIFIER(), nullable=True),
    sa.Column('event_timestamp', sa.DateTime(), nullable=True),
    sa.Column('value', sa.String(length=255), nullable=True),
    sa.Column('page_url', sa.String(length=255), nullable=True),
    sa.PrimaryKeyConstraint('analytics_id')
    )
    op.create_table('scores',
    sa.Column('quiz_uuid', mssql.UNIQUEIDENTIFIER(), nullable=False),
    sa.Column('security', sa.Float(), nullable=True),
    sa.Column('conformity', sa.Float(), nullable=True),
    sa.Column('benevolence', sa.Float(), nullable=True),
    sa.Column('tradition', sa.Float(), nullable=True),
    sa.Column('universalism', sa.Float(), nullable=True),
    sa.Column('self_direction', sa.Float(), nullable=True),
    sa.Column('stimulation', sa.Float(), nullable=True),
    sa.Column('hedonism', sa.Float(), nullable=True),
    sa.Column('achievement', sa.Float(), nullable=True),
    sa.Column('power', sa.Float(), nullable=True),
    sa.Column('scores_created_timestamp', sa.DateTime(), nullable=True),
    sa.Column('session_uuid', mssql.UNIQUEIDENTIFIER(), nullable=True),
    sa.Column('postal_code', sa.String(length=5), nullable=True),
    sa.ForeignKeyConstraint(['session_uuid'], ['sessions.session_uuid'], ),
    sa.PrimaryKeyConstraint('quiz_uuid')
    )
    
    op.create_foreign_key("fk_quiz_uuid", "users", "scores", ["quiz_uuid"], ["quiz_uuid"])
        
    op.create_table('climate_feed',
    sa.Column('climate_feed_id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('event_timestamp', sa.DateTime(), nullable=True),
    sa.Column('effect_position', sa.Integer(), nullable=True),
    sa.Column('effect_iri', sa.String(length=255), nullable=True),
    sa.Column('effect_score', sa.Float(), nullable=True),
    sa.Column('solution_1_iri', sa.String(length=255), nullable=True),
    sa.Column('solution_2_iri', sa.String(length=255), nullable=True),
    sa.Column('solution_3_iri', sa.String(length=255), nullable=True),
    sa.Column('solution_4_iri', sa.String(length=255), nullable=True),
    sa.Column('isPossiblyLocal', sa.Boolean(), nullable=True),
    sa.Column('session_uuid', mssql.UNIQUEIDENTIFIER(), nullable=True),
    sa.ForeignKeyConstraint(['session_uuid'], ['sessions.session_uuid'], ),
    sa.PrimaryKeyConstraint('climate_feed_id')
    )
    op.create_table('conversation',
    sa.Column('conversation_uuid', mssql.UNIQUEIDENTIFIER(), nullable=False),
    sa.Column('sender_user_uuid', mssql.UNIQUEIDENTIFIER(), nullable=False),
    sa.Column('sender_session_uuid', mssql.UNIQUEIDENTIFIER(), nullable=False),
    sa.Column('receiver_session_uuid', mssql.UNIQUEIDENTIFIER(), nullable=True),
    sa.Column('receiver_name', sa.String(length=50), nullable=False),
    sa.Column('conversation_status', sa.Integer(), nullable=True),
    sa.Column('conversation_create_time', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['receiver_session_uuid'], ['sessions.session_uuid'], ),
    sa.ForeignKeyConstraint(['sender_session_uuid'], ['sessions.session_uuid'], ),
    sa.ForeignKeyConstraint(['sender_user_uuid'], ['users.user_uuid'], ),
    sa.PrimaryKeyConstraint('conversation_uuid')
    )
    op.create_index(op.f('ix_conversation_sender_user_uuid'), 'conversation', ['sender_user_uuid'], unique=False)
    op.create_table('signup',
    sa.Column('signup_email', sa.String(length=254), nullable=True),
    sa.Column('signup_timestamp', sa.DateTime(), nullable=True),
    sa.Column('session_uuid', mssql.UNIQUEIDENTIFIER(), nullable=True),
    sa.Column('signup_id', sa.Integer(), autoincrement=True, nullable=False),
    sa.ForeignKeyConstraint(['session_uuid'], ['sessions.session_uuid'], ),
    sa.PrimaryKeyConstraint('signup_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('signup')
    op.drop_index(op.f('ix_conversation_sender_user_uuid'), table_name='conversation')
    op.drop_table('conversation')
    op.drop_table('climate_feed')
    op.drop_index(op.f('ix_users_user_email'), table_name='users')
    op.drop_table('users')
    op.drop_table('sessions')
    op.drop_table('scores')
    op.drop_table('analytics_data')
    # ### end Alembic commands ###
