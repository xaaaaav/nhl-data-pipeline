from datetime import date

from sqlalchemy import Date, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from src.models.base import Base, TimestampMixin


class Player(TimestampMixin, Base):
    __tablename__ = "players"

    player_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    first_name: Mapped[str] = mapped_column(String(100), nullable=False)
    last_name: Mapped[str] = mapped_column(String(100), nullable=False)
    position: Mapped[str] = mapped_column(String(5), nullable=False)
    birth_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    nationality: Mapped[str | None] = mapped_column(String(10), nullable=True)
    height_inches: Mapped[int | None] = mapped_column(Integer, nullable=True)
    weight_pounds: Mapped[int | None] = mapped_column(Integer, nullable=True)
    shoots_catches: Mapped[str | None] = mapped_column(String(5), nullable=True)

    def __repr__(self) -> str:
        return f"<Player {self.first_name} {self.last_name}>"
