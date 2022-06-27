"""add all current tables

Revision ID: 11bef167c5c2
Revises: 
Create Date: 2022-05-27 17:14:28.071799

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mssql

# revision identifiers, used by Alembic.
revision = "11bef167c5c2"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "alignment_feed",
        sa.Column("alignment_feed_uuid", mssql.UNIQUEIDENTIFIER(), nullable=False),
        sa.Column("aligned_effect_1_iri", sa.String(length=255), nullable=True),
        sa.Column("aligned_effect_2_iri", sa.String(length=255), nullable=True),
        sa.Column("aligned_effect_3_iri", sa.String(length=255), nullable=True),
        sa.Column("aligned_solution_1_iri", sa.String(length=255), nullable=True),
        sa.Column("aligned_solution_2_iri", sa.String(length=255), nullable=True),
        sa.Column("aligned_solution_3_iri", sa.String(length=255), nullable=True),
        sa.Column("aligned_solution_4_iri", sa.String(length=255), nullable=True),
        sa.Column("aligned_solution_5_iri", sa.String(length=255), nullable=True),
        sa.Column("aligned_solution_6_iri", sa.String(length=255), nullable=True),
        sa.Column("aligned_solution_7_iri", sa.String(length=255), nullable=True),
        sa.PrimaryKeyConstraint("alignment_feed_uuid"),
    )
    op.create_table(
        "alignment_scores",
        sa.Column("alignment_scores_uuid", mssql.UNIQUEIDENTIFIER(), nullable=False),
        sa.Column("overall_similarity_score", sa.Float(), nullable=True),
        sa.Column("security_alignment", sa.Float(), nullable=True),
        sa.Column("conformity_alignment", sa.Float(), nullable=True),
        sa.Column("benevolence_alignment", sa.Float(), nullable=True),
        sa.Column("tradition_alignment", sa.Float(), nullable=True),
        sa.Column("universalism_alignment", sa.Float(), nullable=True),
        sa.Column("self_direction_alignment", sa.Float(), nullable=True),
        sa.Column("stimulation_alignment", sa.Float(), nullable=True),
        sa.Column("hedonism_alignment", sa.Float(), nullable=True),
        sa.Column("achievement_alignment", sa.Float(), nullable=True),
        sa.Column("power_alignment", sa.Float(), nullable=True),
        sa.Column("top_match_percent", sa.Float(), nullable=True),
        sa.Column("top_match_value", sa.String(length=255), nullable=True),
        sa.PrimaryKeyConstraint("alignment_scores_uuid"),
    )
    op.create_table(
        "analytics_data",
        sa.Column("analytics_id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("category", sa.String(length=50), nullable=True),
        sa.Column("action", sa.String(length=50), nullable=True),
        sa.Column("label", sa.String(length=50), nullable=True),
        sa.Column("session_uuid", mssql.UNIQUEIDENTIFIER(), nullable=True),
        sa.Column("event_timestamp", sa.DateTime(), nullable=True),
        sa.Column("value", sa.String(length=255), nullable=True),
        sa.Column("page_url", sa.String(length=255), nullable=True),
        sa.PrimaryKeyConstraint("analytics_id"),
    )
    op.create_table(
        "effect_choice",
        sa.Column("effect_choice_uuid", mssql.UNIQUEIDENTIFIER(), nullable=False),
        sa.Column("effect_choice_1_iri", sa.String(length=255), nullable=True),
        sa.PrimaryKeyConstraint("effect_choice_uuid"),
    )
    op.create_table(
        "scores",
        sa.Column("quiz_uuid", mssql.UNIQUEIDENTIFIER(), nullable=False),
        sa.Column("security", sa.Float(), nullable=True),
        sa.Column("conformity", sa.Float(), nullable=True),
        sa.Column("benevolence", sa.Float(), nullable=True),
        sa.Column("tradition", sa.Float(), nullable=True),
        sa.Column("universalism", sa.Float(), nullable=True),
        sa.Column("self_direction", sa.Float(), nullable=True),
        sa.Column("stimulation", sa.Float(), nullable=True),
        sa.Column("hedonism", sa.Float(), nullable=True),
        sa.Column("achievement", sa.Float(), nullable=True),
        sa.Column("power", sa.Float(), nullable=True),
        sa.Column("scores_created_timestamp", sa.DateTime(), nullable=True),
        sa.Column("session_uuid", mssql.UNIQUEIDENTIFIER(), nullable=True),
        sa.Column("postal_code", sa.String(length=5), nullable=True),
        # sa.ForeignKeyConstraint(
        #     ["session_uuid"],
        #     ["sessions.session_uuid"],
        # ),
        sa.PrimaryKeyConstraint("quiz_uuid"),
    )
    op.create_table(
        "sessions",
        sa.Column("ip_address", sa.String(length=255), nullable=True),
        sa.Column("user_uuid", mssql.UNIQUEIDENTIFIER(), nullable=True),
        sa.Column("session_uuid", mssql.UNIQUEIDENTIFIER(), nullable=False),
        sa.Column("session_created_timestamp", sa.DateTime(), nullable=True),
        # sa.ForeignKeyConstraint(
        #     ["user_uuid"],
        #     ["users.user_uuid"],
        # ),
        sa.PrimaryKeyConstraint("session_uuid"),
    )
    op.create_table(
        "solution_choice",
        sa.Column("solution_choice_uuid", mssql.UNIQUEIDENTIFIER(), nullable=False),
        sa.Column("solution_choice_1_iri", sa.String(length=255), nullable=True),
        sa.Column("solution_choice_2_iri", sa.String(length=255), nullable=True),
        sa.PrimaryKeyConstraint("solution_choice_uuid"),
    )
    op.create_table(
        "users",
        sa.Column("user_uuid", mssql.UNIQUEIDENTIFIER(), nullable=False),
        sa.Column("user_email", sa.String(length=120), nullable=True),
        sa.Column("user_created_timestamp", sa.DateTime(), nullable=True),
        sa.Column("password_hash", sa.String(length=128), nullable=True),
        sa.Column("first_name", sa.String(length=50), nullable=False),
        sa.Column("last_name", sa.String(length=50), nullable=False),
        sa.Column("quiz_uuid", mssql.UNIQUEIDENTIFIER(), nullable=True),
        # sa.ForeignKeyConstraint(
        #     ["quiz_uuid"],
        #     ["scores.quiz_uuid"],
        # ),
        sa.PrimaryKeyConstraint("user_uuid"),
    )
    op.create_index(op.f("ix_users_user_email"), "users", ["user_email"], unique=True)
    op.create_table(
        "climate_feed",
        sa.Column("climate_feed_id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("event_timestamp", sa.DateTime(), nullable=True),
        sa.Column("effect_position", sa.Integer(), nullable=True),
        sa.Column("effect_iri", sa.String(length=255), nullable=True),
        sa.Column("effect_score", sa.Float(), nullable=True),
        sa.Column("solution_1_iri", sa.String(length=255), nullable=True),
        sa.Column("solution_2_iri", sa.String(length=255), nullable=True),
        sa.Column("solution_3_iri", sa.String(length=255), nullable=True),
        sa.Column("solution_4_iri", sa.String(length=255), nullable=True),
        sa.Column("isPossiblyLocal", sa.Boolean(), nullable=True),
        sa.Column("session_uuid", mssql.UNIQUEIDENTIFIER(), nullable=True),
        # sa.ForeignKeyConstraint(
        #     ["session_uuid"],
        #     ["sessions.session_uuid"],
        # ),
        sa.PrimaryKeyConstraint("climate_feed_id"),
    )
    op.create_table(
        "conversations",
        sa.Column("conversation_uuid", mssql.UNIQUEIDENTIFIER(), nullable=False),
        sa.Column("sender_user_uuid", mssql.UNIQUEIDENTIFIER(), nullable=False),
        sa.Column("sender_session_uuid", mssql.UNIQUEIDENTIFIER(), nullable=False),
        sa.Column("receiver_name", sa.String(length=50), nullable=False),
        sa.Column("conversation_status", sa.Integer(), nullable=True),
        sa.Column("conversation_created_timestamp", sa.DateTime(), nullable=True),
        sa.Column("user_b_share_consent", sa.Boolean(), nullable=True),
        sa.Column("state", sa.Integer(), nullable=True),
        sa.Column("user_a_rating", sa.Integer(), nullable=True),
        # sa.ForeignKeyConstraint(
        #     ["sender_session_uuid"],
        #     ["sessions.session_uuid"],
        # ),
        # sa.ForeignKeyConstraint(
        #     ["sender_user_uuid"],
        #     ["users.user_uuid"],
        # ),
        sa.PrimaryKeyConstraint("conversation_uuid"),
    )
    op.create_index(
        op.f("ix_conversations_sender_user_uuid"),
        "conversations",
        ["sender_user_uuid"],
        unique=False,
    )
    op.create_table(
        "signup",
        sa.Column("signup_email", sa.String(length=254), nullable=True),
        sa.Column("signup_timestamp", sa.DateTime(), nullable=True),
        sa.Column("session_uuid", mssql.UNIQUEIDENTIFIER(), nullable=True),
        sa.Column("signup_id", sa.Integer(), autoincrement=True, nullable=False),
        # sa.ForeignKeyConstraint(
        #     ["session_uuid"],
        #     ["sessions.session_uuid"],
        # ),
        sa.PrimaryKeyConstraint("signup_id"),
    )
    op.create_table(
        "user_b_analytics_data",
        sa.Column("event_log_uuid", mssql.UNIQUEIDENTIFIER(), nullable=False),
        sa.Column("conversation_uuid", mssql.UNIQUEIDENTIFIER(), nullable=True),
        sa.Column("event_type", sa.String(length=255), nullable=True),
        sa.Column("event_value", sa.String(length=255), nullable=True),
        sa.Column("event_timestamp", sa.DateTime(), nullable=True),
        sa.Column("event_value_type", sa.String(length=255), nullable=True),
        sa.Column("session_uuid", mssql.UNIQUEIDENTIFIER(), nullable=True),
        # sa.ForeignKeyConstraint(
        #     ["conversation_uuid"],
        #     ["conversations.conversation_uuid"],
        # ),
        # sa.ForeignKeyConstraint(
        #     ["session_uuid"],
        #     ["sessions.session_uuid"],
        # ),
        sa.PrimaryKeyConstraint("event_log_uuid"),
    )
    op.create_table(
        "user_b_journey",
        sa.Column("conversation_uuid", mssql.UNIQUEIDENTIFIER(), nullable=False),
        sa.Column("quiz_uuid", mssql.UNIQUEIDENTIFIER(), nullable=True),
        sa.Column("alignment_scores_uuid", mssql.UNIQUEIDENTIFIER(), nullable=True),
        sa.Column("alignment_feed_uuid", mssql.UNIQUEIDENTIFIER(), nullable=True),
        sa.Column("effect_choice_uuid", mssql.UNIQUEIDENTIFIER(), nullable=True),
        sa.Column("solution_choice_uuid", mssql.UNIQUEIDENTIFIER(), nullable=True),
        sa.Column("consent", sa.Boolean(), nullable=True),
        # sa.ForeignKeyConstraint(
        #     ["alignment_feed_uuid"],
        #     ["alignment_feed.alignment_feed_uuid"],
        # ),
        # sa.ForeignKeyConstraint(
        #     ["alignment_scores_uuid"],
        #     ["alignment_scores.alignment_scores_uuid"],
        # ),
        # sa.ForeignKeyConstraint(
        #     ["conversation_uuid"],
        #     ["conversations.conversation_uuid"],
        # ),
        # sa.ForeignKeyConstraint(
        #     ["effect_choice_uuid"],
        #     ["effect_choice.effect_choice_uuid"],
        # ),
        # sa.ForeignKeyConstraint(
        #     ["quiz_uuid"],
        #     ["scores.quiz_uuid"],
        # ),
        # sa.ForeignKeyConstraint(
        #     ["solution_choice_uuid"],
        #     ["solution_choice.solution_choice_uuid"],
        # ),
        sa.PrimaryKeyConstraint("conversation_uuid"),
    )

    op.create_foreign_key(
        "fk_scores_session_uuid",
        "scores",
        "sessions",
        ["session_uuid"],
        ["session_uuid"],
    )

    # sa.ForeignKeyConstraint(
    #     ["session_uuid"],
    #     ["sessions.session_uuid"],
    # ),

    op.create_foreign_key(
        "fk_sessions_user_uuid",
        "sessions",
        "users",
        ["user_uuid"],
        ["user_uuid"],
    )

    # sa.ForeignKeyConstraint(
    #     ["user_uuid"],
    #     ["users.user_uuid"],
    # ),

    op.create_foreign_key(
        "fk_users_quiz_uuid",
        "users",
        "scores",
        ["quiz_uuid"],
        ["quiz_uuid"],
    )

    # sa.ForeignKeyConstraint(
    #     ["quiz_uuid"],
    #     ["scores.quiz_uuid"],
    # ),

    op.create_foreign_key(
        "fk_climate_feed_session_uuid",
        "climate_feed",
        "sessions",
        ["session_uuid"],
        ["session_uuid"],
    )
    # sa.ForeignKeyConstraint(
    #     ["session_uuid"],
    #     ["sessions.session_uuid"],
    # ),

    op.create_foreign_key(
        "fk_conversations_session_uuid",
        "conversations",
        "sessions",
        ["sender_session_uuid"],
        ["session_uuid"],
    )

    op.create_foreign_key(
        "fk_conversations_user_uuid",
        "conversations",
        "users",
        ["sender_user_uuid"],
        ["user_uuid"],
    )

    # sa.ForeignKeyConstraint(
    #     ["sender_session_uuid"],
    #     ["sessions.session_uuid"],
    # ),
    # sa.ForeignKeyConstraint(
    #     ["sender_user_uuid"],
    #     ["users.user_uuid"],
    # ),

    op.create_foreign_key(
        "fk_signup_session_uuid",
        "signup",
        "sessions",
        ["session_uuid"],
        ["session_uuid"],
    )

    # sa.ForeignKeyConstraint(
    #     ["session_uuid"],
    #     ["sessions.session_uuid"],
    # ),

    op.create_foreign_key(
        "fk_user_b_analytics_data_conversation_uuid",
        "user_b_analytics_data",
        "conversations",
        ["conversation_uuid"],
        ["conversation_uuid"],
    )

    op.create_foreign_key(
        "fk_user_b_analytics_data_session_uuid",
        "user_b_analytics_data",
        "sessions",
        ["session_uuid"],
        ["session_uuid"],
    )

    # sa.ForeignKeyConstraint(
    #     ["conversation_uuid"],
    #     ["conversations.conversation_uuid"],
    # ),
    # sa.ForeignKeyConstraint(
    #     ["session_uuid"],
    #     ["sessions.session_uuid"],
    # ),

    op.create_foreign_key(
        "fk_user_b_journey_alignment_feed_uuid",
        "user_b_journey",
        "alignment_feed",
        ["alignment_feed_uuid"],
        ["alignment_feed_uuid"],
    )

    op.create_foreign_key(
        "fk_user_b_journey_alignment_scores_uuid",
        "user_b_journey",
        "alignment_scores",
        ["alignment_scores_uuid"],
        ["alignment_scores_uuid"],
    )

    op.create_foreign_key(
        "fk_user_b_journey_conversation_uuid",
        "user_b_journey",
        "conversations",
        ["conversation_uuid"],
        ["conversation_uuid"],
    )

    op.create_foreign_key(
        "fk_user_b_journey_effect_choice_uuid",
        "user_b_journey",
        "effect_choice",
        ["effect_choice_uuid"],
        ["effect_choice_uuid"],
    )

    op.create_foreign_key(
        "fk_user_b_journey_quiz_uuid",
        "user_b_journey",
        "scores",
        ["quiz_uuid"],
        ["quiz_uuid"],
    )

    op.create_foreign_key(
        "fk_user_b_journey_solution_choice_uuid",
        "user_b_journey",
        "solution_choice",
        ["solution_choice_uuid"],
        ["solution_choice_uuid"],
    )

    # sa.ForeignKeyConstraint(
    #     ["alignment_feed_uuid"],
    #     ["alignment_feed.alignment_feed_uuid"],
    # ),
    # sa.ForeignKeyConstraint(
    #     ["alignment_scores_uuid"],
    #     ["alignment_scores.alignment_scores_uuid"],
    # ),
    # sa.ForeignKeyConstraint(
    #     ["conversation_uuid"],
    #     ["conversations.conversation_uuid"],
    # ),
    # sa.ForeignKeyConstraint(
    #     ["effect_choice_uuid"],
    #     ["effect_choice.effect_choice_uuid"],
    # ),
    # sa.ForeignKeyConstraint(
    #     ["quiz_uuid"],
    #     ["scores.quiz_uuid"],
    # ),
    # sa.ForeignKeyConstraint(
    #     ["solution_choice_uuid"],
    #     ["solution_choice.solution_choice_uuid"],
    # ),

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("user_b_journey")
    op.drop_table("user_b_analytics_data")
    op.drop_table("signup")
    op.drop_index(op.f("ix_conversations_sender_user_uuid"), table_name="conversations")
    op.drop_table("conversations")
    op.drop_table("climate_feed")
    op.drop_index(op.f("ix_users_user_email"), table_name="users")
    op.drop_table("users")
    op.drop_table("solution_choice")
    op.drop_table("sessions")
    op.drop_table("scores")
    op.drop_table("effect_choice")
    op.drop_table("analytics_data")
    op.drop_table("alignment_scores")
    op.drop_table("alignment_feed")
    # ### end Alembic commands ###