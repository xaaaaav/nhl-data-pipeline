from sqlalchemy import ForeignKey, Integer, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from src.models.base import Base, TimestampMixin


class DraftPick(TimestampMixin, Base):
    __tablename__ = "draft_picks"
    __table_args__ = (UniqueConstraint("draft_year", "round_number", "pick_in_round"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    draft_year: Mapped[int] = mapped_column(Integer, nullable=False)
    round_number: Mapped[int] = mapped_column(Integer, nullable=False)
    pick_in_round: Mapped[int] = mapped_column(Integer, nullable=False)
    overall_pick: Mapped[int | None] = mapped_column(Integer, nullable=True)
    team_id: Mapped[int | None] = mapped_column(
        Integer, ForeignKey("teams.team_id"), nullable=True
    )
    player_id: Mapped[int | None] = mapped_column(
        Integer, ForeignKey("players.player_id"), nullable=True
    )

    def __repr__(self) -> str:
        return f"<DraftPick {self.draft_year} R{self.round_number} #{self.pick_in_round}>"
