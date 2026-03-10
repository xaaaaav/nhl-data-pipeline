from sqlalchemy import ForeignKey, Integer, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from src.models.base import Base, TimestampMixin


class Roster(TimestampMixin, Base):
    __tablename__ = "rosters"
    __table_args__ = (UniqueConstraint("team_id", "season_id", "player_id"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    team_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("teams.team_id"), nullable=False
    )
    season_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("seasons.season_id"), nullable=False
    )
    player_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("players.player_id"), nullable=False
    )
    roster_type: Mapped[str] = mapped_column(String(20), nullable=False)

    def __repr__(self) -> str:
        return f"<Roster team={self.team_id} player={self.player_id} season={self.season_id}>"
