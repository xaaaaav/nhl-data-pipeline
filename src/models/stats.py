from sqlalchemy import Float, ForeignKey, Integer, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from src.models.base import Base, TimestampMixin

# ---------------------------------------------------------------------------
# Skater stats
# ---------------------------------------------------------------------------


class SkaterStatsSummary(TimestampMixin, Base):
    __tablename__ = "skater_stats_summary"
    __table_args__ = (
        UniqueConstraint("player_id", "season_id", "team_id", "game_type_id"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    player_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("players.player_id"), nullable=False
    )
    season_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("seasons.season_id"), nullable=False
    )
    team_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("teams.team_id"), nullable=False
    )
    game_type_id: Mapped[int] = mapped_column(Integer, nullable=False)
    games_played: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    goals: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    assists: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    points: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    plus_minus: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    pim: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    shots: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    shooting_pct: Mapped[float | None] = mapped_column(Float, nullable=True)
    time_on_ice_per_game: Mapped[str | None] = mapped_column(String(10), nullable=True)
    pp_goals: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    sh_goals: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    game_winning_goals: Mapped[int] = mapped_column(Integer, nullable=False, default=0)


class SkaterStatsBios(TimestampMixin, Base):
    __tablename__ = "skater_stats_bios"
    __table_args__ = (
        UniqueConstraint("player_id", "season_id", "team_id", "game_type_id"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    player_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("players.player_id"), nullable=False
    )
    season_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("seasons.season_id"), nullable=False
    )
    team_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("teams.team_id"), nullable=False
    )
    game_type_id: Mapped[int] = mapped_column(Integer, nullable=False)
    games_played: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    birth_city: Mapped[str | None] = mapped_column(String(100), nullable=True)
    birth_country: Mapped[str | None] = mapped_column(String(10), nullable=True)
    nationality: Mapped[str | None] = mapped_column(String(10), nullable=True)
    height_inches: Mapped[int | None] = mapped_column(Integer, nullable=True)
    weight_pounds: Mapped[int | None] = mapped_column(Integer, nullable=True)
    draft_year: Mapped[int | None] = mapped_column(Integer, nullable=True)
    draft_round: Mapped[int | None] = mapped_column(Integer, nullable=True)
    draft_pick: Mapped[int | None] = mapped_column(Integer, nullable=True)
    draft_overall: Mapped[int | None] = mapped_column(Integer, nullable=True)


class SkaterStatsFaceoffPercentages(TimestampMixin, Base):
    __tablename__ = "skater_stats_faceoffpercentages"
    __table_args__ = (
        UniqueConstraint("player_id", "season_id", "team_id", "game_type_id"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    player_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("players.player_id"), nullable=False
    )
    season_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("seasons.season_id"), nullable=False
    )
    team_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("teams.team_id"), nullable=False
    )
    game_type_id: Mapped[int] = mapped_column(Integer, nullable=False)
    games_played: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    total_faceoffs: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    faceoff_wins: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    faceoff_losses: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    faceoff_pct: Mapped[float | None] = mapped_column(Float, nullable=True)
    d_zone_faceoff_pct: Mapped[float | None] = mapped_column(Float, nullable=True)
    n_zone_faceoff_pct: Mapped[float | None] = mapped_column(Float, nullable=True)
    o_zone_faceoff_pct: Mapped[float | None] = mapped_column(Float, nullable=True)


class SkaterStatsFaceoffWins(TimestampMixin, Base):
    __tablename__ = "skater_stats_faceoffwins"
    __table_args__ = (
        UniqueConstraint("player_id", "season_id", "team_id", "game_type_id"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    player_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("players.player_id"), nullable=False
    )
    season_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("seasons.season_id"), nullable=False
    )
    team_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("teams.team_id"), nullable=False
    )
    game_type_id: Mapped[int] = mapped_column(Integer, nullable=False)
    games_played: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    total_faceoff_wins: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    d_zone_faceoff_wins: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    n_zone_faceoff_wins: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    o_zone_faceoff_wins: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    ev_faceoff_wins: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    pp_faceoff_wins: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    sh_faceoff_wins: Mapped[int] = mapped_column(Integer, nullable=False, default=0)


class SkaterStatsGoalsForAgainst(TimestampMixin, Base):
    __tablename__ = "skater_stats_goalsforagainst"
    __table_args__ = (
        UniqueConstraint("player_id", "season_id", "team_id", "game_type_id"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    player_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("players.player_id"), nullable=False
    )
    season_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("seasons.season_id"), nullable=False
    )
    team_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("teams.team_id"), nullable=False
    )
    game_type_id: Mapped[int] = mapped_column(Integer, nullable=False)
    games_played: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    ev_goals_for: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    ev_goals_against: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    pp_goals_for: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    pp_goals_against: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    sh_goals_for: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    sh_goals_against: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    on_ice_shooting_pct: Mapped[float | None] = mapped_column(Float, nullable=True)
    on_ice_save_pct: Mapped[float | None] = mapped_column(Float, nullable=True)


class SkaterStatsPenalties(TimestampMixin, Base):
    __tablename__ = "skater_stats_penalties"
    __table_args__ = (
        UniqueConstraint("player_id", "season_id", "team_id", "game_type_id"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    player_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("players.player_id"), nullable=False
    )
    season_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("seasons.season_id"), nullable=False
    )
    team_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("teams.team_id"), nullable=False
    )
    game_type_id: Mapped[int] = mapped_column(Integer, nullable=False)
    games_played: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    pim: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    penalties: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    minor_penalties: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    major_penalties: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    misconduct_penalties: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    penalties_drawn: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    pim_drawn: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    net_penalties: Mapped[int] = mapped_column(Integer, nullable=False, default=0)


class SkaterStatsPenaltyKill(TimestampMixin, Base):
    __tablename__ = "skater_stats_penaltykill"
    __table_args__ = (
        UniqueConstraint("player_id", "season_id", "team_id", "game_type_id"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    player_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("players.player_id"), nullable=False
    )
    season_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("seasons.season_id"), nullable=False
    )
    team_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("teams.team_id"), nullable=False
    )
    game_type_id: Mapped[int] = mapped_column(Integer, nullable=False)
    games_played: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    sh_goals: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    sh_assists: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    sh_points: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    sh_shots: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    sh_toi: Mapped[str | None] = mapped_column(String(20), nullable=True)
    sh_toi_per_game: Mapped[str | None] = mapped_column(String(20), nullable=True)
    sh_shooting_pct: Mapped[float | None] = mapped_column(Float, nullable=True)


class SkaterStatsPenaltyShots(TimestampMixin, Base):
    __tablename__ = "skater_stats_penaltyshots"
    __table_args__ = (
        UniqueConstraint("player_id", "season_id", "team_id", "game_type_id"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    player_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("players.player_id"), nullable=False
    )
    season_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("seasons.season_id"), nullable=False
    )
    team_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("teams.team_id"), nullable=False
    )
    game_type_id: Mapped[int] = mapped_column(Integer, nullable=False)
    games_played: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    penalty_shots_attempts: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    penalty_shots_goals: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    penalty_shot_pct: Mapped[float | None] = mapped_column(Float, nullable=True)


class SkaterStatsPowerplay(TimestampMixin, Base):
    __tablename__ = "skater_stats_powerplay"
    __table_args__ = (
        UniqueConstraint("player_id", "season_id", "team_id", "game_type_id"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    player_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("players.player_id"), nullable=False
    )
    season_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("seasons.season_id"), nullable=False
    )
    team_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("teams.team_id"), nullable=False
    )
    game_type_id: Mapped[int] = mapped_column(Integer, nullable=False)
    games_played: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    pp_goals: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    pp_assists: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    pp_points: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    pp_shots: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    pp_toi: Mapped[str | None] = mapped_column(String(20), nullable=True)
    pp_toi_per_game: Mapped[str | None] = mapped_column(String(20), nullable=True)
    pp_shooting_pct: Mapped[float | None] = mapped_column(Float, nullable=True)


class SkaterStatsPuckPossessions(TimestampMixin, Base):
    __tablename__ = "skater_stats_puckpossessions"
    __table_args__ = (
        UniqueConstraint("player_id", "season_id", "team_id", "game_type_id"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    player_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("players.player_id"), nullable=False
    )
    season_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("seasons.season_id"), nullable=False
    )
    team_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("teams.team_id"), nullable=False
    )
    game_type_id: Mapped[int] = mapped_column(Integer, nullable=False)
    games_played: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    goals: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    total_primary_assists: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    total_secondary_assists: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    total_points: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    shots_on_net_pct: Mapped[float | None] = mapped_column(Float, nullable=True)
    zone_start_pct: Mapped[float | None] = mapped_column(Float, nullable=True)
    sat_pct: Mapped[float | None] = mapped_column(Float, nullable=True)
    time_on_ice_per_game: Mapped[str | None] = mapped_column(String(10), nullable=True)


class SkaterStatsRealtime(TimestampMixin, Base):
    __tablename__ = "skater_stats_realtime"
    __table_args__ = (
        UniqueConstraint("player_id", "season_id", "team_id", "game_type_id"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    player_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("players.player_id"), nullable=False
    )
    season_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("seasons.season_id"), nullable=False
    )
    team_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("teams.team_id"), nullable=False
    )
    game_type_id: Mapped[int] = mapped_column(Integer, nullable=False)
    games_played: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    hits: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    blocked_shots: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    missed_shots: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    giveaways: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    takeaways: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    time_on_ice: Mapped[str | None] = mapped_column(String(20), nullable=True)
    hits_taken: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    shots_blocked: Mapped[int] = mapped_column(Integer, nullable=False, default=0)


class SkaterStatsShootout(TimestampMixin, Base):
    __tablename__ = "skater_stats_shootout"
    __table_args__ = (
        UniqueConstraint("player_id", "season_id", "team_id", "game_type_id"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    player_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("players.player_id"), nullable=False
    )
    season_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("seasons.season_id"), nullable=False
    )
    team_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("teams.team_id"), nullable=False
    )
    game_type_id: Mapped[int] = mapped_column(Integer, nullable=False)
    games_played: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    shootout_attempts: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    shootout_goals: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    shootout_pct: Mapped[float | None] = mapped_column(Float, nullable=True)
    shootout_game_deciding_goals: Mapped[int] = mapped_column(
        Integer, nullable=False, default=0
    )


class SkaterStatsShottype(TimestampMixin, Base):
    __tablename__ = "skater_stats_shottype"
    __table_args__ = (
        UniqueConstraint("player_id", "season_id", "team_id", "game_type_id"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    player_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("players.player_id"), nullable=False
    )
    season_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("seasons.season_id"), nullable=False
    )
    team_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("teams.team_id"), nullable=False
    )
    game_type_id: Mapped[int] = mapped_column(Integer, nullable=False)
    games_played: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    goals: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    shots: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    backhand_goals: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    wrist_goals: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    snap_goals: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    slap_goals: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    deflected_goals: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    tip_in_goals: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    wrap_around_goals: Mapped[int] = mapped_column(Integer, nullable=False, default=0)


class SkaterStatsTimeOnIce(TimestampMixin, Base):
    __tablename__ = "skater_stats_timeonice"
    __table_args__ = (
        UniqueConstraint("player_id", "season_id", "team_id", "game_type_id"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    player_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("players.player_id"), nullable=False
    )
    season_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("seasons.season_id"), nullable=False
    )
    team_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("teams.team_id"), nullable=False
    )
    game_type_id: Mapped[int] = mapped_column(Integer, nullable=False)
    games_played: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    ev_time_on_ice: Mapped[str | None] = mapped_column(String(20), nullable=True)
    ev_time_on_ice_per_game: Mapped[str | None] = mapped_column(String(20), nullable=True)
    pp_time_on_ice: Mapped[str | None] = mapped_column(String(20), nullable=True)
    pp_time_on_ice_per_game: Mapped[str | None] = mapped_column(String(20), nullable=True)
    sh_time_on_ice: Mapped[str | None] = mapped_column(String(20), nullable=True)
    sh_time_on_ice_per_game: Mapped[str | None] = mapped_column(String(20), nullable=True)
    total_time_on_ice: Mapped[str | None] = mapped_column(String(20), nullable=True)
    total_time_on_ice_per_game: Mapped[str | None] = mapped_column(String(20), nullable=True)


class SkaterStatsPointsPerGame(TimestampMixin, Base):
    __tablename__ = "skater_stats_pointspergame"
    __table_args__ = (
        UniqueConstraint("player_id", "season_id", "team_id", "game_type_id"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    player_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("players.player_id"), nullable=False
    )
    season_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("seasons.season_id"), nullable=False
    )
    team_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("teams.team_id"), nullable=False
    )
    game_type_id: Mapped[int] = mapped_column(Integer, nullable=False)
    games_played: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    goals: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    assists: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    points: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    points_per_game: Mapped[float | None] = mapped_column(Float, nullable=True)
    goals_per_game: Mapped[float | None] = mapped_column(Float, nullable=True)
    assists_per_game: Mapped[float | None] = mapped_column(Float, nullable=True)
    shots_per_game: Mapped[float | None] = mapped_column(Float, nullable=True)


# ---------------------------------------------------------------------------
# Goalie stats
# ---------------------------------------------------------------------------


class GoalieStatsSummary(TimestampMixin, Base):
    __tablename__ = "goalie_stats_summary"
    __table_args__ = (
        UniqueConstraint("player_id", "season_id", "team_id", "game_type_id"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    player_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("players.player_id"), nullable=False
    )
    season_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("seasons.season_id"), nullable=False
    )
    team_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("teams.team_id"), nullable=False
    )
    game_type_id: Mapped[int] = mapped_column(Integer, nullable=False)
    games_played: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    games_started: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    wins: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    losses: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    ot_losses: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    shots_against: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    goals_against: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    goals_against_avg: Mapped[float | None] = mapped_column(Float, nullable=True)
    save_pct: Mapped[float | None] = mapped_column(Float, nullable=True)
    shutouts: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    time_on_ice: Mapped[str | None] = mapped_column(String(20), nullable=True)


class GoalieStatsAdvanced(TimestampMixin, Base):
    __tablename__ = "goalie_stats_advanced"
    __table_args__ = (
        UniqueConstraint("player_id", "season_id", "team_id", "game_type_id"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    player_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("players.player_id"), nullable=False
    )
    season_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("seasons.season_id"), nullable=False
    )
    team_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("teams.team_id"), nullable=False
    )
    game_type_id: Mapped[int] = mapped_column(Integer, nullable=False)
    games_played: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    goals_against_avg: Mapped[float | None] = mapped_column(Float, nullable=True)
    save_pct: Mapped[float | None] = mapped_column(Float, nullable=True)
    ev_save_pct: Mapped[float | None] = mapped_column(Float, nullable=True)
    pp_save_pct: Mapped[float | None] = mapped_column(Float, nullable=True)
    sh_save_pct: Mapped[float | None] = mapped_column(Float, nullable=True)
    quality_starts: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    quality_start_pct: Mapped[float | None] = mapped_column(Float, nullable=True)
    goals_saved_above_avg: Mapped[float | None] = mapped_column(Float, nullable=True)


class GoalieStatsBios(TimestampMixin, Base):
    __tablename__ = "goalie_stats_bios"
    __table_args__ = (
        UniqueConstraint("player_id", "season_id", "team_id", "game_type_id"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    player_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("players.player_id"), nullable=False
    )
    season_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("seasons.season_id"), nullable=False
    )
    team_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("teams.team_id"), nullable=False
    )
    game_type_id: Mapped[int] = mapped_column(Integer, nullable=False)
    games_played: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    birth_city: Mapped[str | None] = mapped_column(String(100), nullable=True)
    birth_country: Mapped[str | None] = mapped_column(String(10), nullable=True)
    nationality: Mapped[str | None] = mapped_column(String(10), nullable=True)
    height_inches: Mapped[int | None] = mapped_column(Integer, nullable=True)
    weight_pounds: Mapped[int | None] = mapped_column(Integer, nullable=True)
    draft_year: Mapped[int | None] = mapped_column(Integer, nullable=True)
    draft_round: Mapped[int | None] = mapped_column(Integer, nullable=True)
    draft_overall: Mapped[int | None] = mapped_column(Integer, nullable=True)


class GoalieStatsSavesByStrength(TimestampMixin, Base):
    __tablename__ = "goalie_stats_savesbystrength"
    __table_args__ = (
        UniqueConstraint("player_id", "season_id", "team_id", "game_type_id"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    player_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("players.player_id"), nullable=False
    )
    season_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("seasons.season_id"), nullable=False
    )
    team_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("teams.team_id"), nullable=False
    )
    game_type_id: Mapped[int] = mapped_column(Integer, nullable=False)
    games_played: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    ev_shots_against: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    ev_goals_against: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    ev_save_pct: Mapped[float | None] = mapped_column(Float, nullable=True)
    pp_shots_against: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    pp_goals_against: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    pp_save_pct: Mapped[float | None] = mapped_column(Float, nullable=True)
    sh_shots_against: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    sh_goals_against: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    sh_save_pct: Mapped[float | None] = mapped_column(Float, nullable=True)


class GoalieStatsShootout(TimestampMixin, Base):
    __tablename__ = "goalie_stats_shootout"
    __table_args__ = (
        UniqueConstraint("player_id", "season_id", "team_id", "game_type_id"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    player_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("players.player_id"), nullable=False
    )
    season_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("seasons.season_id"), nullable=False
    )
    team_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("teams.team_id"), nullable=False
    )
    game_type_id: Mapped[int] = mapped_column(Integer, nullable=False)
    games_played: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    shootout_shots_against: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    shootout_goals_against: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    shootout_save_pct: Mapped[float | None] = mapped_column(Float, nullable=True)
    shootout_wins: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    shootout_losses: Mapped[int] = mapped_column(Integer, nullable=False, default=0)


class GoalieStatsStartedVsRelieved(TimestampMixin, Base):
    __tablename__ = "goalie_stats_startedvsrelieved"
    __table_args__ = (
        UniqueConstraint("player_id", "season_id", "team_id", "game_type_id"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    player_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("players.player_id"), nullable=False
    )
    season_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("seasons.season_id"), nullable=False
    )
    team_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("teams.team_id"), nullable=False
    )
    game_type_id: Mapped[int] = mapped_column(Integer, nullable=False)
    games_started: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    games_relieved: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    started_wins: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    relieved_wins: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    started_goals_against_avg: Mapped[float | None] = mapped_column(Float, nullable=True)
    relieved_goals_against_avg: Mapped[float | None] = mapped_column(Float, nullable=True)
    started_save_pct: Mapped[float | None] = mapped_column(Float, nullable=True)
    relieved_save_pct: Mapped[float | None] = mapped_column(Float, nullable=True)


# ---------------------------------------------------------------------------
# Team stats
# ---------------------------------------------------------------------------


class TeamStatsSummary(TimestampMixin, Base):
    __tablename__ = "team_stats_summary"
    __table_args__ = (UniqueConstraint("team_id", "season_id", "game_type_id"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    team_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("teams.team_id"), nullable=False
    )
    season_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("seasons.season_id"), nullable=False
    )
    game_type_id: Mapped[int] = mapped_column(Integer, nullable=False)
    games_played: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    wins: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    losses: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    ot_losses: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    points: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    goals_for: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    goals_against: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    shots_for_per_game: Mapped[float | None] = mapped_column(Float, nullable=True)
    shots_against_per_game: Mapped[float | None] = mapped_column(Float, nullable=True)
    pp_pct: Mapped[float | None] = mapped_column(Float, nullable=True)
    pk_pct: Mapped[float | None] = mapped_column(Float, nullable=True)


class TeamStatsFaceoffPercentages(TimestampMixin, Base):
    __tablename__ = "team_stats_faceoffpercentages"
    __table_args__ = (UniqueConstraint("team_id", "season_id", "game_type_id"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    team_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("teams.team_id"), nullable=False
    )
    season_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("seasons.season_id"), nullable=False
    )
    game_type_id: Mapped[int] = mapped_column(Integer, nullable=False)
    games_played: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    faceoff_wins: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    faceoff_losses: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    faceoff_pct: Mapped[float | None] = mapped_column(Float, nullable=True)
    d_zone_faceoff_pct: Mapped[float | None] = mapped_column(Float, nullable=True)
    o_zone_faceoff_pct: Mapped[float | None] = mapped_column(Float, nullable=True)
    n_zone_faceoff_pct: Mapped[float | None] = mapped_column(Float, nullable=True)


class TeamStatsFaceoffWins(TimestampMixin, Base):
    __tablename__ = "team_stats_faceoffwins"
    __table_args__ = (UniqueConstraint("team_id", "season_id", "game_type_id"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    team_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("teams.team_id"), nullable=False
    )
    season_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("seasons.season_id"), nullable=False
    )
    game_type_id: Mapped[int] = mapped_column(Integer, nullable=False)
    games_played: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    total_faceoff_wins: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    d_zone_faceoff_wins: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    o_zone_faceoff_wins: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    n_zone_faceoff_wins: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    ev_faceoff_wins: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    pp_faceoff_wins: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    sh_faceoff_wins: Mapped[int] = mapped_column(Integer, nullable=False, default=0)


class TeamStatsGoalsAgainstByStrength(TimestampMixin, Base):
    __tablename__ = "team_stats_goalsagainstbystrength"
    __table_args__ = (UniqueConstraint("team_id", "season_id", "game_type_id"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    team_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("teams.team_id"), nullable=False
    )
    season_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("seasons.season_id"), nullable=False
    )
    game_type_id: Mapped[int] = mapped_column(Integer, nullable=False)
    games_played: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    ev_goals_against: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    pp_goals_against: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    sh_goals_against: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    en_goals_against: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    total_goals_against: Mapped[int] = mapped_column(Integer, nullable=False, default=0)


class TeamStatsGoalsForByStrength(TimestampMixin, Base):
    __tablename__ = "team_stats_goalsforbystrength"
    __table_args__ = (UniqueConstraint("team_id", "season_id", "game_type_id"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    team_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("teams.team_id"), nullable=False
    )
    season_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("seasons.season_id"), nullable=False
    )
    game_type_id: Mapped[int] = mapped_column(Integer, nullable=False)
    games_played: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    ev_goals_for: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    pp_goals_for: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    sh_goals_for: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    en_goals_for: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    total_goals_for: Mapped[int] = mapped_column(Integer, nullable=False, default=0)


class TeamStatsGoalsLeaders(TimestampMixin, Base):
    __tablename__ = "team_stats_goalsleaders"
    __table_args__ = (UniqueConstraint("team_id", "season_id", "game_type_id"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    team_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("teams.team_id"), nullable=False
    )
    season_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("seasons.season_id"), nullable=False
    )
    game_type_id: Mapped[int] = mapped_column(Integer, nullable=False)
    games_played: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    goals_leader_player_id: Mapped[int | None] = mapped_column(
        Integer, ForeignKey("players.player_id"), nullable=True
    )
    goals_leader_goals: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    assists_leader_player_id: Mapped[int | None] = mapped_column(
        Integer, ForeignKey("players.player_id"), nullable=True
    )
    assists_leader_assists: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    points_leader_player_id: Mapped[int | None] = mapped_column(
        Integer, ForeignKey("players.player_id"), nullable=True
    )
    points_leader_points: Mapped[int] = mapped_column(Integer, nullable=False, default=0)


class TeamStatsPowerplay(TimestampMixin, Base):
    __tablename__ = "team_stats_powerplay"
    __table_args__ = (UniqueConstraint("team_id", "season_id", "game_type_id"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    team_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("teams.team_id"), nullable=False
    )
    season_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("seasons.season_id"), nullable=False
    )
    game_type_id: Mapped[int] = mapped_column(Integer, nullable=False)
    games_played: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    pp_goals_for: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    pp_opportunities: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    pp_pct: Mapped[float | None] = mapped_column(Float, nullable=True)
    pp_goals_against: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    pp_toi: Mapped[str | None] = mapped_column(String(20), nullable=True)
    pp_shots_for: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    pp_shooting_pct: Mapped[float | None] = mapped_column(Float, nullable=True)


class TeamStatsPenaltyKill(TimestampMixin, Base):
    __tablename__ = "team_stats_penaltykill"
    __table_args__ = (UniqueConstraint("team_id", "season_id", "game_type_id"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    team_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("teams.team_id"), nullable=False
    )
    season_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("seasons.season_id"), nullable=False
    )
    game_type_id: Mapped[int] = mapped_column(Integer, nullable=False)
    games_played: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    pk_goals_against: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    pk_times_shorthanded: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    pk_pct: Mapped[float | None] = mapped_column(Float, nullable=True)
    pk_toi: Mapped[str | None] = mapped_column(String(20), nullable=True)
    sh_goals_for: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    sh_shots_for: Mapped[int] = mapped_column(Integer, nullable=False, default=0)


class TeamStatsRealtime(TimestampMixin, Base):
    __tablename__ = "team_stats_realtime"
    __table_args__ = (UniqueConstraint("team_id", "season_id", "game_type_id"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    team_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("teams.team_id"), nullable=False
    )
    season_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("seasons.season_id"), nullable=False
    )
    game_type_id: Mapped[int] = mapped_column(Integer, nullable=False)
    games_played: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    hits: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    blocked_shots: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    missed_shots: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    giveaways: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    takeaways: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    hits_per_game: Mapped[float | None] = mapped_column(Float, nullable=True)
    blocked_shots_per_game: Mapped[float | None] = mapped_column(Float, nullable=True)


class TeamStatsPenalties(TimestampMixin, Base):
    __tablename__ = "team_stats_penalties"
    __table_args__ = (UniqueConstraint("team_id", "season_id", "game_type_id"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    team_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("teams.team_id"), nullable=False
    )
    season_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("seasons.season_id"), nullable=False
    )
    game_type_id: Mapped[int] = mapped_column(Integer, nullable=False)
    games_played: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    pim: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    penalties: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    minor_penalties: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    major_penalties: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    misconduct_penalties: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    net_penalties: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    pim_drawn: Mapped[int] = mapped_column(Integer, nullable=False, default=0)


class TeamStatsPenaltyShots(TimestampMixin, Base):
    __tablename__ = "team_stats_penaltyshots"
    __table_args__ = (UniqueConstraint("team_id", "season_id", "game_type_id"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    team_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("teams.team_id"), nullable=False
    )
    season_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("seasons.season_id"), nullable=False
    )
    game_type_id: Mapped[int] = mapped_column(Integer, nullable=False)
    games_played: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    penalty_shots_for: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    penalty_shot_goals_for: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    penalty_shot_pct_for: Mapped[float | None] = mapped_column(Float, nullable=True)
    penalty_shots_against: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    penalty_shot_goals_against: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    penalty_shot_save_pct: Mapped[float | None] = mapped_column(Float, nullable=True)


class TeamStatsPointsPerGame(TimestampMixin, Base):
    __tablename__ = "team_stats_pointspergame"
    __table_args__ = (UniqueConstraint("team_id", "season_id", "game_type_id"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    team_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("teams.team_id"), nullable=False
    )
    season_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("seasons.season_id"), nullable=False
    )
    game_type_id: Mapped[int] = mapped_column(Integer, nullable=False)
    games_played: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    points: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    points_per_game: Mapped[float | None] = mapped_column(Float, nullable=True)
    goals_for_per_game: Mapped[float | None] = mapped_column(Float, nullable=True)
    goals_against_per_game: Mapped[float | None] = mapped_column(Float, nullable=True)
    shots_for_per_game: Mapped[float | None] = mapped_column(Float, nullable=True)
    shots_against_per_game: Mapped[float | None] = mapped_column(Float, nullable=True)


class TeamStatsPercentages(TimestampMixin, Base):
    __tablename__ = "team_stats_percentages"
    __table_args__ = (UniqueConstraint("team_id", "season_id", "game_type_id"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    team_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("teams.team_id"), nullable=False
    )
    season_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("seasons.season_id"), nullable=False
    )
    game_type_id: Mapped[int] = mapped_column(Integer, nullable=False)
    games_played: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    shooting_pct: Mapped[float | None] = mapped_column(Float, nullable=True)
    save_pct: Mapped[float | None] = mapped_column(Float, nullable=True)
    pdo: Mapped[float | None] = mapped_column(Float, nullable=True)
    faceoff_pct: Mapped[float | None] = mapped_column(Float, nullable=True)
    pp_pct: Mapped[float | None] = mapped_column(Float, nullable=True)
    pk_pct: Mapped[float | None] = mapped_column(Float, nullable=True)
    sat_pct: Mapped[float | None] = mapped_column(Float, nullable=True)


class TeamStatsScoretrail(TimestampMixin, Base):
    __tablename__ = "team_stats_scoretrail"
    __table_args__ = (UniqueConstraint("team_id", "season_id", "game_type_id"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    team_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("teams.team_id"), nullable=False
    )
    season_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("seasons.season_id"), nullable=False
    )
    game_type_id: Mapped[int] = mapped_column(Integer, nullable=False)
    games_played: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    wins_trailing: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    wins_tied: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    wins_leading: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    losses_trailing: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    losses_tied: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    losses_leading: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    games_trailing: Mapped[int] = mapped_column(Integer, nullable=False, default=0)


class TeamStatsShootout(TimestampMixin, Base):
    __tablename__ = "team_stats_shootout"
    __table_args__ = (UniqueConstraint("team_id", "season_id", "game_type_id"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    team_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("teams.team_id"), nullable=False
    )
    season_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("seasons.season_id"), nullable=False
    )
    game_type_id: Mapped[int] = mapped_column(Integer, nullable=False)
    games_played: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    shootout_wins: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    shootout_losses: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    shootout_goals_for: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    shootout_goals_against: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    shootout_attempts: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    shootout_pct: Mapped[float | None] = mapped_column(Float, nullable=True)
    shootout_save_pct: Mapped[float | None] = mapped_column(Float, nullable=True)
