from typing import Any

import structlog
from sqlalchemy.dialects.postgresql import insert as pg_insert
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.player import Player

logger = structlog.get_logger(__name__)


def _parse_player(data: dict[str, Any]) -> dict[str, Any]:
    """Map raw API player data to Player model fields."""
    first_name = data.get("firstName", {})
    last_name = data.get("lastName", {})
    if isinstance(first_name, dict):
        first_name = first_name.get("default", "")
    if isinstance(last_name, dict):
        last_name = last_name.get("default", "")

    return {
        "player_id": data["playerId"],
        "first_name": first_name,
        "last_name": last_name,
        "position": data.get("position", data.get("positionCode", "")),
        "birth_date": data.get("birthDate"),
        "nationality": data.get("birthCountry", data.get("nationality")),
        "height_inches": data.get("heightInInches"),
        "weight_pounds": data.get("weightInPounds"),
        "shoots_catches": data.get("shootsCatches"),
    }


async def upsert_player(session: AsyncSession, data: dict[str, Any]) -> Player:
    """Upsert a player record from raw API data."""
    parsed = _parse_player(data)
    stmt = (
        pg_insert(Player)
        .values(**parsed)
        .on_conflict_do_update(
            index_elements=["player_id"],
            set_={k: v for k, v in parsed.items() if k != "player_id"},
        )
        .returning(Player)
    )
    result = await session.execute(stmt)
    player = result.scalar_one()
    logger.debug("upserted player", player_id=parsed["player_id"])
    return player
