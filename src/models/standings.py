from datetime import date

from sqlalchemy import Date, ForeignKey, Integer, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from src.models.base import Base, TimestampMixin


class StandingsSnapshot(TimestampMixin, Base):
    __tablename__ = "standings_snapshots"
    __table_args__ = (UniqueConstraint("season_id", "date", "team_id"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    season_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("seasons.season_id"), nullable=False
    )
    date: Mapped[date] = mapped_column(Date, nullable=False)
    team_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("teams.team_id"), nullable=False
    )
    points: Mapped[int] = mapped_column(Integer, nullable=False)
    wins: Mapped[int] = mapped_column(Integer, nullable=False)
    losses: Mapped[int] = mapped_column(Integer, nullable=False)
    ot_losses: Mapped[int] = mapped_column(Integer, nullable=False)
    games_played: Mapped[int] = mapped_column(Integer, nullable=False)
    goals_for: Mapped[int | None] = mapped_column(Integer, nullable=True)
    goals_against: Mapped[int | None] = mapped_column(Integer, nullable=True)
    regulation_wins: Mapped[int | None] = mapped_column(Integer, nullable=True)
    streak_type: Mapped[str | None] = mapped_column(String(5), nullable=True)
    streak_count: Mapped[int | None] = mapped_column(Integer, nullable=True)

    def __repr__(self) -> str:
        return f"<StandingsSnapshot team={self.team_id} date={self.date} pts={self.points}>"
