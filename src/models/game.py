from datetime import date

from sqlalchemy import Date, Float, ForeignKey, Integer, String
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from src.models.base import Base, TimestampMixin


class Game(TimestampMixin, Base):
    __tablename__ = "games"

    game_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    season_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("seasons.season_id"), nullable=False
    )
    game_type: Mapped[int] = mapped_column(Integer, nullable=False)
    game_date: Mapped[date] = mapped_column(Date, nullable=False)
    home_team_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("teams.team_id"), nullable=False
    )
    away_team_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("teams.team_id"), nullable=False
    )
    venue: Mapped[str | None] = mapped_column(String(200), nullable=True)
    game_state: Mapped[str] = mapped_column(String(10), nullable=False)
    home_score: Mapped[int | None] = mapped_column(Integer, nullable=True)
    away_score: Mapped[int | None] = mapped_column(Integer, nullable=True)
    period: Mapped[int | None] = mapped_column(Integer, nullable=True)

    def __repr__(self) -> str:
        return f"<Game {self.game_id} {self.game_state}>"


class GameBoxscore(TimestampMixin, Base):
    __tablename__ = "game_boxscores"

    game_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("games.game_id"), primary_key=True
    )
    home_shots: Mapped[int | None] = mapped_column(Integer, nullable=True)
    home_hits: Mapped[int | None] = mapped_column(Integer, nullable=True)
    home_blocked_shots: Mapped[int | None] = mapped_column(Integer, nullable=True)
    home_pp_goals: Mapped[int | None] = mapped_column(Integer, nullable=True)
    home_pp_opportunities: Mapped[int | None] = mapped_column(Integer, nullable=True)
    home_faceoff_pct: Mapped[float | None] = mapped_column(Float, nullable=True)
    home_giveaways: Mapped[int | None] = mapped_column(Integer, nullable=True)
    home_takeaways: Mapped[int | None] = mapped_column(Integer, nullable=True)
    home_pim: Mapped[int | None] = mapped_column(Integer, nullable=True)
    away_shots: Mapped[int | None] = mapped_column(Integer, nullable=True)
    away_hits: Mapped[int | None] = mapped_column(Integer, nullable=True)
    away_blocked_shots: Mapped[int | None] = mapped_column(Integer, nullable=True)
    away_pp_goals: Mapped[int | None] = mapped_column(Integer, nullable=True)
    away_pp_opportunities: Mapped[int | None] = mapped_column(Integer, nullable=True)
    away_faceoff_pct: Mapped[float | None] = mapped_column(Float, nullable=True)
    away_giveaways: Mapped[int | None] = mapped_column(Integer, nullable=True)
    away_takeaways: Mapped[int | None] = mapped_column(Integer, nullable=True)
    away_pim: Mapped[int | None] = mapped_column(Integer, nullable=True)
    raw: Mapped[dict] = mapped_column(JSONB, nullable=False, default=dict)

    def __repr__(self) -> str:
        return f"<GameBoxscore game_id={self.game_id}>"
