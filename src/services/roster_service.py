from typing import Any

import structlog
from sqlalchemy.dialects.postgresql import insert as pg_insert
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.roster import Roster

logger = structlog.get_logger(__name__)

_POSITION_TO_ROSTER_TYPE: dict[str, str] = {
    "C": "forward",
    "LW": "forward",
    "RW": "forward",
    "D": "defense",
    "G": "goalie",
}


def _roster_type(position: str) -> str:
    return _POSITION_TO_ROSTER_TYPE.get(position.upper(), "forward")


async def upsert_roster_entry(
    session: AsyncSession,
    team_id: int,
    season_id: int,
    data: dict[str, Any],
) -> Roster:
    """Upsert a single roster entry."""
    position = data.get("position", data.get("positionCode", ""))
    parsed = {
        "team_id": team_id,
        "season_id": season_id,
        "player_id": data["playerId"],
        "roster_type": _roster_type(position),
    }
    stmt = (
        pg_insert(Roster)
        .values(**parsed)
        .on_conflict_do_update(
            index_elements=["team_id", "season_id", "player_id"],
            set_={"roster_type": parsed["roster_type"]},
        )
        .returning(Roster)
    )
    result = await session.execute(stmt)
    roster = result.scalar_one()
    return roster


async def upsert_roster(
    session: AsyncSession,
    team_id: int,
    season_id: int,
    roster_data: dict[str, Any],
) -> list[Roster]:
    """Process a full roster response and upsert all entries."""
    rosters: list[Roster] = []
    for group in ("forwards", "defensemen", "goalies"):
        for player_data in roster_data.get(group, []):
            entry = await upsert_roster_entry(session, team_id, season_id, player_data)
            rosters.append(entry)
    logger.debug(
        "upserted roster", team_id=team_id, season_id=season_id, count=len(rosters)
    )
    return rosters
