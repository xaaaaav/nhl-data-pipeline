from typing import Any

import structlog
from sqlalchemy.dialects.postgresql import insert as pg_insert
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.franchise import Franchise
from src.models.team import Team

logger = structlog.get_logger(__name__)


async def upsert_franchise(
    session: AsyncSession, data: dict[str, Any]
) -> Franchise:
    """Upsert a franchise from raw API data."""
    parsed = {
        "franchise_id": data["franchiseId"],
        "full_name": data.get("fullName", ""),
        "team_name": data.get("teamName", ""),
        "most_recent_team_id": data.get("mostRecentTeamId"),
    }
    stmt = (
        pg_insert(Franchise)
        .values(**parsed)
        .on_conflict_do_update(
            index_elements=["franchise_id"],
            set_={k: v for k, v in parsed.items() if k != "franchise_id"},
        )
        .returning(Franchise)
    )
    result = await session.execute(stmt)
    franchise = result.scalar_one()
    logger.debug("upserted franchise", franchise_id=parsed["franchise_id"])
    return franchise


async def upsert_team(session: AsyncSession, data: dict[str, Any]) -> Team:
    """Upsert a team record (season-scoped)."""
    parsed = {
        "team_id": data["teamId"],
        "franchise_id": data["franchiseId"],
        "season_id": data["seasonId"],
        "abbrev": data.get("abbrev", ""),
        "city": data.get("placeName", {}).get("default", data.get("city", "")),
        "full_name": data.get("fullName", ""),
        "conference": data.get("conferenceName"),
        "division": data.get("divisionName"),
    }
    stmt = (
        pg_insert(Team)
        .values(**parsed)
        .on_conflict_do_update(
            index_elements=["team_id"],
            set_={k: v for k, v in parsed.items() if k != "team_id"},
        )
        .returning(Team)
    )
    result = await session.execute(stmt)
    team = result.scalar_one()
    logger.debug("upserted team", team_id=parsed["team_id"])
    return team
