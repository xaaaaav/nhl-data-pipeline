"""initial schema

Revision ID: 0001
Revises:
Create Date: 2024-01-01 00:00:00.000000
"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "0001"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # seasons
    op.create_table(
        "seasons",
        sa.Column("season_id", sa.Integer(), nullable=False),
        sa.Column("regular_season_start", sa.Date(), nullable=False),
        sa.Column("regular_season_end", sa.Date(), nullable=False),
        sa.Column("playoff_end", sa.Date(), nullable=True),
        sa.Column("formatted_season_id", sa.String(10), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("season_id"),
    )

    # franchises
    op.create_table(
        "franchises",
        sa.Column("franchise_id", sa.Integer(), nullable=False),
        sa.Column("full_name", sa.String(100), nullable=False),
        sa.Column("team_name", sa.String(100), nullable=False),
        sa.Column("most_recent_team_id", sa.Integer(), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("franchise_id"),
    )

    # teams
    op.create_table(
        "teams",
        sa.Column("team_id", sa.Integer(), nullable=False),
        sa.Column("franchise_id", sa.Integer(), nullable=False),
        sa.Column("season_id", sa.Integer(), nullable=False),
        sa.Column("abbrev", sa.String(10), nullable=False),
        sa.Column("city", sa.String(100), nullable=False),
        sa.Column("full_name", sa.String(100), nullable=False),
        sa.Column("conference", sa.String(50), nullable=True),
        sa.Column("division", sa.String(50), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(["franchise_id"], ["franchises.franchise_id"]),
        sa.ForeignKeyConstraint(["season_id"], ["seasons.season_id"]),
        sa.PrimaryKeyConstraint("team_id"),
    )

    # players
    op.create_table(
        "players",
        sa.Column("player_id", sa.Integer(), nullable=False),
        sa.Column("first_name", sa.String(100), nullable=False),
        sa.Column("last_name", sa.String(100), nullable=False),
        sa.Column("position", sa.String(5), nullable=False),
        sa.Column("birth_date", sa.Date(), nullable=True),
        sa.Column("nationality", sa.String(10), nullable=True),
        sa.Column("height_inches", sa.Integer(), nullable=True),
        sa.Column("weight_pounds", sa.Integer(), nullable=True),
        sa.Column("shoots_catches", sa.String(5), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("player_id"),
    )

    # rosters
    op.create_table(
        "rosters",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("team_id", sa.Integer(), nullable=False),
        sa.Column("season_id", sa.Integer(), nullable=False),
        sa.Column("player_id", sa.Integer(), nullable=False),
        sa.Column("roster_type", sa.String(20), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(["team_id"], ["teams.team_id"]),
        sa.ForeignKeyConstraint(["season_id"], ["seasons.season_id"]),
        sa.ForeignKeyConstraint(["player_id"], ["players.player_id"]),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("team_id", "season_id", "player_id"),
    )

    # games
    op.create_table(
        "games",
        sa.Column("game_id", sa.Integer(), nullable=False),
        sa.Column("season_id", sa.Integer(), nullable=False),
        sa.Column("game_type", sa.Integer(), nullable=False),
        sa.Column("game_date", sa.Date(), nullable=False),
        sa.Column("home_team_id", sa.Integer(), nullable=False),
        sa.Column("away_team_id", sa.Integer(), nullable=False),
        sa.Column("venue", sa.String(200), nullable=True),
        sa.Column("game_state", sa.String(10), nullable=False),
        sa.Column("home_score", sa.Integer(), nullable=True),
        sa.Column("away_score", sa.Integer(), nullable=True),
        sa.Column("period", sa.Integer(), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(["season_id"], ["seasons.season_id"]),
        sa.ForeignKeyConstraint(["home_team_id"], ["teams.team_id"]),
        sa.ForeignKeyConstraint(["away_team_id"], ["teams.team_id"]),
        sa.PrimaryKeyConstraint("game_id"),
    )

    # game_boxscores
    op.create_table(
        "game_boxscores",
        sa.Column("game_id", sa.Integer(), nullable=False),
        sa.Column("home_shots", sa.Integer(), nullable=True),
        sa.Column("home_hits", sa.Integer(), nullable=True),
        sa.Column("home_blocked_shots", sa.Integer(), nullable=True),
        sa.Column("home_pp_goals", sa.Integer(), nullable=True),
        sa.Column("home_pp_opportunities", sa.Integer(), nullable=True),
        sa.Column("home_faceoff_pct", sa.Float(), nullable=True),
        sa.Column("home_giveaways", sa.Integer(), nullable=True),
        sa.Column("home_takeaways", sa.Integer(), nullable=True),
        sa.Column("home_pim", sa.Integer(), nullable=True),
        sa.Column("away_shots", sa.Integer(), nullable=True),
        sa.Column("away_hits", sa.Integer(), nullable=True),
        sa.Column("away_blocked_shots", sa.Integer(), nullable=True),
        sa.Column("away_pp_goals", sa.Integer(), nullable=True),
        sa.Column("away_pp_opportunities", sa.Integer(), nullable=True),
        sa.Column("away_faceoff_pct", sa.Float(), nullable=True),
        sa.Column("away_giveaways", sa.Integer(), nullable=True),
        sa.Column("away_takeaways", sa.Integer(), nullable=True),
        sa.Column("away_pim", sa.Integer(), nullable=True),
        sa.Column("raw", postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(["game_id"], ["games.game_id"]),
        sa.PrimaryKeyConstraint("game_id"),
    )

    # play_by_play_events
    op.create_table(
        "play_by_play_events",
        sa.Column("event_id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("game_id", sa.Integer(), nullable=False),
        sa.Column("event_number", sa.Integer(), nullable=False),
        sa.Column("period", sa.Integer(), nullable=False),
        sa.Column("period_type", sa.String(5), nullable=False),
        sa.Column("time_in_period", sa.String(10), nullable=False),
        sa.Column("time_remaining", sa.String(10), nullable=False),
        sa.Column("event_type", sa.String(50), nullable=False),
        sa.Column("team_id", sa.Integer(), nullable=True),
        sa.Column("x_coord", sa.Float(), nullable=True),
        sa.Column("y_coord", sa.Float(), nullable=True),
        sa.Column("zone", sa.String(5), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(["game_id"], ["games.game_id"]),
        sa.ForeignKeyConstraint(["team_id"], ["teams.team_id"]),
        sa.PrimaryKeyConstraint("event_id"),
        sa.UniqueConstraint("game_id", "event_number"),
    )
    op.create_index("ix_pbp_game_id", "play_by_play_events", ["game_id"])
    op.create_index("ix_pbp_event_type", "play_by_play_events", ["event_type"])

    # pbp detail tables
    _create_pbp_detail_tables()

    # standings_snapshots
    op.create_table(
        "standings_snapshots",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("season_id", sa.Integer(), nullable=False),
        sa.Column("date", sa.Date(), nullable=False),
        sa.Column("team_id", sa.Integer(), nullable=False),
        sa.Column("points", sa.Integer(), nullable=False),
        sa.Column("wins", sa.Integer(), nullable=False),
        sa.Column("losses", sa.Integer(), nullable=False),
        sa.Column("ot_losses", sa.Integer(), nullable=False),
        sa.Column("games_played", sa.Integer(), nullable=False),
        sa.Column("goals_for", sa.Integer(), nullable=True),
        sa.Column("goals_against", sa.Integer(), nullable=True),
        sa.Column("regulation_wins", sa.Integer(), nullable=True),
        sa.Column("streak_type", sa.String(5), nullable=True),
        sa.Column("streak_count", sa.Integer(), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(["season_id"], ["seasons.season_id"]),
        sa.ForeignKeyConstraint(["team_id"], ["teams.team_id"]),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("season_id", "date", "team_id"),
    )

    # draft_picks
    op.create_table(
        "draft_picks",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("draft_year", sa.Integer(), nullable=False),
        sa.Column("round_number", sa.Integer(), nullable=False),
        sa.Column("pick_in_round", sa.Integer(), nullable=False),
        sa.Column("overall_pick", sa.Integer(), nullable=True),
        sa.Column("team_id", sa.Integer(), nullable=True),
        sa.Column("player_id", sa.Integer(), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(["team_id"], ["teams.team_id"]),
        sa.ForeignKeyConstraint(["player_id"], ["players.player_id"]),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("draft_year", "round_number", "pick_in_round"),
    )

    # stats tables
    _create_stats_tables()


def _ts_cols() -> list[sa.Column]:
    return [
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
    ]


def _create_pbp_detail_tables() -> None:
    op.create_table(
        "pbp_goals",
        sa.Column("event_id", sa.Integer(), nullable=False),
        sa.Column("scoring_player_id", sa.Integer(), nullable=True),
        sa.Column("assist1_player_id", sa.Integer(), nullable=True),
        sa.Column("assist2_player_id", sa.Integer(), nullable=True),
        sa.Column("goalie_id", sa.Integer(), nullable=True),
        sa.Column("shot_type", sa.String(50), nullable=True),
        sa.Column("strength", sa.String(5), nullable=True),
        sa.Column("empty_net", sa.Boolean(), nullable=False),
        sa.ForeignKeyConstraint(["event_id"], ["play_by_play_events.event_id"]),
        sa.ForeignKeyConstraint(["scoring_player_id"], ["players.player_id"]),
        sa.ForeignKeyConstraint(["assist1_player_id"], ["players.player_id"]),
        sa.ForeignKeyConstraint(["assist2_player_id"], ["players.player_id"]),
        sa.ForeignKeyConstraint(["goalie_id"], ["players.player_id"]),
        sa.PrimaryKeyConstraint("event_id"),
    )
    op.create_table(
        "pbp_shots",
        sa.Column("event_id", sa.Integer(), nullable=False),
        sa.Column("shooting_player_id", sa.Integer(), nullable=True),
        sa.Column("goalie_id", sa.Integer(), nullable=True),
        sa.Column("shot_type", sa.String(50), nullable=True),
        sa.ForeignKeyConstraint(["event_id"], ["play_by_play_events.event_id"]),
        sa.ForeignKeyConstraint(["shooting_player_id"], ["players.player_id"]),
        sa.ForeignKeyConstraint(["goalie_id"], ["players.player_id"]),
        sa.PrimaryKeyConstraint("event_id"),
    )
    op.create_table(
        "pbp_missed_shots",
        sa.Column("event_id", sa.Integer(), nullable=False),
        sa.Column("shooting_player_id", sa.Integer(), nullable=True),
        sa.Column("goalie_id", sa.Integer(), nullable=True),
        sa.Column("shot_type", sa.String(50), nullable=True),
        sa.Column("miss_reason", sa.String(100), nullable=True),
        sa.ForeignKeyConstraint(["event_id"], ["play_by_play_events.event_id"]),
        sa.ForeignKeyConstraint(["shooting_player_id"], ["players.player_id"]),
        sa.ForeignKeyConstraint(["goalie_id"], ["players.player_id"]),
        sa.PrimaryKeyConstraint("event_id"),
    )
    op.create_table(
        "pbp_blocked_shots",
        sa.Column("event_id", sa.Integer(), nullable=False),
        sa.Column("shooter_player_id", sa.Integer(), nullable=True),
        sa.Column("blocking_player_id", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(["event_id"], ["play_by_play_events.event_id"]),
        sa.ForeignKeyConstraint(["shooter_player_id"], ["players.player_id"]),
        sa.ForeignKeyConstraint(["blocking_player_id"], ["players.player_id"]),
        sa.PrimaryKeyConstraint("event_id"),
    )
    op.create_table(
        "pbp_hits",
        sa.Column("event_id", sa.Integer(), nullable=False),
        sa.Column("hitting_player_id", sa.Integer(), nullable=True),
        sa.Column("hittee_player_id", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(["event_id"], ["play_by_play_events.event_id"]),
        sa.ForeignKeyConstraint(["hitting_player_id"], ["players.player_id"]),
        sa.ForeignKeyConstraint(["hittee_player_id"], ["players.player_id"]),
        sa.PrimaryKeyConstraint("event_id"),
    )
    op.create_table(
        "pbp_faceoffs",
        sa.Column("event_id", sa.Integer(), nullable=False),
        sa.Column("winning_player_id", sa.Integer(), nullable=True),
        sa.Column("losing_player_id", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(["event_id"], ["play_by_play_events.event_id"]),
        sa.ForeignKeyConstraint(["winning_player_id"], ["players.player_id"]),
        sa.ForeignKeyConstraint(["losing_player_id"], ["players.player_id"]),
        sa.PrimaryKeyConstraint("event_id"),
    )
    op.create_table(
        "pbp_penalties",
        sa.Column("event_id", sa.Integer(), nullable=False),
        sa.Column("committed_by_player_id", sa.Integer(), nullable=True),
        sa.Column("drawn_by_player_id", sa.Integer(), nullable=True),
        sa.Column("penalty_type", sa.String(50), nullable=True),
        sa.Column("penalty_description", sa.String(200), nullable=True),
        sa.Column("duration_minutes", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(["event_id"], ["play_by_play_events.event_id"]),
        sa.ForeignKeyConstraint(["committed_by_player_id"], ["players.player_id"]),
        sa.ForeignKeyConstraint(["drawn_by_player_id"], ["players.player_id"]),
        sa.PrimaryKeyConstraint("event_id"),
    )
    op.create_table(
        "pbp_stoppages",
        sa.Column("event_id", sa.Integer(), nullable=False),
        sa.Column("reason", sa.String(200), nullable=True),
        sa.ForeignKeyConstraint(["event_id"], ["play_by_play_events.event_id"]),
        sa.PrimaryKeyConstraint("event_id"),
    )
    op.create_table(
        "pbp_period_events",
        sa.Column("event_id", sa.Integer(), nullable=False),
        sa.Column("period_number", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(["event_id"], ["play_by_play_events.event_id"]),
        sa.PrimaryKeyConstraint("event_id"),
    )


def _player_stats_cols(extra: list[sa.Column]) -> list[sa.Column]:
    return [
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("player_id", sa.Integer(), nullable=False),
        sa.Column("season_id", sa.Integer(), nullable=False),
        sa.Column("team_id", sa.Integer(), nullable=False),
        sa.Column("game_type_id", sa.Integer(), nullable=False),
    ] + extra + _ts_cols()


def _team_stats_cols(extra: list[sa.Column]) -> list[sa.Column]:
    return [
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("team_id", sa.Integer(), nullable=False),
        sa.Column("season_id", sa.Integer(), nullable=False),
        sa.Column("game_type_id", sa.Integer(), nullable=False),
    ] + extra + _ts_cols()


def _create_stats_tables() -> None:  # noqa: PLR0915
    player_fks = [
        sa.ForeignKeyConstraint(["player_id"], ["players.player_id"]),
        sa.ForeignKeyConstraint(["season_id"], ["seasons.season_id"]),
        sa.ForeignKeyConstraint(["team_id"], ["teams.team_id"]),
    ]
    team_fks = [
        sa.ForeignKeyConstraint(["team_id"], ["teams.team_id"]),
        sa.ForeignKeyConstraint(["season_id"], ["seasons.season_id"]),
    ]

    # skater_stats_summary
    op.create_table(
        "skater_stats_summary",
        *_player_stats_cols([
            sa.Column("games_played", sa.Integer(), nullable=False),
            sa.Column("goals", sa.Integer(), nullable=False),
            sa.Column("assists", sa.Integer(), nullable=False),
            sa.Column("points", sa.Integer(), nullable=False),
            sa.Column("plus_minus", sa.Integer(), nullable=False),
            sa.Column("pim", sa.Integer(), nullable=False),
            sa.Column("shots", sa.Integer(), nullable=False),
            sa.Column("shooting_pct", sa.Float(), nullable=True),
            sa.Column("time_on_ice_per_game", sa.String(10), nullable=True),
            sa.Column("pp_goals", sa.Integer(), nullable=False),
            sa.Column("sh_goals", sa.Integer(), nullable=False),
            sa.Column("game_winning_goals", sa.Integer(), nullable=False),
        ]),
        *player_fks,
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("player_id", "season_id", "team_id", "game_type_id"),
    )

    # skater_stats_bios
    op.create_table(
        "skater_stats_bios",
        *_player_stats_cols([
            sa.Column("games_played", sa.Integer(), nullable=False),
            sa.Column("birth_city", sa.String(100), nullable=True),
            sa.Column("birth_country", sa.String(10), nullable=True),
            sa.Column("nationality", sa.String(10), nullable=True),
            sa.Column("height_inches", sa.Integer(), nullable=True),
            sa.Column("weight_pounds", sa.Integer(), nullable=True),
            sa.Column("draft_year", sa.Integer(), nullable=True),
            sa.Column("draft_round", sa.Integer(), nullable=True),
            sa.Column("draft_pick", sa.Integer(), nullable=True),
            sa.Column("draft_overall", sa.Integer(), nullable=True),
        ]),
        *player_fks,
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("player_id", "season_id", "team_id", "game_type_id"),
    )

    # Remaining skater stat tables (abbreviated for clarity - same pattern)
    for table_name, extra_cols in [
        ("skater_stats_faceoffpercentages", [
            sa.Column("games_played", sa.Integer(), nullable=False),
            sa.Column("total_faceoffs", sa.Integer(), nullable=False),
            sa.Column("faceoff_wins", sa.Integer(), nullable=False),
            sa.Column("faceoff_losses", sa.Integer(), nullable=False),
            sa.Column("faceoff_pct", sa.Float(), nullable=True),
            sa.Column("d_zone_faceoff_pct", sa.Float(), nullable=True),
            sa.Column("n_zone_faceoff_pct", sa.Float(), nullable=True),
            sa.Column("o_zone_faceoff_pct", sa.Float(), nullable=True),
        ]),
        ("skater_stats_faceoffwins", [
            sa.Column("games_played", sa.Integer(), nullable=False),
            sa.Column("total_faceoff_wins", sa.Integer(), nullable=False),
            sa.Column("d_zone_faceoff_wins", sa.Integer(), nullable=False),
            sa.Column("n_zone_faceoff_wins", sa.Integer(), nullable=False),
            sa.Column("o_zone_faceoff_wins", sa.Integer(), nullable=False),
            sa.Column("ev_faceoff_wins", sa.Integer(), nullable=False),
            sa.Column("pp_faceoff_wins", sa.Integer(), nullable=False),
            sa.Column("sh_faceoff_wins", sa.Integer(), nullable=False),
        ]),
        ("skater_stats_goalsforagainst", [
            sa.Column("games_played", sa.Integer(), nullable=False),
            sa.Column("ev_goals_for", sa.Integer(), nullable=False),
            sa.Column("ev_goals_against", sa.Integer(), nullable=False),
            sa.Column("pp_goals_for", sa.Integer(), nullable=False),
            sa.Column("pp_goals_against", sa.Integer(), nullable=False),
            sa.Column("sh_goals_for", sa.Integer(), nullable=False),
            sa.Column("sh_goals_against", sa.Integer(), nullable=False),
            sa.Column("on_ice_shooting_pct", sa.Float(), nullable=True),
            sa.Column("on_ice_save_pct", sa.Float(), nullable=True),
        ]),
        ("skater_stats_penalties", [
            sa.Column("games_played", sa.Integer(), nullable=False),
            sa.Column("pim", sa.Integer(), nullable=False),
            sa.Column("penalties", sa.Integer(), nullable=False),
            sa.Column("minor_penalties", sa.Integer(), nullable=False),
            sa.Column("major_penalties", sa.Integer(), nullable=False),
            sa.Column("misconduct_penalties", sa.Integer(), nullable=False),
            sa.Column("penalties_drawn", sa.Integer(), nullable=False),
            sa.Column("pim_drawn", sa.Integer(), nullable=False),
            sa.Column("net_penalties", sa.Integer(), nullable=False),
        ]),
        ("skater_stats_penaltykill", [
            sa.Column("games_played", sa.Integer(), nullable=False),
            sa.Column("sh_goals", sa.Integer(), nullable=False),
            sa.Column("sh_assists", sa.Integer(), nullable=False),
            sa.Column("sh_points", sa.Integer(), nullable=False),
            sa.Column("sh_shots", sa.Integer(), nullable=False),
            sa.Column("sh_toi", sa.String(20), nullable=True),
            sa.Column("sh_toi_per_game", sa.String(20), nullable=True),
            sa.Column("sh_shooting_pct", sa.Float(), nullable=True),
        ]),
        ("skater_stats_penaltyshots", [
            sa.Column("games_played", sa.Integer(), nullable=False),
            sa.Column("penalty_shots_attempts", sa.Integer(), nullable=False),
            sa.Column("penalty_shots_goals", sa.Integer(), nullable=False),
            sa.Column("penalty_shot_pct", sa.Float(), nullable=True),
        ]),
        ("skater_stats_powerplay", [
            sa.Column("games_played", sa.Integer(), nullable=False),
            sa.Column("pp_goals", sa.Integer(), nullable=False),
            sa.Column("pp_assists", sa.Integer(), nullable=False),
            sa.Column("pp_points", sa.Integer(), nullable=False),
            sa.Column("pp_shots", sa.Integer(), nullable=False),
            sa.Column("pp_toi", sa.String(20), nullable=True),
            sa.Column("pp_toi_per_game", sa.String(20), nullable=True),
            sa.Column("pp_shooting_pct", sa.Float(), nullable=True),
        ]),
        ("skater_stats_puckpossessions", [
            sa.Column("games_played", sa.Integer(), nullable=False),
            sa.Column("goals", sa.Integer(), nullable=False),
            sa.Column("total_primary_assists", sa.Integer(), nullable=False),
            sa.Column("total_secondary_assists", sa.Integer(), nullable=False),
            sa.Column("total_points", sa.Integer(), nullable=False),
            sa.Column("shots_on_net_pct", sa.Float(), nullable=True),
            sa.Column("zone_start_pct", sa.Float(), nullable=True),
            sa.Column("sat_pct", sa.Float(), nullable=True),
            sa.Column("time_on_ice_per_game", sa.String(10), nullable=True),
        ]),
        ("skater_stats_realtime", [
            sa.Column("games_played", sa.Integer(), nullable=False),
            sa.Column("hits", sa.Integer(), nullable=False),
            sa.Column("blocked_shots", sa.Integer(), nullable=False),
            sa.Column("missed_shots", sa.Integer(), nullable=False),
            sa.Column("giveaways", sa.Integer(), nullable=False),
            sa.Column("takeaways", sa.Integer(), nullable=False),
            sa.Column("time_on_ice", sa.String(20), nullable=True),
            sa.Column("hits_taken", sa.Integer(), nullable=False),
            sa.Column("shots_blocked", sa.Integer(), nullable=False),
        ]),
        ("skater_stats_shootout", [
            sa.Column("games_played", sa.Integer(), nullable=False),
            sa.Column("shootout_attempts", sa.Integer(), nullable=False),
            sa.Column("shootout_goals", sa.Integer(), nullable=False),
            sa.Column("shootout_pct", sa.Float(), nullable=True),
            sa.Column("shootout_game_deciding_goals", sa.Integer(), nullable=False),
        ]),
        ("skater_stats_shottype", [
            sa.Column("games_played", sa.Integer(), nullable=False),
            sa.Column("goals", sa.Integer(), nullable=False),
            sa.Column("shots", sa.Integer(), nullable=False),
            sa.Column("backhand_goals", sa.Integer(), nullable=False),
            sa.Column("wrist_goals", sa.Integer(), nullable=False),
            sa.Column("snap_goals", sa.Integer(), nullable=False),
            sa.Column("slap_goals", sa.Integer(), nullable=False),
            sa.Column("deflected_goals", sa.Integer(), nullable=False),
            sa.Column("tip_in_goals", sa.Integer(), nullable=False),
            sa.Column("wrap_around_goals", sa.Integer(), nullable=False),
        ]),
        ("skater_stats_timeonice", [
            sa.Column("games_played", sa.Integer(), nullable=False),
            sa.Column("ev_time_on_ice", sa.String(20), nullable=True),
            sa.Column("ev_time_on_ice_per_game", sa.String(20), nullable=True),
            sa.Column("pp_time_on_ice", sa.String(20), nullable=True),
            sa.Column("pp_time_on_ice_per_game", sa.String(20), nullable=True),
            sa.Column("sh_time_on_ice", sa.String(20), nullable=True),
            sa.Column("sh_time_on_ice_per_game", sa.String(20), nullable=True),
            sa.Column("total_time_on_ice", sa.String(20), nullable=True),
            sa.Column("total_time_on_ice_per_game", sa.String(20), nullable=True),
        ]),
        ("skater_stats_pointspergame", [
            sa.Column("games_played", sa.Integer(), nullable=False),
            sa.Column("goals", sa.Integer(), nullable=False),
            sa.Column("assists", sa.Integer(), nullable=False),
            sa.Column("points", sa.Integer(), nullable=False),
            sa.Column("points_per_game", sa.Float(), nullable=True),
            sa.Column("goals_per_game", sa.Float(), nullable=True),
            sa.Column("assists_per_game", sa.Float(), nullable=True),
            sa.Column("shots_per_game", sa.Float(), nullable=True),
        ]),
    ]:
        op.create_table(
            table_name,
            *_player_stats_cols(extra_cols),
            *player_fks,
            sa.PrimaryKeyConstraint("id"),
            sa.UniqueConstraint("player_id", "season_id", "team_id", "game_type_id"),
        )

    # goalie stats tables
    for table_name, extra_cols in [
        ("goalie_stats_summary", [
            sa.Column("games_played", sa.Integer(), nullable=False),
            sa.Column("games_started", sa.Integer(), nullable=False),
            sa.Column("wins", sa.Integer(), nullable=False),
            sa.Column("losses", sa.Integer(), nullable=False),
            sa.Column("ot_losses", sa.Integer(), nullable=False),
            sa.Column("shots_against", sa.Integer(), nullable=False),
            sa.Column("goals_against", sa.Integer(), nullable=False),
            sa.Column("goals_against_avg", sa.Float(), nullable=True),
            sa.Column("save_pct", sa.Float(), nullable=True),
            sa.Column("shutouts", sa.Integer(), nullable=False),
            sa.Column("time_on_ice", sa.String(20), nullable=True),
        ]),
        ("goalie_stats_advanced", [
            sa.Column("games_played", sa.Integer(), nullable=False),
            sa.Column("goals_against_avg", sa.Float(), nullable=True),
            sa.Column("save_pct", sa.Float(), nullable=True),
            sa.Column("ev_save_pct", sa.Float(), nullable=True),
            sa.Column("pp_save_pct", sa.Float(), nullable=True),
            sa.Column("sh_save_pct", sa.Float(), nullable=True),
            sa.Column("quality_starts", sa.Integer(), nullable=False),
            sa.Column("quality_start_pct", sa.Float(), nullable=True),
            sa.Column("goals_saved_above_avg", sa.Float(), nullable=True),
        ]),
        ("goalie_stats_bios", [
            sa.Column("games_played", sa.Integer(), nullable=False),
            sa.Column("birth_city", sa.String(100), nullable=True),
            sa.Column("birth_country", sa.String(10), nullable=True),
            sa.Column("nationality", sa.String(10), nullable=True),
            sa.Column("height_inches", sa.Integer(), nullable=True),
            sa.Column("weight_pounds", sa.Integer(), nullable=True),
            sa.Column("draft_year", sa.Integer(), nullable=True),
            sa.Column("draft_round", sa.Integer(), nullable=True),
            sa.Column("draft_overall", sa.Integer(), nullable=True),
        ]),
        ("goalie_stats_savesbystrength", [
            sa.Column("games_played", sa.Integer(), nullable=False),
            sa.Column("ev_shots_against", sa.Integer(), nullable=False),
            sa.Column("ev_goals_against", sa.Integer(), nullable=False),
            sa.Column("ev_save_pct", sa.Float(), nullable=True),
            sa.Column("pp_shots_against", sa.Integer(), nullable=False),
            sa.Column("pp_goals_against", sa.Integer(), nullable=False),
            sa.Column("pp_save_pct", sa.Float(), nullable=True),
            sa.Column("sh_shots_against", sa.Integer(), nullable=False),
            sa.Column("sh_goals_against", sa.Integer(), nullable=False),
            sa.Column("sh_save_pct", sa.Float(), nullable=True),
        ]),
        ("goalie_stats_shootout", [
            sa.Column("games_played", sa.Integer(), nullable=False),
            sa.Column("shootout_shots_against", sa.Integer(), nullable=False),
            sa.Column("shootout_goals_against", sa.Integer(), nullable=False),
            sa.Column("shootout_save_pct", sa.Float(), nullable=True),
            sa.Column("shootout_wins", sa.Integer(), nullable=False),
            sa.Column("shootout_losses", sa.Integer(), nullable=False),
        ]),
        ("goalie_stats_startedvsrelieved", [
            sa.Column("games_started", sa.Integer(), nullable=False),
            sa.Column("games_relieved", sa.Integer(), nullable=False),
            sa.Column("started_wins", sa.Integer(), nullable=False),
            sa.Column("relieved_wins", sa.Integer(), nullable=False),
            sa.Column("started_goals_against_avg", sa.Float(), nullable=True),
            sa.Column("relieved_goals_against_avg", sa.Float(), nullable=True),
            sa.Column("started_save_pct", sa.Float(), nullable=True),
            sa.Column("relieved_save_pct", sa.Float(), nullable=True),
        ]),
    ]:
        op.create_table(
            table_name,
            *_player_stats_cols(extra_cols),
            *player_fks,
            sa.PrimaryKeyConstraint("id"),
            sa.UniqueConstraint("player_id", "season_id", "team_id", "game_type_id"),
        )

    # team stats tables
    for table_name, extra_cols in [
        ("team_stats_summary", [
            sa.Column("games_played", sa.Integer(), nullable=False),
            sa.Column("wins", sa.Integer(), nullable=False),
            sa.Column("losses", sa.Integer(), nullable=False),
            sa.Column("ot_losses", sa.Integer(), nullable=False),
            sa.Column("points", sa.Integer(), nullable=False),
            sa.Column("goals_for", sa.Integer(), nullable=False),
            sa.Column("goals_against", sa.Integer(), nullable=False),
            sa.Column("shots_for_per_game", sa.Float(), nullable=True),
            sa.Column("shots_against_per_game", sa.Float(), nullable=True),
            sa.Column("pp_pct", sa.Float(), nullable=True),
            sa.Column("pk_pct", sa.Float(), nullable=True),
        ]),
        ("team_stats_faceoffpercentages", [
            sa.Column("games_played", sa.Integer(), nullable=False),
            sa.Column("faceoff_wins", sa.Integer(), nullable=False),
            sa.Column("faceoff_losses", sa.Integer(), nullable=False),
            sa.Column("faceoff_pct", sa.Float(), nullable=True),
            sa.Column("d_zone_faceoff_pct", sa.Float(), nullable=True),
            sa.Column("o_zone_faceoff_pct", sa.Float(), nullable=True),
            sa.Column("n_zone_faceoff_pct", sa.Float(), nullable=True),
        ]),
        ("team_stats_faceoffwins", [
            sa.Column("games_played", sa.Integer(), nullable=False),
            sa.Column("total_faceoff_wins", sa.Integer(), nullable=False),
            sa.Column("d_zone_faceoff_wins", sa.Integer(), nullable=False),
            sa.Column("o_zone_faceoff_wins", sa.Integer(), nullable=False),
            sa.Column("n_zone_faceoff_wins", sa.Integer(), nullable=False),
            sa.Column("ev_faceoff_wins", sa.Integer(), nullable=False),
            sa.Column("pp_faceoff_wins", sa.Integer(), nullable=False),
            sa.Column("sh_faceoff_wins", sa.Integer(), nullable=False),
        ]),
        ("team_stats_goalsagainstbystrength", [
            sa.Column("games_played", sa.Integer(), nullable=False),
            sa.Column("ev_goals_against", sa.Integer(), nullable=False),
            sa.Column("pp_goals_against", sa.Integer(), nullable=False),
            sa.Column("sh_goals_against", sa.Integer(), nullable=False),
            sa.Column("en_goals_against", sa.Integer(), nullable=False),
            sa.Column("total_goals_against", sa.Integer(), nullable=False),
        ]),
        ("team_stats_goalsforbystrength", [
            sa.Column("games_played", sa.Integer(), nullable=False),
            sa.Column("ev_goals_for", sa.Integer(), nullable=False),
            sa.Column("pp_goals_for", sa.Integer(), nullable=False),
            sa.Column("sh_goals_for", sa.Integer(), nullable=False),
            sa.Column("en_goals_for", sa.Integer(), nullable=False),
            sa.Column("total_goals_for", sa.Integer(), nullable=False),
        ]),
        ("team_stats_goalsleaders", [
            sa.Column("games_played", sa.Integer(), nullable=False),
            sa.Column("goals_leader_player_id", sa.Integer(), nullable=True),
            sa.Column("goals_leader_goals", sa.Integer(), nullable=False),
            sa.Column("assists_leader_player_id", sa.Integer(), nullable=True),
            sa.Column("assists_leader_assists", sa.Integer(), nullable=False),
            sa.Column("points_leader_player_id", sa.Integer(), nullable=True),
            sa.Column("points_leader_points", sa.Integer(), nullable=False),
        ]),
        ("team_stats_powerplay", [
            sa.Column("games_played", sa.Integer(), nullable=False),
            sa.Column("pp_goals_for", sa.Integer(), nullable=False),
            sa.Column("pp_opportunities", sa.Integer(), nullable=False),
            sa.Column("pp_pct", sa.Float(), nullable=True),
            sa.Column("pp_goals_against", sa.Integer(), nullable=False),
            sa.Column("pp_toi", sa.String(20), nullable=True),
            sa.Column("pp_shots_for", sa.Integer(), nullable=False),
            sa.Column("pp_shooting_pct", sa.Float(), nullable=True),
        ]),
        ("team_stats_penaltykill", [
            sa.Column("games_played", sa.Integer(), nullable=False),
            sa.Column("pk_goals_against", sa.Integer(), nullable=False),
            sa.Column("pk_times_shorthanded", sa.Integer(), nullable=False),
            sa.Column("pk_pct", sa.Float(), nullable=True),
            sa.Column("pk_toi", sa.String(20), nullable=True),
            sa.Column("sh_goals_for", sa.Integer(), nullable=False),
            sa.Column("sh_shots_for", sa.Integer(), nullable=False),
        ]),
        ("team_stats_realtime", [
            sa.Column("games_played", sa.Integer(), nullable=False),
            sa.Column("hits", sa.Integer(), nullable=False),
            sa.Column("blocked_shots", sa.Integer(), nullable=False),
            sa.Column("missed_shots", sa.Integer(), nullable=False),
            sa.Column("giveaways", sa.Integer(), nullable=False),
            sa.Column("takeaways", sa.Integer(), nullable=False),
            sa.Column("hits_per_game", sa.Float(), nullable=True),
            sa.Column("blocked_shots_per_game", sa.Float(), nullable=True),
        ]),
        ("team_stats_penalties", [
            sa.Column("games_played", sa.Integer(), nullable=False),
            sa.Column("pim", sa.Integer(), nullable=False),
            sa.Column("penalties", sa.Integer(), nullable=False),
            sa.Column("minor_penalties", sa.Integer(), nullable=False),
            sa.Column("major_penalties", sa.Integer(), nullable=False),
            sa.Column("misconduct_penalties", sa.Integer(), nullable=False),
            sa.Column("net_penalties", sa.Integer(), nullable=False),
            sa.Column("pim_drawn", sa.Integer(), nullable=False),
        ]),
        ("team_stats_penaltyshots", [
            sa.Column("games_played", sa.Integer(), nullable=False),
            sa.Column("penalty_shots_for", sa.Integer(), nullable=False),
            sa.Column("penalty_shot_goals_for", sa.Integer(), nullable=False),
            sa.Column("penalty_shot_pct_for", sa.Float(), nullable=True),
            sa.Column("penalty_shots_against", sa.Integer(), nullable=False),
            sa.Column("penalty_shot_goals_against", sa.Integer(), nullable=False),
            sa.Column("penalty_shot_save_pct", sa.Float(), nullable=True),
        ]),
        ("team_stats_pointspergame", [
            sa.Column("games_played", sa.Integer(), nullable=False),
            sa.Column("points", sa.Integer(), nullable=False),
            sa.Column("points_per_game", sa.Float(), nullable=True),
            sa.Column("goals_for_per_game", sa.Float(), nullable=True),
            sa.Column("goals_against_per_game", sa.Float(), nullable=True),
            sa.Column("shots_for_per_game", sa.Float(), nullable=True),
            sa.Column("shots_against_per_game", sa.Float(), nullable=True),
        ]),
        ("team_stats_percentages", [
            sa.Column("games_played", sa.Integer(), nullable=False),
            sa.Column("shooting_pct", sa.Float(), nullable=True),
            sa.Column("save_pct", sa.Float(), nullable=True),
            sa.Column("pdo", sa.Float(), nullable=True),
            sa.Column("faceoff_pct", sa.Float(), nullable=True),
            sa.Column("pp_pct", sa.Float(), nullable=True),
            sa.Column("pk_pct", sa.Float(), nullable=True),
            sa.Column("sat_pct", sa.Float(), nullable=True),
        ]),
        ("team_stats_scoretrail", [
            sa.Column("games_played", sa.Integer(), nullable=False),
            sa.Column("wins_trailing", sa.Integer(), nullable=False),
            sa.Column("wins_tied", sa.Integer(), nullable=False),
            sa.Column("wins_leading", sa.Integer(), nullable=False),
            sa.Column("losses_trailing", sa.Integer(), nullable=False),
            sa.Column("losses_tied", sa.Integer(), nullable=False),
            sa.Column("losses_leading", sa.Integer(), nullable=False),
            sa.Column("games_trailing", sa.Integer(), nullable=False),
        ]),
        ("team_stats_shootout", [
            sa.Column("games_played", sa.Integer(), nullable=False),
            sa.Column("shootout_wins", sa.Integer(), nullable=False),
            sa.Column("shootout_losses", sa.Integer(), nullable=False),
            sa.Column("shootout_goals_for", sa.Integer(), nullable=False),
            sa.Column("shootout_goals_against", sa.Integer(), nullable=False),
            sa.Column("shootout_attempts", sa.Integer(), nullable=False),
            sa.Column("shootout_pct", sa.Float(), nullable=True),
            sa.Column("shootout_save_pct", sa.Float(), nullable=True),
        ]),
    ]:
        op.create_table(
            table_name,
            *_team_stats_cols(extra_cols),
            *team_fks,
            sa.PrimaryKeyConstraint("id"),
            sa.UniqueConstraint("team_id", "season_id", "game_type_id"),
        )


def downgrade() -> None:
    # Drop in reverse FK dependency order
    team_stat_tables = [
        "team_stats_shootout", "team_stats_scoretrail", "team_stats_percentages",
        "team_stats_pointspergame", "team_stats_penaltyshots", "team_stats_penalties",
        "team_stats_realtime", "team_stats_penaltykill", "team_stats_powerplay",
        "team_stats_goalsleaders", "team_stats_goalsforbystrength",
        "team_stats_goalsagainstbystrength", "team_stats_faceoffwins",
        "team_stats_faceoffpercentages", "team_stats_summary",
    ]
    goalie_stat_tables = [
        "goalie_stats_startedvsrelieved", "goalie_stats_shootout",
        "goalie_stats_savesbystrength", "goalie_stats_bios",
        "goalie_stats_advanced", "goalie_stats_summary",
    ]
    skater_stat_tables = [
        "skater_stats_pointspergame", "skater_stats_timeonice", "skater_stats_shottype",
        "skater_stats_shootout", "skater_stats_realtime", "skater_stats_puckpossessions",
        "skater_stats_powerplay", "skater_stats_penaltyshots", "skater_stats_penaltykill",
        "skater_stats_penalties", "skater_stats_goalsforagainst", "skater_stats_faceoffwins",
        "skater_stats_faceoffpercentages", "skater_stats_bios", "skater_stats_summary",
    ]
    for t in team_stat_tables + goalie_stat_tables + skater_stat_tables:
        op.drop_table(t)

    op.drop_table("draft_picks")
    op.drop_table("standings_snapshots")
    op.drop_table("pbp_period_events")
    op.drop_table("pbp_stoppages")
    op.drop_table("pbp_penalties")
    op.drop_table("pbp_faceoffs")
    op.drop_table("pbp_hits")
    op.drop_table("pbp_blocked_shots")
    op.drop_table("pbp_missed_shots")
    op.drop_table("pbp_shots")
    op.drop_table("pbp_goals")
    op.drop_index("ix_pbp_event_type", "play_by_play_events")
    op.drop_index("ix_pbp_game_id", "play_by_play_events")
    op.drop_table("play_by_play_events")
    op.drop_table("game_boxscores")
    op.drop_table("games")
    op.drop_table("rosters")
    op.drop_table("players")
    op.drop_table("teams")
    op.drop_table("franchises")
    op.drop_table("seasons")
