from sqlalchemy import Boolean, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from src.models.base import Base, TimestampMixin


class PlayByPlayEvent(TimestampMixin, Base):
    __tablename__ = "play_by_play_events"

    event_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    game_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("games.game_id"), nullable=False, index=True
    )
    event_number: Mapped[int] = mapped_column(Integer, nullable=False)
    period: Mapped[int] = mapped_column(Integer, nullable=False)
    period_type: Mapped[str] = mapped_column(String(5), nullable=False)
    time_in_period: Mapped[str] = mapped_column(String(10), nullable=False)
    time_remaining: Mapped[str] = mapped_column(String(10), nullable=False)
    event_type: Mapped[str] = mapped_column(String(50), nullable=False, index=True)
    team_id: Mapped[int | None] = mapped_column(
        Integer, ForeignKey("teams.team_id"), nullable=True
    )
    x_coord: Mapped[float | None] = mapped_column(nullable=True)
    y_coord: Mapped[float | None] = mapped_column(nullable=True)
    zone: Mapped[str | None] = mapped_column(String(5), nullable=True)

    def __repr__(self) -> str:
        return f"<PlayByPlayEvent game={self.game_id} #{self.event_number} {self.event_type}>"


class PbpGoal(Base):
    __tablename__ = "pbp_goals"

    event_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("play_by_play_events.event_id"), primary_key=True
    )
    scoring_player_id: Mapped[int | None] = mapped_column(
        Integer, ForeignKey("players.player_id"), nullable=True
    )
    assist1_player_id: Mapped[int | None] = mapped_column(
        Integer, ForeignKey("players.player_id"), nullable=True
    )
    assist2_player_id: Mapped[int | None] = mapped_column(
        Integer, ForeignKey("players.player_id"), nullable=True
    )
    goalie_id: Mapped[int | None] = mapped_column(
        Integer, ForeignKey("players.player_id"), nullable=True
    )
    shot_type: Mapped[str | None] = mapped_column(String(50), nullable=True)
    strength: Mapped[str | None] = mapped_column(String(5), nullable=True)
    empty_net: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)


class PbpShot(Base):
    __tablename__ = "pbp_shots"

    event_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("play_by_play_events.event_id"), primary_key=True
    )
    shooting_player_id: Mapped[int | None] = mapped_column(
        Integer, ForeignKey("players.player_id"), nullable=True
    )
    goalie_id: Mapped[int | None] = mapped_column(
        Integer, ForeignKey("players.player_id"), nullable=True
    )
    shot_type: Mapped[str | None] = mapped_column(String(50), nullable=True)


class PbpMissedShot(Base):
    __tablename__ = "pbp_missed_shots"

    event_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("play_by_play_events.event_id"), primary_key=True
    )
    shooting_player_id: Mapped[int | None] = mapped_column(
        Integer, ForeignKey("players.player_id"), nullable=True
    )
    goalie_id: Mapped[int | None] = mapped_column(
        Integer, ForeignKey("players.player_id"), nullable=True
    )
    shot_type: Mapped[str | None] = mapped_column(String(50), nullable=True)
    miss_reason: Mapped[str | None] = mapped_column(String(100), nullable=True)


class PbpBlockedShot(Base):
    __tablename__ = "pbp_blocked_shots"

    event_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("play_by_play_events.event_id"), primary_key=True
    )
    shooter_player_id: Mapped[int | None] = mapped_column(
        Integer, ForeignKey("players.player_id"), nullable=True
    )
    blocking_player_id: Mapped[int | None] = mapped_column(
        Integer, ForeignKey("players.player_id"), nullable=True
    )


class PbpHit(Base):
    __tablename__ = "pbp_hits"

    event_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("play_by_play_events.event_id"), primary_key=True
    )
    hitting_player_id: Mapped[int | None] = mapped_column(
        Integer, ForeignKey("players.player_id"), nullable=True
    )
    hittee_player_id: Mapped[int | None] = mapped_column(
        Integer, ForeignKey("players.player_id"), nullable=True
    )


class PbpFaceoff(Base):
    __tablename__ = "pbp_faceoffs"

    event_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("play_by_play_events.event_id"), primary_key=True
    )
    winning_player_id: Mapped[int | None] = mapped_column(
        Integer, ForeignKey("players.player_id"), nullable=True
    )
    losing_player_id: Mapped[int | None] = mapped_column(
        Integer, ForeignKey("players.player_id"), nullable=True
    )


class PbpPenalty(Base):
    __tablename__ = "pbp_penalties"

    event_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("play_by_play_events.event_id"), primary_key=True
    )
    committed_by_player_id: Mapped[int | None] = mapped_column(
        Integer, ForeignKey("players.player_id"), nullable=True
    )
    drawn_by_player_id: Mapped[int | None] = mapped_column(
        Integer, ForeignKey("players.player_id"), nullable=True
    )
    penalty_type: Mapped[str | None] = mapped_column(String(50), nullable=True)
    penalty_description: Mapped[str | None] = mapped_column(String(200), nullable=True)
    duration_minutes: Mapped[int | None] = mapped_column(Integer, nullable=True)


class PbpStoppage(Base):
    __tablename__ = "pbp_stoppages"

    event_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("play_by_play_events.event_id"), primary_key=True
    )
    reason: Mapped[str | None] = mapped_column(String(200), nullable=True)


class PbpPeriodEvent(Base):
    __tablename__ = "pbp_period_events"

    event_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("play_by_play_events.event_id"), primary_key=True
    )
    period_number: Mapped[int | None] = mapped_column(Integer, nullable=True)
