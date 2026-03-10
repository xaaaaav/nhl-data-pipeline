from typing import Any

import structlog
from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert as pg_insert
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.season import Season

logger = structlog.get_logger(__name__)


def _parse_season(data: dict[str, Any]) -> dict[str, Any]:
    """Map raw API season data to Season model fields."""
    return {
        "season_id": data["id"],
        "regular_season_start": data["regularSeasonStartDate"],
        "regular_season_end": data["regularSeasonEndDate"],
        "playoff_end": data.get("playoffEndDate"),
        "formatted_season_id": _format_season_id(data["id"]),
    }


def _format_season_id(season_id: int) -> str:
    s = str(season_id)
    start_year = s[:4]
    end_year = s[4:]
    return f"{start_year}-{end_year[2:]}"


async def upsert_season(session: AsyncSession, data: dict[str, Any]) -> Season:
    """Upsert a season record from raw API data."""
    parsed = _parse_season(data)
    stmt = (
        pg_insert(Season)
        .values(**parsed)
        .on_conflict_do_update(
            index_elements=["season_id"],
            set_={k: v for k, v in parsed.items() if k != "season_id"},
        )
        .returning(Season)
    )
    result = await session.execute(stmt)
    season = result.scalar_one()
    logger.debug("upserted season", season_id=parsed["season_id"])
    return season


async def get_all_season_ids(session: AsyncSession) -> list[int]:
    """Return all stored season IDs ordered ascending."""
    result = await session.execute(
        select(Season.season_id).order_by(Season.season_id)
    )
    return list(result.scalars().all())
