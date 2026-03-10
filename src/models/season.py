from datetime import date

from sqlalchemy import Date, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from src.models.base import Base, TimestampMixin


class Season(TimestampMixin, Base):
    __tablename__ = "seasons"

    season_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    regular_season_start: Mapped[date] = mapped_column(Date, nullable=False)
    regular_season_end: Mapped[date] = mapped_column(Date, nullable=False)
    playoff_end: Mapped[date | None] = mapped_column(Date, nullable=True)
    formatted_season_id: Mapped[str] = mapped_column(String(10), nullable=False)

    def __repr__(self) -> str:
        return f"<Season {self.formatted_season_id}>"
